import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# === CONFIGURATION ===
BOT_TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 21486  # remplace par ton vrai user_id Telegram si besoin

user_data = {}

# === LOGS ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === HANDLER /START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"active": True}

    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url="https://www.instagram.com/")],
        [InlineKeyboardButton("📸 Insta 2", url="https://www.instagram.com/")],
        [InlineKeyboardButton("📸 Insta 3", url="https://www.instagram.com/")],
        [InlineKeyboardButton("📸 Insta 4", url="https://www.instagram.com/")],
        [InlineKeyboardButton("📸 Insta 5", url="https://www.instagram.com/")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey bebe 😘 Clique sur un de mes nouveaux Insta 🔥👇",
        reply_markup=reply_markup,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ C’est fait, envoie la surprise 🔥"
    )

# === HANDLER /STATS ===
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total = len(user_data)
    active = sum(1 for u in user_data.values() if u["active"])
    await update.message.reply_text(f"📊 Utilisateurs : {total}\n✅ Actifs : {active}")

# === HANDLER /GET_FILE_ID ===
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérifie que le message est une réponse
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        file_id = update.message.reply_to_message.photo[-1].file_id
        await update.message.reply_text(f"🆔 file_id :\n`{file_id}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Aucune image détectée. Réponds à ce message avec une photo.")

# === ERREUR GENERALE ===
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# === MAIN ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("get_file_id", get_file_id))

    app.add_error_handler(error_handler)

    print("Bot démarré ✅")
    app.run_polling()
