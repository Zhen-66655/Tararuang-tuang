from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, CallbackQueryHandler
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

# Logging (untuk debug di Render log)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8252579113:AAF_9zQEFe_W9lSH2KjHdFL4zu1MQK4xYY0"
GROUP_CHAT_ID = -1002599585664  # Ganti dengan ID grup kamu

# Daftar username
USERS = [
    "@Zhen_8886", "@iamrendyy", "@Lcifer966", "@D黛安",
    "@毗湿奴", "@Rafi_Al", "@拉騰", "@Deva", "@samasamterserah", "@Gatot_whose_hair_is_tied_up"
]

# Fungsi kirim pesan
async def send_meal_reminder(context: ContextTypes.DEFAULT_TYPE, waktu: str):
    mention_text = ' '.join(USERS)
    pesan = f"⏰ *Waktu makan {waktu} telah tiba!*\n{mention_text}"
    tombol = InlineKeyboardMarkup([[InlineKeyboardButton("OK ✅", callback_data="ok")]])
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=pesan, reply_markup=tombol, parse_mode="Markdown")

# Callback tombol OK
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user.username
    await query.edit_message_text(text=f"{query.message.text}\n\n✅ Sudah dilihat oleh @{user}")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Saya akan mengingatkan makan 3x sehari.")

# Fungsi utama
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_meal_reminder, 'cron', hour=1, minute=40, args=[{"bot": app.bot}, "pagi"])
    scheduler.add_job(send_meal_reminder, 'cron', hour=4, minute=30, args=[{"bot": app.bot}, "siang"])
    scheduler.add_job(send_meal_reminder, 'cron', hour=10, minute=30, args=[{"bot": app.bot}, "sore"])
    scheduler.start()

    print("Bot sedang berjalan di Render...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
