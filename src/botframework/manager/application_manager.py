import logging
from typing import Optional

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, Defaults, PicklePersistence, TypeHandler

from botframework.commands import base_callback
from botframework.config import config
from botframework.utils.typing import CommandHandlerRegistryType, HandlerType, RegisteredHandlerType


class ApplicationManager:
    """An application manager used to manage the application
    and the handlers, providing convenient methods.

    Attributes:
        application (:class:`telegram.ext.Application`): The Telegram application.
    """

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.command_handlers: CommandHandlerRegistryType = {}
        self.build()

        if config.add_base_handler:
            base_handler = TypeHandler(Update, base_callback)
            self.log.debug("Adding base handler to the bot")
            self.application.add_handler(base_handler, -1)

    def build(self) -> None:
        """Build the application, using parameters provided by the user configuration."""
        application_builder = ApplicationBuilder().token(config.api_token)
        if config.persistence:
            persistence = PicklePersistence(filepath=config.persistence_filepath)  # type: ignore
            application_builder.persistence(persistence)

        if config.defaults is not None:
            config_dct = {k: v for k, v in config.defaults.dict().items() if v is not None}
            defaults = Defaults(**config_dct)
            application_builder.defaults(defaults)

        self.application = application_builder.build()

    def register(self, command: HandlerType, name: Optional[str] = None, group: Optional[int] = None) -> None:
        """Register a command handler, by using the register decorator.

        Args:
            command: The command to be added to the registry.
            name (optional): The name of the command to be registered. If not provided, the ``command.__name__``
                attribute will be used instead.
            group (optional): The group identifier. Default is ``0``.
        """
        self.log.debug("Adding the handler %r to the bot", command.__name__)
        command_cfg: RegisteredHandlerType = {"handler": CommandHandler(name or command.__name__, command)}
        if group is not None:
            command_cfg["group"] = group
        self.command_handlers[name or command.__name__] = command_cfg

    def enable_configured_handlers(self) -> None:
        """Enable command handlers set as active in user configuration."""
        for command_name, command_cfg in config.commands.items():
            if command_cfg.active:
                if command_name not in self.command_handlers:
                    self.log.warning("Can't find command %r", command_name)
                    continue
                self.enable_command_handler(command_name)

    def enable_command_handler(self, command_name: str) -> None:
        """Add a handler from the registry to the Telegram application.

        Args:
            command_name: The command name to be added to the Telegram application.
        """
        if command_name not in self.command_handlers:
            raise ValueError(f"{command_name!r} does not exist")
        self.log.debug("Enabling %r", command_name)
        self.application.add_handler(**self.command_handlers[command_name])

    def disable_command_handler(self, command_name: str) -> None:
        """Remove a handler from the registry to the Telegram application.

        Args:
            command_name: The command name to be added to the Telegram application.
        """
        if command_name not in self.command_handlers:
            raise ValueError(f"{command_name!r} does not exist")
        self.log.debug("Disabling %r", command_name)
        self.application.remove_handler(**self.command_handlers[command_name])
