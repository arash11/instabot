import sys
import os
import time
import random
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

from insta_client import InstaClient
from responder import Responder
from order_handler import OrderHandler
from reply_generator import ReplyGenerator
from settings import SETTINGS


if os.environ.get("SESSION_JSON"):
    session_data = json.loads(os.environ["SESSION_JSON"])
    with open("session.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f)


def main():
    insta = InstaClient("session.json")
    generator = ReplyGenerator()
    responder = Responder(insta, generator)
    order_handler = OrderHandler()

    while True:
        messages = insta.get_unread_messages()

        for msg in messages:
            if msg.user_id == insta.my_user_id:
                continue

            if order_handler.is_order_request(msg.text):
                order_handler.save_order(msg.user_id, msg.text)

            reply = generator.generate_reply(msg.text)
          # delay = random.randint(300, 3000)
          # time.sleep(delay)
            responder.send_reply(msg, reply)

        time.sleep(60)

if __name__ == "__main__":
    main()
