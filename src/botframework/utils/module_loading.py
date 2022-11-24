from importlib import import_module


def autodiscover_handlers(*module_names: str) -> None:
    """Auto-discover commands module, to force an import and register handlers.

    Args:
        module_names (str): Names of the modules to be imported.
    """
    for module in module_names:
        try:
            import_module(f"botframework.handlers.{module}.handler")
        except ModuleNotFoundError:
            pass
