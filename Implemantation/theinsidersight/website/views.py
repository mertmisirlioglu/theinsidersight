from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from website.forms import ExtendedUserCreationForm, ProfileForm


def home_view(request):
    return render(request, 'anasayfa.html')


def confessions_view(request):
    return render(request, 'itiraflar.html')


def answers_view(request):
    return render(request, 'cevaplar.html')


def leader_board_view(request):
    return render(request, 'siralama.html')


def discover_view(request):
    return render(request, 'kesfet.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    return render(request, 'register.html')


def signup(request):
    form = ExtendedUserCreationForm(request.POST or None)
    profile = ProfileForm(request.POST or None)
    if form.is_valid() and profile.is_valid():
        user = form.save()
        profile = profile.save(commit=False)
        profile.user = user
        profile.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'register.html',
                      {'form': ExtendedUserCreationForm, 'profile_form': ProfileForm})



