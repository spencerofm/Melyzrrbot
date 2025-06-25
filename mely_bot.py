import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ====== CONFIG ======
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503  # ton ID perso admin

# ====== LOGGING ======
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== LIENS INSTA ======
INSTAGRAM_URLS = {
    'insta1': 'https://instagram.com/melyxrr',
    'insta2': 'https://instagram.com/melyzrr',
    'insta3': 'https://instagram.com/_melyzr',
    'insta4': 'https://instagram.com/melypartage',
    'insta5': 'https://instagram.com/melyko',
}

# ====== MESSAGES ======
MESSAGES = {
    'welcome': (
        "🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?\n\n"
        "J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, "
        "je t’envoie une surprise interdite aux mineurs 😈\n\n"
        "👇 T’as juste à cliquer sur les boutons pour t’abonner. "
        "Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋"
    ),
    'done': "🔥 Bien joué 😏 ! La surprise arrive très vite…"
}

# ====== GESTION USERS ======
class BotManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, username):
        self.users[user_id] = {
            "username": username,
            "joined": datetime.now(),
            "active": True
        }

    def get_active_users(self):
        return [u for u in self.users.values() if u["active"]]

bot_manager = BotManager()

# ====== HANDLER START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or "inconnu"

    bot_manager.add_user(user_id, username)

    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url=INSTAGRAM_URLS['insta1'])],
        [InlineKeyboardButton("📸 Insta 2", url=INSTAGRAM_URLS['insta2'])],
        [InlineKeyboardButton("📸 Insta 3", url=INSTAGRAM_URLS['insta3'])],
        [InlineKeyboardButton("📸 Insta 4", url=INSTAGRAM_URLS['insta4'])],
        [InlineKeyboardButton("📸 Insta 5", url=INSTAGRAM_URLS['insta5'])],
        [InlineKeyboardButton("✅ C’est fait, envoie la surprise 🔥", callback_data="done")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = MESSAGES['welcome']
    photo_url = "https://i.imgur.com/R2aqZ08.jpeg"  # Image de Mely en rouge

    try:
        await update.message.reply_photo(
            photo=photo_url,
            caption=welcome_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# ====== CALLBACK BUTTON ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "done":
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(MESSAGES['done'])

# ====== STATS ADMIN ======
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total = len(bot_manager.users)
    active = len(bot_manager.get_active_users())
    stats = f"📊 Utilisateurs : {total}\n✅ Actifs : {active}"
    await update.message.reply_text(stats)

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", admin_stats))

    print("✅ Bot lancé")
    app.run_polling()

if __name__ == "__main__":
    main()
