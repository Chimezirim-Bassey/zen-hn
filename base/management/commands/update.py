import asyncio
# from multiprocessing.pool import worker

from django.core.management.base import BaseCommand

from ...utils.api_queue import APIQueue


class Command(BaseCommand):
    help = "Update the database with new data"

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=120)

    def handle(self, *args, **options):
        timeout = options['timeout']
        api_queue = APIQueue(workers=1000)
        asyncio.run(api_queue.update(timeout=timeout))
