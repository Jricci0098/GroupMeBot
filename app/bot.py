from app.utils import send_message

def handle_message_payload(data):
    text = data.get("text", "").strip().lower()
    sender = data.get("name", "")

    if text == "!novena":
        send_message("📿 Today’s novena message (placeholder).")
    elif text.startswith("!add novena"):
        send_message(f"✅ {sender}, your novena request has been received (TBD).")
