"""User configuration of the application."""


import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, TypeVar

import pytz

try:
    import tomllib  # type: ignore
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, BaseSettings, SecretStr, ValidationError, root_validator, validator
from telegram.constants import ParseMode

C = TypeVar("C", bound="Config")


class Handler(BaseModel):
    active: bool
    env: Dict[str, Any]


class Defaults(BaseModel):
    parse_mode: Optional[ParseMode] = None
    disable_notifications: Optional[bool] = None
    disable_web_page_preview: Optional[bool] = None
    quote: Optional[bool] = None
    tzinfo: Optional[pytz.BaseTzInfo] = None
    block: Optional[bool] = None
    allow_sending_without_reply: Optional[bool] = None
    protect_content: Optional[bool] = None

    @validator("tzinfo", pre=True)
    def validate_tzinfo(cls, v: str) -> pytz.BaseTzInfo:
        try:
            return pytz.timezone(v)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"{v} is not a valid timezone")

    class Config:
        arbitrary_types_allowed = True


class Config(BaseSettings):
    api_token: SecretStr
    persistence: bool
    persistence_filepath: Optional[Path] = None
    add_base_handler: bool
    handlers: Dict[str, Handler]
    defaults: Optional[Defaults] = None
    logging: Dict[str, Any]

    class Config:
        env_prefix = "telegram_"

    @classmethod
    def from_toml(cls: type[C], path: Path) -> C:
        if not path.exists():
            raise FileNotFoundError(f"Config filepath {path} was not found")
        if not path.is_file():
            raise FileNotFoundError(f"Config filepath {path} is not a file.")
        with open(path, "rb") as config_file:
            return cls(**tomllib.load(config_file))

    @root_validator(skip_on_failure=True)
    def validate_config(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["persistence"] and not values["persistence_filepath"]:
            raise ValueError("'persistence_filepath' is required when 'persistence' is set to true")

        return values


load_dotenv(dotenv_path=find_dotenv(usecwd=True))


try:
    config = Config.from_toml(Path(os.environ.get("TELEGRAM_CONFIG", "config.toml")))
except ValidationError as e:
    logging.exception("Error when validating config", exc_info=e)
    raise SystemExit()
