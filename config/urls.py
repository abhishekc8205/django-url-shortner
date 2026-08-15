"""Top-level routes.

Keep the redirect route last: it deliberately accepts one short code at the
root, while API and admin routes need to take precedence.
"""
from django.contrib import admin
from django.urls import include, path

from shortener.views import home, redirect_to_original

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("shortener.urls")),
    path("<str:code>/", redirect_to_original, name="redirect-to-original"),
]
