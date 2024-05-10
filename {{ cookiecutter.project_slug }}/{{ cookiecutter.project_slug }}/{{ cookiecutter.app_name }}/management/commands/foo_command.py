from django.conf import settings
from django.core.management.base import BaseCommand


import structlog

logger = structlog.get_logger()


class Command(BaseCommand):
    help = 'Basic Command'

    def handle(self, *args, **options):
       logger.info("I'm a management command")
