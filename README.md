# N8N Personal Assistant

A Flask-based API service that integrates with OpenAI's GPT models to provide AI assistance through n8n workflows. This project leverages the `gpt-4o-search-preview` model, which enables web search capabilities.

## Features

- REST API with a `/ask` endpoint for AI queries
- Integration with OpenAI's GPT models with web search capabilities
- Docker containerization for easy deployment
- Cloudflare Tunnel support for secure public access
- n8n integration for workflow automation

## Setup and Deployment

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- n8n instance (for workflow integration)
- Windows or Linux environment

### Basic Setup

1. **Clone this repository**

2. **Configure environment variables**
   Create a `.env` file with the following:
   ```
   OPENAI_API_KEY=your_api_key_here
   RUN_API=true
   ```

3. **Install dependencies** (for local development only)
   ```
   pip install -r requirements.txt
   ```

### Deployment Options

#### Option 1: Run directly with Python (Development)

```
python main.py
```

#### Option 2: Deploy with Docker (Recommended)

1. **Build the Docker image**
   ```
   docker build -t openai-websearch-api .
   ```

2. **Start the container**
   ```
   docker-compose up -d
   ```

3. **Verify deployment**
   ```
   docker ps
   ```
   You should see your container running and listening on port 5000.

#### Option 3: Deploy with Docker and Cloudflare Tunnel (Production)

1. **Deploy the Docker container** (follow Option 2 steps)

2. **Set up Cloudflare Tunnel**

   **Windows:**
   - Download cloudflared:
     ```
     Invoke-WebRequest -Uri https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -OutFile cloudflared.exe
     ```
   - Start a tunnel:
     ```
     .\cloudflared.exe tunnel --url http://localhost:5000
     ```
   - Keep the tunnel running in the background:
     ```
     Start-Process -NoNewWindow .\cloudflared.exe -ArgumentList "tunnel --url http://localhost:5000"
     ```

   **Linux:**
   - Download and install cloudflared:
     ```
     curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
     sudo dpkg -i cloudflared.deb
     ```
   - Start a tunnel:
     ```
     cloudflared tunnel --url http://localhost:5000
     ```
   - Keep the tunnel running in the background:
     ```
     nohup cloudflared tunnel --url http://localhost:5000 > cloudflared.log 2>&1 &
     ```

3. **Note the assigned URL** (e.g., `https://something-random-name.trycloudflare.com`)

## API Usage

### Direct API Calls

Send POST requests to the `/ask` endpoint:
```
POST /ask
Content-Type: application/json

{
  "prompt": "Your question for the AI assistant"
}
```

Example with curl:
```
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d "{\"prompt\":\"What is the current Bitcoin price?\"}"
```

Example with PowerShell (Windows):
```
Invoke-WebRequest -Uri "http://localhost:5000/ask" -Method POST -ContentType "application/json" -Body '{"prompt":"What is the current Bitcoin price?"}'
```

### n8n Integration

Configure an HTTP Request node in n8n:

1. **Set the request details**:
   - URL: `http://localhost:5000/ask` (local) or `https://your-tunnel-url.trycloudflare.com/ask` (with Cloudflare)
   - Method: `POST`
   - Headers: `Content-Type: application/json`
   - Body: 
     ```json
     {
       "prompt": {{$json.intent}}
     }
     ```

2. **Process the response** in subsequent nodes using `{{$json.response}}`

## VPS Deployment Notes

To deploy on a VPS:

1. Transfer all project files to your VPS:
   
   **Windows to Linux VPS:**
   ```
   scp -r ./* user@your-vps-ip:/path/to/app/
   ```
   
   **Linux to Linux VPS:**
   ```
   rsync -avz --exclude 'venv' --exclude '.git' ./ user@your-vps-ip:/path/to/app/
   ```

2. Install Docker and Docker Compose on VPS:
   
   **Ubuntu/Debian:**
   ```
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   ```
   
   **CentOS/RHEL:**
   ```
   sudo yum install -y docker docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

3. Follow the Docker deployment steps above

4. Install cloudflared on the VPS:
   ```
   curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared.deb
   ```

5. Run the tunnel command on the VPS:
   ```
   nohup cloudflared tunnel --url http://localhost:5000 > cloudflared.log 2>&1 &
   ```

6. To make the tunnel start automatically on system boot, create a systemd service:
   ```
   sudo nano /etc/systemd/system/cloudflared.service
   ```
   
   Add the following content:
   ```
   [Unit]
   Description=Cloudflare Tunnel
   After=network.target

   [Service]
   ExecStart=/usr/local/bin/cloudflared tunnel --url http://localhost:5000
   Restart=always
   User=ubuntu

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start the service:
   ```
   sudo systemctl enable cloudflared
   sudo systemctl start cloudflared
   ```

## Important Notes

- **API Security**: Consider adding authentication for production deployments
- **Cloudflare URL Changes**: The free quick tunnel URL changes each time you restart the tunnel
- **Rate Limiting**: Be mindful of OpenAI API rate limits and costs
- **Error Handling**: The API includes basic error handling for OpenAI API issues
- **Linux Permissions**: If running on Linux, ensure proper permissions for Docker and cloudflared 