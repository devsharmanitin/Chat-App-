from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
# Create your views here.




def UserRegisterController(request):
    if request.method == "POST":
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        ConfPassword = request.POST.get('ConfPass')
        print(Username , Password)
        
        if Password != ConfPassword:
            messages.warning(request , "Password Not Matching!!")
            return redirect('RegisterController')
        
        if User.objects.filter(username = Username).exists():
            messages.warning(request , 'Username Already Exists. Try Something New!! ')
            return redirect('RegisterController')
        
        try:
            NewUser = User.objects.create(
            username = Username ,
            )
            NewUser.set_password(Password)
            NewUser.save()
            messages.success(request , 'Sign Up Successful')
            return redirect('LoginController')
        except Exception as error:
            messages.warning(request , error)
            return redirect('RegiRegisterControllers')
    else:
        return render(request , 'Auth/Register.html')
    
    
def UserLoginController(request):
    if request.method == "POST":
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        
        GetUser = authenticate(username = Username , password = Password)
        if GetUser is not None:
            login(request  , GetUser)
            messages.success(request , 'Sign In Successful')
            return redirect('HomePageController')
        else:
            messages.warning(request , 'Credientials Not Matching!!')
            return redirect('LoginController')
    else:
        return render(request , 'Auth/Login.html')
    
def UserLogoutController(request):
    logout(request)
    return redirect('HomePageController')
    
def HomePageController(request):
    GetUsers = User.objects.exclude(is_superuser=True).exclude(username = request.user)
    Context = {
        'GetUsers':GetUsers
    }
    return render(request , 'Home/HomePage.html' , Context)



def ChatController(request):
    GetUsers = User.objects.exclude(is_superuser=True).exclude(username = request.user)
    Context = {
        'GetUsers':GetUsers
    }
    return render(request , 'Chat/Index.html' , Context)