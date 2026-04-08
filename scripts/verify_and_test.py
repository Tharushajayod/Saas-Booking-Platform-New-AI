#!/usr/bin/env python3
r"""
Verification script to ensure all microservices are healthy and functioning
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def log(msg, color=BLUE):
    print(f"{color}{msg}{RESET}")

def run_cmd(cmd, capture=False):
    print(f"  Running: {cmd}")
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            return {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        else:
            result = subprocess.run(cmd, shell=True, timeout=300)
            return {'returncode': result.returncode}
    except Exception as e:
        return {'returncode': 1, 'stderr': str(e)}

def main():
    log("\n" + "="*70, BLUE)
    log("Post-Fix Verification & Comprehensive Testing", BLUE)
    log("="*70 + "\n", BLUE)
    
    # Step 1: Restart services with fixes
    log("\n[1] Rebuild and restart Docker services with fixes...", YELLOW)
    result = run_cmd("docker compose up --build -d")
    if result['returncode'] != 0:
        log("WARNING: Docker compose up had issues", YELLOW)
    time.sleep(5)
    
    # Step 2: Verify all services are running
    log("\n[2] Verify all Docker services are running...", YELLOW)
    result = run_cmd("docker compose ps", capture=True)
    log(result['stdout'], RESET)
    
    # Step 3: Wait for backend health
    log("\n[3] Waiting for backend health endpoint...", YELLOW)
    for attempt in range(60):
        try:
            resp = requests.get("http://localhost:8000/api/auth/health/", timeout=5)
            if resp.status_code == 200:
                log(f"✓ Backend healthy: {resp.json()}", GREEN)
                break
        except:
            pass
        if attempt % 10 == 0:
            print(f"    Attempt {attempt}/60...")
        time.sleep(1)
    else:
        log("✗ Backend health timeout", RED)
    
    # Step 4: Check frontend
    log("\n[4] Checking frontend...", YELLOW)
    for attempt in range(30):
        try:
            resp = requests.get("http://localhost:3001/", timeout=5)
            if resp.status_code == 200:
                log(f"✓ Frontend is up (HTTP {resp.status_code}, {len(resp.text)} bytes)", GREEN)
                break
        except:
            pass
        if attempt % 10 == 0:
            print(f"    Attempt {attempt}/30...")
        time.sleep(1)
    else:
        log("⚠ Frontend not responding yet", YELLOW)
    
    # Step 5: Test critical API endpoints
    log("\n[5] Testing critical API endpoints...", YELLOW)
    endpoints = [
        ("GET", "http://localhost:8000/api/auth/health/"),
        ("GET", "http://localhost:8000/api/properties/"),
    ]
    
    for method, url in endpoints:
        try:
            resp = requests.get(url, timeout=5)
            log(f"✓ {method} {url}: HTTP {resp.status_code}", GREEN)
        except Exception as e:
            log(f"✗ {method} {url}: {e}", RED)
    
    # Step 6: Check backend logs for errors
    log("\n[6] Backend logs (last 30 lines)...", YELLOW)
    result = run_cmd("docker compose logs backend --tail 30", capture=True)
    print(result['stdout'][-500:] if result['stdout'] else "No logs")
    
    # Step 7: Check frontend logs for errors
    log("\n[7] Frontend logs (last 20 lines)...", YELLOW)
    result = run_cmd("docker compose logs frontend --tail 20", capture=True)
    print(result['stdout'][-400:] if result['stdout'] else "No logs / Frontend may not have started")
    
    # Step 8: Summary
    log("\n" + "="*70, BLUE)
    log("NEXT STEPS:", BLUE)
    log("1. Open http://localhost:3001 in your browser", BLUE)
    log("2. Test login/register functionality", BLUE)
    log("3. Create a property and booking", BLUE)
    log("4. Monitor logs: docker compose logs -f", BLUE)
    log("="*70 + "\n", BLUE)

if __name__ == "__main__":
    main()
