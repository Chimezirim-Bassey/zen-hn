from django.urls import path, include, re_path

from .views import UserCreateView, UserDetailView, UserUpdateView, LogoutView

# the urls can be overridden to provide custom context and redirection
# templates for contrib.auth is in registration
urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("django.contrib.auth.urls")), # authentication urls for in built auth app
    path("profile/", UserDetailView.as_view(), name="user_profile"),
    path("profile/<slug:slug>/", UserDetailView.as_view(), name="user_profile"),
    path("update/", UserUpdateView.as_view(), name="user_update"),
    path("signup/", UserCreateView.as_view(), name="signup")
]
