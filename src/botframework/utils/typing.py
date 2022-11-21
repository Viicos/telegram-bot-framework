"""Custom typing aliases to be used within the library.
"""

from typing import Any, Dict, TypedDict

from telegram import Update
from telegram.ext import BaseHandler, ContextTypes
from telegram.ext._utils.types import HandlerCallback
from typing_extensions import NotRequired


class RegisteredHandlerType(TypedDict):
    handler: BaseHandler[Update, ContextTypes.DEFAULT_TYPE]
    group: NotRequired[int]


HandlerType = HandlerCallback[Update, ContextTypes.DEFAULT_TYPE, Any]


CommandHandlerRegistryType = Dict[str, RegisteredHandlerType]
