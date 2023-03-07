import inspect

from flask_with_json_logging.adaptors import logging
from flask_with_json_logging.service_layer import handlers, messagebus, unit_of_work


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }

    return lambda message: handler(message, **deps)


def bootstrap(
        logging_adaptor: logging.AbstractLoggingAdaptor = None
):
    uow = unit_of_work.UnitOfWork()
    dependencies = {
        "uow": uow,
        "logging_adaptor": logging_adaptor,
    }

    injected_command_handlers = {
        command_type: inject_dependencies(command_handler, dependencies)
        for command_type, command_handler in handlers.COMMAND_HANDLERS.items()
    }
    injected_event_handlers = {
        event_type: [
            inject_dependencies(event_handler, dependencies)
            for event_handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        command_handlers=injected_command_handlers,
        event_handlers=injected_event_handlers,
    )
