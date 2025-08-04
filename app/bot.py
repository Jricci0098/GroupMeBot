from app.utils import send_message

import json
from datetime import datetime
from app.utils import send_message

INTENTION_FILE = "app/data/intentions.json"

def handle_message_payload(data):
    text = data.get("text", "").strip()
    sender = data.get("name", "")

    if text.lower("!intention"):
        message = text[len("!intention"):].strip()
        if message:
            log_intention(message)
            send_message("🙏 Your intention has been submitted anonymously.")
        else:
            send_message("⚠️ Please provide an intention after the command. Example:\n`!intention For my grandfather’s healing`")

    elif text.lower() == "!novena":
        send_message("📿 Today’s novena message (placeholder).")

    elif text.lower() == "!intentions":
        today_intentions = get_today_intentions()
        if today_intentions:
            message = "🕊️ *Today's Novena Intentions (so far)*:\n\n"
            for i, intent in enumerate(today_intentions, 1):
                message += f"{i}. {intent['message']}\n"
        else:
            message = "📭 No intentions submitted yet today. Use `!intention [your prayer]` to add one."

        send_message(message)


def log_intention(msg):
    try:
        with open(INTENTION_FILE, "r") as f:
            intentions = json.load(f)
    except FileNotFoundError:
        intentions = []

    intentions.append({
        "message": msg,
        "timestamp": datetime.now().isoformat()
    })

    with open(INTENTION_FILE, "w") as f:
        json.dump(intentions, f, indent=2)

def get_today_intentions():
    from datetime import datetime

    try:
        with open(INTENTION_FILE, "r") as f:
            intentions = json.load(f)
    except FileNotFoundError:
        return []

    today = datetime.now().date().isoformat()
    return [i for i in intentions if i["timestamp"].startswith(today)]
