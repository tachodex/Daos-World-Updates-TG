from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "DAO Monitor Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    t = Thread(target=run)
    t.start()
