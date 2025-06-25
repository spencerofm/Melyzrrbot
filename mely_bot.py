import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
TOKEN = "7714076813:AAFrzgdzZDXD2KKfD5_rpOF-ltK4Hy2HmTg"
ADMIN_ID = 5845745503

# Logs
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Données utilisateurs
class BotManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, username=None, first_name=None):
        self.users[str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "joined_date": datetime.now().isoformat(),
            "active": True
        }

    def deactivate_user(self, user_id):
        if str(user_id) in self.users:
            self.users[str(user_id)]["active"] = False

    def get_active_users(self):
        return [user_id for user_id, data in self.users.items() if data.get("active", True)]

    def get_stats(self):
        total = len(self.users)
        active = len(self.get_active_users())
        return total, active

bot_manager = BotManager()

# Liste des comptes Instagram
INSTAGRAM_URLS = {
    "insta1": "https://instagram.com/melykxr",
    "insta2": "https://instagram.com/melyzrr02",
    "insta3": "https://instagram.com/_melybbz",
    "insta4": "https://instagram.com/melypzr",
    "insta5": "https://instagram.com/melykdz"
}

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = []

    for i in range(5):
        keyboard.append([
            InlineKeyboardButton(f"📸 Insta {i+1}", url=INSTAGRAM_URLS[f"insta{i+1}"])
        ])

    keyboard.append([InlineKeyboardButton("✅ J’ai follow les 5 comptes", callback_data="check_follow")])
    keyboard.append([InlineKeyboardButton("❌ Se désabonner", callback_data="unsubscribe")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = "Hey bebe 😘 Clique sur un de mes nouveaux Insta 🔥 👇"

    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/IMG_5618.jpeg"

    try:
        await update.message.reply_photo(
            photo=photo_url,
            caption=welcome_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Gestion des boutons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "check_follow":
        message = "Super je vais aller vérifier ça et si t’es bien abonné aux 5 comptes je t’envoie ta surprise 🎁😘"
        await query.edit_message_caption(caption=message)

    elif query.data == "unsubscribe":
        bot_manager.deactivate_user(user.id)
        message = "😢 Vous avez été désabonné des notifications.

Pour vous réabonner, tapez /start

Merci ! ❤️"
        await query.edit_message_caption(caption=message)

# Commande /stats (admin)
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Commande admin uniquement.")
        return

    total, active = bot_manager.get_stats()
    stats_text = f"""
📊 STATISTIQUES DU BOT

👥 Total utilisateurs : {total}
✅ Utilisateurs actifs : {active}
❌ Désabonnés : {total - active}

📅 Mis à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
"""
    await update.message.reply_text(stats_text)

# Commande /broadcast (admin)
async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Commande admin uniquement.")
        return

    if not context.args:
        await update.message.reply_text("Utilisation : /broadcast [votre message]")
        return

    message = ' '.join(context.args)
    active_users = bot_manager.get_active_users()

    sent = 0
    failed = 0

    await update.message.reply_text(f"📤 Envoi en cours à {len(active_users)} utilisateurs...")

    for user_id in active_users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            failed += 1
            logger.error(f"Erreur envoi à {user_id}: {e}")

    await update.message.reply_text(f"✅ Envoyé : {sent}
❌ Échecs : {failed}")

# Fonction principale
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("broadcast", admin_broadcast))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("🤖 Bot démarré !")
    application.run_polling()

if __name__ == "__main__":
    main()
