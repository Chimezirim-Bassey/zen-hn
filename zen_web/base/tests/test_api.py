from django.test import SimpleTestCase, TestCase

from ..utils import API

class TestApi(SimpleTestCase):
    def setUp(self):
        self.api = API()

    async def test_max_item(self):
        res = await self.api.max_item()
        self.assertIsInstance(res, int)
        self.assertGreater(res, 0)

    async def test_top_stories(self):
        res = await self.api.top_stories()
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)

    async def test_ask_stories(self):
        res = await self.api.ask_stories()
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)

    async def test_job_stories(self):
        res = await self.api.job_stories()
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)

    async def test_show_stories(self):
        res = await self.api.show_stories()
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)

    async def test_updates(self):
        res = await self.api.updates()
        self.assertIsInstance(res, dict)
        self.assertIn('items', res)
        self.assertIn('profiles', res)
        self.assertIsInstance(res['items'], list)
        self.assertIsInstance(res['profiles'], list)

    async def test_get_by_id(self):
        item_id = 42390647
        res = await self.api.get_by_id(item_id=item_id)
        self.assertIsInstance(res, dict)
        self.assertEqual(res['id'], item_id)

    async def test_get_user(self):
        user_id = 'jl'
        res = await self.api.get_user(user_id=user_id)
        self.assertIsInstance(res, dict)
        self.assertEqual(res['id'], user_id)
