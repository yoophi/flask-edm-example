import abc
from dataclasses import dataclass

from flask_with_json_logging import commands


class Event(abc.ABC):
    pass


@dataclass
class CommandFailed(Event):
    command: commands.Command
    message: str


@dataclass
class CommandFinished(Event):
    message: str
