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
import notifications
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from website import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('itiraflar/', views.confessions_view, name='confessions'),
    path('cevaplar/', views.answer_page, name='answers'),
    path('sıralama/', views.leader_board_view, name='leader_board'),
    path('kesfet/', views.discover_view, name='discover'),
    path('giris/', views.login_view, name='login'),
    url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    path('cikis/', views.logout_view, name='logout'),
    path('kayit/', views.register_view, name='register'),
    path('profilim/', views.my_profile, name='my_profile'),
    path('itiraf-et/', views.send_post, name='make_confession'),
    path('cevapla/<int:post_id>/', views.reply_post, name='reply_post'),
    path('begen/api/<int:post_id>/', views.post_like_api_toggle.as_view(), name='like_api_post'),
    path('takip/api/<int:user_id>/', views.follow_api_toggle.as_view(), name='follow_api'),
    path('post/sil/<int:post_id>/', views.delete_post, name='post_delete'),
    path('sil/<int:user_id>/', views.delete_user, name='delete_user'),
    path('profil/<int:user_id>/', views.profile_view, name='profile'),
    path('soru-sor/', views.send_question, name='send_question'),
    path('sorular/', views.question_page, name='questions'),
    path('kullanicilar-admin/', views.admin_user, name='adminkullanicilar'),
    path('ask-itiraf/', views.ask_confessions_view, name='ask_itiraf'),
    path('dost-itiraf/', views.dost_confessions_view, name='dost_itiraf'),
    path('civciv-itiraf/', views.civciv_confessions_view, name='civciv_itiraf'),
    path('avci-itiraf/', views.avci_confessions_view, name='avci_itiraf'),
    path('diger-itiraf/', views.diger_confessions_view, name='diger_itiraf'),
    path('prof-itiraf/', views.prof_confessions_view, name='prof_itiraf'),
    path('user_followers/', views.user_followers, name='user_followers'),
    path('user-following/', views.user_following, name='user_following'),
    path('bildirimler/',views.notifications_mobile_view, name='not_mobile'),
    path('kullanici-ara',views.user_search_view,name='user_search')
]
