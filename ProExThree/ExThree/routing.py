
from django.urls import path 
from ExThree.consumers import *


URLPatterns = [
    path('ws/user/<int:custom_user_id>/connect/<int:request_user_id>/' , ChatConsumerController.as_asgi()),
]