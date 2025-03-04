from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app.py - Add these lines
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def ask_ai(prompt, history=[]):
    try:
        messages = [
            {"role": "system", "content": "You are Coral AI, a coding assistant."}
        ] + history + [
            {"role": "user", "content": prompt}
        ]

        logging.debug(f"Sending to OpenAI: {messages}")  # Debug log
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    except Exception as e:
        logging.error(f"OpenAI Error: {str(e)}")  # Detailed error logging
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_prompt = data.get('prompt', '')
        history = data.get('history', [])
        
        if not user_prompt:
            return jsonify({"response": "Error: Empty prompt"}), 400
            
        ai_response = ask_ai(user_prompt, history)
        return jsonify({"response": ai_response})
    
    except Exception as e:
        logging.error(f"Route Error: {str(e)}")
        return jsonify({"response": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)