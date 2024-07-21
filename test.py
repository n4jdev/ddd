import streamlit as st
import requests
from flask import Flask, request, jsonify
from threading import Thread
import json

# Flask app for API endpoint
app = Flask(__name__)

# API endpoint
@app.route('/api/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    
    # Forward the request to the specified API
    response = requests.post(
        'https://api.discord.rocks/chat/completions',
        headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'authority': 'api.discord.rocks',
            'accept-language': 'en-PH,en-US;q=0.9,en;q=0.8',
            'authorization': 'Bearer null',
            'origin': 'https://llmplayground.net',
            'referer': 'https://llmplayground.net/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site'
        },
        json=data
    )
    
    return jsonify(response.json())

# Function to run Flask app
def run_flask():
    app.run(port=5000)

# Start Flask app in a separate thread
Thread(target=run_flask).start()

# Streamlit app
st.title("Chat Application")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your message?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the request to the API
    data = {
        "messages": st.session_state.messages,
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 4096,
        "temperature": 1,
        "top_p": 1,
        "stream": False
    }

    # Send request to local API endpoint
    response = requests.post('https://n5codsmov4n9imskpaqupq.streamlit.app/api/chat/completions', json=data)
    
    if response.status_code == 200:
        assistant_response = response.json()
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    else:
        st.error("Failed to get response from the API")
