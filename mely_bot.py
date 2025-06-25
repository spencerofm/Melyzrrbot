import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
TOKEN = "7714076813:AAFrzgdzZDXD2KKfD5_rpOF-ltK4Hy2HmTg"
ADMIN_ID = 5845745503

# Logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Instagram URLs
INSTAGRAM_URLS = {
    'insta1': 'https://instagram.com/melykxr',
    'insta2': 'https://instagram.com/melyzrr02',
    'insta3': 'https://instagram.com/_melybbz',
    'insta4': 'https://instagram.com/melypzr',
    'insta5': 'https://instagram.com/melykdz'
}

# Gestionnaire d'utilisateurs
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

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = []
    for i in range(5):
        keyboard.append([InlineKeyboardButton(f"ð¸ Insta {i+1}", callback_data=f'instagram_{i+1}')])
    keyboard.append([InlineKeyboardButton("â Jâai follow les 5 comptes", callback_data='confirm_follow')])
    keyboard.append([InlineKeyboardButton("â Se dÃ©sabonner", callback_data='unsubscribe')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = f"Hey bebe ð Clique sur un de mes nouveaux Insta ð¥ð"

    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/refs/heads/main/IMG_5618.jpeg"

    try:
        await update.message.reply_photo(
            photo=photo_url,
            caption=welcome_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Boutons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data

    if data.startswith("instagram_"):
        index = data.split("_")[1]
        url = INSTAGRAM_URLS.get(f"insta{index}")
        if url:
            keyboard = [[InlineKeyboardButton("ð Ouvrir Instagram", url=url)],
                        [InlineKeyboardButton("â¬ï¸ Retour", callback_data='back_to_menu')]]
            await query.edit_message_caption(
                caption=f"Voici le lien vers mon Insta {index} : {instagram_url}"
{url}",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif data == "confirm_follow":
        await query.edit_message_caption(
            caption="Super je vais aller vÃ©rifier Ã§a et si tâes bien abonnÃ© aux 5 comptes je tâenvoie ta surprise ðð"
        )

    elif data == "unsubscribe":
        bot_manager.deactivate_user(user.id)
        await query.edit_message_caption(caption="ð¢ Tu as Ã©tÃ© dÃ©sabonnÃ©. Pour revenir, tape /start â¤ï¸")

    elif data == "back_to_menu":
        keyboard = []
        for i in range(5):
            keyboard.append([InlineKeyboardButton(f"ð¸ Insta {i+1}", callback_data=f'instagram_{i+1}')])
        keyboard.append([InlineKeyboardButton("â Jâai follow les 5 comptes", callback_data='confirm_follow')])
        keyboard.append([InlineKeyboardButton("â Se dÃ©sabonner", callback_data='unsubscribe')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="Hey bebe ð Clique sur un de mes nouveaux Insta ð¥ð",
            reply_markup=reply_markup
        )

# /stats
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total, active = bot_manager.get_stats()
    text = f"ð Stats
Total: {total}
Actifs: {active}
Inactifs: {total - active}"
    await update.message.reply_text(text)

# /broadcast
async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Utilisation : /broadcast votre message ici")
        return
    message = " ".join(context.args)
    sent = 0
    for user_id in bot_manager.get_active_users():
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            continue
    await update.message.reply_text(f"â Message envoyÃ© Ã  {sent} utilisateurs.")

# DÃ©marrage
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.run_polling()

if __name__ == "__main__":
    main()
