
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"

# 🔧 Logs Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ➕ Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Envoie-moi une photo pour récupérer son file_id")

# 📸 Quand quelqu’un envoie une photo
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.photo:
        photo = update.message.photo[-1]  # On prend la meilleure qualité
        file_id = photo.file_id
        await update.message.reply_text(f"✅ file_id détecté :\n`{file_id}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Aucune image détectée. Envoie une photo directement dans le chat.")

# 🧱 Lancement du bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
