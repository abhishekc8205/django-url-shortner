from django.urls import path

from . import views

urlpatterns = [
    path("links/", views.create_link, name="create-link"),
    path("links/<str:code>/", views.link_detail, name="link-detail"),
    path("links/<str:code>/analytics/", views.link_analytics, name="link-analytics"),
]
