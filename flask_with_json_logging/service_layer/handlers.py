from flask_with_json_logging import commands, events
from flask_with_json_logging.adaptors.logging import AbstractLoggingAdaptor
from flask_with_json_logging.service_layer import unit_of_work


def handle_say_hello(
        command: commands.SayHello,
        uow: unit_of_work.AbstractUnitOfWork,
        logging_adaptor: AbstractLoggingAdaptor
):
    logging_adaptor.info('this is an info log message')
    if not command.is_valid():
        logging_adaptor.error('command is not valid', command=command)
        uow.append_events(events.CommandFailed(command=command, message='command is not valid'))
        return False

    uow.append_events(events.CommandFinished(message='success'))
    logging_adaptor.debug('this is an debug log message')

    return command.message


def handle_command_failed(
        event: events.Event,
        logging_adaptor: AbstractLoggingAdaptor
):
    logging_adaptor.error(f'event {event} failed')


def handle_command_finished(
        event: events.Event,
        logging_adaptor: AbstractLoggingAdaptor
):
    logging_adaptor.info(f'event {event} finished')


COMMAND_HANDLERS = {
    commands.SayHello: handle_say_hello
}

EVENT_HANDLERS = {
    events.CommandFailed: [handle_command_failed, ],
    events.CommandFinished: [handle_command_finished, ]
}
