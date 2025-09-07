from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm


@login_required
def apphome(request):
    return render(request, "apphome.html")


def index(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def forum(request):
    return render(request, "forum.html")


@login_required
def resources(request):
    return render(request, "resources.html")


@login_required
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
