import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIG ===
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
ADMIN_ID = 5845745503
FILE_ID_PHOTO = "AgACAgQAAxkBAAIDg2ZlvaVzDZuYx9Yq8vZ7hFOTNZXkAAI9zDEbdHdgUfwJ4I0e63ZBAQADAgADeQADMAQ"

users = set()

# === MESSAGES ===
MESSAGES = {
    "welcome": """🚨 T’as déjà vu une ASIATIQUE avec des ÉNORMES SEINS ?

J’ai dû créer 5 nouveaux comptes Insta... Si tu t’abonnes aux 5, je t’envoie une surprise interdite aux mineurs 😈

👇 T’as juste à cliquer sur les boutons pour t’abonner. Et clique sur le dernier une fois que c’est fait pour recevoir ta surprise 💋""",
    
    "buttons": [
        ("📸 Insta 1", "https://www.instagram.com/compte1"),
        ("📸 Insta 2", "https://www.instagram.com/compte2"),
        ("📸 Insta 3", "https://www.instagram.com/compte3"),
        ("📸 Insta 4", "https://www.instagram.com/compte4"),
        ("📸 Insta 5", "https://www.instagram.com/compte5"),
        ("✅ C’est fait, envoie la surprise 🔥", "done")
    ],
    
    "done": "🔥 Bien vu ! T’es un vrai. La surprise arrive dans quelques secondes...",
    
    "help_admin": "/stats – Voir le nombre d’utilisateurs\n/broadcast [message] – Envoyer un message à tous\n/help_admin – Voir les commandes admin"
}

# === LOGS ===
logging.basicConfig(level=logging.INFO)

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    keyboard = [
        [InlineKeyboardButton(text, url=url) if url != "done" else InlineKeyboardButton(text, callback_data="done")]
        for text, url in MESSAGES["buttons"]
    ]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=FILE_ID_PHOTO,
        caption=MESSAGES["welcome"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "done":
        await query.message.reply_text(MESSAGES["done"])

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        total = len(users)
        await update.message.reply_text(f"📊 Utilisateurs : {total}\n✅ Actifs : {total}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    message = ' '.join(context.args)
    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=message)
        except:
            pass

async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(MESSAGES["help_admin"])

# === APP ===
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("help_admin", help_admin))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == '__main__':
    app.run_polling()
