import logging

from telegram import Update
from telegram.ext import ContextTypes


async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Base callback used to log any incoming update.
    Additionnal logic can be added in this callback.
    """
    log = logging.getLogger("bot")
    log.info("Incoming update: %s", update)
