# Create your views here.
from models import POI, Image, Object
from django.http import HttpResponse
from django.http import Http404
from forms import UploadFileForm
from PhoneARtDemo.utils import *
from django.views.decorators.csrf import csrf_exempt

"""
upload_image_for_match: upload information from client to server
    -title
    -longitude, latitude, azimuth, pitch, roll
    -image
"""
@csrf_exempt
def upload_image_for_match(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #title
            tit = request.REQUEST.get("title", None)
            
            #Sensor
            lon = request.REQUEST.get('longitude', None)
            lat = request.REQUEST.get('latitude', None)
            azi = request.REQUEST.get("azimuth", None)
            pit = request.REQUEST.get("pitch", None)
            rol = request.REQUEST.get("roll", None)
            
            #Image
            image = Image(image_path = request.FILES['file'],
                          azimuth = azi,
                          pitch = pit,
                          roll = rol,
                          longitude = lon,
                          latitude = lat,
                          title = tit)
            image.save()
            
            '''match the image against the database'''
            name = image.match()
            obj = Object.objects.get(object_name = name)
            
            #wrap object_url and object_name as json and return
            return responseJson({'object_url':obj.img_path.name, 'object':obj.object_name})
            
        else:
            return fail()
    else:
        return fail()

"""
request_image_url: request the static url of the reference image
    - object_name
"""
@csrf_exempt
def request_image_url(request):
    name = request.REQUEST.get('object_name', None)
    if name is None:
        raise IncompleteParamException()
    # if object name is not None
    obj = Object.objects.get(object_name = name)
    if object is None:
        return Http404
    
    # return the image path
    url = obj.img_path.name
    return responseJson({'object_url:':url})
    
     
    