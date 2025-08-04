import json
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils import send_message

INTENTION_FILE = "app/data/intentions.json"

def post_intentions():
    try:
        with open(INTENTION_FILE, "r") as f:
            intentions = json.load(f)
    except FileNotFoundError:
        intentions = []

    if not intentions:
        return  # Nothing to post

    message = "🕊️ *Today’s Novena Intentions*:\n\n"
    for i, intent in enumerate(intentions, 1):
        message += f"{i}. {intent['message']}\n"

    send_message(message)

    # Clear intentions after posting
    with open(INTENTION_FILE, "w") as f:
        json.dump([], f)

def schedule_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(post_intentions, 'cron', hour=18, minute=0)  # 6 PM
    scheduler.start()
