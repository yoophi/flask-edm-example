import os

USE_JSON_LOGGER = os.environ.get('USE_JSON_LOGGER') == 'true'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')


class Config:
    USE_JSON_LOGGER = USE_JSON_LOGGER
    LOG_LEVEL = LOG_LEVEL

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
