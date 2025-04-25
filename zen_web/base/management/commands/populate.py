import asyncio

from django.core.management.base import BaseCommand

from ...utils.api_queue import APIQueue


class Command(BaseCommand):
    help = "Populate the database with some data"

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=600)

    def handle(self, *args, **options):
        timeout = options['timeout']
        api_queue = APIQueue(workers=1000)
        asyncio.run(api_queue.traverse_api(timeout=timeout))
