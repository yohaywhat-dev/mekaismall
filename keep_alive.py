#keep_alive.py
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is awake ✅"

def run():
    # host="0.0.0.0" 代表接受所有外部請求
    # port=8080 你部署的平台通常都支援
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    # 用 Thread 讓 Flask 在背景跑，不阻塞主程式
    server_thread = Thread(target=run)
    server_thread.start()
