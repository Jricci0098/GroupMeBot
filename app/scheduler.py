import json
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.rss_reader import get_nab_daily_reading
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


def post_daily_message():
    # index, novena = get_active_novena()
    # novena_msg = get_today_message(novena["Novena Name"], int(novena["Day"])) if novena else "📿 No active novena."
    scripture = get_nab_daily_reading()

    try:
        with open(INTENTION_FILE, "r") as f:
            intentions = json.load(f)
    except FileNotFoundError:
        intentions = []

    today = datetime.now().date().isoformat()
    today_intentions = [i for i in intentions if i["timestamp"].startswith(today)]

    if today_intentions:
        intent_block = "🙏 *Today's Intentions:*\n\n" + "\n".join([f"{i+1}. {x['message']}" for i, x in enumerate(today_intentions)])
    else:
        intent_block = "🙏 No intentions submitted yet."

    post = f"""
📖 *Daily Scripture Reading (New American Bible via USCCB)*:
{scripture}

{intent_block}
""".strip()

    send_message(post)
#    advance_novena_day(index)
    with open(INTENTION_FILE, "w") as f:
        json.dump([], f, indent=2)


def schedule_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(post_intentions, 'cron', hour=18, minute=0)  # 6 PM
    scheduler.add_job(post_daily_message, 'cron', hour=7, minute=0)
    scheduler.start()
