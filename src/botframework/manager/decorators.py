from typing import Callable, Optional, Union, overload

from telegram.ext.filters import BaseFilter

from botframework.utils.typing import HandlerType


@overload
def command_handler(
    function: None, *, name: Optional[str] = None, group: Optional[int] = None
) -> Callable[[HandlerType], HandlerType]:
    ...


@overload
def command_handler(function: HandlerType, *, name: Optional[str] = None, group: Optional[int] = None) -> HandlerType:
    ...


def command_handler(
    function: Optional[HandlerType] = None, *, name: Optional[str] = None, group: Optional[int] = None
) -> Union[Callable[[HandlerType], HandlerType], HandlerType]:
    """Decorator used to register a command handler to the application manager."""

    from botframework.manager import application_manager

    def decorator(func: HandlerType) -> HandlerType:
        application_manager.register_command_handler(func, name, group)
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)


@overload
def message_handler(
    function: None, *, name: Optional[str] = None, filters: Optional[BaseFilter] = None, group: Optional[int] = None
) -> Callable[[HandlerType], HandlerType]:
    ...


@overload
def message_handler(
    function: HandlerType,
    *,
    name: Optional[str] = None,
    filters: Optional[BaseFilter] = None,
    group: Optional[int] = None
) -> HandlerType:
    ...


def message_handler(
    function: Optional[HandlerType] = None,
    *,
    name: Optional[str] = None,
    filters: Optional[BaseFilter] = None,
    group: Optional[int] = None
) -> Union[Callable[[HandlerType], HandlerType], HandlerType]:

    from botframework.manager import application_manager

    def decorator(func: HandlerType) -> HandlerType:
        application_manager.register_message_handler(func, name, filters, group)
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)
