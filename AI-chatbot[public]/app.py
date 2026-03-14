from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/chat/completions"

conversation = [
    {"role": "system", "content": "You are a helpful AI assistant"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    conversation.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "deepseek-chat",
        "messages": conversation, 
        "temperature": 1.3 #Setting 1.3 Temperature for general conversation
    }

    try:
        response = requests.post(BASE_URL, json=body, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.json()
        print("DeepSeek response:", data)  # DEBUG: see the raw API response

        # Adjust to DeepSeek response format
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "message" in data:  # some DeepSeek plans return 'message'
            reply = data["message"]["content"]
        else:
            reply = "Sorry, I couldn't get a response from the AI."

    except requests.exceptions.RequestException as e:
        print("API request error:", e)
        reply = "Sorry, there was an error contacting the AI."
    except Exception as e:
        print("Unexpected error:", e)
        reply = "Sorry, something went wrong."

    conversation.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)