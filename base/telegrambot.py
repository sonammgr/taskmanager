import os
import django
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import logging

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taskmanager.settings')
django.setup()

from django.conf import settings
from base.models import Telegramuser
from django.contrib.auth.models import User 

TOKEN = settings.TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(f"User {user.username if user else 'N/A'} sent /start")
    await update.message.reply_html(
        f"Hi {user.mention_html() if user else 'there'}! I am Bot Pookie. "
        f"Thank thank you for chatting with me. Send /join to register your Telegram username "
        f"for Taskmanager updates, or /help if you need assistance."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.username if update.effective_user else 'N/A'} sent /help")
    await update.message.reply_text('HI I AM POOKIE BOT, HOW CAN I HELP YOU? '
                                     'Try /start to see my welcome message, '
                                     'or /join to register your Telegram username.')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.username if update.effective_user else 'N/A'} sent /custom")
    await update.message.reply_text('Hello! This is a custom command response from Bot Pookie.')

async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user_info = update.effective_user
    chat_id = update.effective_chat.id

    if telegram_user_info and telegram_user_info.username:
        telegram_username = telegram_user_info.username
        logger.info(f"User @{telegram_username} sent /join. Saving to DB.")

        try:
            django_user, user_created = await asyncio.to_thread(
                User.objects.get_or_create,
                username=telegram_username,
                defaults={'email': f'{telegram_username}@telegram.com', 'password': User.objects.make_random_password()}
            )
            await asyncio.to_thread(
                Telegramuser.objects.update_or_create,
                telegram_username=telegram_username,
                defaults={'telegram_chat_id': str(chat_id), 'user': django_user}
            )
            await update.message.reply_text(f"@{telegram_username}, you are now registered with Taskmanager Bot!")
        except Exception as e:
            logger.error(f"Error saving /join for @{telegram_username}: {e}")
            await update.message.reply_text("Sorry, an error occurred while registering you.")
    else:
        logger.warning(f"Received /join from user without username: {telegram_user_info.id if telegram_user_info else 'N/A'}")
        await update.message.reply_text("Please set a Telegram username to use /join.")

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text:
        logger.info(f"User {update.effective_user.username if update.effective_user else 'N/A'} sent text: '{update.message.text}'")
        await update.message.reply_text(f"You said: {update.message.text}\nTry a command like /start or /join!")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))
    application.add_handler(CommandHandler("join", join_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    logger.info("Bot Pookie is starting and listening...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"Telegram Bot failed to start: {e}", exc_info=True)