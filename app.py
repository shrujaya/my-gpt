#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Set your Gemini API key as an environment variable for security
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user_message = data.get('message')
    if not model:
        return jsonify({'reply': 'Gemini API key not set.'})
    
    try:
        with open('sme_prompt.md', 'r') as file:
            system_prompt = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{'sme_prompt.md'}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    prompt = f"{system_prompt}\n\nHere is the user's input: {user_message}"
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(port=9999)