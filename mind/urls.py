from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.apphome, name="apphome"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forum/", views.forum, name="forum"),
    path("resources/", views.resources, name="resources"),
    path("emergency/", views.emergency, name="emergency"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
]
