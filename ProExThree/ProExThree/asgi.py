"""
ASGI config for ProExThree project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter , URLRouter
import ExThree.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProExThree.settings')

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': URLRouter(
            ExThree.routing.URLPatterns
        ),
})
