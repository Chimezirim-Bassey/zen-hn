from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HomeView, StoryDetailView, AskStoriesView, ShowStoriesView, JobsView, StoriesView, JobDetailView

urlpatterns = [
    path("", cache_page(60*5)(HomeView.as_view()), name="home"), # cache the home page for 5 minutes
    path("story/<int:pk>/", StoryDetailView.as_view(), name="story-detail"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("stories/", StoriesView.as_view(), name="stories"),
    path("ask_stories/", AskStoriesView.as_view(), name="ask-stories"),
    path("show_stories/", ShowStoriesView.as_view(), name="show-stories"),
    path("jobs/", JobsView.as_view(), name="jobs"),
    path("about/", HomeView.as_view(), name="about"),
    path("contact/", HomeView.as_view(), name="contact"),
]
