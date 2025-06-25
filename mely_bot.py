import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ======================== CONFIG ========================

TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503

INSTAGRAM_URLS = {
    'insta1': 'https://instagram.com/melykxr',
    'insta2': 'https://instagram.com/melyzrr02',
    'insta3': 'https://instagram.com/_melybbz',
    'insta4': 'https://instagram.com/melypzr',
    'insta5': 'https://instagram.com/melykdz'
}

PHOTO_URL = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/IMG_5618.jpeg"

# ======================== LOGGING ========================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================== BOT MANAGER ========================

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

    def get_stats(self):
        total = len(self.users)
        active = len(self.get_active_users())
        return total, active

bot_manager = BotManager()

# ======================== HANDLERS ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url=INSTAGRAM_URLS['insta1'])],
        [InlineKeyboardButton("📸 Insta 2", url=INSTAGRAM_URLS['insta2'])],
        [InlineKeyboardButton("📸 Insta 3", url=INSTAGRAM_URLS['insta3'])],
        [InlineKeyboardButton("📸 Insta 4", url=INSTAGRAM_URLS['insta4'])],
        [InlineKeyboardButton("📸 Insta 5", url=INSTAGRAM_URLS['insta5'])],
        [InlineKeyboardButton("✅ J’ai follow les 5 comptes", callback_data='final_action')]
    ]

    welcome_text = (
        "🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?\n\n"
        "J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 🔞\n\n"
        "👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋"
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(
            photo=PHOTO_URL,
            caption=welcome_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'final_action':
        await query.edit_message_caption(
            caption="Super je vais aller vérifier ça et si t’es bien abonné aux 5 comptes je t’envoie ta surprise 🎁😘"
        )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total, active = bot_manager.get_stats()
    await update.message.reply_text(
        f"📊 Stats bot :\n\n"
        f"👥 Total utilisateurs : {total}\n"
        f"✅ Actifs : {active}\n"
        f"🕒 MAJ : {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "📢 Utilisation : /broadcast Votre message ici"
        )
        return

    message = ' '.join(context.args)
    active_users = bot_manager.get_active_users()

    sent = 0
    failed = 0

    await update.message.reply_text(f"⏳ Envoi en cours à {len(active_users)} utilisateurs...")

    for user_id in active_users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Erreur envoi à {user_id}: {e}")
            failed += 1

    await update.message.reply_text(
        f"✅ Envoi terminé\n"
        f"📤 Succès : {sent}\n"
        f"❌ Échecs : {failed}"
    )

# ======================== MAIN ========================

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("broadcast", admin_broadcast))

    logger.info("🚀 Bot lancé")
    application.run_polling()

if __name__ == "__main__":
    main()
