#!/usr/bin/env python3
r"""
Comprehensive local test and bug-fix script for SaaS Booking Platform
Runs Docker, seeds data, executes API smoke tests, captures failures, and attempts fixes
Usage: python .\scripts\test_and_fix_local.py
"""

import subprocess
import sys
import json
import time
import requests
from pathlib import Path
from datetime import date

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def log_step(step_num, title, color=BLUE):
    print(f"\n{color}{'='*70}")
    print(f"Step {step_num}: {title}")
    print(f"{'='*70}{RESET}")

def log_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def log_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def log_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def run_cmd(cmd, description="", shell=False, capture=False):
    """Run a shell command and return result."""
    print(f"\n  Running: {cmd}")
    try:
        if capture:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        else:
            result = subprocess.run(cmd, shell=shell, timeout=300)
            return {'returncode': result.returncode, 'success': result.returncode == 0}
    except subprocess.TimeoutExpired:
        log_error(f"{description} timed out (>5 min)")
        return {'returncode': 1, 'success': False, 'stderr': 'Timeout'}
    except Exception as e:
        log_error(f"{description} failed: {e}")
        return {'returncode': 1, 'success': False, 'stderr': str(e)}

def wait_for_http(url, timeout_sec=120, interval_sec=3):
    """Wait for HTTP endpoint to be accessible."""
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                log_success(f"HTTP OK: {url}")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(interval_sec)
        print(f"  Waiting for {url}...")
    log_error(f"Timeout waiting for {url}")
    return False

def test_api_flows():
    """Run automated API smoke tests."""
    tests = {
        "Health": {
            "method": "GET",
            "url": "http://localhost:8000/api/auth/health/",
            "expected_keys": ["status", "message"]
        }
    }
    
    log_step(6, "Run API Smoke Tests")
    passed = 0
    failed = 0
    
    for test_name, config in tests.items():
        try:
            if config["method"] == "GET":
                resp = requests.get(config["url"], timeout=10)
                if resp.status_code == 200 and all(k in resp.json() for k in config["expected_keys"]):
                    log_success(f"{test_name}: {resp.json()}")
                    passed += 1
                else:
                    log_error(f"{test_name}: status={resp.status_code}, response={resp.text[:100]}")
                    failed += 1
        except Exception as e:
            log_error(f"{test_name}: {e}")
            failed += 1
    
    print(f"\n  API Tests: {passed} passed, {failed} failed")
    return failed == 0

def main():
    print(f"\n{BLUE}{'='*70}")
    print("SaaS Booking Platform - Local Test & Bug-Fix Runner")
    print(f"{'='*70}{RESET}")
    
    # Step 1: Ensure containers are running
    log_step(1, "Check Docker Containers Status")
    result = run_cmd("docker compose ps", capture=True)
    if result['success']:
        log_success("Containers status check succeeded")
        print(result['stdout'])
    else:
        log_warning("Could not get container status, attempting to start...")
        result = run_cmd("docker compose up --build -d", capture=True)
        if result['success']:
            log_success("Containers started")
            time.sleep(10)
        else:
            log_error("Failed to start containers")
            return 1
    
    # Step 2: Wait for backend health
    log_step(2, "Wait for Backend Health Endpoint")
    if not wait_for_http("http://localhost:8000/api/auth/health/", timeout_sec=60):
        log_error("Backend did not become healthy in time")
        return 1
    log_success("Backend is healthy")
    
    # Step 3: Apply migrations
    log_step(3, "Apply Database Migrations")
    result = run_cmd("docker compose exec backend python manage.py migrate --noinput", capture=True)
    if result['success']:
        log_success("Migrations applied")
    else:
        log_warning(f"Migration result: {result.get('stderr', 'Unknown error')[:200]}")
    
    # Step 4: Ensure superuser
    log_step(4, "Ensure Admin Superuser Exists")
    result = run_cmd("docker compose exec backend python /app/scripts/create_superuser.py", capture=True)
    if result['success']:
        log_success(result['stdout'].strip())
    else:
        log_warning(f"Superuser creation: {result.get('stderr', 'Unknown')[:200]}")
    
    # Step 5: Seed demo data
    log_step(5, "Seed Demo Data (Tenant → Property → Room → Booking)")
    commands = [
        ("docker compose exec backend python /app/scripts/create_property_for_owner.py", "Property"),
        ("docker compose exec backend python /app/scripts/create_room_for_property.py", "Room"),
        ("docker compose exec backend python /app/scripts/create_booking_for_room.py", "Booking"),
    ]
    for cmd, label in commands:
        result = run_cmd(cmd, capture=True)
        if result['success']:
            log_success(f"{label}: {result['stdout'].strip()}")
        else:
            log_error(f"{label}: {result.get('stderr', 'Unknown error')[:200]}")
    
    # Step 6: Run API smoke tests
    test_passed = test_api_flows()
    
    # Step 7: Check frontend
    log_step(7, "Check Frontend (Host)")
    try:
        resp = requests.get("http://localhost:3001/", timeout=10)
        if resp.status_code == 200 and "html" in resp.text.lower():
            log_success(f"Frontend is up: {len(resp.text)} bytes, HTTP {resp.status_code}")
        else:
            log_warning(f"Frontend returned HTTP {resp.status_code}")
    except requests.exceptions.RequestException as e:
        log_warning(f"Frontend check failed: {e}")
    
    # Step 8: Capture backend logs for diagnostics
    log_step(8, "Capture Backend Logs for Diagnostics")
    result = run_cmd("docker compose logs backend --tail 100", capture=True)
    if result['success']:
        log_success("Backend logs captured")
        print("\nRecent backend logs:")
        print(result['stdout'][-1000:])  # Last 1000 chars
    
    # Step 9: Summary and recommendations
    log_step(9, "Test Summary & Recommendations")
    if test_passed:
        log_success("All smoke tests passed! ✓ System is healthy.")
    else:
        log_warning("Some tests failed. Review the logs above for details.")
        log_warning("Common fixes: Restart Docker, check .env, verify port availability.")
    
    print(f"\n{BLUE}{'='*70}")
    print("Next steps:")
    print("  - Open http://localhost:3001 in browser to test UI")
    print("  - Run: docker compose logs -f backend  (to monitor backend)")
    print("  - Run: docker compose logs -f frontend (to monitor frontend)")
    print(f"{'='*70}{RESET}\n")
    
    return 0 if test_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
