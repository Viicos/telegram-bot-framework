import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from botframework.manager import register

from .config import config


@register
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    context.bot_data.setdefault("ping", {})
    ping_no = context.bot_data["ping"].setdefault("count", 1)

    if update.effective_chat is not None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ping...")
        await asyncio.sleep(config.wait_time)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Pong no {ping_no}!")

    context.bot_data["ping"]["count"] += 1
