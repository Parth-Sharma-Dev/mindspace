# /mindspace/asgi.py

import os
from django.core.asgi import get_asgi_application

# This line MUST come first to tell Django which settings file to use.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mindspace.settings")

# This line runs the actual Django setup.
django_asgi_app = get_asgi_application()

# --- IMPORTANT ---
# Now that Django is set up, we can safely import our app's routing.
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import mind.routing


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mind.routing.websocket_urlpatterns
        )
    ),
})