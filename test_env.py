#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("OPENROUTER_API_KEY")

print("🔍 Environment Variable Test")
print("-" * 30)

if api_key:
    # Mask the key for security (show only first 8 and last 4 characters)
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print(f"✅ API Key found: {masked_key}")
    print(f"✅ Key length: {len(api_key)} characters")
    print(f"✅ Key starts with: {api_key[:8]}...")
else:
    print("❌ OPENROUTER_API_KEY not found!")
    print("\nTo fix this:")
    print("1. Create a .env file in your project root")
    print("2. Add this line: OPENROUTER_API_KEY=your_actual_key_here")
    print("3. Replace 'your_actual_key_here' with your real OpenRouter API key")

print("\n📁 Current working directory:", os.getcwd())
print("📄 Looking for .env file at:", os.path.join(os.getcwd(), ".env"))
print("📄 .env file exists:", os.path.exists(".env")) 