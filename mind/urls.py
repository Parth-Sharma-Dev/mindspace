from django.urls import path
from . import views

urlpatterns = [
    # ---------------- Template Views (render HTML) ----------------
    path("", views.index, name="index"),
    path("home/", views.apphome, name="apphome"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forum/", views.forum, name="forum"),          # forum homepage template
    path("forum/posts/<uuid:post_id>/comment/", views.add_comment, name="add-comment"),
    path("forum/your-posts/", views.your_posts, name="your-posts"),
    path("resources/", views.resources, name="resources"),  # <-- your rooms page
    path("emergency/", views.emergency, name="emergency"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ---------------- API Views (return JSON) ----------------
    # Rooms
    path("api/rooms/", views.RoomListView.as_view(), name="room-list"),
    path("api/rooms/<uuid:room_id>/messages/", views.MessageListView.as_view(), name="message-list"),
    path("api/rooms/<uuid:room_id>/messages/new/", views.MessageCreateView.as_view(), name="message-create"),

    # Forum
    path("api/forum/posts/", views.ForumPostListCreateView.as_view(), name="post-list-create"),
    path("api/forum/posts/<uuid:pk>/", views.ForumPostDetailView.as_view(), name="post-detail"),
    path("api/forum/posts/<uuid:post_id>/comments/new/", views.ForumCommentCreateView.as_view(), name="comment-create"),
]
