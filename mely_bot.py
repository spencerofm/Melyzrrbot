import asyncio
import logging
import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration depuis les variables d’environnement

TOKEN = “7714076813:AAFrzgdzZDXD2KKfD5_rpOF-ltK4Hy2HmTg”
ADMIN_ID = 5845745503

# Configuration des logs

logging.basicConfig(format=’%(asctime)s - %(name)s - %(levelname)s - %(message)s’, level=logging.INFO)
logger = logging.getLogger(**name**)

# URLs Instagram

INSTAGRAM_URLS = {
‘insta1’: ‘https://instagram.com/melykxr’,
‘insta2’: ‘https://instagram.com/melyzrr02’,
‘insta3’: ‘https://instagram.com/_melybbz’,
‘insta4’: ‘https://instagram.com/melypzr’,
‘insta5’: ‘https://instagram.com/melykdz’
}

# Messages personnalisables

MESSAGES = {
‘welcome’: “””
🔥 Message de bienvenue personnalisable

Vous pouvez modifier ce texte selon vos besoins.

👇 Cliquez sur les boutons ci-dessous :
“””,

```
'button_labels': [
    "📸 Insta 1",
    "📸 Insta 2", 
    "📸 Insta 3",
    "📸 Insta 4",
    "📸 Insta 5",
    "✅ C'est fait ! 🔥"
],

'instagram_message': """
```

📱 SUIVEZ-MOI SUR INSTAGRAM !

Cliquez sur le lien pour accéder à mon compte :
{url}

👉 Abonnez-vous et activez les notifications !
“””,

```
'final_message': """
```

🎉 MERCI !

Merci de m’avoir suivi sur tous mes comptes !

💌 Restez connectés pour du contenu exclusif !
“””,

```
'unsubscribe_message': """
```

😢 Vous avez été désabonné des notifications.

Pour vous réabonner, tapez /start

Merci ! ❤️
“””
}

class BotManager:
def **init**(self):
self.users = {}

```
def add_user(self, user_id, username=None, first_name=None):
    """Ajoute un utilisateur"""
    self.users[str(user_id)] = {
        'username': username,
        'first_name': first_name,
        'joined_date': datetime.now().isoformat(),
        'active': True
    }

def deactivate_user(self, user_id):
    """Désactive un utilisateur"""
    if str(user_id) in self.users:
        self.users[str(user_id)]['active'] = False

def get_active_users(self):
    """Retourne la liste des utilisateurs actifs"""
    return [user_id for user_id, data in self.users.items() if data.get('active', True)]

def get_stats(self):
    """Retourne les statistiques"""
    total = len(self.users)
    active = len(self.get_active_users())
    return total, active
```

# Instance du gestionnaire

bot_manager = BotManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Fonction appelée quand un utilisateur tape /start”””
user = update.effective_user

```
# Ajouter l'utilisateur à la base de données
bot_manager.add_user(user.id, user.username, user.first_name)

# Créer les boutons avec les 5 comptes Instagram + bouton final
keyboard = []

# Boutons Instagram
for i in range(5):
    button_text = MESSAGES['button_labels'][i]
    callback_data = f'instagram_{i+1}'
    keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

# Bouton final
keyboard.append([InlineKeyboardButton(MESSAGES['button_labels'][5], callback_data='final_action')])

# Bouton désabonnement
keyboard.append([InlineKeyboardButton("❌ Se désabonner", callback_data='unsubscribe')])

reply_markup = InlineKeyboardMarkup(keyboard)

# Message de bienvenue personnalisé
welcome_text = MESSAGES['welcome'].format(first_name=user.first_name or "")

# URL de votre photo GitHub
photo_url = "https://raw.githubusercontent.com/spencerofm/Melyzrrbot/refs/heads/main/IMG_5618.jpeg"

try:
    await update.message.reply_photo(
        photo=photo_url,
        caption=welcome_text,
        reply_markup=reply_markup
    )
except Exception as e:
    logger.error(f"Erreur envoi photo: {e}")
    # Si pas de photo, envoyer juste le texte
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
```

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Gère les clics sur les boutons”””
query = update.callback_query
await query.answer()

