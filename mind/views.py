from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .forms import SignUpForm, LoginForm
from .models import ForumPost, ForumComment, Room, Message
from .serializers import ForumPostSerializer, ForumCommentSerializer, RoomSerializer, MessageSerializer
from .utils.pseudonyms import pseudonym_for, anon_id

@login_required(login_url='')
def apphome(request):
    return render(request, "apphome.html")


def index(request):
    return render(request, "index.html")


@login_required(login_url='')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url='')
def forum(request):
    user_anon_id = anon_id(request.user.id) if request.user.is_authenticated else None
    user_pseudonym = pseudonym_for(request.user.id, "forum") if request.user.is_authenticated else "Guest"

    if request.method == "POST":
        title = request.POST.get("post_title")
        content = request.POST.get("post_content")
        if title and content:
            ForumPost.objects.create(
                title=title,
                content=content,
                pseudonym=user_pseudonym,
                anon_id=user_anon_id
            )
        return redirect("forum")

    posts = ForumPost.objects.prefetch_related("comments__replies").all()
    return render(request, "forum.html", {
        "posts": posts,
        "user_pseudonym": user_pseudonym,
    })


def add_comment(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    user_anon_id = anon_id(request.user.id) if request.user.is_authenticated else None
    user_pseudonym = pseudonym_for(request.user.id, "forum") if request.user.is_authenticated else "Guest"

    if request.method == "POST":
        text = request.POST.get("comment_text")
        if text:
            ForumComment.objects.create(
                post=post,
                pseudonym=user_pseudonym,
                anon_id=user_anon_id,
                text=text
            )
    return redirect("forum")


@login_required(login_url='')
def your_posts(request):
    user_anon = anon_id(request.user.id)
    user_pseudonym = pseudonym_for(request.user.id, "forum")

    user_posts = ForumPost.objects.filter(anon_id=user_anon)
    user_comments = ForumComment.objects.filter(anon_id=user_anon)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "edit_post":
            post = get_object_or_404(ForumPost, id=request.POST.get("edit_post_id"), anon_id=user_anon)
            post.title = request.POST.get("post_title", post.title)
            post.content = request.POST.get("post_content", post.content)
            post.save()

        elif action == "delete_post":
            post = get_object_or_404(ForumPost, id=request.POST.get("delete_post_id"), anon_id=user_anon)
            post.delete()

        elif action == "edit_comment":
            comment = get_object_or_404(ForumComment, id=request.POST.get("edit_comment_id"), anon_id=user_anon)
            comment.text = request.POST.get("comment_text", comment.text)
            comment.save()

        elif action == "delete_comment":
            comment = get_object_or_404(ForumComment, id=request.POST.get("delete_comment_id"), anon_id=user_anon)
            comment.delete()

        return redirect("your-posts")

    return render(request, "your_posts.html", {
        "user_pseudonym": user_pseudonym,
        "user_posts": user_posts,
        "user_comments": user_comments,
    })


@login_required(login_url='')
def resources(request):
    rooms = Room.objects.all()
    return render(request, "resources.html", {"rooms": rooms})

@login_required(login_url='')
def chat_room(request, room_id):
    user_anon_id = anon_id(request.user.id) if request.user.is_authenticated else None
    user_pseudonym = pseudonym_for(request.user.id, "chat") if request.user.is_authenticated else "Guest"
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by("created_at")

    if request.method == "POST":
        text = request.POST.get("message")
        if text.strip():
            Message.objects.create(
                room=room,
                pseudonym=user_pseudonym,
                anon_id=user_anon_id,
                text=text
            )
        return redirect("chat_room", room_id=room.id)

    return render(request, "chat.html", {
        "room": room,
        "messages": messages,
        "pseudonym": user_pseudonym,
        "anon_id": user_anon_id,
    })

@login_required(login_url='')
def fetch_messages(request, room_id):
    """Return all messages for a given room in JSON format (for AJAX polling)."""
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.order_by("created_at")

    data = []
    for msg in messages:
        data.append({
            "pseudonym": msg.pseudonym,  
            "text": msg.text,
            "created_at": msg.created_at.strftime("%H:%M"),
            "own": msg.anon_id == anon_id(request.user.id),  
        })

    return JsonResponse({"messages": data})



@login_required(login_url='')
def emergency(request):
    return render(request, "emergency.html")


def signup(request):
    """
    Handles user registration.
    On GET, displays a blank registration form.
    On POST, validates the form data, creates a new user, logs them in,
    and redirects them to the dashboard.
    """
    if request.method == "POST":
        # Create a form instance with the submitted data
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the form, which creates a new user object
            user = form.save()
            # Log the new user in automatically
            login(request, user)
            # Redirect to the main dashboard after successful signup
            return redirect("apphome")
    else:
        # If it's a GET request, create a blank instance of the form
        form = SignUpForm()

    # Render the signup page, passing the form instance to the template
    return render(request, "signup.html", {"form": form})


def login_view(request):
    """
    Handles user authentication. If a user is already logged in, they are
    redirected to the dashboard. On POST, it validates credentials and
    logs the user in.
    """
    # If user is already authenticated, redirect them away from the login page
    if request.user.is_authenticated:
        return redirect("apphome")

    if request.method == "POST":
        # AuthenticationForm requires the request object to be passed in
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # If the form is valid, get the authenticated user
            user = form.get_user()
            # Log the user in
            login(request, user)
            # Redirect to the dashboard
            return redirect("apphome")
    else:
        # For a GET request, create a blank instance of the form
        form = LoginForm()

    # If the form was invalid, it will be re-rendered with errors
    return render(request, "login.html", {"form": form})


def logout_view(request):
    """
    Logs the current user out of the application.
    """
    logout(request)
    # Redirect to the main landing page after logging out.
    # Make sure you have a URL named 'index'.
    return redirect("index")


class ForumPostListCreateView(generics.ListCreateAPIView):
    """List posts or create a new one"""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ForumPostDetailView(generics.RetrieveAPIView):
    """Get a single post + its comments"""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]

class ForumCommentCreateView(generics.CreateAPIView):
    """Add a comment to a post"""
    serializer_class = ForumCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        serializer.save(user=self.request.user, post_id=post_id)


class RoomListView(generics.ListAPIView):
    """List all rooms (pre-generated)"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageListView(generics.ListAPIView):
    """Fetch recent messages for a room"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return Message.objects.filter(room_id=room_id).order_by("-created_at")[:50]  # last 50 messages

class MessageCreateView(generics.CreateAPIView):
    """Send a new message to a room"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room_id = self.kwargs["room_id"]
        serializer.save(user=self.request.user, room_id=room_id)