'''
Created on Apr 12, 2014

@author: yulu
'''

from django.contrib import admin
from models import POI, Object, Image, Content

class POIAdmin(admin.ModelAdmin):
    search_fields = ["location_name"]
    list_display = ["location_name"]
    
class ObjectAdmin(admin.ModelAdmin):
    search_fields = ["object_name"]
    list_display = ["object_name"]
    
class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title"]
    fields = ('object_of_interest', 'title', 'image_path')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        
class ContentAdmin(admin.ModelAdmin):
    list_display = ["object_of_interest", "description", "url", "model_path"]

admin.site.register(POI, POIAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Content, ContentAdmin)
