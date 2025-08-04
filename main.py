from flask import Flask, request
from app.bot import handle_message_payload

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "GroupMe Novena Bot is running"

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    if data and data.get("sender_type") != "bot":  # Prevent bot from responding to itself
        handle_message_payload(data)
    return "OK", 200

