import logging

from telegram import Update
from telegram.ext import ContextTypes

from botframework.config import config
from botframework.utils.constants import name_to_level


async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Base callback used to log any incoming update.
    Additionnal logic can be added in this callback.
    """
    log = logging.getLogger("botframework")
    log.log(name_to_level.get(config.base_handler_log_level, logging.INFO), "Incoming update: %s", update)
