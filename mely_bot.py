import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIGURATION ===

TOKEN = "7714076813:AAFrzgdzZDXD2KKfD5_rpOF-ltK4Hy2HmTg"
ADMIN_ID = 5845745503

# URLs Instagram
INSTAGRAM_URLS = {
    'insta1': 'https://instagram.com/melykxr',
    'insta2': 'https://instagram.com/melyzrr02',
    'insta3': 'https://instagram.com/_melybbz',
    'insta4': 'https://instagram.com/melypzr',
    'insta5': 'https://instagram.com/melykdz'
}

# Texte boutons
BUTTONS = [
    "📸 Insta 1",
    "📸 Insta 2",
    "📸 Insta 3",
    "📸 Insta 4",
    "📸 Insta 5",
    "✅ J’ai follow les 5 comptes"
]

# === LOGS ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === GESTION UTILISATEURS ===
class BotManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, username=None, first_name=None):
        self.users[str(user_id)] = {
            'username': username,
            'first_name': first_name,
            'joined': datetime.now().isoformat(),
            'active': True
        }

    def get_active_users(self):
        return [int(uid) for uid, u in self.users.items() if u.get("active", True)]

    def get_stats(self):
        total = len(self.users)
        active = len(self.get_active_users())
        return total, active

bot_manager = BotManager()

# === HANDLERS ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_manager.add_user(user.id, user.username, user.first_name)

    keyboard = [
        [InlineKeyboardButton(BUTTONS[i], callback_data=f"instagram_{i+1}")] for i in range(5)
    ]
    keyboard.append([InlineKeyboardButton(BUTTONS[5], callback_data="verify")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/main/IMG_5618.jpeg"

    await update.message.reply_photo(
        photo=photo_url,
        caption="Hey bébé 😘 Clique sur un de mes nouveaux Insta 🔥 👇",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    data = query.data

    if data.startswith("instagram_"):
        index = int(data.split("_")[1])
        url = INSTAGRAM_URLS.get(f"insta{index}")
        if url:
            await query.edit_message_caption(
                caption=f"Voici le lien vers mon Insta {index} : {url}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Retour", callback_data="back")]
                ])
            )
    elif data == "verify":
        await query.edit_message_caption(
            caption="Super je vais aller vérifier ça et si t’es bien abonné aux 5 comptes je t’envoie ta surprise 🎁😘",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour", callback_data="back")]
            ])
        )
    elif data == "back":
        keyboard = [
            [InlineKeyboardButton(BUTTONS[i], callback_data=f"instagram_{i+1}")] for i in range(5)
        ]
        keyboard.append([InlineKeyboardButton(BUTTONS[5], callback_data="verify")])
        await query.edit_message_caption(
            caption="Hey bébé 😘 Clique sur un de mes nouveaux Insta 🔥 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total, active = bot_manager.get_stats()
    await update.message.reply_text(
        f"""📊 Stats bot:

👥 Total utilisateurs: {total}
✅ Actifs: {active}
📅 MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')}"""
    )

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Utilisation: /broadcast ton message ici")
        return

    message = " ".join(context.args)
    active_users = bot_manager.get_active_users()

    count = 0
    for user_id in active_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
            await asyncio.sleep(0.05)
        except:
            pass
    await update.message.reply_text(f"✅ Message envoyé à {count} utilisateurs actifs.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CommandHandler("broadcast", admin_broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot lancé.")
    app.run_polling()

if __name__ == "__main__":
    main()
