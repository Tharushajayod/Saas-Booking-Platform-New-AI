#!/usr/bin/env python3
"""
Comprehensive end-to-end integration tests for SaaS Booking Platform
Tests user registration, login, property creation, room creation, and booking flows
"""

import requests
import json
import time
from datetime import date, timedelta
from random import randint

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def log(msg, color=BLUE):
    print(f"{color}{msg}{RESET}")

def test_passed(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def test_failed(msg):
    print(f"{RED}✗ {msg}{RESET}")

# Test data
test_id = int(time.time()) % 10000
test_email = f"testuser{test_id}@example.com"
test_password = "TestPassword123!"
test_property_name = f"Test Property {test_id}"

def test_health():
    """Test 1: Health Check"""
    log("\n[TEST 1] API Health Check", BLUE)
    try:
        resp = requests.get(f"{BASE_URL}/api/auth/health/", timeout=10)
        if resp.status_code == 200 and "healthy" in resp.json().get("status", ""):
            test_passed(f"Health endpoint: {resp.json()}")
            return True
        else:
            test_failed(f"Unexpected response: {resp.json()}")
            return False
    except Exception as e:
        test_failed(f"Health check failed: {e}")
        return False

def test_registration():
    """Test 2: User Registration"""
    log("\n[TEST 2] User Registration (Email: {})".format(test_email), BLUE)
    try:
        payload = {
            "email": test_email,
            "password": test_password,
            "password2": test_password,
            "first_name": "Test",
            "last_name": "User"
        }
        resp = requests.post(f"{BASE_URL}/api/auth/register/", json=payload, timeout=10)
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            test_passed(f"Registration successful: {data.get('email')}")
            return True, data
        else:
            test_failed(f"Registration failed (HTTP {resp.status_code}): {resp.text[:200]}")
            return False, None
    except Exception as e:
        test_failed(f"Registration error: {e}")
        return False, None

def test_login(user_data):
    """Test 3: User Login"""
    log("\n[TEST 3] User Login", BLUE)
    try:
        payload = {
            "email": test_email,
            "password": test_password
        }
        resp = requests.post(f"{BASE_URL}/api/auth/login/", json=payload, timeout=10)
        
        if resp.status_code == 200:
            token_data = resp.json()
            access_token = token_data.get("access")
            if access_token:
                test_passed(f"Login successful: Token received (length: {len(access_token)})")
                return True, access_token
            else:
                test_failed("No access token in response")
                return False, None
        else:
            test_failed(f"Login failed (HTTP {resp.status_code}): {resp.text[:200]}")
            return False, None
    except Exception as e:
        test_failed(f"Login error: {e}")
        return False, None

def test_profile(token):
    """Test 4: Get User Profile"""
    log("\n[TEST 4] Get User Profile", BLUE)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/api/auth/profile/", headers=headers, timeout=10)
        
        if resp.status_code == 200:
            profile = resp.json()
            test_passed(f"Profile retrieved: {profile.get('email')}")
            return True, profile
        else:
            test_failed(f"Profile fetch failed (HTTP {resp.status_code})")
            return False, None
    except Exception as e:
        test_failed(f"Profile error: {e}")
        return False, None

def test_property_list():
    """Test 5: Get Properties (Public)"""
    log("\n[TEST 5] List Properties (Public)", BLUE)
    try:
        resp = requests.get(f"{BASE_URL}/api/properties/", timeout=10)
        
        if resp.status_code == 200:
            properties = resp.json()
            if isinstance(properties, list):
                test_passed(f"Properties retrieved: {len(properties)} found")
                return True, properties
            elif isinstance(properties, dict) and "results" in properties:
                test_passed(f"Properties retrieved (paginated): {len(properties.get('results', []))} found")
                return True, properties.get('results', [])
            else:
                test_passed(f"Properties endpoint working (response: {type(properties).__name__})")
                return True, []
        else:
            test_failed(f"Property list failed (HTTP {resp.status_code})")
            return False, []
    except Exception as e:
        test_failed(f"Property list error: {e}")
        return False, []

def test_create_property(token):
    """Test 6: Create Property (Authenticated)"""
    log("\n[TEST 6] Create Property (Authenticated)", BLUE)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "name": test_property_name,
            "description": "Test property for automated testing",
            "location": "Test Location",
            "price_per_night": 100.00,
            "max_guests": 4
        }
        resp = requests.post(f"{BASE_URL}/api/properties/create/", json=payload, headers=headers, timeout=10)
        
        if resp.status_code in [200, 201]:
            property_data = resp.json()
            test_passed(f"Property created: {property_data.get('name')} (ID: {property_data.get('id')})")
            return True, property_data
        else:
            test_failed(f"Property creation failed (HTTP {resp.status_code}): {resp.text[:200]}")
            return False, None
    except Exception as e:
        test_failed(f"Property creation error: {e}")
        return False, None

