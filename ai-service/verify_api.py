#!/usr/bin/env python3
"""
Day 17 - Groq API Verification Script
Tests all 3 endpoints to confirm API key and credits are active
"""

import os
import sys
from dotenv import load_dotenv
import requests
import time
import json

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
AI_SERVICE_URL = "http://localhost:5000"

def verify_groq_key():
    """Verify Groq API key is active"""
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY not set in .env")
        return False
    print(f"✓ Groq API Key found: {GROQ_API_KEY[:10]}...")
    return True

def test_health():
    """Test /health endpoint"""
    try:
        response = requests.get(f"{AI_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ /health endpoint working")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"❌ /health returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /health failed: {e}")
        return False

def test_describe():
    """Test /describe endpoint"""
    try:
        payload = {
            "vendor_name": "TechCorp Inc",
            "risk_factors": "Financial instability, poor compliance record"
        }
        start = time.time()
        response = requests.post(f"{AI_SERVICE_URL}/describe", json=payload, timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✓ /describe endpoint working ({elapsed:.2f}s)")
            data = response.json()
            print(f"  Generated: {data.get('generated_at')}")
            print(f"  Description preview: {data.get('description', '')[:100]}...")
            return True
        else:
            print(f"❌ /describe returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /describe failed: {e}")
        return False

def test_recommend():
    """Test /recommend endpoint"""
    try:
        payload = {
            "vendor_name": "TechCorp Inc",
            "risk_factors": "Financial instability, poor compliance record"
        }
        start = time.time()
        response = requests.post(f"{AI_SERVICE_URL}/recommend", json=payload, timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✓ /recommend endpoint working ({elapsed:.2f}s)")
            data = response.json()
            print(f"  Generated: {data.get('generated_at')}")
            recs = data.get('recommendations', [])
            print(f"  Recommendations count: {len(recs) if isinstance(recs, list) else 'N/A'}")
            return True
        else:
            print(f"❌ /recommend returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /recommend failed: {e}")
        return False

def test_generate_report():
    """Test /generate-report endpoint"""
    try:
        payload = {
            "vendor_name": "TechCorp Inc",
            "risk_factors": "Financial instability, poor compliance record"
        }
        start = time.time()
        response = requests.post(f"{AI_SERVICE_URL}/generate-report", json=payload, timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✓ /generate-report endpoint working ({elapsed:.2f}s)")
            data = response.json()
            print(f"  Generated: {data.get('generated_at')}")
            report = data.get('report', {})
            print(f"  Report keys: {list(report.keys()) if isinstance(report, dict) else 'N/A'}")
            return True
        else:
            print(f"❌ /generate-report returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /generate-report failed: {e}")
        return False

def main():
    print("=" * 60)
    print("DAY 17: GROQ API VERIFICATION")
    print("=" * 60)
    
    results = []
    
    print("\n1. Checking API Key...")
    results.append(verify_groq_key())
    
    print("\n2. Testing Endpoints (Ensure AI service is running on port 5000)...")
    print("   Starting tests in 2 seconds...")
    time.sleep(2)
    
    print("\n   a) Testing /health...")
    results.append(test_health())
    
    print("\n   b) Testing /describe...")
    results.append(test_describe())
    
    print("\n   c) Testing /recommend...")
    results.append(test_recommend())
    
    print("\n   d) Testing /generate-report...")
    results.append(test_generate_report())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"VERIFICATION RESULT: {passed}/{total} checks passed")
    print("=" * 60)
    
    if passed == total:
        print("✓ All endpoints confirmed working!")
        print("✓ Groq API key is active and credits sufficient")
        return 0
    else:
        print("❌ Some checks failed. Review above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())