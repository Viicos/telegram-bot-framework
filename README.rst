
telegram-bot-framework
======================

.. image:: https://img.shields.io/badge/python-3.7%2B-blue.svg
    :alt: Supported Python versions

.. image:: https://img.shields.io/badge/python--telegram--bot-v20-blue
    :target: https://github.com/python-telegram-bot/python-telegram-bot
    :alt: Supported python-telegram-bot version

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: Black
    :target: https://github.com/psf/black

A small configurable Python framework to create and manage a Telegram bot, using the `python-telegram-bot <https://github.com/python-telegram-bot/python-telegram-bot>`_ library.

Introduction
------------

This framework provides a convenient development environment to create and configure command handlers for your Telegram bot. Application and created command handlers are configurable through
the use of `pydantic <https://github.com/pydantic/pydantic>`_.

Installation
------------

It is strongly recommended to use a `virtual environment <https://docs.python.org/3/library/venv.html>`_ to install and run the application.

`pip-tools <https://github.com/jazzband/pip-tools>`_ is the recommended way of handling requirements. Before using the application, install ``pip-tools`` and run the following script:

.. code-block:: shell

    ./bin/compile-dependencies.sh

You can then use ``pip`` to install requirements:

.. code-block:: shell

    pip install -r requirements/requirements.txt  // or dev.txt

Configure your bot
------------------

To get started, configure your application using the ``config_example.toml`` file given in this repository. This file provides basic configuration to your bot (such as your `API token <https://core.telegram.org/bots/api#authorizing-your-bot>`_)
and your created command handlers.

The following is a description of the available fields in the configuration file:

.. code-block:: toml

    api_token = 'change_me'  # Your Telegram API token
    persistence = true  # Whether PicklePersistence should be used or not
    persistence_filepath = 'bot.data'  # Filepath of the bot data, relative to the cwd. Required if persistence is set to true
    add_base_handler = true  # Add a base handler with group -1, called before all the others (serves as a logging wrapper by default)

    [defaults]  # Default fields to be provided to telegram.ext.Defaults
    tzinfo = 'utc'

    [handlers]  # See 'Creating your first handler'

    [logging]  # Logging configuration
    version = 1
    disable_existing_loggers = true

    [logging.formatters.verbose]
    format = '{asctime} [{levelname}] {name} - {message}'
    style = '{'

    [logging.handlers.console]
    class = 'logging.StreamHandler'
    formatter = 'verbose'
    level = 'DEBUG'

    [logging.handlers.file]
    class = 'logging.handlers.RotatingFileHandler'
    formatter = 'verbose'
    filename = 'log/telegram.log'
    maxBytes = 10485760  # 10 MB
    backupCount = 10

    [logging.loggers.botframework]
    level = 'DEBUG'
    propagate = true
    handlers = ['console', 'file']

All ``defaults`` fields are optional, and logging config can be tweaked to fit your needs (only the ``botframework`` logger is required).

You can specify the location of your config file with the ``TELEGRAM_CONFIG`` environment variable. If not set, it will try to load the config from the ``config.toml`` file, relative to the current working directory.

Additionally, settings can be read from environment variables (e.g. ``api_token`` will take the value of the environment variable ``telegram_api_key``).
See `pydantic docs <https://pydantic-docs.helpmanual.io/usage/settings/>`_ for more details.

Creating your first handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each handler is defined as a submodule of the ``botframework.handlers`` module. We will take the ``ping`` command provided in this repository as an example. The structure of the module is as follow:

.. code-block::

    handlers
    ├── ping
    ├──── __init__.py
    ├──── config.py
    ├──── handler.py

The ``handler.py`` file contains the definition of the async handler:

.. code-block:: python

    from telegram import Update
    from telegram.ext import ContextTypes

    from botframework.manager import command_handler

    @command_handler
    async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        ...

All handlers must be decorated using either the ``command_handler`` or ``message_handler`` decorator, so that they are correctly picked up by the application manager. The decorator takes two optional arguments:

- ``name``: ``str``, the name of the handler. If not provided, the handler's ``__name__`` attribute will be used.
- ``group``: ``int``, the group identifier of the handler (``python-telegram-bot`` will use the default value of ``0``).

If you are using the ``command_handler`` and you do not provide a name, the handler's ``__name__`` attribute will be used as the ``command`` attribute of ``CommandHandler``.

You can specify filters to the ``message_handler`` as well.

If you want to add user configuration for this handler, you can define a pydantic model in ``config.py``:

.. code-block:: python

    import logging

    from pydantic import BaseModel, ValidationError

    from botframework.config import config as bot_config


    class Config(BaseModel):
        wait_time: int


    try:
        config = Config(**bot_config.handlers["ping"].env)
    except ValidationError as e:
        logging.exception("Error when validating config", exc_info=e)
        raise SystemExit()

And finally here is the corresponding user configuration:

.. code-block:: toml

    [handlers]  # Section to configure your defined handlers

    [handlers.ping]  # The name of the handler should correspond to the one provided in the register decorator
    active = true  # Whether the command should be added to the bot or not
    [handlers.ping.env]  # Command related configuration
    wait_time = 2

Run the application
-------------------

To run the application, you can call the ``main.py`` file:

.. code-block:: shell

    python src/main.py
