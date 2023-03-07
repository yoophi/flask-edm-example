from flask import current_app
from werkzeug.local import LocalProxy

from flask_with_json_logging.adaptors import logging
from flask_with_json_logging import bootstrap
from flask_with_json_logging.service_layer.messagebus import MessageBus

_bus = None


def get_message_bus():
    global _bus

    if _bus is None:
        logging_adaptor = get_logging_adaptor(current_app.config)
        _bus = bootstrap.bootstrap(
            logging_adaptor=logging_adaptor,
        )

    return _bus


bus: MessageBus = LocalProxy(get_message_bus)  # noqa


def get_logging_adaptor(config):
    if config.get('USE_JSON_LOGGER'):
        return logging.JsonLoggingAdaptor(log_level=config.get('LOG_LEVEL'))

    return logging.StdoutLoggingAdaptor()
