from typing import Type, Dict, Callable, List, Union

from flask_with_json_logging import commands, events
from flask_with_json_logging.service_layer import unit_of_work


class MessageBus:
    def __init__(
            self,
            uow: unit_of_work.AbstractUnitOfWork,
            command_handlers: Dict[Type[commands.Command], Callable],
            event_handlers: Dict[Type[events.Event], List[Callable]],
    ):
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
        self.queue = []

    def handle(self, event_or_command: Union[commands.Command, events.Event]):
        self.queue = [event_or_command]
        response = None

        while self.queue:
            msg = self.queue.pop(0)
            if isinstance(msg, commands.Command):
                response = self.handle_command(msg)
            elif isinstance(msg, events.Event):
                self.handle_event(msg)
            else:
                raise Exception(f"{msg} is not Command or Event instance.")
            self.queue.extend(self.uow.collect_new_events())

        return response

    def handle_command(self, command):
        handler = self.command_handlers[type(command)]

        return handler(command)

    def handle_event(self, event):
        for handler in self.event_handlers[type(event)]:
            handler(event)
