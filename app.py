from flask import Flask, request, jsonify, render_template
from cyberbot import CyberBot
from botbuilder.core import TurnContext
import os
import pandas as pd
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask app
app = Flask(__name__)
bot = CyberBot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    
    # Try FAQ match first
    for keyword, answer in bot.faq.items():
        if keyword in user_message:
            return jsonify({"reply": answer})
    
    # Fallback to OpenAI
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"[ERROR] OpenAI failed: {e}")
        return jsonify({"reply": "Sorry, I couldn't find an answer."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3978)))
