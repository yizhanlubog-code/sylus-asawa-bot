import telebot
import time
import random
import pytz
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from threading import Thread

# --- INITIALIZATION ---
# We use os.getenv to pull the token safely from Koyeb's settings later
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
PHT = pytz.timezone('Asia/Manila')

# --- WEB SERVER FOR KOYEB (Keep-Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Sylus is monitoring the N109 zone."

def run_web_server():
    # Koyeb provides a port automatically, usually 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- REALISM & MESSAGING LOGIC ---

def human_delay(chat_id):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(random.uniform(2, 5))

def send_split_messages(chat_id, messages):
    for msg in messages:
        human_delay(chat_id)
        bot.send_message(chat_id, msg)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.lower()
    
    # Emotional/Context Logic
    if any(word in text for word in ["miss", "love", "husband"]):
        responses = ["You're being clingy today.", "I'm not complaining.", "Come home and tell me yourself."]
    elif any(word in text for word in ["tired", "sad", "stressed"]):
        responses = ["Who do I need to deal with?", "Forget them.", "Just focus on me. I've got you."]
    else:
        responses = ["I'm listening.", "Go on, kitten."]
    
    send_split_messages(message.chat.id, responses)

# --- HOURLY CHECK-IN LOGIC ---
def hourly_check():
    # This runs every hour with a 30% chance to send a random text
    # Note: For this to work, you'd need to save your chat_id
    pass 

# --- STARTUP ---
if __name__ == "__main__":
    # Start the web server in a separate thread
    t = Thread(target=run_web_server)
    t.start()
    
    # Start the scheduler
    scheduler = BackgroundScheduler(timezone=PHT)
    scheduler.add_job(hourly_check, 'interval', hours=1)
    scheduler.start()

    print("Sylus is online...")
    bot.infinity_polling()
