from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = "8252579113:AAF_9zQEFe_W9lSH2KjHdFL4zu1MQK4xYY0"
GROUP_CHAT_ID = -1002599585664  # Ganti dengan ID grup kamu

# Daftar user
USERS = [
    "@Zhen_8886", "@iamrendyy", "@Lcifer966", "@D黛安",
    "@毗湿奴", "@Rafi_Al", "@拉騰", "@Deva", "@samasamterserah", "@Gatot_whose_hair_is_tied_up"
]

# Tombol OK ditekan
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user.username
    await query.edit_message_text(text=f"{query.message.text}\n\n✅ Sudah dilihat oleh @{user}")

# Fungsi kirim pesan
async def send_meal_reminder(context: ContextTypes.DEFAULT_TYPE, waktu: str):
    mention_text = ' '.join(USERS)
    pesan = f"⏰ *Waktu ambil makan {waktu} telah tiba!*\n{mention_text}"
    tombol = InlineKeyboardMarkup([[InlineKeyboardButton("OK ✅", callback_data="ok")]])
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=pesan, reply_markup=tombol, parse_mode="Markdown")

# Buat scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_meal_reminder, 'cron', hour=1, minute=40, args=["pagi"])   # 08:40 WIB
scheduler.add_job(send_meal_reminder, 'cron', hour=4, minute=30, args=["siang"])  # 11:30 WIB
scheduler.add_job(send_meal_reminder, 'cron', hour=10, minute=30, args=["sore"])  # 17:30 WIB
scheduler.start()

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Saya akan mengingatkan makan 3x sehari.")

# Jalankan bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot berjalan...")
    app.run_polling()
