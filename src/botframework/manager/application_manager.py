import logging
from typing import Optional

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    BaseHandler,
    CommandHandler,
    ContextTypes,
    Defaults,
    MessageHandler,
    PicklePersistence,
    TypeHandler,
    filters as filters_module,
)

from botframework.config import config
from botframework.handlers import base_callback
from botframework.utils.typing import CommandHandlerRegistryType, HandlerType, RegisteredHandlerType


class ApplicationManager:
    """An application manager used to manage the application
    and the handlers, providing convenient methods.

    Attributes:
        application (:class:`telegram.ext.Application`): The Telegram application.
    """

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.handlers: CommandHandlerRegistryType = {}
        self.build()

        if config.add_base_handler:
            base_handler = TypeHandler(Update, base_callback)
            self.log.debug("Adding base handler to the bot")
            self.application.add_handler(base_handler, -1)

    def build(self) -> None:
        """Build the application, using parameters provided by the user configuration."""
        application_builder = ApplicationBuilder().token(config.api_token.get_secret_value())
        if config.persistence:
            persistence = PicklePersistence(filepath=config.persistence_filepath)  # type: ignore
            application_builder.persistence(persistence)

        if config.defaults is not None:
            config_dct = {k: v for k, v in config.defaults.dict().items() if v is not None}
            defaults = Defaults(**config_dct)
            application_builder.defaults(defaults)

        self.application = application_builder.build()

    def register_handler(
        self, handler: BaseHandler[Update, ContextTypes.DEFAULT_TYPE], name: str, group: Optional[int] = None
    ) -> None:
        """Register a handler.

        Args:
            handler: The handler to be added to the registry.
            name: The name of the handler, used a key in the registry.
            group (optional): The group identifier. Default is ``0``.
        """
        handler_cfg: RegisteredHandlerType = {"handler": handler}
        if group is not None:
            handler_cfg["group"] = group
        self.handlers[name] = handler_cfg

    def register_command_handler(
        self, command_handler: HandlerType, name: Optional[str] = None, group: Optional[int] = None
    ) -> None:
        """Create and register a command handler.

        Args:
            command_handler: The command handler to be added to the registry.
            name (optional): The name of the command to be registered. If not provided, the ``command_handler.__name__``
                attribute will be used instead.
            group (optional): The group identifier. Default is ``0``.
        """
        handler_name = name or command_handler.__name__
        self.log.debug("Adding the command handler %r to the bot", handler_name)
        self.register_handler(CommandHandler(handler_name, command_handler), handler_name, group)

    def register_message_handler(
        self,
        message_handler: HandlerType,
        name: Optional[str] = None,
        filters: Optional[filters_module.BaseFilter] = None,
        group: Optional[int] = None,
    ) -> None:
        """Create and register a message handler.

        Args:
            message_handler: The message handler to be added to the registry.
            name (optional): The name of the command to be registered. If not provided, the ``message_handler.__name__``
                attribute will be used instead.
            group (optional): The group identifier. Default is ``0``.
        """
        handler_name = name or message_handler.__name__
        self.log.debug("Adding the message handler %r to the bot", name)
        self.register_handler(MessageHandler(filters or filters_module.ALL, message_handler), handler_name, group)

    def enable_configured_handlers(self) -> None:
        """Enable handlers set as active in user configuration."""
        for command_name, command_cfg in config.commands.items():
            if command_cfg.active:
                if command_name not in self.handlers:
                    self.log.warning("Can't find handler %r", command_name)
                    continue
                self.enable_handler(command_name)

    def enable_handler(self, handler_name: str) -> None:
        """Add a handler from the registry to the Telegram application.

        Args:
            handler_name: The command name to be added to the Telegram application.
        """
        if handler_name not in self.handlers:
            raise ValueError(f"{handler_name!r} does not exist")
        self.log.debug("Enabling %r", handler_name)
        self.application.add_handler(**self.handlers[handler_name])

    def disable_handler(self, handler_name: str) -> None:
        """Remove a handler from the registry to the Telegram application.

        Args:
            handler_name: The command name to be added to the Telegram application.
        """
        if handler_name not in self.handlers:
            raise ValueError(f"{handler_name!r} does not exist")
        self.log.debug("Disabling %r", handler_name)
        self.application.remove_handler(**self.handlers[handler_name])
