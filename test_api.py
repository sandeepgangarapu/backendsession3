#!/usr/bin/env python3
"""
Simple test script for the TSA Item Checker API
"""

import httpx
import asyncio
import json

BASE_URL = "http://localhost:8000"

async def test_api():
    """Test the TSA Item Checker API endpoints"""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing TSA Item Checker API\n")
        
        # Test health endpoint
        print("1. Testing health endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test detailed health endpoint
        print("2. Testing detailed health endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Test item checking with various items
        test_items = [
            "laptop",
            "water bottle",
            "nail scissors", 
            "phone charger",
            "large knife"
        ]
        
        print("3. Testing item checking...")
        for item in test_items:
            try:
                print(f"   Testing item: '{item}'")
                response = await client.post(
                    f"{BASE_URL}/check-item",
                    json={"item": item},
                    timeout=30.0
                )
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"   Carry-on: {result['carry_on_allowed']}")
                    print(f"   Checked: {result['checked_baggage_allowed']}")
                    print(f"   Description: {result['description']}")
                    print(f"   Restrictions: {result['restrictions']}")
                else:
                    print(f"   Error: {response.text}")
                print()
            except Exception as e:
                print(f"   Error testing '{item}': {e}\n")

if __name__ == "__main__":
    print("Make sure the API is running on http://localhost:8000")
    print("Start it with: python main.py\n")
    asyncio.run(test_api()) 