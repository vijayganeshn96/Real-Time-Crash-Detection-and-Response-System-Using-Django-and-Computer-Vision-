from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.shortcuts import render, HttpResponse
from django.http.response import StreamingHttpResponse
from accidentdetectionapp.stream import streaming
from googleplaces import GooglePlaces, types, lang
import requests
import json
import vonage
import time
from .models import *
from django.shortcuts import redirect
import pusher

from tensorflow import keras

model = keras.models.load_model(r'D:\1. Accident Detection AI Methods Using Django frame work\deep learning\model_weights.h5')  # Update with the correct file path
global hospital_name
hospital_name ="Vijay Hospital"

def send_response():
    pusher_client = pusher.Pusher(
    app_id='1328110',
    key='4da6311b184ace45d1dc',
    secret='469709e6b17fadfab16f',
    cluster='ap2',
    ssl=True
    )
  
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Request Accepted'})
    return

def home(request):
    return render(request,'index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def webcam_feed(request):
    # print("W1")
    return StreamingHttpResponse(gen(streaming()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def maps(request):
    API_KEY = 'AIzaSyBj-F7jxbhMYXYn8WuLwZpnEInBX6S4Dew'
    google_places = GooglePlaces(API_KEY)


    query_result = google_places.nearby_search(
            # lat_lng ={'lat': 46.1667, 'lng': -1.15},
            lat_lng ={'lat': 28.4089, 'lng': 77.3178},
            radius = 5000,
  
            types =[types.TYPE_HOSPITAL])

    if query_result.has_attributions:
        print (query_result.html_attributions)


    # Iterate over the search results
    for place in query_result.places:
        # print(type(place))
        # place.get_details()
        print (place.name)
        print("Latitude", place.geo_location['lat'])
        print("Longitude", place.geo_location['lng'])
        print()
    return render(request,'index.html')
    
def hospital(request):
    return render(request,'hospital.html')

def test(request):
    global hospital_name
    notifications = Notifications.objects.all().order_by('-n_id') 
    # text = ref.child('notify').child('Notification').get()
    # accepted = ref.child('notify').child('accepted').get()
    # projectname = database.child('Data').child('Projectname').get().val()
    context = {
        'notifications': notifications,
        'hospital_name':hospital_name,
    }
    return render(request,"index2.html",context)

def accept(request,id):
    notification = Notifications.objects.filter(n_id=id).update(accepted = 1)
    send_response()
    return redirect('test')

def register(request):
    global hospital_name
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        latitude=request.POST.get('latitude')
        longitude=request.POST.get('longitude')
        print(name,email,latitude,longitude)
        hospital=Hospital(name=name,email=email,h_lattitude=latitude,h_longitude=longitude)
        hospital.save()
        hospital_name=name
        return redirect('test')
    return render(request, 'register.html')