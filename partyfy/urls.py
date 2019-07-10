"""trydjango URL Configuration

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
from pages import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('signin/', views.signin_view, name='signin'),
    path('playlist/', views.playlist_view, name='playlist'),
    path('createplaylist/', views.create_playlist_view, name='createplaylist'),
    path('showtracks/', views.show_tracks_view, name='showtracks'),
    path('removed/', views.remove_track_view, name='removetrack'),
    path('search/', views.search_track_view, name='searchtrack'),
    path('add/', views.add_track_view, name='addtrack'),
     path('backtoplaylist/', views.back_to_playlist_view, name='backtoplaylist'),
     path('welcome/', views.welcome_view, name='welcome'),
     path('map/', views.map_view, name='map'),
     path('request/', views.request_view, name='request'),
     path('request_access/', views.request_access_view, name='request_access'),
     path('delete_playlist/', views.delete_playlist_view, name='delete_playlist'),
     path('toggle_activation/', views.toggle_activation_view, name='toggle_activation')
     

]
