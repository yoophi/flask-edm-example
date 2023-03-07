import abc

from flask_with_json_logging import events


class AbstractUnitOfWork(abc.ABC):
    def __init__(self):
        self.events = []

    def append_events(self, event: events.Event):
        self.events.append(event)

    def collect_new_events(self):
        _events = self.events
        self.events = []

        return _events


class UnitOfWork(AbstractUnitOfWork):
    pass
