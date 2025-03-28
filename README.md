# N8N Personal Assistant

A Flask-based API service that integrates with OpenAI's GPT models to provide AI assistance. The most crucial part of this project is that we're using the `gpt-4o-search-preview` model, which is a new model that allows us to search the web.

## Features

- Simple REST API with a `/ask` endpoint
- Integration with OpenAI's GPT models
- Docker support for easy deployment
- Cloudflare Tunnel support for secure public access

## Setup

1. Clone this repository
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   RUN_API=true
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

### Run directly with Python:
```
python main.py
```

### Run with Docker:
```
docker-compose up
```

## API Usage

Send POST requests to the `/ask` endpoint:
```
POST /ask
Content-Type: application/json

{
  "prompt": "Your question for the AI assistant"
}
```

The response will be a JSON object with the AI's answer.

## Docker and Cloudflare Tunnel Setup

### Step 1: Build and Run Your Docker Container

1. **Build your Docker image**:
   ```
   docker build -t openai-websearch-api .
   ```

2. **Run your Docker container**:
   ```
   docker-compose up -d
   ```

3. **Verify your container is running**:
   ```
   docker ps
   ```
   You should see your container running and listening on port 5000.

### Step 2: Set Up Cloudflare Tunnel Manually

1. **Download cloudflared** (if you haven't already):
   ```
   Invoke-WebRequest -Uri https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -OutFile cloudflared.exe
   ```

2. **Start a quick tunnel** to expose your Docker container:
   ```
   .\cloudflared.exe tunnel --url http://localhost:5000
   ```

3. **Note the assigned URL**:
   When you run the command, cloudflared will output a URL like:
   ```
   https://something-random-name.trycloudflare.com
   ```
   This is your public URL for accessing the API.

### Step 3: Test Your API Through the Tunnel

1. **Test with curl**:
   ```
   curl -X POST https://your-tunnel-url.trycloudflare.com/ask -H "Content-Type: application/json" -d "{\"prompt\":\"What is the current Bitcoin price?\"}"
   ```

2. **Or with PowerShell**:
   ```
   Invoke-WebRequest -Uri "https://your-tunnel-url.trycloudflare.com/ask" -Method POST -ContentType "application/json" -Body '{"prompt":"What is the current Bitcoin price?"}'
   ```

### Step 4: Configure n8n to Use Your Tunneled API

In your n8n HTTP Request node:
1. Set the URL to your Cloudflare tunnel URL: `https://your-tunnel-url.trycloudflare.com/ask`
2. Set the method to `POST`
3. Add a header:
   - Name: `Content-Type`
   - Value: `application/json`
4. Set the JSON body to:
   ```
   {
     "prompt": {{$json.intent}}
   }
   ```

### Important Notes

1. **Keeping the Tunnel Running**:
   - The tunnel will only remain active as long as the cloudflared process is running
   - If you close your terminal, the tunnel will stop
   - To keep it running in the background, you can use:
     ```
     Start-Process -NoNewWindow .\cloudflared.exe -ArgumentList "tunnel --url http://localhost:5000"
     ```

2. **For VPS Deployment**:
   - Transfer your Docker files to the VPS
   - Build and run the container as described above
   - Install cloudflared on the VPS
   - Run the tunnel command on the VPS

3. **URL Changes**:
   - With the free quick tunnel, the URL will change each time you restart the tunnel
   - You'll need to update your n8n configuration with the new URL each time 