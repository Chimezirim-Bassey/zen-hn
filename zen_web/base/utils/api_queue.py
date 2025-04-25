import asyncio
from logging import getLogger
import random

from async_queue import TaskQueue, QueueItem
from .call_api import API
from .save_to_db import save_item, save_user

logger = getLogger(__name__)


class APIQueue:

    def __init__(self, **task_queue_kwargs):
        self.visited = set()
        self.task_queue = TaskQueue(**task_queue_kwargs)
        self.api = API()

    async def get_user(self, *, user_id):
        try:
            res = await self.api.get_user(user_id=user_id)
            # self.task_queue.add(item=QueueItem(save_user, user=res), must_complete=True, priority=4)
            if submitted := res.get('submitted', []):
                [self.task_queue.add(item=QueueItem(self.get_by_id, item_id=item), priority=1) for item in submitted]
            await save_user(user=res)
        except Exception as err:
            logger.error("%s: Error in getting user", err)

    async def get_by_id(self, *, item_id):
        try:
            if item_id in self.visited:
                return

            res = await self.api.get_by_id(item_id=item_id)
            self.visited.add(res['id'])

            if res.get('deleted', False):
                return

            if (parent := res.get('parent')) and parent not in self.visited:
                self.task_queue.add(item=QueueItem(self.get_by_id, item_id=parent), priority=1)

            if (poll := res.get('poll')) and poll not in self.visited:
                self.task_queue.add(item=QueueItem(self.get_by_id, item_id=poll), priority=1)

            if kids := res.get('kids', []):
                [self.task_queue.add(item=QueueItem(self.get_by_id, item_id=item), priority=1) for item in kids]

            if parts := res.get('parts', []):
                [self.task_queue.add(item=QueueItem(self.get_by_id, item_id=item), priority=1) for item in parts]

            if (by := res.get('by')) and by not in self.visited:
                self.task_queue.add(item=QueueItem(self.get_user, user_id=by), priority=1)

            await save_item(item=res)
            return res
        except Exception as err:
            logger.error("%s: Error in getting item", err)

    async def traverse_api(self, timeout: int = 0):
        try:
            (show_stories,
             job_stories,
             top_stories,
             ask_stories) = await asyncio.gather(self.api.show_stories(), self.api.job_stories(),
                                                 self.api.top_stories(),
                                                 self.api.ask_stories())
            stories = set(show_stories) | set(ask_stories) | set(job_stories) | set(top_stories)
            stories = list(stories)
            random.shuffle(stories)
            [self.task_queue.add(item=QueueItem(self.get_by_id, item_id=itd)) for itd in stories]
            self.task_queue.workers = len(stories)
            await self.task_queue.run(absolute_timeout=timeout)
        except Exception as err:
            logger.error("%s: Error in traversing API", err)

    async def update(self, timeout: int = 0):
        try:
            res = await self.api.updates()
            items = res['items']
            profiles = res['profiles']
            [self.task_queue.add(item=QueueItem(self.get_user, user_id=profile)) for profile in profiles]
            [self.task_queue.add(item=QueueItem(self.get_by_id, item_id=item)) for item in items]
            self.task_queue.workers = len(items) + len(profiles)
            await self.task_queue.run(absolute_timeout=timeout)
        except Exception as err:
            logger.error("%s: Error in updating", err)

    async def walk_back(self, *, amount: int = 5000, timeout: int = 0):
        largest = await self.api.max_item()
        print(f"Walking back from item {largest} to {largest - amount}")

        for item in range(largest, largest - amount, -1):
            self.task_queue.add(item=QueueItem(self.get_by_id, item_id=item), priority=0) if item not in self.visited else ...
        self.task_queue.workers = amount
        await self.task_queue.run(absolute_timeout=timeout)
