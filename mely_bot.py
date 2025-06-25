import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token et admin ID
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503

# Configuration des logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# URLs Instagram
INSTAGRAM_URLS = {
    "insta1": "https://instagram.com/melykxr",
    "insta2": "https://instagram.com/melyzrr02",
    "insta3": "https://instagram.com/_melybbz",
    "insta4": "https://instagram.com/melypzr",
    "insta5": "https://instagram.com/melykdz",
}

# Message principal
WELCOME_MESSAGE = """🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?

J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 🔞

👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋"""

# Gestion utilisateurs
class BotManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, username=None, first_name=None):
        self.users[str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "joined_date": datetime.now().isoformat(),
            "active": True,
        }

    def get_active_users(self):
        return [user_id for user_id, data in self.users.items() if data.get("active", True)]

    def get_stats(self):
        total = len(self.users)
        active = len(self.get_active_users())
        return total, active

bot_manager = BotManager()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url=INSTAGRAM_URLS["insta1"])],
        [InlineKeyboardButton("📸 Insta 2", url=INSTAGRAM_URLS["insta2"])],
        [InlineKeyboardButton("📸 Insta 3", url=INSTAGRAM_URLS["insta3"])],
        [InlineKeyboardButton("📸 Insta 4", url=INSTAGRAM_URLS["insta4"])],
        [InlineKeyboardButton("📸 Insta 5", url=INSTAGRAM_URLS["insta5"])],
        [InlineKeyboardButton("✅ J’ai follow les 5 comptes", callback_data="check_follow")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/refs/heads/main/IMG_5618.jpeg"

    try:
        await update.message.reply_photo(photo=photo_url, caption=WELCOME_MESSAGE, reply_markup=reply_markup)
    except:
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

# Handler pour les boutons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "check_follow":
        text = "Super je vais aller vérifier ça et si t’es bien abonné aux 5 comptes je t’envoie ta surprise 🎁😘"
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="back_to_menu")]]
        await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("📸 Insta 1", url=INSTAGRAM_URLS["insta1"])],
            [InlineKeyboardButton("📸 Insta 2", url=INSTAGRAM_URLS["insta2"])],
            [InlineKeyboardButton("📸 Insta 3", url=INSTAGRAM_URLS["insta3"])],
            [InlineKeyboardButton("📸 Insta 4", url=INSTAGRAM_URLS["insta4"])],
            [InlineKeyboardButton("📸 Insta 5", url=INSTAGRAM_URLS["insta5"])],
            [InlineKeyboardButton("✅ J’ai follow les 5 comptes", callback_data="check_follow")]
        ]
        await query.edit_message_caption(caption=WELCOME_MESSAGE, reply_markup=InlineKeyboardMarkup(keyboard))

# /stats
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Commande réservée à l’admin.")
    total, active = bot_manager.get_stats()
    text = f"""📊 Total utilisateurs : {total}
✅ Actifs : {active}"""
    await update.message.reply_text(text)

# /broadcast
async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Commande réservée à l’admin.")
    if not context.args:
        return await update.message.reply_text("Utilisation : /broadcast votre message")

    message = " ".join(context.args)
    users = bot_manager.get_active_users()
    sent = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Erreur broadcast vers {user_id}: {e}")

    await update.message.reply_text(f"✅ Message envoyé à {sent} utilisateurs")

# === /broadcast_image COMMAND ===
async def broadcast_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("❌ Tu dois répondre à une photo avec cette commande.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("❌ Tu dois écrire un texte après la commande.")
        return

    caption = ' '.join(context.args)
    photo = update.message.reply_to_message.photo[-1].file_id

    success = 0
    for user_id in user_ids:
        try:
            await context.bot.send_photo(chat_id=user_id, photo=photo, caption=caption)
            success += 1
        except Exception as e:
            print(f"Erreur avec l'utilisateur {user_id}: {e}")
            pass

    await update.message.reply_text(f"✅ Message envoyé à {success} abonnés.")

# N'oublie pas d'enregistrer le handler :
app.add_handler(CommandHandler("broadcast_image", broadcast_image))

# main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    logger.info("Bot lancé.")
    app.run_polling()

if __name__ == "__main__":
    main()
