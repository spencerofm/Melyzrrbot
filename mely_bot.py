
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Configuration du bot
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

# Messages personnalisés
MESSAGES = {
    "welcome": """
🚨 T’as déjà vu une *ASIATIQUE* avec des *ÉNORMES SEINS* ?

J’ai dû créer 5 nouveaux comptes Insta… Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 🔞

👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋
""",
    "button_labels": [
        "📸 Insta 1",
        "📸 Insta 2",
        "📸 Insta 3",
        "📸 Insta 4",
        "📸 Insta 5",
        "✅ C’est fait, envoie la surprise 🔥",
    ],
    "unsubscribe_message": "❌ Tu as été désabonné. Pour te réabonner, tape /start.",
}

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = []
    for i in range(5):
        button_text = MESSAGES["button_labels"][i]
        callback_data = f"instagram_{i+1}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton(MESSAGES["button_labels"][5], callback_data="final_action")])
    keyboard.append([InlineKeyboardButton("❌ Se désabonner", callback_data="unsubscribe")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = MESSAGES["welcome"]
    file_id_photo = "TON_FILE_ID_ICI"  # ← Remplace par le vrai file_id une fois récupéré

    try:
        await update.message.reply_photo(
            photo=file_id_photo,
            caption=welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )
    except Exception as e:
        logger.error(f"Erreur envoi photo: {e}")
        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    button_data = query.data

    if button_data.startswith("instagram_"):
        instagram_number = button_data.split("_")[1]
        instagram_key = f"insta{instagram_number}"
        if instagram_key in INSTAGRAM_URLS:
            instagram_url = INSTAGRAM_URLS[instagram_key]
            keyboard = [
                [InlineKeyboardButton("🔗 Ouvrir Instagram", url=instagram_url)],
                [InlineKeyboardButton("⬅️ Retour", callback_data="back_to_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message = f"👉 Clique sur le lien pour accéder : {instagram_url}"
            await query.edit_message_caption(caption=message, reply_markup=reply_markup)

    elif button_data == "final_action":
        message = "🔥 C’est noté ! Tu recevras ta surprise dans quelques instants laisse moi juste verifier que tu t'es bien abonné aux 5 comptes insta"
        keyboard = [[InlineKeyboardButton("⬅️ Retour au menu", callback_data="back_to_menu")]]
        await query.edit_message_caption(caption=message, reply_markup=InlineKeyboardMarkup(keyboard))

    elif button_data == "back_to_menu":
        return await start(update, context)

    elif button_data == "unsubscribe":
        bot_manager.deactivate_user(user.id)
        await query.edit_message_caption(caption=MESSAGES["unsubscribe_message"])

# Handler pour récupérer le file_id d’une photo
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file_id = photo.file_id
        await update.message.reply_text(f"🆔 File ID reçu : `{file_id}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("Erreur lors de la récupération du file_id 😓")
        logger.error(f"Erreur handle_photo : {e}")

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Commande admin uniquement.")
        return
    total, active = bot_manager.get_stats()
    await update.message.reply_text(
        f"👥 Total : {total} utilisateurs
✅ Actifs : {active}
❌ Désabonnés : {total - active}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # ← Pour capturer file_id
    logger.info("🤖 Bot lancé")
    app.run_polling()

if __name__ == "__main__":
    main()
