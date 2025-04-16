import sys
import os
import time
import random
import json

print("✅ Starting main.py...")

# Create session.json from ENV if present
if os.environ.get("SESSION_JSON"):
    print("🔐 SESSION_JSON found. Writing to session.json ...")
    session_data = json.loads(os.environ["SESSION_JSON"])
    with open("session.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f)
    print("✅ session.json created successfully.")

# Add module paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

print("📦 Importing modules ...")

from insta_client import InstaClient
from responder import Responder
from order_handler import OrderHandler
from reply_generator import ReplyGenerator
from settings import SETTINGS

def main():
    print("🚀 Initializing bot ...")
    insta = InstaClient("session.json")
    print("✅ Connected to Instagram.")

    generator = ReplyGenerator()
    print("🧠 Language model loaded.")

    responder = Responder(insta, generator)
    print("📤 Responder module is ready.")

    order_handler = OrderHandler()
    print("📝 Order handler initialized.")

    while True:
        print("🔄 Checking for new messages ...")
        messages = insta.get_unread_messages()
        print(f"📬 Messages received: {len(messages)}")

        for msg in messages:
            print(f"👤 Message from user {msg.user_id}: {msg.text}")

            if msg.user_id == insta.my_user_id:
                print("↩️ Skipping message from self.")
                continue

            if order_handler.is_order_request(msg.text):
                print("🛒 Order request detected.")
                order_handler.save_order(msg.user_id, msg.text)

            reply = generator.generate_reply(msg.text)
            print(f"✍️ Generated reply: {reply}")
            responder.send_reply(msg, reply)
            print("📤 Reply sent.")

        print("🕐 Sleeping for 60 seconds ...")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error during execution: {e}")
