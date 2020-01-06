"""theinsidersight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('itiraflar/', views.confessions_view, name='confessions'),
    path('cevaplar/', views.answer_page, name='answers'),
    path('sıralama/', views.leader_board_view, name='leader_board'),
    path('kesfet/', views.discover_view, name='discover'),
    path('giris/', views.login_view, name='login'),
    path('cikis/', views.logout_view, name='logout'),
    path('kayit/', views.signup, name='register'),
    path('profilim/', views.my_profile, name='my_profile'),
    path('itiraf-et/', views.send_post, name='make_confession'),
    path('cevapla/<int:post_id>/', views.reply_post, name='reply_post'),
    path('soru-sor/', views.send_question, name='send_question'),
    path('sorular/', views.question_page, name='questions'),
]
