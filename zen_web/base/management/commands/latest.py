import asyncio

from django.core.management.base import BaseCommand

from ...utils.api_queue import APIQueue


class Command(BaseCommand):
    help = "Walk through the API and save data to the database"

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=600)
        parser.add_argument('--amount', type=int, default=6000)

    def handle(self, *args, **options):
        timeout = options['timeout']
        amount = options['amount']
        api_queue = APIQueue(workers=1000)
        asyncio.run(api_queue.walk_back(amount=amount, timeout=timeout))
