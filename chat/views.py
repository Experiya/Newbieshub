from django.shortcuts import render

def index(request):

    return render(request, 'chat/index.html', {})

def room(request,who ,room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'who':who,
        'username':who
    })