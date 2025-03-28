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
   
   **Windows:**
   ```
   docker build -t openai-websearch-api .
   ```
   
   **Linux:**
   ```
   sudo docker build -t openai-websearch-api .
   ```

2. **Start the container**
   
   The docker-compose.yml uses host network mode for better compatibility with n8n:
   ```yaml
   version: '3'
   
   services:
     openai-websearch-api:
       build: .
       network_mode: "host"
       env_file: 
         - .env
       restart: unless-stopped
   ```
   
   Start the container:
   ```
   sudo docker-compose up -d
   ```

3. **Verify deployment**
   ```
   sudo docker ps
   ```
   You should see your container running and using the host network.

4. **Find your host IP** (for n8n configuration):
   ```
   ip addr show
   ```
   Look for your main network interface (usually eth0 or ens4). For example:
   ```
   2: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
       inet 10.138.0.2/32 ...
   ```
   Note down this IP address (in this example, 10.138.0.2).

### n8n Integration

Configure an HTTP Request node in n8n:

1. **Set the request details**:
   - URL: `http://your.host.ip:5000/ask` (e.g., `http://10.138.0.2:5000/ask`)
   - Method: `POST`
   - Headers: `Content-Type: application/json`
   - Body: 
     ```json
     {
       "prompt": {{$json.intent}}
     }
     ```

2. **Process the response** in subsequent nodes using `{{$json.response}}`

### Troubleshooting n8n Connection

If you encounter connection issues:

1. **Verify the API is running**:
   ```
   curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d "{\"prompt\":\"test\"}"
   ```

2. **Check container logs**:
   ```
   sudo docker logs $(sudo docker ps -q --filter ancestor=openai-websearch-api)
   ```

3. **Verify network access**:
   ```
   # Test from the host machine
   curl -X POST http://your.host.ip:5000/ask -H "Content-Type: application/json" -d "{\"prompt\":\"test\"}"
   ```

4. **Common issues and solutions**:
   - If n8n can't connect, ensure it's running on the same network or has access to the host network
   - If the host IP changes, update the n8n HTTP Request node URL accordingly
   - For security, consider setting up proper network isolation in production environments

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
   sudo apt install -y docker.io
   
   # Install Docker Compose V2 (plugin method)
   sudo apt install -y docker-compose-plugin
   
   # OR install standalone docker-compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   
   sudo systemctl enable docker
   sudo systemctl start docker
   ```
   
   **CentOS/RHEL:**
   ```
   sudo yum install -y docker
   
   # Install Docker Compose V2 (plugin method)
   sudo yum install -y docker-compose-plugin
   
   # OR install standalone docker-compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

3. Follow the Docker deployment steps above (using sudo for all Docker commands)

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
- **Docker without sudo**: To run Docker without sudo on Linux, add your user to the docker group:
  ```
  sudo usermod -aG docker $USER
  # Log out and log back in for changes to take effect
  ```
- **Network Mode**: Using host network mode provides better compatibility with n8n but may not be suitable for all production environments
- **Security**: When using host network mode, your API is accessible on your host's network interface. Consider implementing additional security measures
- **IP Address**: The host IP may change after system restart on some cloud platforms. Update your n8n configuration accordingly 