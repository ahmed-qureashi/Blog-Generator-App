from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render , redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to home page after successful login
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('repeatPassword')

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)  # Automatically log in the user after signup
                return redirect('/')  # Redirect to login page after successful signup
            except:
                error_message = "Error creating user. Please try again."
                return render(request, 'signup.html', {'error_message': error_message})
            
        
        else:
            error_message = "Passwords do not match."
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')
def user_logout(request):
    pass   