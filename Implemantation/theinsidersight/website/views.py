from django.shortcuts import render


def home_view(request):
    return render(request, 'anasayfa.html')


def confessions_view(request):
    return render(request, 'itiraflar.html')


def answers_view(request):
    return render(request, 'cevaplar.html')


def leader_board_view(request):
    return render(request, 'siralama.html')


def discover_view(request):
    return render(request,'kesfet.html')
