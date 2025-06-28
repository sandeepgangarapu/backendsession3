# TSA Item Checker API

A FastAPI application that checks whether items are allowed in TSA carry-on or checked baggage using AI-powered analysis via OpenRouter API.

## Features

- ✅ Check if items are allowed in carry-on baggage
- ✅ Check if items are allowed in checked baggage  
- ✅ Get detailed descriptions and restrictions
- ✅ RESTful API with automatic documentation
- ✅ CORS enabled for web applications
- ✅ Health check endpoints for monitoring

## API Endpoints

### Main Endpoints

- `POST /check-item` - Check TSA rules for an item
- `GET /` - Health check
- `GET /health` - Detailed health check
- `GET /docs` - Interactive API documentation (Swagger)
- `GET /redoc` - Alternative API documentation

### Example Usage

```bash
# Check if a laptop is allowed
curl -X POST "http://localhost:8000/check-item" \
     -H "Content-Type: application/json" \
     -d '{"item": "laptop"}'
```

Expected response:
```json
{
  "item": "laptop",
  "carry_on_allowed": true,
  "checked_baggage_allowed": true,
  "description": "Electronic device - personal computer",
  "restrictions": "Must be removed from bag during security screening. Lithium batteries should be in carry-on when possible."
}
```

## Setup Instructions

### 1. Get OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Generate an API key
4. Note down your API key

### 2. Local Development

1. Clone/download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

4. Run the application:
   ```bash
   python main.py
   ```
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. Open your browser to `http://localhost:8000/docs` to see the interactive API documentation

### 3. Deploy to Render

1. Push your code to a Git repository (GitHub, GitLab, etc.)

2. Go to [Render](https://render.com/) and sign up

3. Create a new Web Service:
   - Connect your Git repository
   - Choose the branch to deploy
   - Set the following:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
     - **Environment**: Python 3

4. Add Environment Variables in Render dashboard:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `PORT`: 8000 (optional, Render sets this automatically)

5. Deploy! Render will provide you with a URL like `https://your-app.onrender.com`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |
| `PORT` | Port to run the server on | No (default: 8000) |

## Testing

Test with curl:
```bash
# Test health endpoint
curl http://localhost:8000/

# Test item checking
curl -X POST "http://localhost:8000/check-item" \
     -H "Content-Type: application/json" \
     -d '{"item": "water bottle"}'

curl -X POST "http://localhost:8000/check-item" \
     -H "Content-Type: application/json" \
     -d '{"item": "knife"}'
```

## API Response Format

All `/check-item` responses follow this format:

```json
{
  "item": "string",
  "carry_on_allowed": boolean,
  "checked_baggage_allowed": boolean,
  "description": "string",
  "restrictions": "string"
}
```

## Error Handling

The API includes comprehensive error handling:
- 400: Bad request (empty item name)
- 500: Server errors (API key issues, OpenRouter problems)
- 504: Timeout errors

## Security Notes

- Never commit your `.env` file or API keys to version control
- The API key should be kept secure
- Consider implementing rate limiting for production use

## Support

For TSA-related questions, always refer to the official [TSA website](https://www.tsa.gov/travel/security-screening/whatcanibring/all) for the most up-to-date information. 