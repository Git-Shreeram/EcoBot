from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Azure OpenAI details
AZURE_OPENAI_ENDPOINT = "https://openai.azure.com/"  # Replace with your Azure OpenAI endpoint
AZURE_OPENAI_API_KEY = "OPENAI_API_KEY"  # Replace with your Azure OpenAI API key


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/messages', methods=['POST'])
def api_messages():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY  # Changed from Authorization to api-key
        }
        data = {
            "messages": [{"role": "user", "content": user_message}]
        }

        response = requests.post(
            f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/EcoBot/chat/completions?api-version=2024-05-01-preview",
            json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            bot_response = response_data['choices'][0]['message']['content']
            return jsonify({"response": bot_response})
        else:
            error_message = f"Error from Azure OpenAI: {response.status_code} {response.text}"
            print(error_message)  # Log the error message
            return jsonify({"error": "Failed to get a response from Azure OpenAI"}), response.status_code
    except Exception as e:
        error_message = f"Exception: {str(e)}"
        print(error_message)  # Log the exception
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
