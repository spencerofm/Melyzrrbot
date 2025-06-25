import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token et ID Admin
TOKEN = "7714076813:AAFrzgdzZDXD2KKfD5_rpOF-ltK4Hy2HmTg"
ADMIN_ID = 5845745503

# Config des logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Liens Instagram
INSTAGRAM_URLS = [
    "https://instagram.com/melykxr",
    "https://instagram.com/melyzrr02",
    "https://instagram.com/_melybbz",
    "https://instagram.com/melypzr",
    "https://instagram.com/melykdz"
]

# Gestion des utilisateurs
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

    def get_active_users(self):
        return [int(uid) for uid, data in self.users.items() if data.get("active", True)]

    def get_stats(self):
        total = len(self.users)
        active = len(self.get_active_users())
        return total, active

bot_manager = BotManager()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/IMG_5618.jpeg"
    message_text = (
        "ð¨ Tâas dÃ©jÃ  vu une ASIATIQUE avec des ÃNORMES SEINS ?

"
        "Jâai dÃ» crÃ©er 5 nouveaux comptes Instaâ¦ Si tu tâabonnes aux 5, je tâenvoie une surprise interdite aux mineurs ð

"
        "ð Tâas juste Ã  cliquer sur les boutons pour tâabonner. Et clique sur le dernier une fois que câest fait pour recevoir ta surprise ð"
    )

    keyboard = [
        [InlineKeyboardButton("ð¸ Insta 1", url=INSTAGRAM_URLS[0])],
        [InlineKeyboardButton("ð¸ Insta 2", url=INSTAGRAM_URLS[1])],
        [InlineKeyboardButton("ð¸ Insta 3", url=INSTAGRAM_URLS[2])],
        [InlineKeyboardButton("ð¸ Insta 4", url=INSTAGRAM_URLS[3])],
        [InlineKeyboardButton("ð¸ Insta 5", url=INSTAGRAM_URLS[4])],
        [InlineKeyboardButton("â Jâai follow les 5 comptes", callback_data="final_action")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(photo=photo_url, caption=message_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(message_text, reply_markup=reply_markup)

# Final bouton
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "final_action":
        await query.edit_message_caption("Super je vais aller vÃ©rifier Ã§a et si tâes bien abonnÃ© aux 5 comptes je tâenvoie ta surprise ðð")

# /stats
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total, active = bot_manager.get_stats()
    await update.message.reply_text(
        f"ð Stats bot:

"
        f"ð¥ Total utilisateurs: {total}
"
        f"â Actifs: {active}
"
        f"ð MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

# /broadcast
async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Utilisation: /broadcast [votre message]")
        return

    msg = " ".join(context.args)
    users = bot_manager.get_active_users()
    sent, fail = 0, 0

    await update.message.reply_text(f"ð¤ Envoi Ã  {len(users)} utilisateurs...")

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=msg)
            sent += 1
            await asyncio.sleep(0.1)
        except:
            fail += 1

    await update.message.reply_text(f"â EnvoyÃ©s: {sent} | â Ãchecs: {fail}")

# Lancement du bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("ð¤ Bot dÃ©marrÃ©")
    app.run_polling()

if __name__ == "__main__":
    main()
