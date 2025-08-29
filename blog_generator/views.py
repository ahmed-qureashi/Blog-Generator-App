import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data.get('link')
            return JsonResponse({'content': yt_link})

        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
        #title

        title = yt_title(yt_link)
        #transcript
        #summary of open ai
        #save to database
        #return blog article as response
            

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)


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
    logout(request) 
    return redirect('/')  # Redirect to home page after logout