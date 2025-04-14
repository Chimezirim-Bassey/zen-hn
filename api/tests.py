import json

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from job.models import Job
from story.models import Story


class APITest(APITestCase):
    """
    Base test case for API tests.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the test case with necessary data.
        """
        user = get_user_model().objects.create(username="testuser", email="testuser@zenhn.com")
        for i in range(10):
            Job.objects.create(title=f"Test Job{i}", by=user, item_id=i, type='job')
        for i in range(10):
            Story.objects.create(title=f"Test Story{i}", by=user, item_id=i, type='story')
        for i in range(10, 20):
            Story.objects.create(title=f"Ask HN: Ask Test Story{i}", by=user, item_id=i, type='story')
        for i in range(20, 30):
            Story.objects.create(title=f"Show HN: Show Test Story{i}", by=user, item_id=i, type='story')

    def test_ask_stories(self):
        """
        Test that the ask stories endpoint returns the expected data.
        """
        response = self.client.get(reverse("api:ask-stories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        res = json.loads(response.content)
        self.assertEqual(len(res), 10)

    def test_jobs(self):
        """
        Test that the ask jobs endpoint returns the expected data.
        """
        response = self.client.get(reverse("api:jobs-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        res = json.loads(response.content)
        self.assertEqual(len(res), 10)

    def test_show_stories(self):
        """
        Test that the show stories endpoint returns the expected data.
        """
        response = self.client.get(reverse("api:show-stories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        res = json.loads(response.content)
        self.assertEqual(len(res), 10)

    def test_stories(self):
        """
        Test that the stories endpoint returns the expected data.
        """
        response = self.client.get(reverse("api:stories-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        res = json.loads(response.content)
        self.assertEqual(len(res), 30)
