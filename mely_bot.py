
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "7714076813:AAFrzgdzZDXD2KKfD5_rpOF-ltK4Hy2HmTg"
ADMIN_ID = 5845745503  # à modifier si besoin

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

INSTAGRAM_URLS = {
    'insta1': 'https://instagram.com/melykxr',
    'insta2': 'https://instagram.com/melyzrr02',
    'insta3': 'https://instagram.com/_melybbz',
    'insta4': 'https://instagram.com/melypzr',
    'insta5': 'https://instagram.com/melykdz'
}

MESSAGES = {
    'welcome': """🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?

J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 🔞

👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋""",
    'button_labels': [
        "📸 Insta 1",
        "📸 Insta 2",
        "📸 Insta 3",
        "📸 Insta 4",
        "📸 Insta 5",
        "✅ C’est fait, envoie la surprise 🔥"
    ]
}

class BotManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, username=None, first_name=None):
        self.users[str(user_id)] = {
            'username': username,
            'first_name': first_name,
            'joined_date': datetime.now().isoformat(),
            'active': True
        }

    def deactivate_user(self, user_id):
        if str(user_id) in self.users:
            self.users[str(user_id)]['active'] = False

    def get_active_users(self):
        return [user_id for user_id, data in self.users.items() if data.get('active', True)]

bot_manager = BotManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = []

    for i in range(5):
        button_text = MESSAGES['button_labels'][i]
        url = INSTAGRAM_URLS[f"insta{i+1}"]
        keyboard.append([InlineKeyboardButton(button_text, url=url)])

    keyboard.append([InlineKeyboardButton(MESSAGES['button_labels'][5], callback_data='done')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = MESSAGES['welcome']

    photo_url = "https://i.imgur.com/bVc9FTj.jpeg"

    try:
        await update.message.reply_photo(
            photo=photo_url,
            caption=welcome_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "done":
        await query.edit_message_reply_markup(reply_markup=None)

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total = len(bot_manager.users)
    active = len(bot_manager.get_active_users())
    stats = f"👥 Utilisateurs : {total} (actifs : {active})"
    await update.message.reply_text(stats)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", admin_stats))
    print("✅ Bot lancé")
    app.run_polling()

if __name__ == "__main__":
    main()
