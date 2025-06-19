#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user_message = data.get('message')
    # For now, just echo the message back
    return jsonify({'reply': f'You said: {user_message}'})

if __name__ == '__main__':
    app.run(port=9999)