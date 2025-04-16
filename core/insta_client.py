from instagrapi import Client
import json

class Message:
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text

class InstaClient:
    def __init__(self, session_path):
        with open(session_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            sessionid = data["authorization_data"]["sessionid"]

        self.cl = Client()
        self.cl.login_by_sessionid(sessionid)
        self.my_user_id = self.cl.user_id

    def get_unread_messages(self):
        inbox = self.cl.direct_threads(amount=10)
        messages = []
        for thread in inbox:
            if thread.messages:
                last_msg = thread.messages[0]  # آخرین پیام در چت
                if last_msg.user_id != self.my_user_id:
                    messages.append(Message(last_msg.user_id, last_msg.text))
        return messages
