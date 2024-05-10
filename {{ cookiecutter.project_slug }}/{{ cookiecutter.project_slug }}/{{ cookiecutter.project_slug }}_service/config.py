import json
import os
import sys
from typing import Literal
from pydantic import BaseModel, validator
from pydantic import ValidationError as PydanticValidationError
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


class DotEnvLoadMixin:
    """Allow the class to load from a dot env.
    Should be used as a mixin + on a pydantic model.
    """

    @classmethod
    def from_env(cls):
        """
        To run, you need to expose the correct environment variables
        otherwise pydantic will complain.

        In containers: it will be loaded from the envfiles by docker / docker-compose
        In k8s: it will be loaded from the vars in k8s config
        In local: you need to export the variables from the .env file
            You cannot just export the file, you need to "set -a; source .env; set +a"
            See https://stackoverflow.com/questions/19331497
        """
        try:
            return cls.model_validate(os.environ)
        except PydanticValidationError as e:
            print(f'Error while validating configuration: {str(e)}')
            sys.exit(1)


class BaseConfig(BaseModel, DotEnvLoadMixin):
    """Default configuration for both services and entrypoints"""

    SECRET_KEY: str = ''
    ENV: str
    DEBUG: bool = False
    ALLOWED_HOSTS: str = ['localhost', '127.0.0.1']
    CSRF_TRUSTED_ORIGINS: str = ['http://localhost', 'http://127.0.0.1']
    DJANGO_DB_NAME: str
    DJANGO_DB_HOST: str
    DJANGO_DB_USER: str
    DJANGO_DB_PASSWORD: str
    DJANGO_DB_PORT: int
    LOGGING_JSON: bool = True
    LOGGING_REQUESTS: bool = True
    LOGGING_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    ALLOW_CORS: bool = True
    SENTRY_ACTIVATE: bool = False
    USE_OBJECT_STORAGE: bool = False
    STATIC_ROOT_FOLDER: str = ''
    MEDIA_ROOT_FOLDER: str = ''

    @validator('ALLOWED_HOSTS', 'CSRF_TRUSTED_ORIGINS')
    @classmethod
    def split_string(cls, value):
        return value.split(' ')


class DjangoSuperUserMixin(BaseModel):
    """Default Django superadmin created"""

    DJANGO_SU_NAME: str
    DJANGO_SU_EMAIL: str
    DJANGO_SU_PASSWORD: str


class SentryConfig(BaseModel, DotEnvLoadMixin):
    SENTRY_DSN: str
    SENTRY_SAMPLE_RATE: float = 0.1

    def setup_sentry(self, env: str):
        print('Setting up sentry...')

        sentry_sdk.init(
            dsn=self.SENTRY_DSN,
            enable_tracing=True,
            auto_session_tracking=False,
            traces_sample_rate=self.SENTRY_SAMPLE_RATE,
            integrations=[LoggingIntegration(event_level=None, level=None)],
            environment=env,
        )
        print('Sentry set up')
