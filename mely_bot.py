import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🎯 Ton token, à garder secret
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

INSTAGRAM_URLS = {
    "insta1": "https://instagram.com/melykxr",
    "insta2": "https://instagram.com/melyzrr02",
    "insta3": "https://instagram.com/_melybbz",
    "insta4": "https://instagram.com/melypzr",
    "insta5": "https://instagram.com/melykdz",
}

# 🎁 Gestion des utilisateurs
class BotManager:
    def __init__(self):
        self.users = {}
    def add_user(self, user_id):
        self.users[user_id] = True
    def get_stats(self):
        total = len(self.users)
        return total, total

bot_manager = BotManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id)

    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/IMG_5618.jpeg"
    caption = (
        "🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?\n\n"
        "J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 🔞\n\n"
        "👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋"
    )

    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url=INSTAGRAM_URLS["insta1"])],
        [InlineKeyboardButton("📸 Insta 2", url=INSTAGRAM_URLS["insta2"])],
        [InlineKeyboardButton("📸 Insta 3", url=INSTAGRAM_URLS["insta3"])],
        [InlineKeyboardButton("📸 Insta 4", url=INSTAGRAM_URLS["insta4"])],
        [InlineKeyboardButton("📸 Insta 5", url=INSTAGRAM_URLS["insta5"])],
        [InlineKeyboardButton("✅ J’ai follow les 5 comptes", callback_data="final_follow")]
    ]

    await update.message.reply_photo(photo=photo_url, caption=caption,
                                     reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "final_follow":
        msg = "Super je vais aller vérifier ça et si t’es bien abonné aux 5 comptes je t’envoie ta surprise 🎁😘"
        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="go_back")]]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "go_back":
        # Recréer le menu principal (on peut rappeler start)
        await start(update, context)

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total, active = bot_manager.get_stats()
    text = (
        f"📊 Stats bot:\n\n"
        f"👥 Total abonnés : {total}\n"
        f"✅ Actifs : {active}\n"
        f"📅 MAJ : {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    await update.message.reply_text(text)

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("📢 Utilisation : /broadcast [message]")
        return
    message = " ".join(context.args)
    total, _ = bot_manager.get_stats()
    sent = 0
    for uid in bot_manager.users:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
            sent += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(e)
    await update.message.reply_text(f"Envoi broadcast : {sent}/{total}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    logger.info("Bot démarré")
    app.run_polling()

if __name__ == "__main__":
    main()
