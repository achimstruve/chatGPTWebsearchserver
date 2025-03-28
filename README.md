# N8N Personal Assistant

A Flask-based API service that integrates with OpenAI's GPT models to provide AI assistance. The most crucial part of this project is that we're using the `gpt-4o-search-preview` model, which is a new model that allows us to search the web.

## Features

- Simple REST API with a `/ask` endpoint
- Integration with OpenAI's GPT models
- Docker support for easy deployment

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