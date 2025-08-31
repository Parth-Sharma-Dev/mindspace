from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def dashboard(request):
    return render(request, "dashboard.html")

def forum(request):
    return render(request, "forum.html")

def resources(request):
    return render(request, "resources.html")

def emergency(request):
    return render(request, "emergency.html")
