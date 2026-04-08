#!/usr/bin/env python3
"""
Simple frontend build and integration test
"""
import subprocess
import time
import requests
from pathlib import Path

def run(cmd):
    print(f"\n➜ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout[-1000:])  # Last 1000 chars
    if result.returncode != 0 and result.stderr:
        print(f"ERROR: {result.stderr[-500:]}")  # Last 500 chars
    return result.returncode

print("="*70)
print("FRONTEND BUILD & INTEGRATION TEST")
print("="*70)

print("\n[1] Stopping containers...")
run("docker compose down")

print("\n[2] Rebuilding frontend with improved Dockerfile...")
rc = run("docker compose build frontend --progress=plain 2>&1")
if rc != 0:
    print("❌ Frontend build FAILED")
    exit(1)

print("\n[3] Starting all services...")
run("docker compose up -d")

print("\n[4] Waiting for services to stabilize...")
time.sleep(10)

print("\n[5] Testing endpoints...")

# Test backend
try:
    resp = requests.get("http://localhost:8000/api/auth/health/", timeout=5)
    if resp.status_code == 200:
        print(f"✓ Backend API: {resp.json()}")
    else:
        print(f"✗ Backend returned HTTP {resp.status_code}")
except Exception as e:
    print(f"✗ Backend error: {e}")

# Test frontend
try:
    resp = requests.get("http://localhost:3001/", timeout=5)
    if resp.status_code == 200:
        print(f"✓ Frontend: HTTP 200, {len(resp.text)} bytes")
        # Check for common HTML markers
        if any(marker in resp.text for marker in ['<html', '</html>', 'next', 'login']):
            print("  ✓ HTML content looks valid")
        else:
            print("  ⚠ HTML content might be corrupted")
    else:
        print(f"✗ Frontend returned HTTP {resp.status_code}")
except Exception as e:
    print(f"✗ Frontend error: {e}")

print("\n[6] Service status:")
run("docker compose ps")

print("\n[7] Frontend container logs (last 20 lines):")
run("docker compose logs frontend --tail 20")

print("\n" + "="*70)
print("FRONTEND BUILD & INTEGRATION TEST COMPLETE")
print("="*70)
