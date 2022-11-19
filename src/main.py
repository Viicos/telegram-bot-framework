import logging
import logging.config

from botframework.config import config
from botframework.manager import application_manager
from botframework.utils.module_loading import autodiscover_handlers

if __name__ == "__main__":
    logging.config.dictConfig(config.logging)
    log = logging.getLogger("botframework")
    autodiscover_handlers(*config.commands.keys())

    application_manager.enable_configured_handlers()
    log.info("Starting Telegram bot...")
    application_manager.application.run_polling()
