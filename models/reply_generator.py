import random
import asyncio

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
        """Generate a human-like delay between 20 and 120 minutes"""
        base_delay = random.randint(20 * 60, 120 * 60)  # 20 to 120 minutes
        jitter = random.uniform(-30, 30)  # ±30 seconds noise
        delay = max(0, base_delay + jitter)
        print(f"⏳ Human-like delay: {delay / 60:.1f} minutes")
        return delay

    async def generate_reply(self, input_text, max_new_tokens=50):
        """Generate a reply for the input text"""
        print(f"🤖 Generating reply for: {input_text}")
        reply = random.choice(self.replies)
        emoji = random.choice(self.emojis)
        final_reply = f"{reply} {emoji}"
        print(f"✍️ Reply generated: {final_reply}")
        # Small random delay to simulate processing
        await asyncio.sleep(random.uniform(0.5, 2))
        return final_reply
