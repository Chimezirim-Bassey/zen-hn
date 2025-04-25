from django.test import TestCase
from django.db.models import Q
from django.contrib.auth import get_user_model

from job.models import Job
from story.models import Story


class HomePageTests(TestCase):
    """
    Test suite for the home page views.
    """

    # uses setUpTestData to create test data once for all tests, ideal for TestCase
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

    def test_homepage(self):
        """
        Test that the home page contains the text 'ZenHN'.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ZenHN")

    def test_homepage_template(self):
        """
        Test that the home page uses the correct template.
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home/home.html")

    def test_homepage_context(self):
        """
        Test that the home page context data contains the expected keys.
        """
        response = self.client.get("/")
        self.assertIn("slide_image", response.context)
        self.assertIn("slide_items", response.context)
        self.assertIn("post_landscape", response.context)
        self.assertIn("person", response.context)
        self.assertIn("ask_stories", response.context)
        self.assertIn("show_stories", response.context)
        self.assertIn("stories", response.context)

    def test_homepage_querysets(self):
        """
        Test that the home page querysets return the expected data.
        """
        response = self.client.get("/")
        jobs = Job.objects.all()[5:]
        asks = Story.objects.filter(title__startswith="Ask HN")[5:]
        shows = Story.objects.filter(title__startswith="Show HN")[5:]
        stories = Story.objects.filter(~Q(title__startswith="Ask HN") & ~Q(title__startswith="Show HN"))[5:]
        self.assertQuerySetEqual(response.context["ask_stories"], asks)
        self.assertQuerySetEqual(response.context["show_stories"], shows)
        self.assertQuerySetEqual(response.context["stories"], stories)
        self.assertQuerySetEqual(response.context["jobs"], jobs)
