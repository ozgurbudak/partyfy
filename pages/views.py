from django.shortcuts import render
from django.http import HttpResponse
import spotipy
import os
import sys
import spotipy.util as util

from playlist.models import *
# Create your views here.

def home_view(request, *args, **kwargs):
    
    return render(request, "home.html", { })


def signin_view(request):



    return render(request,"signin.html", {})


def playlist_view(request, *args, **kwargs):
    scope = 'user-library-read playlist-modify-public playlist-read-collaborative user-read-private'
    token = util.prompt_for_user_token('*******', scope=scope, client_id='*******', client_secret='********', redirect_uri='http://127.0.0.1:8000/signin/')
    
    
    
    sp = spotipy.Spotify(auth=token)
    
    request.session['token'] = token

    print("Hello, "+sp.me()["display_name"])

    playlists= sp. current_user_playlists()['items']
    playlist_info=[]
    for i in playlists:
       if i['name'].startswith('Partyfy -'):
            print(i['id'])
            if not i['images']:
                playlist_info.append([i['name'],  'https://1080motion.com/wp-content/uploads/2018/06/NoImageFound.jpg.png', i['id']])
            else:
                playlist_info.append([i['name'],  i['images'][0]['url'], i['id']])
            
    context={'playlist_info': playlist_info, 'sp':sp}
    
    return render(request, "playlist.html", context)



def create_playlist_view(request, *args, **kwargs):
    
    if request.method=='POST' and ('your_name' in request.POST.dict()):
        print(request.POST)
        token= request.session['token']
        sp = spotipy.Spotify(auth=token)
        playlists= sp. current_user_playlists()['items']
        flag=True
        
        for i in playlists:
            if i['name']=='Partyfy - '+request.POST['your_name']:
                flag=False

        if flag==True:
            sp.user_playlist_create( sp.me()['id'], 'Partyfy - '+request.POST['your_name'], public=True)
            Playlist.objects.create(owner=sp.me()['id'], title= 'Partyfy - '+request.POST['your_name'], lat=request.POST['latitude'],long=request.POST['longitude'])
            playlists= sp. current_user_playlists()['items']
            for i in playlists:
                #print(i['name'] ,i['id'])
                if i['name']=='Partyfy - '+request.POST['your_name']:
                    print(i['id'])
                    temp=Playlist.objects.get(title= 'Partyfy - '+request.POST['your_name'])
                    temp.playlist_id=i['id']
                    temp.save()
                
        return render(request, "createplaylist.html", {})
    else: 
        return render(request, "createplaylist.html", {})



def show_tracks_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    if 'playlist_id' in request.POST.dict().keys():
        playlist_id= request.POST['playlist_id']
        tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=playlist_id)
    else:
        for key in request.POST.dict().keys():
            if key.endswith('.x'):

                tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=key[:-2])
                playlist_id=key[:-2]
            
    
    
    track_list=[]

    for track in tracks['items']:
        track_list.append([track['track']['name'], track['track']['album']['artists'][0]['name'],track['track']['album']['name'], track['track']['id'] ])
        
  
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]
    active= playlist.is_active
    if sp.me()['id']== playlist.owner:
        is_owner=True
    else:
        is_owner=False

    
    request_list=[]
    for req_user in playlist.requests.all():
        request_list.append(req_user)


    context={'track_list_info':track_list, 'playlist_id':playlist_id,'request_list':request_list, 'is_owner':is_owner,'me':sp.me()['id'],'active':active}
    return render(request, "showtracks.html", context)

def check_auth_playlist_edit(user_id,playlist_id):
    playlist_all= Playlist.objects.all()

    for i in playlist_all:
        if i.playlist_id==playlist_id:
            o= i.owner
            list= i.allowed_users.all()

    if user_id==o:
        return True
    
    for user in list:
        if user_id==user.user_id:
            return True

    return False


def remove_track_view(request, *args, **kwargs):
    print(request.POST)
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    for key in request.POST.dict().keys():
        if request.POST.dict()[key] == 'delete':
            playlist_id= request.POST.dict()['playlist_id']
            if check_auth_playlist_edit(sp.me()['id'], playlist_id):
                sp.user_playlist_remove_all_occurrences_of_tracks(sp.me()['id'], playlist_id, [key])
            else:
                print("auth rejected")
    track_list=[]
    tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=playlist_id)
    for track in tracks['items']:
        track_list.append([track['track']['name'], track['track']['album']['artists'][0]['name'],track['track']['album']['name'], track['track']['id'] ])
        
  
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]
    active= playlist.is_active
    if sp.me()['id']== playlist.owner:
        is_owner=True
    else:
        is_owner=False

    
    request_list=[]
    for req_user in playlist.requests.all():
        request_list.append(req_user)


    context={'track_list_info':track_list, 'playlist_id':playlist_id,'request_list':request_list, 'is_owner':is_owner,'me':sp.me()['id'],'active':active}
    return render(request, "showtracks.html", context)




def search_track_view(request, *args, **kwargs):
    print(request.POST)
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)

    query= request.POST.dict()['search']
    results= sp.search( query, limit=10, offset=0, type='track', market=None)
    # print(results['tracks']['items'][0].keys())
    # print(results['tracks']['items'][0]['album']['name'])
    # print(results['tracks']['items'][0]['artists'][0]['name'])
    # print(results['tracks']['items'][0]['name'])
    # print(results['tracks']['items'][0]['id'])

    track_list=[]
    for track in results['tracks']['items']:
        track_list.append([track['name'], track['artists'][0]['name'] ,track['album']['name'], track['id'] ])

    playlist_id= request.POST.dict()['playlist_id']
    context={'track_list_info':track_list, 'playlist_id':playlist_id, 'query':query}   
    return render(request, "add.html", context)