```
user = query.from_user
button_data = query.data

# Gestion des boutons Instagram
if button_data.startswith('instagram_'):
    instagram_number = button_data.split('_')[1]
    instagram_key = f'insta{instagram_number}'
    
    if instagram_key in INSTAGRAM_URLS:
        instagram_url = INSTAGRAM_URLS[instagram_key]
        
        # Créer un bouton pour ouvrir Instagram
        keyboard = [[InlineKeyboardButton("🔗 Ouvrir Instagram", url=instagram_url)]]
        keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data='back_to_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = MESSAGES['instagram_message'].format(url=instagram_url)
        
        await query.edit_message_caption(
            caption=message,
            reply_markup=reply_markup
        )

# Bouton final (6ème bouton)
elif button_data == 'final_action':
    message = MESSAGES['final_message']
    
    # Bouton pour revenir au menu
    keyboard = [[InlineKeyboardButton("⬅️ Retour au menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_caption(
        caption=message,
        reply_markup=reply_markup
    )

# Retour au menu principal
elif button_data == 'back_to_menu':
    # Recréer le menu principal
    keyboard = []
    
    for i in range(5):
        button_text = MESSAGES['button_labels'][i]
        callback_data = f'instagram_{i+1}'
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    keyboard.append([InlineKeyboardButton(MESSAGES['button_labels'][5], callback_data='final_action')])
    keyboard.append([InlineKeyboardButton("❌ Se désabonner", callback_data='unsubscribe')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = MESSAGES['welcome'].format(first_name=user.first_name or "")
    
    await query.edit_message_caption(
        caption=welcome_text,
        reply_markup=reply_markup
    )

# Désabonnement
elif button_data == 'unsubscribe':
    bot_manager.deactivate_user(user.id)
    message = MESSAGES['unsubscribe_message']
    
    await query.edit_message_caption(caption=message)
```

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Statistiques du bot (admin seulement)”””
if update.effective_user.id != ADMIN_ID:
await update.message.reply_text(“❌ Commande admin uniquement.”)
return

```
total, active = bot_manager.get_stats()

stats_text = f"""
```

📊 STATISTIQUES DU BOT

👥 Total utilisateurs : {total}
✅ Utilisateurs actifs : {active}
❌ Désabonnés : {total - active}

📅 Mis à jour : {datetime.now().strftime(’%d/%m/%Y à %H:%M’)}

🔗 URLs Instagram configurées :
“””

```
for key, url in INSTAGRAM_URLS.items():
    stats_text += f"• {key}: {url}\n"

await update.message.reply_text(stats_text)
```

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Envoyer un message à tous les utilisateurs actifs (admin seulement)”””
if update.effective_user.id != ADMIN_ID:
await update.message.reply_text(“❌ Commande admin uniquement.”)
return

```
if not context.args:
    await update.message.reply_text("""
```

📢 ENVOYER UN MESSAGE GROUPÉ

Utilisation : /broadcast [votre message]

Exemple : /broadcast Nouveau post sur Instagram ! 🔥

Le message sera envoyé à tous les utilisateurs actifs.
“””)
return

```
message = ' '.join(context.args)
active_users = bot_manager.get_active_users()

if not active_users:
    await update.message.reply_text("Aucun utilisateur actif à qui envoyer le message.")
    return

sent = 0
failed = 0

await update.message.reply_text(f"📤 Envoi en cours à {len(active_users)} utilisateurs...")

for user_id in active_users:
    try:
        await context.bot.send_message(chat_id=int(user_id), text=message)
        sent += 1
        await asyncio.sleep(0.1)  # Pause pour éviter les limites
    except Exception as e:
        failed += 1
        logger.error(f"Erreur envoi à {user_id}: {e}")

result_text = f"""
```

✅ MESSAGE ENVOYÉ !

📤 Envoyé avec succès : {sent}
❌ Échecs : {failed}
👥 Total : {len(active_users)}
“””

```
await update.message.reply_text(result_text)
```

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Aide pour les commandes admin”””
if update.effective_user.id != ADMIN_ID:
return

```
help_text = """
```

🔧 COMMANDES ADMIN

/stats - Voir les statistiques du bot
/broadcast [message] - Envoyer un message à tous
/help_admin - Afficher cette aide

📊 Le bot collecte automatiquement les utilisateurs
📤 Vous pouvez envoyer des messages groupés
🔗 Les 5 comptes Instagram sont configurés
“””

```
await update.message.reply_text(help_text)
```

def main():
“”“Fonction principale”””
# Créer l’application
application = Application.builder().token(TOKEN).build()

```
# Ajouter les handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(CommandHandler("stats", admin_stats))
application.add_handler(CommandHandler("broadcast", admin_broadcast))
application.add_handler(CommandHandler("help_admin", admin_help))

# Démarrer le bot
logger.info("🤖 Bot démarré !")
logger.info(f"👥 Bot configuré pour l'admin ID: {ADMIN_ID}")
application.run_polling()
```

if **name** == ‘**main**’:
main()
