import sys
import os
import asyncio
import random
import json
import datetime
import logging
from logging.handlers import RotatingFileHandler

# تنظیمات لاگ
LOG_FILE = "bot_log.json"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 مگابایت
LOG_BACKUP_COUNT = 3  # حداکثر 3 فایل آرشیو

# تنظیم لاگ کنسول
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# تنظیم لاگ فایل چرخشی
file_handler = RotatingFileHandler("bot.log", maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

def log_event(event_type, details):
    """ثبت رویداد در فایل JSON و کنسول"""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }
    logger.info(f"{event_type}: {details}")
    
    # ذخیره در فایل JSON
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        logs.append(log_entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"خطا در ذخیره لاگ: {e}")

# Create session.json from ENV if present
if os.environ.get("SESSION_JSON"):
    log_event("info", "SESSION_JSON found. Writing to session.json")
    session_data = json.loads(os.environ["SESSION_JSON"])
    with open("session.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f)
    log_event("info", "session.json created successfully")

# Add module paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

log_event("info", "Importing modules")

from insta_client import InstaClient
from responder import Responder
from order_handler import OrderHandler
from reply_generator import ReplyGenerator
from settings import SETTINGS

# تنظیمات محدودیت اینستاگرام
MAX_MESSAGES_PER_HOUR = 10
MAX_MESSAGES_PER_DAY = 30
ACTIVE_HOURS = range(8, 22)  # 8 صبح تا 10 شب
MESSAGE_LOG = []  # لاگ پیام‌های ارسالی

def is_active_time():
    """چک کردن ساعات فعال"""
    return datetime.datetime.now().hour in ACTIVE_HOURS

async def main():
    log_event("info", "Initializing bot")
    insta = InstaClient("session.json")
    log_event("info", "Connected to Instagram")

    generator = ReplyGenerator()
    await asyncio.sleep(generator.get_human_delay())  # تأخیر اولیه
    log_event("info", "Language model loaded")

    responder = Responder(insta, generator)
    log_event("info", "Responder module is ready")

    order_handler = OrderHandler()
    log_event("info", "Order handler initialized")

    daily_count = 0
    hourly_count = 0
    last_hour = datetime.datetime.now().hour

    while True:
        if not is_active_time():
            log_event("info", "خارج از ساعات فعال، خواب برای 1 ساعت")
            await asyncio.sleep(3600)
            continue

        # ریست شمارشگر ساعتی
        current_hour = datetime.datetime.now().hour
        if current_hour != last_hour:
            hourly_count = 0
            last_hour = current_hour

        # ریست شمارشگر روزانه
        if MESSAGE_LOG and datetime.datetime.now().day != MESSAGE_LOG[-1]["timestamp"].day:
            daily_count = 0

        # چک کردن محدودیت‌ها
        if hourly_count >= MAX_MESSAGES_PER_HOUR or daily_count >= MAX_MESSAGES_PER_DAY:
            log_event("warning", f"به محدودیت پیام رسیدیم (ساعتی: {hourly_count}, روزانه: {daily_count})، خواب برای 1 ساعت")
            await asyncio.sleep(3600)
            continue

        log_event("info", "Checking for new messages")
        try:
            messages = insta.get_unread_messages()
            log_event("info", f"Messages received: {len(messages)}")

            for msg in messages:
                log_event("info", f"Message from user {msg.user_id}: {msg.text}")

                if msg.user_id == insta.my_user_id:
                    log_event("info", "Skipping message from self")
                    continue

                # جلوگیری از پاسخ تکراری
                if any(log["recipient"] == msg.user_id for log in MESSAGE_LOG[-10:]):
                    log_event("info", f"پیام تکراری از {msg.user_id}، رد می‌شود")
                    continue

                if order_handler.is_order_request(msg.text):
                    log_event("info", f"Order request detected from {msg.user_id}")
                    order_handler.save_order(msg.user_id, msg.text)

                reply = await generator.generate_reply(msg.text)
                log_event("info", f"Generated reply: {reply}")

                try:
                    responder.send_reply(msg, reply)
                    log_event("message_sent", f"Reply sent to {msg.user_id}: {reply}")
                    MESSAGE_LOG.append({
                        "recipient": msg.user_id,
                        "message": reply,
                        "timestamp": datetime.datetime.now()
                    })
                    hourly_count += 1
                    daily_count += 1
                    # تأخیر تصادفی بین پیام‌ها
                    await asyncio.sleep(random.uniform(5, 30))
                except Exception as e:
                    log_event("error", f"خطا در ارسال پیام به {msg.user_id}: {e}")
                    if "rate limit" in str(e).lower() or "challenge_required" in str(e).lower():
                        log_event("warning", "محدودیت API، خواب برای 4 ساعت")
                        await asyncio.sleep(4 * 3600)

        except Exception as e:
            log_event("error", f"خطا در گرفتن پیام‌ها: {e}")
            await asyncio.sleep(60)

        log_event("info", "Sleeping for 30-120 seconds")
        await asyncio.sleep(random.uniform(30, 120))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        log_event("error", f"Error during execution: {e}")
