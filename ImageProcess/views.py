# Create your views here.
from models import POI, Image, Object
from django.http import HttpResponse
from django.http import Http404
from forms import UploadFileForm
from PhoneARtDemo.utils import *
from django.views.decorators.csrf import csrf_exempt

"""
api function: upload information from client to server
    -POI
    -Obj-of-Int
    -Image file (triger background PR automatically after successful upload)
"""
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            #POI
            lon = request.REQUEST.get('longitude', 0.0)
            lat = request.REQUEST.get('latitude', 0.0)
            loc_name = request.REQUEST.get('location_name', 'default')
            poi = POI(longtitude=lon, latitude=lat, location_name=loc_name)
            poi.save()
            
            #Object
            obj_name = request.REQUEST.get('object_name', 'default')
            obj = Object(poi = poi, object_name = obj_name)
            obj.save()
            
            #Image
            image = Image(object_of_interest = obj, image_path = request.FILES['file'])
            image.save()
            
            '''match the image against the database'''
            idx, class_name = image.match()
            
            #wrap idx and class_name as json and return
            return responseJson({'class_name':class_name})
            
        else:
            return fail()
    else:
        return fail()