from dotenv import load_dotenv
from os import getenv
from flask import Flask, request, jsonify
import openai


load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
app = Flask(__name__)

# Set the API key at the module level
openai.api_key = OPENAI_API_KEY


def get_gpt_answer(prompt):                
    try:
        # Use the older style client approach
        response = openai.ChatCompletion.create(
            model="gpt-4o-search-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.choices[0].message.content
        return text
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return f"Error: {str(e)}"
   

@app.route('/ask', methods=['POST'])
def ask_gpt():
    # Log request details
    print(f"Request headers: {request.headers}")
    print(f"Request content type: {request.content_type}")
    print(f"Request data: {request.data}")
    
    # Check content type
    if request.content_type != 'application/json':
        return jsonify({"error": f"Unsupported media type. Expected application/json but got {request.content_type}"}), 415
    
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "Please provide a prompt in the request body"}), 400
        
        prompt = data['prompt']
        response = get_gpt_answer(prompt)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Keep the original functionality for direct script execution
    if getenv("RUN_API", "false").lower() == "true":
        # Make sure to use host='0.0.0.0' to listen on all interfaces
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        # raise
        print("API is not running")
    