from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
import openai

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'

def get_openai_response(prompt):
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 60,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["text"]

if __name__ == '__main__':
    app.run(debug=True)
