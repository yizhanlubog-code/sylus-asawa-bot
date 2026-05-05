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
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
PHT = pytz.timezone('Asia/Manila')
app = Flask('')

# --- SYLUS DATA ASSETS ---
MEPHISTO_PICS = [
    "https://example.com/mephisto1.jpg", # Replace with real links
    "https://example.com/mephisto2.jpg"
]

# --- WEB SERVER (Keep-Alive) ---
@app.route('/')
def home():
    return "Sylus is active. Monitoring N109 Zone."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CORE LOGIC: BEHAVIOR & REALISM ---

def simulate_human_behavior(chat_id, message_type='text'):
    """Simulates realistic delays and Telegram indicators"""
    # 1. Random 'Read' delay (Busy leader vibe)
    time.sleep(random.uniform(1, 4))
    
    # 2. Typing/Uploading indicator
    action = 'typing' if message_type == 'text' else 'upload_photo'
    bot.send_chat_action(chat_id, action)
    
    # 3. Simulate thinking/typing time
    time.sleep(random.uniform(2, 5))

def send_sylus_messages(chat_id, message_list):
    """Sends thoughts in separate bubbles like a real person"""
    for msg in message_list:
        simulate_human_behavior(chat_id, 'text')
        bot.send_message(chat_id, msg)

# --- PERSONALITY ENGINE ---

def get_sylus_response(user_text):
    text = user_text.lower()
    
    # Emotional Intelligence & Context
    if any(word in text for word in ["miss", "love", "husband"]):
        return ["You're being awfully clingy today, kitten.", "I'm not complaining.", "Come home and say that to my face. I'm waiting."]
    
    if any(word in text for word in ["tired", "sad", "stressed", "cry"]):
        return ["Who bothered you?", "Give me a name and I'll deal with it.", "For now, just focus on me. Everything is under control."]
    
    if any(word in text for word in ["late", "going out", "work"]):
        return ["I didn't give you permission to stay out late.", "Tell me where you are. I'm sending a car.", "Don't make me come find you myself."]

    if any(word in text for word in ["mephisto", "crow", "bird"]):
        return ["Mephisto is circling the perimeter.", "He's watching you for me. Stay safe."]

    # Default/Generic
    return [random.choice(["I'm listening, sweetie.", "Go on.", "Is that all you wanted to tell me?"])]

# --- HANDLERS ---

@bot.message_handler(commands=['start', 'status'])
def handle_commands(message):
    responses = {
        '/start': ["Finally home?", "Sit down. Let's see how your day was."],
        '/status': ["The N109 zone is quiet.", f"It's {datetime.now(PHT).strftime('%I:%M %p')} here.", "I have everything under control."]
    }
    cmd = message.text.split()[0]
    send_sylus_messages(message.chat.id, responses.get(cmd, ["I'm busy."]))

@bot.message_handler(content_types=['text'])
def handle_chat(message):
    # This ensures he doesn't feel like a 'bot'
    response_bubbles = get_sylus_response(message.text)
    send_sylus_messages(message.chat.id, response_bubbles)

# --- SCHEDULER (Hourly & Daily Checks) ---

def hourly_random_text():
    """30% chance to check in every hour"""
    # Note: In a real app, you'd store chat_ids in a database. 
    # For now, this prints to logs. 
    if random.random() < 0.30:
        print("Sylus is thinking about the user...")

def scheduled_texts():
    """Morning and Night orders"""
    # logic for 7am and 10pm PHT would go here
    pass

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # Start Keep-Alive
    t = Thread(target=run_web_server)
    t.setDaemon(True)
    t.start()

    # Start Scheduler
    scheduler = BackgroundScheduler(timezone=PHT)
    scheduler.add_job(hourly_random_text, 'interval', hours=1)
    # Add your 7am / 10pm jobs here
    scheduler.start()

    while True:
        try:
            print("Sylus is online...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Connection error: {e}. Restarting in 5 seconds...")
            time.sleep(5)
