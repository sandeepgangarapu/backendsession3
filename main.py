from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TSA Item Checker API",
    description="Check if items are allowed in TSA carry-on or checked baggage",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ItemRequest(BaseModel):
    item: str

class TSAResponse(BaseModel):
    item: str
    carry_on_allowed: bool
    checked_baggage_allowed: bool
    description: str
    restrictions: str

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    logger.warning("OPENROUTER_API_KEY not found in environment variables")

async def check_tsa_rules(item: str) -> Dict[str, Any]:
    """
    Use OpenRouter API to check TSA rules for a given item
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
    
    prompt = f"""
    You are a TSA (Transportation Security Administration) expert. 
    
    For the item "{item}", please provide:
    1. Whether it's allowed in carry-on baggage (true/false)
    2. Whether it's allowed in checked baggage (true/false)
    3. A brief description of the item category
    4. Any specific restrictions or requirements
    
    Please respond in JSON format with these exact keys:
    {{
        "carry_on_allowed": boolean,
        "checked_baggage_allowed": boolean,
        "description": "brief description of the item and its category",
        "restrictions": "any specific restrictions, size limits, or special requirements"
    }}
    
    Base your response on official TSA guidelines. If unsure about an item, err on the side of caution and suggest checking with TSA directly.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.1
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail="Error communicating with AI service")
            
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            
            # Try to parse JSON from AI response
            try:
                import json
                # Extract JSON from the response (AI might include extra text)
                start_idx = ai_response.find('{')
                end_idx = ai_response.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = ai_response[start_idx:end_idx]
                    parsed_result = json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
                
                return parsed_result
                
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse AI response: {ai_response}")
                # Fallback response
                return {
                    "carry_on_allowed": False,
                    "checked_baggage_allowed": False,
                    "description": f"Unable to determine rules for {item}",
                    "restrictions": "Please check with TSA directly for this item"
                }
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to AI service timed out")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "TSA Item Checker API is running!", "status": "healthy"}

@app.post("/check-item", response_model=TSAResponse)
async def check_item(request: ItemRequest):
    """
    Check if an item is allowed in carry-on or checked baggage according to TSA rules
    """
    if not request.item.strip():
        raise HTTPException(status_code=400, detail="Item name cannot be empty")
    
    try:
        # Get TSA rules from AI
        tsa_info = await check_tsa_rules(request.item)
        
        return TSAResponse(
            item=request.item,
            carry_on_allowed=tsa_info["carry_on_allowed"],
            checked_baggage_allowed=tsa_info["checked_baggage_allowed"],
            description=tsa_info["description"],
            restrictions=tsa_info["restrictions"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing item {request.item}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing request")

@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "api_key_configured": bool(OPENROUTER_API_KEY),
        "service": "TSA Item Checker API"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 