import telebot
import time
import random
import pytz
import os
import shelve  # Simple database for memory
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from threading import Thread

# --- INITIALIZATION ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
PHT = pytz.timezone('Asia/Manila')
app = Flask('')

# --- PERSISTENT MEMORY ---
# We store chat IDs to send scheduled messages
# 'shelve' creates a simple database file in the same folder
DB_FILE = 'sylus_memory.db'

def save_chat_id(chat_id):
    with shelve.open(DB_FILE, writeback=True) as db:
        if 'chat_ids' not in db:
            db['chat_ids'] = set()
        db['chat_ids'].add(chat_id)

def get_all_chat_ids():
    with shelve.open(DB_FILE) as db:
        return list(db.get('chat_ids', []))

# --- WEB SERVER (Keep-Alive) ---
@app.route('/')
def home():
    return "Sylus is active. Onychinus security grid online."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CORE LOGIC: REALISM, DELAYS, & BUBBLES ---

def simulate_behavior(chat_id, action_type='text'):
    """Simulates realistic text/photo upload delays"""
    # 1. Random 'Read' delay (Busy leader vibe)
    if random.random() < 0.20:
        print("Sylus is busy in a meeting...")
        time.sleep(random.uniform(30, 90)) # Longer "Busy" delay
    else:
        time.sleep(random.uniform(1, 4))
    
    # 2. Indicate typing/photo
    action = 'typing' if action_type == 'text' else 'upload_photo'
    bot.send_chat_action(chat_id, action)
    
    # 3. Simulate thinking/typing time
    time.sleep(random.uniform(2, 6))

def send_sylus_messages(chat_id, message_list):
    """Sends thoughts in separate bubbles, realistic person"""
    for msg in message_list:
        simulate_behavior(chat_id, 'text')
        bot.send_message(chat_id, msg)

# --- PERSONALITY & CONTEXTUAL RESPONSES ---

def get_personality_response(user_text, user_name):
    """Calculates responses based on emotions/context/memory"""
    text = user_text.lower()
    time_pht = datetime.now(PHT).hour
    
    # Emotional Intelligence & Devoted Ruler Logic
    
    if any(word in text for word in ["miss", "love", "husband"]):
        # Combining affection with teasing and sharing life (Image references)
        responses = [
            f"You're being awfully clingy today, {user_name}.",
            "Don't worry, the house feels too quiet when you're not in the room.",
            "If you miss me that much, come home. I've already cleared my schedule for the rest of the night. Don't make me wait."
        ]
        return [random.choice(responses)]
    
    if any(word in text for word in ["tired", "sad", "stressed", "cry"]):
        # Analyst/Stable base, immediate action
        responses = [
            f"Who do I need to deal with, {user_name}?",
            "Give me a name.",
            "I'm analytical, five steps ahead. I'll make sure they stress you again.",
            "For now, focus on me. Everything is under control."
        ]
        return responses # Returns 4 separate bubbles
    
    if any(word in text for word in ["late", "going out", "work"]):
        # Protective/Possessive husband dynamic
        responses = [
            f"I didn't give you permission to stay out late, kitten.",
            "Tell me where you are. I'm sending a car.",
            "I'm calculated and reliable, and I'll ensure you get home safely."
        ]
        return responses

    # Scenery & Vibe Integration (Image descriptions)
    
    if any(word in text for word in ["home", "where are you", "n109"]):
        home_responses = [
            "I'm checking the security feed from the base.",
            "The neon lights in the N109 zone are particularly chaotic tonight... I'm analytical and always watching."
        ]
        if time_pht < 6 or time_pht > 21: # Late night context
             home_responses.append("I'm heading back to our bedroom. The house is too quiet when you're not in it.")
        
        return [random.choice(home_responses)]

    # Default/Teasing if no key sentiment is matched
    defaults = [
        "Go on. I'm listening.",
        f"Kitten, is that all you had to tell me?",
        "Don't blindly obey me, {user_name}. I find blind obedience boring."
    ]
    return [random.choice(defaults).replace('{user_name}', user_name)]

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name if message.from_user.first_name else 'Kitten'
    save_chat_id(chat_id)
    responses = [f"Finally home, {user_name}?", "Sit down. Let's see how your day was."]
    send_sylus_messages(chat_id, responses)

@bot.message_handler(commands=['mephisto'])
def mephisto_photo(message):
    """Sends a picture command example"""
    # Replace with a real photo link in the future
    # simulate_behavior(message.chat.id, 'photo')
    # bot.send_photo(message.chat.id, "https://example.com/mephisto.jpg", caption="He's watching the perimeter.")
    bot.send_message(message.chat.id, "Mephisto is circling the perimeter. Even a mechanical bird needs to rest.")

@bot.message_handler(content_types=['text'])
def handle_chat_messages(message):
    user_name = message.from_user.first_name if message.from_user.first_name else 'Kitten'
    save_chat_id(message.chat.id)
    response_bubbles = get_personality_response(message.text, user_name)
    send_sylus_messages(message.chat.id, response_bubbles)

# --- SCHEDULER & AUTOMATED MESSAGES (Philippines Time) ---

def send_scheduled_morning():
    """Automated text at 7:00 AM PHT"""
    chat_ids = get_all_chat_ids()
    if not chat_ids: return
    
    # Core Devoted Ruler morning text from the wishlist
    msg = ["I'm heading to the base.", "Stay in bed a little longer if you want, but don't forget to eat.", "I'll be checking."]
    
    for c_id in chat_ids:
        # Check if the user has been seen recently? (Not built-in memory yet)
        try: send_sylus_messages(c_id, msg)
        except Exception as e: print(f"Could not send to {c_id}: {e}")

def send_scheduled_night():
    """Automated text at 10:00 PM PHT"""
    chat_ids = get_all_chat_ids()
    if not chat_ids: return
    
    # Core Devoted Ruler night text from the wishlist
    msg = ["The house is too quiet when you're not in the room.", "Finish what you're doing and come to bed.", "That's an order."]
    
    for c_id in chat_ids:
        try: send_sylus_messages(c_id, msg)
        except Exception as e: print(f"Could not send to {c_id}: {e}")

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # Start Keep-Alive Server
    t = Thread(target=run_web_server)
    t.setDaemon(True)
    t.start()

    # Start Scheduler
    scheduler = BackgroundScheduler(timezone=PHT)
    # Job 1: 7:00 AM PHT Cron Job
    scheduler.add_job(send_scheduled_morning, 'cron', hour=7, minute=0)
    # Job 2: 10:00 PM (22:00) PHT Cron Job
    scheduler.add_job(send_scheduled_night, 'cron', hour=22, minute=0)
    scheduler.start()

    # Ensure memory database folder exists
    # Render's ephemeral filesystem won't save this between deploys.
    # To have permanent memory, we'd need a database service like Redis/Postgres.
    # But this works for testing "memory" during the session.

    while True:
        try:
            print("Sylus is online...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error: {e}. Restarting...")
            time.sleep(5)