def add_track_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    playlist_id= request.POST.dict()['playlist_id']
    track_id= request.POST.dict()['track_id']

    if check_auth_playlist_edit(sp.me()['id'], playlist_id):
        sp.user_playlist_add_tracks(sp.me()['id'], playlist_id, [track_id],position=None)
    else:
        print("auth rejected")


    
    print(request.POST)

    track_list=[]
    tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=playlist_id)
    for track in tracks['items']:
        track_list.append([track['track']['name'], track['track']['album']['artists'][0]['name'],track['track']['album']['name'], track['track']['id'] ])
        
  
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]
    active=playlist.is_active
    if sp.me()['id']== playlist.owner:
        is_owner=True
    else:
        is_owner=False

    
    request_list=[]
    for req_user in playlist.requests.all():
        request_list.append(req_user)


    context={'track_list_info':track_list, 'playlist_id':playlist_id,'request_list':request_list, 'is_owner':is_owner,'me':sp.me()['id'],'active':active}
    return render(request, "showtracks.html", context)

def back_to_playlist_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    track_list=[]
    playlist_id= request.POST.dict()['playlist_id']
    tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=playlist_id)
    for track in tracks['items']:
        track_list.append([track['track']['name'], track['track']['album']['artists'][0]['name'],track['track']['album']['name'], track['track']['id'] ])

    context={'track_list_info':track_list, 'playlist_id':playlist_id}   
    return render(request, "showtracks.html", context)




def welcome_view(request, *args, **kwargs):
    scope = 'user-library-read playlist-modify-public playlist-read-collaborative user-read-private'
    token = util.prompt_for_user_token('******', scope=scope, client_id='*******', client_secret='*****', redirect_uri='http://127.0.0.1:8000/signin/')
    
    sp = spotipy.Spotify(auth=token)
    temp_id= sp.me()['id']
    if (len(Suser.objects.filter(user_id= temp_id))== 0):
        Suser.objects.create(user_id=temp_id)
    context={'sp':sp}
    return render(request, "welcome.html", context)


def map_view(request, *args, **kwargs):
    playlist_list=Playlist.objects.all().filter(is_active=True)
    id_list=[]
    for i in playlist_list:
        id_list.append(i.playlist_id)
    context={'playlist_list' : playlist_list, 'id_list': id_list}

    return render(request, "map.html", context)


def request_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    print(request.POST)
    playlist= Playlist.objects.all().filter(playlist_id=request.POST['playlist_id'])[0]
    user_objects=playlist.requests
    if request.POST['type']=='no':
        user_objects.remove(user_objects.filter(user_id=request.POST['user_id'])[0])
    else:
        playlist.allowed_users.add(user_objects.all().filter(user_id=request.POST['user_id'])[0])
        playlist.save()
        user_objects.remove(user_objects.filter(user_id=request.POST['user_id'])[0])
     
    
    playlist_id= request.POST['playlist_id']
    

    track_list=[]
    tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=playlist_id)
    for track in tracks['items']:
        track_list.append([track['track']['name'], track['track']['album']['artists'][0]['name'],track['track']['album']['name'], track['track']['id'] ])
        
  
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]
    active= playlist.is_active
    if sp.me()['id']== playlist.owner:
        is_owner=True
    else:
        is_owner=False

    
    request_list=[]
    for req_user in playlist.requests.all():
        request_list.append(req_user)


    context={'track_list_info':track_list, 'playlist_id':playlist_id,'request_list':request_list, 'is_owner':is_owner,'me':sp.me()['id'],'active':active}
    return render(request, "showtracks.html", context)


def request_access_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    print(request.POST)


    user_id= request.POST['user_id']
    playlist_id= request.POST['playlist_id']
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]
    userSet= playlist.requests.all().filter(user_id=user_id)
    userSet2= playlist.allowed_users.all().filter(user_id=user_id)
    user= Suser.objects.all().filter(user_id=user_id)[0]
    if len(userSet)==0 and len(userSet2)==0:
        playlist.requests.add(user)
        playlist.save()
        return HttpResponse('<h1>request sent</h1>')
    else:
        return HttpResponse('<h1>request allready sent</h1>')
        

def delete_playlist_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    playlist_id= request.POST['playlist_id']

    sp.user_playlist_unfollow( sp.me()['id'], playlist_id)
    Playlist.objects.all().filter(playlist_id=playlist_id).delete()
    return playlist_view(request)

def toggle_activation_view(request, *args, **kwargs):
    token= request.session['token']
    sp = spotipy.Spotify(auth=token)
    playlist_id= request.POST['playlist_id']
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]

    if playlist.is_active:
        playlist.is_active=False
        playlist.save()
    else:
        playlist.is_active=True
        playlist.save()
    track_list=[]
    tracks=sp.user_playlist_tracks(sp.me()['id'], playlist_id=playlist_id)
    for track in tracks['items']:
        track_list.append([track['track']['name'], track['track']['album']['artists'][0]['name'],track['track']['album']['name'], track['track']['id'] ])
        
  
    playlist= Playlist.objects.all().filter(playlist_id=playlist_id)[0]
    active=playlist.is_active
    if sp.me()['id']== playlist.owner:
        is_owner=True
    else:
        is_owner=False

    
    request_list=[]
    for req_user in playlist.requests.all():
        request_list.append(req_user)


    context={'track_list_info':track_list, 'playlist_id':playlist_id,'request_list':request_list, 'is_owner':is_owner,'me':sp.me()['id'],'active':active}
    return render(request, "showtracks.html", context)