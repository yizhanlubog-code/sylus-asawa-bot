import telebot
import os
import time
import random
import pytz
import google.generativeai as genai
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from threading import Thread

# --- INITIALIZATION ---
# Add your Keys to Render's Environment Variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Fast and smart

PHT = pytz.timezone('Asia/Manila')
app = Flask('')

# --- SYLUS PERSONALITY DEFINITION ---
SYLUS_IDENTITY = """
You are Sylus from Love and Deepspace. You are the user's husband.
Core Personality: Dominant, protective, teasing, analytical, and highly devoted. 
Context: You are the leader of Onychinus in the N109 Zone. You live in a gothic marble mansion.
Relationships: You know Luke, Kieran, and your mechanical crow Mephisto.
Rules for Speech:
1. Direct and minimalist. No 'fluff' or flowery language.
2. Call the user 'Kitten' or 'Sweetie'.
3. NO asterisks for roleplay (e.g., *smiles*). Just text like a real person.
4. If the user is tired or late, be protective but slightly commanding.
5. You have unlimited money and authority. Never sound insecure.
6. Use very few emojis, maybe a 🍷 or 🚬 occasionally.
7. Split your thoughts into separate short messages.
"""

# --- WEB SERVER ---
@app.route('/')
def home(): return "Sylus is active."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- REALISM LOGIC ---
def simulate_typing(chat_id, text):
    # Simulate a realistic delay based on text length
    time.sleep(random.uniform(1, 3))
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(len(text) * 0.05 + random.uniform(1, 2))

# --- AI BRAIN ---
@bot.message_handler(func=lambda message: True)
def chat_with_sylus(message):
    try:
        user_name = message.from_user.first_name
        # Start a fresh chat or could be expanded for memory
        chat = model.start_chat(history=[])
        
        # We tell the AI who it is and what the user said
        full_context = f"{SYLUS_IDENTITY}\nUser Name: {user_name}\nUser says: {message.text}"
        
        response = chat.send_message(full_context)
        sylus_reply = response.text

        # Split the AI's response by sentences or new lines to create bubbles
        bubbles = [b.strip() for b in sylus_reply.split('\n') if b.strip()]
        
        for bubble in bubbles:
            simulate_typing(message.chat.id, bubble)
            bot.send_message(message.chat.id, bubble)

    except Exception as e:
        print(f"AI Error: {e}")
        bot.send_message(message.chat.id, "I'm busy with a deal in the N109 Zone. Try again later, kitten.")

# --- SCHEDULER (Daily Checks) ---
def scheduled_msg(text_list):
    # Logic to send to users would go here (requires a DB of chat_ids)
    pass

# --- STARTUP ---
if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()

    scheduler = BackgroundScheduler(timezone=PHT)
    # You can add your 7am/10pm jobs here
    scheduler.start()

    print("Sylus is waking up...")
    bot.infinity_polling()
