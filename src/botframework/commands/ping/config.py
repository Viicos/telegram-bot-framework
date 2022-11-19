import logging

from pydantic import BaseModel, ValidationError

from botframework.config import config as bot_config


class Config(BaseModel):
    wait_time: int


try:
    config = Config(**bot_config.commands["ping"].env)
except ValidationError as e:
    logging.exception("Error when validating config", exc_info=e)
    raise SystemExit()
