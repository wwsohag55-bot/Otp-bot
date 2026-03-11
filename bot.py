import logging
import json
import os
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

# কনফিগারেশন
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8799150227:AAEM7HLL9m_fzONkhLYYEdVHAl2jUh4PPzU")
ADMIN_IDS = [int(id) for id in os.environ.get("ADMIN_IDS", "5653849290").split(",") if id]

# Flask অ্যাপ
app = Flask(__name__)

@app.route('/')
def home():
    return "OTP Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# লগিং
logging.basicConfig(level=logging.INFO)

def load_data():
    if os.path.exists('bot_data.json'):
        with open('bot_data.json', 'r') as f:
            return json.load(f)
    return {"admins": ADMIN_IDS, "members": [], "numbers": []}

def save_data(data):
    with open('bot_data.json', 'w') as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_data()
    
    if user_id in data["admins"]:
        role = "এডমিন"
        msg = "আপনি এডমিন হিসেবে লগইন করেছেন"
    elif user_id in data["members"]:
        role = "মেম্বার"
        msg = "আপনি মেম্বার হিসেবে লগইন করেছেন"
    else:
        role = "অজানা"
        msg = "আপনি রেজিস্টার্ড নন। /join দিন"
    
    await update.message.reply_text(f"স্বাগতম! আপনার রোল: {role}\n{msg}")

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("বট চালু হচ্ছে...")
    await application.run_polling()

if __name__ == "__main__":
    # Flask থ্রেড চালু
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # বট চালু
    import asyncio
    asyncio.run(main())
