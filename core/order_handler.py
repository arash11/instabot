import json
import os

class OrderHandler:
    def __init__(self, path='data/orders.json'):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump([], f)

    def is_order_request(self, text):
        if not text:
            return False
        return "سفارش" in text or "خرید" in text

    def save_order(self, user_id, text):
        with open(self.path, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        orders.append({"user_id": user_id, "text": text})
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
