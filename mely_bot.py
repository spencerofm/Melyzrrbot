from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import json
import os

# ========== CONFIG ==========
TOKEN = "7714076813:AAEDEukD5q88c9mUHnvl0xEoN-5mQr-XQJ0"
DATA_FILE = "users.json"
IMAGE_FILE_ID = "YOUR_FILE_ID_HERE"  # <-- remplace ça après avoir fait /get_file_id
INSTAGRAM_LINKS = [
    ("📸 Insta 1", "https://instagram.com/1"),
    ("📸 Insta 2", "https://instagram.com/2"),
    ("📸 Insta 3", "https://instagram.com/3"),
    ("📸 Insta 4", "https://instagram.com/4"),
    ("📸 Insta 5", "https://instagram.com/5"),
]

# ========== UTILS ==========
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

# ========== HANDLERS ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {"active": True}
        save_users(users)

    # Envoie des boutons
    keyboard = [[InlineKeyboardButton(text, url=url)] for text, url in INSTAGRAM_LINKS]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Hey bebe 😘 Clique sur un de mes nouveaux Insta 🔥👇", reply_markup=reply_markup)
    await update.message.reply_text("✅ C’est fait, envoie la surprise 🔥")

    # Envoie de l'image surprise
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=IMAGE_FILE_ID)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id != "YOUR_TELEGRAM_ID":
        await update.message.reply_text("🚫 Tu n’as pas la permission.")
        return
    users = load_users()
    total = len(users)
    active = sum(1 for u in users.values() if u.get("active"))
    await update.message.reply_text(f"📊 Total : {total} utilisateurs\n✅ Actifs : {active}")

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"📷 Photo file_id:\n`{file_id}`", parse_mode='Markdown')
    elif update.message.document and update.message.document.mime_type.startswith('image/'):
        file_id = update.message.document.file_id
        await update.message.reply_text(f"📁 Document image file_id:\n`{file_id}`", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Aucune image détectée. Envoie une photo ou une image en document.")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

# ========== MAIN ==========
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_file_id))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == "__main__":
    main()
