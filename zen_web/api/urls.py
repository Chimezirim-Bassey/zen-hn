from django.views.generic import RedirectView
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import SimpleRouter

from .views import JobViewSet, PollViewSet, StoryViewSet, UserViewSet, AskStoryList, ShowStoryList

router = SimpleRouter()

# regex paths not playing well with Spectacular
# router.register(r'job(s)?', JobViewSet, basename='job')
# router.register('poll(s)?', PollViewSet, basename='poll')
# router.register(r'stor(y|ies|ys){1}', StoryViewSet, basename='story')
# router.register(r'user(s)?', UserViewSet, basename='user')

router.register('jobs', JobViewSet, basename="jobs")
router.register('polls', PollViewSet, basename="polls")
router.register('stories', StoryViewSet, basename="stories")
router.register('users', UserViewSet, basename="users")

app_name = "api"
urlpatterns = [
    re_path("", include(router.urls)), # add for jobsets, pollsets, storysets, usersets
    path("askstories/", AskStoryList.as_view(), name="ask-stories"),
    path("showstories/", ShowStoryList.as_view(), name="show-stories"),
    path("api-auth/", include("rest_framework.urls")), # add for authentication with browsable API

    # dj-rest-auth not integrating well with django-allauth
    # path("dj-rest-auth/", include("dj_rest_auth.urls")), # add for authentication with jwt
    # path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")), # add for registration with jwt

    # add for dynamic schema generation
    # schema file is automatically generated at /api/schema and downloaded as schema.yml
    path("schema/download", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
    path("schema/swagger/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger"),

    # add for redirecting to docs
    re_path(r"^$", RedirectView.as_view(pattern_name="api:redoc", permanent=False)), # redirect to swagger
]
