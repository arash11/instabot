class Responder:
    def __init__(self, insta_client, reply_generator):
        self.insta = insta_client
        self.generator = reply_generator

    def send_reply(self, msg, reply_text):
        self.insta.cl.direct_send(reply_text, [msg.user_id])
