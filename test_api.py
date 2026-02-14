#!/usr/bin/env python3
"""
Test script for Flask API
Tests all endpoints without starting a server
"""

import json
import sys
from app import app

def test_health():
    """Test health check endpoint"""
    print("Testing /api/health...")
    with app.test_client() as client:
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert data['status'] == 'healthy'
        print("✓ Health check passed")
        return True

def test_india_generate():
    """Test India label generation"""
    print("\nTesting /api/generate/india...")
    
    # Load sample data
    with open('india_dataset/01_packaged_snack.json', 'r') as f:
        product_data = json.load(f)
    
    with app.test_client() as client:
        response = client.post(
            '/api/generate/india',
            json=product_data,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'html' in data
        assert data['region'] == 'india'
        assert data['product_name'] == 'Chocolate Chip Cookies'
        print(f"✓ India label generated: {data['product_name']}")
        print(f"  HTML length: {len(data['html'])} characters")
        return True

def test_us_generate():
    """Test US label generation"""
    print("\nTesting /api/generate/us...")
    
    # Load sample data
    with open('us_dataset/01_packaged_food.json', 'r') as f:
        product_data = json.load(f)
    
    with app.test_client() as client:
        response = client.post(
            '/api/generate/us',
            json=product_data,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'html' in data
        assert data['region'] == 'us'
        print(f"✓ US label generated: {data['product_name']}")
        print(f"  HTML length: {len(data['html'])} characters")
        return True

def test_eu_generate():
    """Test EU label generation"""
    print("\nTesting /api/generate/eu...")
    
    # Load sample data
    with open('eu_dataset/01_packaged_food.json', 'r') as f:
        product_data = json.load(f)
    
    with app.test_client() as client:
        response = client.post(
            '/api/generate/eu',
            json=product_data,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'html' in data
        assert data['region'] == 'eu'
        print(f"✓ EU label generated: {data['product_name']}")
        print(f"  HTML length: {len(data['html'])} characters")
        return True

def test_validation_error():
    """Test validation error handling"""
    print("\nTesting validation error handling...")
    
    # Invalid data (missing required fields)
    invalid_data = {
        "product_name": "Test Product"
        # Missing all other required fields
    }
    
    with app.test_client() as client:
        response = client.post(
            '/api/generate/india',
            json=invalid_data,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
        assert 'errors' in data
        assert len(data['errors']) > 0
        print(f"✓ Validation errors caught: {len(data['errors'])} errors")
        print(f"  Sample error: {data['errors'][0]}")
        return True

def test_404():
    """Test 404 error"""
    print("\nTesting 404 error...")
    
    with app.test_client() as client:
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] == False
        print("✓ 404 error handled correctly")
        return True

def main():
    """Run all tests"""
    print("="*60)
    print("Flask API Test Suite")
    print("="*60)
    
    tests = [
        test_health,
        test_india_generate,
        test_us_generate,
        test_eu_generate,
        test_validation_error,
        test_404
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n✓ All tests passed! API is working correctly.")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())