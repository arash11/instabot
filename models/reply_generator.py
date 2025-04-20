import random
import time

class ReplyGenerator:
    def __init__(self):
        self.replies = [
            "حتماً عزیزم 🌟",
            "الان بررسی می‌کنم 😊",
            "ممنون از پیامت 🙏",
            "در اسرع وقت بهت اطلاع می‌دیم 💬",
            "باشه چشم 👀"
        ]
        self.emojis = ["😊", "🌟", "🙏", "💬", "❤️", "✨", "😎", "🛍️", "📦", "🚀"]

    def get_human_delay(self):
        base_delay = random.randint(20 * 60, 120 * 60)  # 20 تا 120 دقیقه
        jitter = random.uniform(-30, 30)  # نویز ±30 ثانیه
        delay = max(0, base_delay + jitter)
        print(f"⏳ Human-like delay: {delay / 60:.1f} minutes")
        return delay

    def generate_reply(self, input_text, max_new_tokens=50):
        print(f"🤖 Generating reply for: {input_text}")
        reply = random.choice(self.replies)
        emoji = random.choice(self.emojis)
        final_reply = f"{reply} {emoji}"
        print(f"✍️ Reply generated: {final_reply}")
        return final_reply
