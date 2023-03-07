import abc
from dataclasses import dataclass


class Command(abc.ABC):
    @abc.abstractmethod
    def is_valid(self):
        raise NotImplementedError


@dataclass
class SayHello(Command):
    message: str

    def is_valid(self, ):
        return bool(self.message)
