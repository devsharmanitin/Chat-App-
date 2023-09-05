from django.urls import path , include
from ExThree import views

urlpatterns = [
    path('' , views.HomePageController , name = 'HomePageController'),
    path('user/sign/in' , views.UserLoginController , name = 'LoginController'),
    path('user/sign/up' , views.UserRegisterController , name = 'RegisterController'),
    path('user/logout/' , views.UserLogoutController , name='LogoutController'),
    
    path('user/ChatController' , views.ChatController , name='ChatController'),
    
]
