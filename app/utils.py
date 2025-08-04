import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_ID = os.getenv("GROUPME_BOT_ID")
API_URL = "https://api.groupme.com/v3/bots/post"

def send_message(text):
    payload = { "bot_id": BOT_ID, "text": text }
    requests.post(API_URL, json=payload)
