# Environment Variables Setup Guide

## How to Use Environment Variables for API Keys

### 1. Install Required Package
First, install the python-dotenv package to easily load environment variables:
```bash
pip install python-dotenv
```

### 2. Create a .env File
Create a `.env` file in your project directory (same folder as Bot.py):
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
FINNHUB_API_KEY=your_finnhub_api_key_here
```

### 3. Add .env to .gitignore
**IMPORTANT**: Create a `.gitignore` file to prevent committing your secrets:
```
.env
*.pyc
__pycache__/
```

## Setting Environment Variables

### Option 1: Using .env File (Recommended for Development)
1. Copy `.env.example` to `.env`
2. Fill in your actual API keys and webhook URL
3. The bot will automatically load these values

### Option 2: System Environment Variables

#### Windows (PowerShell):
```powershell
$env:DISCORD_WEBHOOK_URL="your_webhook_url_here"
$env:FINNHUB_API_KEY="your_api_key_here"
```

#### Windows (Command Prompt):
```cmd
set DISCORD_WEBHOOK_URL=your_webhook_url_here
set FINNHUB_API_KEY=your_api_key_here
```

#### Linux/Mac:
```bash
export DISCORD_WEBHOOK_URL="your_webhook_url_here"
export FINNHUB_API_KEY="your_api_key_here"
```

### Option 3: For Production Deployment

#### Heroku:
```bash
heroku config:set DISCORD_WEBHOOK_URL="your_webhook_url"
heroku config:set FINNHUB_API_KEY="your_api_key"
```

#### Docker:
```bash
docker run -e DISCORD_WEBHOOK_URL="your_webhook_url" -e FINNHUB_API_KEY="your_api_key" your-bot
```

## Getting Your API Keys

### 1. Finnhub API Key:
1. Go to https://finnhub.io/
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Discord Webhook:
1. Go to your Discord server
2. Right-click on the channel where you want alerts
3. Select "Edit Channel" → "Integrations" → "Webhooks"
4. Create a new webhook and copy the URL

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use different keys for development and production**
3. **Regularly rotate your API keys**
4. **Use the principle of least privilege** - only give keys the minimum permissions needed
5. **Monitor your API usage** to detect unauthorized access

## Troubleshooting

- If you get "environment variable is required" error, make sure your .env file exists and has the correct variable names
- Variable names are case-sensitive
- No spaces around the = sign in .env files
- No quotes needed in .env files unless the value contains special characters
