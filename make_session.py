from instagrapi import Client

username = input("Username: ")
password = input("Password: ")

cl = Client()
cl.login(username, password)
cl.dump_settings("session.json")
print("✅ session.json ذخیره شد.")
