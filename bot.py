from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

TOKEN = "8252579113:AAF_9zQEFe_W9lSH2KjHdFL4zu1MQK4xYY0"
GROUP_CHAT_ID = -1002599585664  # Ganti dengan ID grup kamu

USERS = [
    "@Zhen_8886", "@iamrendyy", "@Lcifer966", "@D黛安",
    "@毗湿奴", "@Rafi_Al", "@拉騰", "@Deva", "@samasamterserah",
    "@Gatot_whose_hair_is_tied_up", "@YANZAIDAN"  # Tambahan Kakang
]

# Fungsi ketika tombol OK ditekan
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user.username
    if user:
        await query.edit_message_text(text=f"{query.message.text}\n\n✅ Sudah dilihat oleh @{user}")
    else:
        await query.edit_message_text(text=f"{query.message.text}\n\n✅ Sudah dilihat.")

# Fungsi untuk kirim pesan
async def send_meal_reminder(context: ContextTypes.DEFAULT_TYPE, waktu: str):
    mention_text = ' '.join(USERS)
    message = f"⏰ *Waktu makan {waktu} telah tiba!*\n{mention_text}"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("OK ✅", callback_data="ok")]])
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message, reply_markup=keyboard, parse_mode="Markdown")

# Fungsi /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif. Akan kirim pengingat makan setiap hari 3x.")

# Fungsi scheduler wrapper
def schedule_jobs(app):
    scheduler = BackgroundScheduler(timezone="Asia/Jakarta")
    scheduler.add_job(lambda: asyncio.create_task(send_meal_reminder(app.bot, "pagi")), trigger='cron', hour=8, minute=40)
    scheduler.add_job(lambda: asyncio.create_task(send_meal_reminder(app.bot, "siang")), trigger='cron', hour=11, minute=30)
    scheduler.add_job(lambda: asyncio.create_task(send_meal_reminder(app.bot, "sore")), trigger='cron', hour=17, minute=30)
    scheduler.start()

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    schedule_jobs(app)
    print("Bot berjalan di Render...")
    app.run_polling()
