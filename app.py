from flask import Flask, request, jsonify
import requests
import re  # Used for simple regex to parse inputs

# Import the simulation functions from your new file
from simulate import estimate_efficiency, compute_gen_adjustment, create_simulation_response

# Create a new Flask web server
app = Flask(__name__)

# Load the system prompt from the PROMPTS.md file
def get_system_prompt():
    try:
        with open('PROMPTS.md', 'r') as f:
            content = f.read()
            if "## System Prompt for LLM" in content:
                prompt_text = content.split("## System Prompt for LLM")[1].strip()
                return prompt_text.replace('"', '').strip()
            else:
                return "You are a helpful assistant."
    except FileNotFoundError:
        print("PROMPTS.md not found. Using a default prompt.")
        return "You are a helpful assistant."

system_prompt = get_system_prompt()

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    return 'Hello, World! The chatbot backend is running.'

# Define the chat route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower() # Get message and convert to lowercase

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # --- New Logic Starts Here ---
    # 1. Check for simulation commands
    temp_match = re.search(r'temp.*?(\d+)', user_message)
    mw_match = re.search(r'mw.*?(\d+)', user_message)

    if "simulate" in user_message and temp_match and mw_match:
        try:
            temp = float(temp_match.group(1))
            mw = float(mw_match.group(1))

            # Use placeholder humidity for this simple example
            humidity = 70.0
            base_eff = mw / 1000 # A simplified baseline efficiency

            new_eff = estimate_efficiency(base_eff, temp, humidity)
            new_gen_mw = compute_gen_adjustment(new_eff, base_gen_capacity_mw=1000)

            efficiency_change = ((new_eff - base_eff) / base_eff) * 100

            # Return the structured simulation response
            return jsonify(create_simulation_response(efficiency_change, new_gen_mw))

        except Exception as e:
            return jsonify({"type": "text", "payload": {"message": "Sorry, I couldn't understand the simulation parameters. Please provide a clear temperature and MW."}})

    # 2. If not a simulation command, use the LLM as a fallback
    try:
        payload = {
            "model": "llama3",
            "prompt": f"{system_prompt}\n\nUser: {user_message}",
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()

        response_json = response.json()
        bot_response = response_json['response'].strip()

        return jsonify({"type": "text", "payload": {"message": bot_response}})

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return jsonify({"type": "text", "payload": {"message": "Failed to get a response from the local chatbot. Is Ollama running?"}}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)