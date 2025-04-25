"""
URL configuration for zen_hn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("home.urls")),
    # no need to use the two together, other than for demonstration
    # users/ is used here instead of accounts/ to avoid conflict with allauth urls
    re_path("user(s)?/", include("user_account.urls")),
    re_path("account(s)?/", include("allauth.urls"))
]

# Serving media and static files in development
if settings.DEBUG:
    print(settings.DEBUG, 'DEBUG', type(settings.DEBUG))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# django-allauth provides a set of URLs for authentication, registration, password reset, etc.
# /accounts/login/ - account_login  - account/login.html
# /accounts/logout/ - account_logout - account/logout.html
# /accounts/signup/ - signup - account/signup.html
# /accounts/confirm-email/token - Confirm email - account/email_confirm.html
# and others
