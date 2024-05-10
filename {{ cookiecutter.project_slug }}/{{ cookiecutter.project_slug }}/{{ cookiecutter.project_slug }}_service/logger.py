from typing import cast
import colorama
import structlog
from structlog_sentry import SentryProcessor
import logging


class PrettyLogLevelColumnFormatter(structlog.dev.LogLevelColumnFormatter):
    def __call__(self, key: str, value: object) -> str:
        self.width = 0
        level = cast(str, value)
        style = '' if self.level_styles is None else self.level_styles.get(level, '')

        return f'[{style}{structlog.dev._pad(level.capitalize(), self.width)}{self.reset_style}]'


def get_config(
    to_json: bool = True, level: str = 'INFO', datetime_fmt: str = '%H:%M:%S'
):
    columns = [
        structlog.dev.Column(
            'timestamp',
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Style.DIM,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            'logger',
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Fore.CYAN,
                reset_style=colorama.Style.RESET_ALL,
                prefix='[',
                postfix=']',
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            'level',
            PrettyLogLevelColumnFormatter(
                level_styles=structlog.dev.ConsoleRenderer.get_default_level_styles(),
                reset_style=colorama.Style.RESET_ALL,
            ),
        ),
        structlog.dev.Column(
            'event',
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Fore.WHITE,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            '',
            structlog.dev.KeyValueColumnFormatter(
                key_style=colorama.Fore.CYAN,
                value_style=colorama.Fore.WHITE,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
    ]

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            SentryProcessor(event_level=logging.ERROR, tag_keys='__all__'),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt=datetime_fmt, utc=False),
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json_formatter': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
            },
            'plain_console': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(columns=columns),
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'plain_console',
            },
            'json_output': {
                'class': 'logging.StreamHandler',
                'formatter': 'json_formatter',
            },
        },
        'loggers': {
            '': {
                'handlers': ['json_output'] if to_json else ['console'],
                'level': level,
            },
            'django': {
                'propagate': True,  # Prevents the pika logs from being propagated to the root logger
                'level': 'ERROR',  # Setting this to CRITICAL means nothing gets logged.
            },
            'pika': {
                'propagate': False,  # Prevents the pika logs from being propagated to the root logger
                'level': 'CRITICAL',  # Setting this to CRITICAL means nothing gets logged.
            },
        },
    }


def trigger_logger():
    logger = structlog.get_logger()

    logger.debug('This is a debug message')
    logger.info('This is a info message')
    logger.warning('This is a warning message')
    logger.error('This is a error message')

    try:
        1 / 0  # noqa
    except ZeroDivisionError:
        logger.error('Raised to test sentry (ZeroDivisionError)')
    1 / 0  # noqa
