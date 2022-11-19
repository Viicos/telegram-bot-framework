from typing import Callable, Optional, Union, overload

from botframework.utils.typing import HandlerType


@overload
def register(
    function: None, *, name: Optional[str] = None, group: Optional[int] = None
) -> Callable[[HandlerType], HandlerType]:
    ...


@overload
def register(function: HandlerType, *, name: Optional[str] = None, group: Optional[int] = None) -> HandlerType:
    ...


def register(
    function: Optional[HandlerType] = None, *, name: Optional[str] = None, group: Optional[int] = None
) -> Union[Callable[[HandlerType], HandlerType], HandlerType]:
    """Decorator used to register a command handler to the application manager."""

    from botframework.manager import application_manager

    def decorator(func: HandlerType) -> HandlerType:
        application_manager.register(func, name, group)
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)
