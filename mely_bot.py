import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

# TOKEN (déjà corrigé précédemment dans ta version)
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503

# Configuration logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Stockage local des users
class BotManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, username):
        self.users[user_id] = {
            "username": username,
            "active": True,
            "last_active": datetime.now()
        }

    def get_stats(self):
        total = len(self.users)
        active = sum(1 for u in self.users.values() if u["active"])
        return total, active

    def get_active_users(self):
        return [uid for uid, data in self.users.items() if data["active"]]

bot_manager = BotManager()

# Boutons d’accueil
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📸 Insta 1", url="https://instagram.com/melyxkr")],
        [InlineKeyboardButton("📸 Insta 2", url="https://instagram.com/melyxrz")],
        [InlineKeyboardButton("📸 Insta 3", url="https://instagram.com/melyxrf")],
        [InlineKeyboardButton("📸 Insta 4", url="https://instagram.com/melyxra")],
        [InlineKeyboardButton("📸 Insta 5", url="https://instagram.com/melyxrp")],
        [InlineKeyboardButton("✅ J’ai follow les 5 comptes", callback_data="check_follow")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Message principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username)

    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/mely_start.jpg"
    caption = (
        "🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?"

        "J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 🔞"

        "👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋"
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=get_main_keyboard()
    )

# Action après clique sur “J’ai follow les 5 comptes”
async def check_follow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    image_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/mely_start.jpg"
    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=image_url,
        caption="Super je vais aller vérifier ça et si t’es bien abonné aux 5 comptes je t’envoie ta surprise 🎁😘",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="back")]])
    )

# Retour à l’accueil
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# /stats pour admin
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    total, active = bot_manager.get_stats()
    await update.message.reply_text(
        f"""📊 Stats bot:

"
        f"👥 Total utilisateurs: {total}
"
        f"✅ Actifs: {active}
"
        f"📅 MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')}"""
    )

# /broadcast pour envoyer un message groupé
async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    message = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ", 1)) > 1 else None
    if not message:
        await update.message.reply_text("Utilise: /broadcast ton_message")
        return

    for user_id in bot_manager.get_active_users():
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logging.warning(f"Erreur en envoyant à {user_id}: {e}")

# Lancer le bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CallbackQueryHandler(check_follow, pattern="check_follow"))
    app.add_handler(CallbackQueryHandler(go_back, pattern="back"))

    app.run_polling()

if __name__ == "__main__":
    main()
