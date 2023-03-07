import abc
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AbstractLoggingAdaptor(abc.ABC):
    @abc.abstractmethod
    def info(self, param):
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, param, command):
        raise NotImplementedError

    @abc.abstractmethod
    def debug(self, param):
        raise NotImplementedError


class StdoutLoggingAdaptor(AbstractLoggingAdaptor):
    def info(self, *args, **kwargs):
        print(f'INFO: {args=} {kwargs=}')

    def error(self, *args, **kwargs):
        print(f'ERROR: {args=} {kwargs=}')

    def debug(self, *args, **kwargs):
        print(f'DEBUG: {args=} {kwargs=}')


class JsonLoggingAdaptor(AbstractLoggingAdaptor):
    def __init__(self, log_level: str = 'info'):
        global logger

        self.logger = logger
        console_handler = logging.StreamHandler()
        log_level = getattr(logging, str.upper(log_level))
        self.logger.setLevel(log_level)
        fmt = (
            '{"timestamp":"%(asctime)s", '
            '"level":"%(levelname)s", '
            '"logger":"%(module)s", '
            '"message":"%(message)s"}'
        )
        json_formatter = JsonFormatter(fmt)
        console_handler.setFormatter(json_formatter)
        self.logger.addHandler(console_handler)

    def info(self, msg, command=None, **kwargs):
        self.logger.info(msg, extra=dict(command=command), **kwargs)

    def error(self, msg, command=None, **kwargs):
        self.logger.error(msg, extra=dict(command=command), **kwargs)

    def debug(self, msg, command=None, **kwargs):
        self.logger.debug(msg, extra=dict(command=command), **kwargs)


class JsonFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(JsonFormatter, self).formatException(exc_info)
        json_result = {
            "timestamp": f"{datetime.now()}",
            "level": "ERROR",
            "logger": "app",
            "message": f"{result}",
        }
        return json.dumps(json_result)
