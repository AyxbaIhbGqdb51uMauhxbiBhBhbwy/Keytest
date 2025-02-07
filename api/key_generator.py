import threading
import time
import random
import string

key = None

def generate_key():
    global key
    while True:
        random_letters = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        key = f"StarX_{random_letters}"
        time.sleep(60)

threading.Thread(target=generate_key, daemon=True).start()
