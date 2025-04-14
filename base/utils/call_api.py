import http.client
import asyncio
import json
from logging import getLogger

logger = getLogger(__name__)


class API:
    URL = "hacker-news.firebaseio.com"

    async def get(self, *, path: str):
        url = f'{self.URL}'
        path = f'/v0/{path}'
        conn = http.client.HTTPSConnection(url)
        await asyncio.to_thread(conn.request, 'GET', path)
        res = await asyncio.to_thread(conn.getresponse)
        res = json.loads(res.read().decode('utf-8'))
        conn.close()
        return res

    async def get_item(self, *, item_id):
        path = f'item/{item_id}.json'
        try:
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get item at %s", err, path)

    async def get_user(self, *, user_id):
        path = f'user/{user_id}.json'
        try:
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get user at %s", err, path)

    async def get_by_id(self, *, item_id):
        path = f'item/{item_id}.json'
        try:
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get item at %s", err, path)

    async def max_item(self):
        try:
            path = 'maxitem.json'
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get max item", err)

    async def top_stories(self):
        try:
            path = 'topstories.json'
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get top stories", err)

    async def ask_stories(self):
        try:
            path = 'askstories.json'
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get ask stories", err)

    async def job_stories(self):
        try:
            path = 'jobstories.json'
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get job stories", err)

    async def show_stories(self):
        try:
            path = 'showstories.json'
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get show stories", err)

    async def updates(self):
        try:
            path = 'updates.json'
            res = await self.get(path=path)
            return res
        except Exception as err:
            logger.error("%s: Unable to get updates", err)
