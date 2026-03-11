import logging
import json
import os
import asyncio
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# কনফিগারেশন
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8799150227:AAEM7HLL9m_fzONkhLYYEdVHAl2jUh4PPzU")
ADMIN_IDS = [int(id) for id in os.environ.get("ADMIN_IDS", "5653849290").split(",") if id]

# Flask অ্যাপ (Render-এর জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    return "OTP Bot is running! Polling aktif..."

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# লগিং
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ডাটা লোড/সেভ
def load_data():
    if os.path.exists('bot_data.json'):
        with open('bot_data.json', 'r') as f:
            return json.load(f)
    return {"admins": ADMIN_IDS, "members": [], "numbers": []}

def save_data(data):
    with open('bot_data.json', 'w') as f:
        json.dump(data, f)

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    data = load_data()
    
    logger.info(f"Start command from user {user_id}")
    
    if user_id in data["admins"]:
        role = "এডমিন 👑"
        msg = "আপনি এডমিন হিসেবে লগইন করেছেন"
    elif user_id in data["members"]:
        role = "মেম্বার 👤"
        msg = "আপনি মেম্বার হিসেবে লগইন করেছেন"
    else:
        role = "অজানা"
        msg = "আপনি রেজিস্টার্ড নন। /join দিন"
    
    await update.message.reply_text(
        f"👋 স্বাগতম {user.first_name}!\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📌 আপনার রোল: {role}\n"
        f"🆔 আইডি: {user_id}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"{msg}"
    )

async def main():
    """বট চালু করার মূল ফাংশন"""
    logger.info("বট চালু হচ্ছে...")
    
    # বট অ্যাপ তৈরি
    application = Application.builder().token(BOT_TOKEN).build()
    
    # হ্যান্ডলার যোগ করুন
    application.add_handler(CommandHandler("start", start))
    
    logger.info("পোলিং শুরু হচ্ছে...")
    
    # পোলিং চালু করুন
    await application.run_polling()

if __name__ == "__main__":
    # Flask থ্রেড চালু
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask সার্ভার চালু হয়েছে")
    
    # বট চালু
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error: {e}")
