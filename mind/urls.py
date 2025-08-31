from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forum/", views.forum, name="forum"),
    path("resources/", views.resources, name="resources"),
    path("emergency/", views.emergency, name="emergency"),
]
