from app.utils import send_message

import json
from datetime import datetime
from app.utils import send_message

INTENTION_FILE = "app/data/intentions.json"

def handle_message_payload(data):
    text = data.get("text", "").strip()
    sender = data.get("name", "")

    if text.lower().startswith("!addintention"):
        message = text[len("!addintention"):].strip()
        if message:
            log_intention(message)
            send_message("🙏 Your intention has been submitted anonymously.")
        else:
            send_message("⚠️ Please provide an intention after the command. Example:\n`!intention For my grandfather’s healing`")

    elif text.lower() == "!novena":
        send_message("📿 Today’s novena message (placeholder).")

    elif text.lower() == "!getintentions":
        today_intentions = get_today_intentions()
        if today_intentions:
            message = "🕊️ *Today's Novena Intentions (so far)*:\n\n"
            for i, intent in enumerate(today_intentions, 1):
                message += f"{i}. {intent['message']}\n"
        else:
            message = "📭 No intentions submitted yet today. Use `!intention [your prayer]` to add one."

        send_message(message)
    elif text.lower().startswith("!deleteintention"):
        parts = text.strip().split()
        if len(parts) != 2 or not parts[1].isdigit():
            send_message("❌ Usage: `!deleteintention [number]`. Example: `!deleteintention 2`")
            return

        delete_index = int(parts[1]) - 1
        success = delete_today_intention(delete_index)

        if success:
            send_message(f"✅ Intention #{parts[1]} was deleted.")
        else:
            send_message(f"⚠️ Could not delete intention #{parts[1]}. Make sure it's valid and from today.")


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

def delete_today_intention(index_to_delete):
    from datetime import datetime

    try:
        with open(INTENTION_FILE, "r") as f:
            intentions = json.load(f)
    except FileNotFoundError:
        return False

    today = datetime.now().date().isoformat()

    # Only keep intentions not from today or not the one being deleted
    today_intentions = [i for i in intentions if i["timestamp"].startswith(today)]
    other_intentions = [i for i in intentions if not i["timestamp"].startswith(today)]

    if index_to_delete < 0 or index_to_delete >= len(today_intentions):
        return False

    # Remove the requested intention
    del today_intentions[index_to_delete]

    # Save updated file
    new_list = other_intentions + today_intentions
    with open(INTENTION_FILE, "w") as f:
        json.dump(new_list, f, indent=2)

    return True
