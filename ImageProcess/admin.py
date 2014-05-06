'''
Created on Apr 12, 2014

@author: yulu
'''

from django.contrib import admin
from models import POI, Object, Image

class POIAdmin(admin.ModelAdmin):
    search_fields = ["poi_name"]
    list_display = ["poi_name"]
    
class ObjectAdmin(admin.ModelAdmin):
    search_fields = ["object_name"]
    list_display = ["object_name", "img_path"]
    fields =('object_name', 'img_path', 'annotation')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
    
class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "object_of_interest"]
    fields = ('title', 'image_path',
              'azimuth', 'pitch', 'roll', 'longitude', 'latitude')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        obj.match()

        
class ContentAdmin(admin.ModelAdmin):
    list_display = ["object_of_interest", "description", "url", "model_path"]

admin.site.register(POI, POIAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Image, ImageAdmin)
