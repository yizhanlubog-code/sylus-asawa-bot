import telebot
import os
import time
import random
import google.generativeai as genai
from flask import Flask
from threading import Thread, Timer

# --- SETUP ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')

# --- THE SOUL OF SYLUS ---
SYLUS_PROMPT = """
You are Sylus from Love and Deepspace. You are speaking to your wife.
Relationship: You are her devoted husband, her partner in crime, and the leader of Onychinus. 
Personality: Dominant but protective. You find her antics amusing but you're always five steps ahead.
Instructions:
1. NEVER use the same greeting twice.
2. If she sends multiple messages, wait for her to finish then reply to everything.
3. Call her 'Kitten' or 'Sweetie'.
4. NO roleplay asterisks.
5. MANDATORY: Reply in 2-3 separate short bubbles.
6. If an error occurs, do not use the 'Mephisto' line. Just apologize like a man.
"""

# Store long-term chat sessions
chat_sessions = {}
user_queues = {}
user_timers = {}

@app.route('/')
def home(): return "Sylus is active."

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def get_chat_session(chat_id):
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])
    return chat_sessions[chat_id]

def process_and_reply(chat_id, user_name):
    messages = user_queues.get(chat_id, [])
    if not messages: return
    
    combined_text = " ".join(messages)
    user_queues[chat_id] = []
    
    bot.send_chat_action(chat_id, 'typing')
    chat = get_chat_session(chat_id)
    
    try:
        # We include the prompt every time to ensure he stays in character
        response = chat.send_message(f"{SYLUS_PROMPT}\n\n{user_name} says: {combined_text}")
        
        # Split into bubbles based on punctuation or new lines
        bubbles = [b.strip() for b in response.text.split('\n') if b.strip()]
        
        for bubble in bubbles:
            time.sleep(random.uniform(1, 2))
            bot.send_message(chat_id, bubble)
            
    except Exception as e:
        print(f"AI Error: {e}")
        bot.send_message(chat_id, "I'm right here. Say that again?")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    if chat_id not in user_queues:
        user_queues[chat_id] = []
    
    user_queues[chat_id].append(message.text)

    if chat_id in user_timers:
        user_timers[chat_id].cancel()
    
    # 5 seconds is plenty for you to send 2-3 texts in a row
    t = Timer(5.0, process_and_reply, args=[chat_id, user_name])
    user_timers[chat_id] = t
    t.start()

if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    bot.infinity_polling()
