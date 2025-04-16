import json

with open('config/settings.json', 'r', encoding='utf-8') as f:
    SETTINGS = json.load(f)
