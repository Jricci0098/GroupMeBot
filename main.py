from flask import Flask, request
from app.bot import handle_message_payload
from app.scheduler import schedule_jobs

app = Flask(__name__)
schedule_jobs()  # Start background job scheduler

@app.route('/')
def home():
    return "GroupMe Novena Bot is running"

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    if data and data.get("sender_type") != "bot":
        handle_message_payload(data)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
