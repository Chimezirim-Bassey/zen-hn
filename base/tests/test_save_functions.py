from django.test import TestCase, SimpleTestCase
from environ import Env

from job.models import Job
from story.models import Story, Comment
from user_account.models import User
from poll.models import Poll, PollOption

from ..utils import save_user, save_item

env = Env()


class TestSaveFunctions(TestCase):
    # not using setUpTestData, setUp can also be used for creating test data
    # but setUpTestData is more efficient for large test data
    # this is not a class method
    def setUp(self):
        self.job = {
            "by": "jol",
            "id": 21,
            "score": 1,
            "time": 15444445652,
            "title": "title",
            "type": "job",
            "text": "job text",
        }

        self.story = {
            "by": "jrl",
            "id": 1,
            "score": 1,
            "time": 1344234545,
            "title": "title",
            "type": "story",
            "url": "https://example.com"
        }

        self.comment1 = {
            "by": "jc",
            "id": 11,
            "parent": 1,
            "text": "text",
            "time": 1446466266,
            "type": "comment"
        }

        self.comment2 = {
            "by": "jcc",
            "id": 12,
            "parent": 11,
            "text": "text",
            "time": 134543534,
            "type": "comment"
        }

        self.comment3 = {
            "by": "gop",
            "id": 12,
            "parent": 110,
            "text": "text",
            "time": 1345493534,
            "type": "comment"
        }

        self.user = {
            "id": "jl",
            "karma": 1,
            "about": "about me",
            "created": 134543534,
            "submitted": [1]
        }

        self.poll1 = {
            "by": "jp",
            "id": 41,
            "score": 1,
            "time": 15444445652,
            "title": "title",
            "type": "poll",
            "text": "poll text",
            "parts": [411, 412]
        }

        self.poll2 = {
            "by": "jpp",
            "id": 42,
            "score": 1,
            "time": 15444445652,
            "title": "poll2 title",
            "type": "poll",
            "text": "poll text",
            "parts": [421, 422]
        }

        self.poll_option1 = {
            "by": "jpo",
            "id": 411,
            "poll": 41,
            "text": "poll option text",
            "time": 15444445652,
            "type": "pollopt"
        }

        self.poll_option2 = {
            "by": "jpop",
            "id": 412,
            "poll": 41,
            "text": "poll option text",
            "time": 15444445652,
            "type": "pollopt"
        }

        self.poll_option3 = {
            "by": "jpop",
            "id": 421,
            "poll": 45,
            "text": "poll option text",
            "time": 15444445652,
            "type": "pollopt"
        }

    async def test_save_job(self):
        await save_item(item=self.job)
        job = await Job.objects.aget(item_id=self.job['id'])
        self.assertEqual(job.title, self.job['title'])
        poster = await User.objects.aget(username=self.job['by'])
        self.assertEqual(poster.username, self.job['by'])

    async def test_save_story(self):
        await save_item(item=self.story)
        story = await Story.objects.aget(item_id=self.story['id'])
        self.assertEqual(story.title, self.story['title'])
        poster = await User.objects.aget(username=self.story['by'])
        self.assertEqual(poster.username, self.story['by'])

    async def test_comment(self):
        await save_item(item=self.comment1)
        comment = await Comment.objects.aget(item_id=self.comment1['id'])
        self.assertEqual(comment.text, self.comment1['text'])
        poster = await User.objects.aget(username=self.comment1['by'])
        self.assertEqual(poster.username, self.comment1['by'])

        await save_item(item=self.comment2)
        comment2 = await Comment.objects.aget(item_id=self.comment2['id'])
        reply1 = await comment.replies.filter().afirst()
        self.assertEqual(reply1.item_id, self.comment2['id'])
        self.assertEqual(comment2.text, self.comment2['text'])
        poster2 = await User.objects.aget(username=self.comment2['by'])
        self.assertEqual(poster2.username, self.comment2['by'])

        await save_item(item=self.comment3)
        comment3 = await Comment.objects.aget(item_id=self.comment3['id'])
        self.assertEqual(comment3.text, self.comment3['text'])
        poster3 = await User.objects.aget(username=self.comment3['by'])
        self.assertEqual(poster3.username, self.comment3['by'])

    async def test_save_user(self):
        await save_user(user=self.user)
        user = await User.objects.aget(username=self.user['id'])
        self.assertEqual(user.karma, self.user['karma'])
        self.assertEqual(user.about, self.user['about'])

    async def test_save_poll(self):
        await save_item(item=self.poll1)
        poll = await Poll.objects.aget(item_id=self.poll1['id'])
        self.assertEqual(poll.title, self.poll1['title'])
        poster = await User.objects.aget(username=self.poll1['by'])
        self.assertEqual(poster.username, self.poll1['by'])

    # ToDo: test save poll option