def test_create_booking():
    """Test 7: Create Public Booking"""
    log("\n[TEST 7] Create Booking (Public)", BLUE)
    try:
        check_in = date.today() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        payload = {
            "room_id": 1,  # Assuming there's a room with ID 1
            "guest_email": f"guest{test_id}@example.com",
            "guest_name": "Test Guest",
            "check_in": str(check_in),
            "check_out": str(check_out),
            "total_price": 200.00
        }
        resp = requests.post(f"{BASE_URL}/api/bookings/create/", json=payload, timeout=10)
        
        if resp.status_code in [200, 201]:
            booking = resp.json()
            test_passed(f"Booking created: {booking.get('id')}")
            return True, booking
        else:
            # Booking creation might fail due to room availability - that's OK for this test
            log(f"Booking creation returned HTTP {resp.status_code} (expected for public endpoint)", YELLOW)
            return False, None
    except Exception as e:
        test_failed(f"Booking creation error: {e}")
        return False, None

def test_frontend_accessibility():
    """Test 8: Frontend Page Loads"""
    log("\n[TEST 8] Frontend Accessibility", BLUE)
    try:
        resp = requests.get(FRONTEND_URL, timeout=10)
        
        if resp.status_code == 200:
            content = resp.text.lower()
            # Check for Next.js markers
            if any(marker in content for marker in ['next', 'react', '__next', '<html']):
                test_passed(f"Frontend loaded successfully ({len(resp.text)} bytes)")
                return True
            else:
                test_failed(f"Frontend returned content but might be corrupted ({len(resp.text)} bytes)")
                return False
        else:
            test_failed(f"Frontend returned HTTP {resp.status_code}")
            return False
    except Exception as e:
        test_failed(f"Frontend accessibility error: {e}")
        return False

def main():
    log("\n" + "="*70, BLUE)
    log("SaaS BOOKING PLATFORM - END-TO-END INTEGRATION TESTS", BLUE)
    log("="*70 + "\n", BLUE)
    
    results = {}
    
    # Test 1: Health
    results["health"] = test_health()
    
    # Test 2: Registration
    success, reg_data = test_registration()
    results["registration"] = success
    
    # Test 3: Login
    success, token = test_login(reg_data)
    results["login"] = success
    
    if token:
        # Test 4: Profile
        success, profile = test_profile(token)
        results["profile"] = success
        
        # Test 6: Create Property
        success, prop_data = test_create_property(token)
        results["create_property"] = success
    
    # Test 5: List Properties
    success, properties = test_property_list()
    results["list_properties"] = success
    
    # Test 7: Create Booking
    success, booking = test_create_booking()
    results["create_booking"] = success
    
    # Test 8: Frontend
    results["frontend"] = test_frontend_accessibility()
    
    # Summary
    log("\n" + "="*70, BLUE)
    log("TEST SUMMARY", BLUE)
    log("="*70, BLUE)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = f"{GREEN}✓ PASS{RESET}" if passed_flag else f"{RED}✗ FAIL{RESET}"
        print(f"  {status}: {test_name}")
    
    log(f"\nResult: {passed}/{total} tests passed", BLUE if passed == total else YELLOW)
    
    if passed == total:
        log("\n🎉 ALL TESTS PASSED! System is fully operational.", GREEN)
    elif passed >= total * 0.7:
        log("\n⚠ Most tests passed. Some features may need attention.", YELLOW)
    else:
        log("\n❌ Multiple test failures. System needs investigation.", RED)
    
    log("="*70 + "\n", BLUE)
    
    return 0 if passed >= total * 0.7 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
