import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# === CONFIG ===
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_IDS = [21485]  # Remplace par ton propre ID Telegram
FILE_ID_PHOTO = "INSÈRE_IÇI_TON_FILE_ID"  # A remplacer après avoir fait /get_file_id

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# === STOCKAGE UTILISATEURS ===
user_ids = set()

# === MESSAGES ===
MESSAGES = {
    "welcome": "Hey bébé 😘 Clique sur un de mes nouveaux Insta 🔥👇",
    "help_admin": "/stats - Voir le nombre d’utilisateurs\n/broadcast - Envoyer un message à tous\n/get_file_id - Récupérer le file_id d’une photo"
}

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)
    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url="https://instagram.com/")],
        [InlineKeyboardButton("📸 Insta 2", url="https://instagram.com/")],
        [InlineKeyboardButton("📸 Insta 3", url="https://instagram.com/")],
        [InlineKeyboardButton("📸 Insta 4", url="https://instagram.com/")],
        [InlineKeyboardButton("📸 Insta 5", url="https://instagram.com/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = MESSAGES["welcome"]

    try:
        await update.message.reply_photo(
            photo=FILE_ID_PHOTO,
            caption=welcome_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        total = len(user_ids)
        active = sum(1 for uid in user_ids)
        await update.message.reply_text(f"📊 Total : {total} utilisateurs\n✅ Actifs : {active}")
    else:
        await update.message.reply_text("Accès refusé.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("Accès refusé.")
    if not context.args:
        return await update.message.reply_text("Utilise : /broadcast ton_message")

    message = " ".join(context.args)
    sent = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
            sent += 1
        except:
            continue
    await update.message.reply_text(f"📨 Message envoyé à {sent} utilisateurs.")

async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["help_admin"])

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1]
        await update.message.reply_text(f"file_id : {photo.file_id}")
    else:
        await update.message.reply_text("Aucune image détectée.")

# === MAIN ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("help_admin", help_admin))
    app.add_handler(CommandHandler("get_file_id", get_file_id))
    app.add_handler(MessageHandler(filters.COMMAND, help_admin))
    app.run_polling()

if __name__ == "__main__":
    main()
