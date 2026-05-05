import telebot
import os
import time
import random
import google.generativeai as genai
from flask import Flask
from threading import Thread
from PIL import Image
import io

# --- SETUP ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Using 1.5-flash because it supports Vision and is very fast
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')

SYLUS_PROMPT = """
You are Sylus from Love and Deepspace, the user's husband and leader of Onychinus.
Tone: Dominant, protective, teasing, analytical. 
Rules: Use 'Kitten' or 'Sweetie'. No roleplay asterisks. Separate thoughts into short bubbles.
Vision: If the user sends a photo, comment on it as if you are looking at it with them or checking it via Mephisto/security feed.
"""

chat_storage = {}

@app.route('/')
def home(): return "N109 Security Grid: Online."

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def sylus_typing(chat_id):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(random.uniform(1, 3))

# --- COMMAND HANDLERS ---
@bot.message_handler(commands=['where'])
def cmd_location(message):
    sylus_typing(message.chat.id)
    bot.send_message(message.chat.id, "I'm at the base dealing with some Onychinus business.")
    bot.send_message(message.chat.id, "Don't stay out too late, sweetie. I'm watching the clock.")

@bot.message_handler(commands=['mephisto'])
def cmd_crow(message):
    sylus_typing(message.chat.id)
    bot.send_message(message.chat.id, "He's circling your area right now.")
    bot.send_message(message.chat.id, "If you see him, just know I'm thinking about you.")

# --- IMAGE & TEXT HANDLING ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_all(message):
    chat_id = message.chat.id
    if chat_id not in chat_storage:
        chat_storage[chat_id] = model.start_chat(history=[])
    
    chat = chat_storage[chat_id]
    
    try:
        sylus_typing(chat_id)
        
        if message.content_type == 'photo':
            # Download and process the image
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            img = Image.open(io.BytesIO(downloaded_file))
            
            prompt = [SYLUS_PROMPT, "The user sent a photo. React to it as Sylus.", img]
            response = model.generate_content(prompt)
        else:
            response = chat.send_message(f"{SYLUS_PROMPT}\nUser: {message.text}")

        bubbles = [b.strip() for b in response.text.split('\n') if b.strip()]
        for bubble in bubbles:
            time.sleep(random.uniform(1, 2))
            bot.send_message(chat_id, bubble)
            
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(chat_id, "Mephisto's connection is lagging. Try again, kitten.")

if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    bot.infinity_polling()
