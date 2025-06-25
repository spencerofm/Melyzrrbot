import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import json
import os

TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503
PHOTO_FILE_ID = "AgACAgQAAxkBAAIBXWZl4Az6Wj5F_JJ0Jz-HFJHLkQeDAAIszTEb4NRJVFzTKo5IXdQYAQADAgADbQADNAQ"  # à récupérer avec /get_file_id

# Activation des logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Base de données (JSON local)
DB_FILE = "users.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

# Boutons Instagram
keyboard = [
    [InlineKeyboardButton("📸 Insta 1", url="https://instagram.com/1")],
    [InlineKeyboardButton("📸 Insta 2", url="https://instagram.com/2")],
    [InlineKeyboardButton("📸 Insta 3", url="https://instagram.com/3")],
    [InlineKeyboardButton("📸 Insta 4", url="https://instagram.com/4")],
    [InlineKeyboardButton("📸 Insta 5", url="https://instagram.com/5")],
    [InlineKeyboardButton("✅ C'est fait, envoie la surprise 🔥", callback_data="surprise")]
]

reply_markup = InlineKeyboardMarkup(keyboard)

# Messages personnalisables
MESSAGES = {
    "welcome": """🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?

J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 😈

👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋""",
    "surprise": "🔞 Voici ta surprise : https://t.me/MelySurprise 🔥",
    "help_admin": "/stats – Voir le nombre d’utilisateurs
/broadcast [message] – Envoyer à tous les utilisateurs"
}

# Charger les utilisateurs
def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(DB_FILE, "w") as f:
            json.dump(users, f)

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    try:
        await update.message.reply_photo(
            photo=PHOTO_FILE_ID,
            caption=MESSAGES["welcome"],
            reply_markup=reply_markup,
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo : {e}")
        await update.message.reply_text(MESSAGES["welcome"], reply_markup=reply_markup)

# Handler du bouton "surprise"
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "surprise":
        await query.edit_message_text(MESSAGES["surprise"])

# Commande /stats (admin uniquement)
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    users = load_users()
    total = len(users)
    active = sum(1 for u in users if await context.bot.get_chat_member(u, u))
    await update.message.reply_text(f"👥 Total : {total} utilisateurs
✅ Actifs : {active}")

# Commande /broadcast [message]
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    message = " ".join(context.args)
    users = load_users()
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception:
            continue
    await update.message.reply_text("📨 Message envoyé.")

# Commande /help_admin
async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(MESSAGES["help_admin"])

# Lancer le bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("help_admin", help_admin))
    app.run_polling()
