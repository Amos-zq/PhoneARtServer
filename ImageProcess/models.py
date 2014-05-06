import os.path
from django.db import models
from PhoneARtDemo.settings import MEDIA_ROOT,MEDIA_DATABASE
from time import gmtime, strftime

import sys
sys.path.append(os.path.abspath('../PatternRecognition'))
from MainSource.Classifier import Classifier #import PatternRecognition package


# name the uploaded image with current time
def content_file_name(instance, filename):
    name = "img_" + strftime("%Y%m%d%H%M%S", gmtime())+".png"
    return os.path.join('images/', name)

def database_file_name(instance, filename):
    name = "img_" + strftime("%Y%m%d%H%M%S", gmtime())+".png"
    return os.path.join(MEDIA_DATABASE, name)

"""
Object Model: the primitive for image-based localization and tracking
    - object_name: PRIMARY KEY
    - referece_img: path to the reference image
    - annotation: optional descriptions for object
    **  Might introduce descriptors or some other vision primitives 
        for recognition and tracking
"""
class Object(models.Model):
    object_name = models.CharField(max_length=30, primary_key=True)
    img_path = models.FileField(upload_to=database_file_name) 
    annotation = models.CharField(max_length=100, blank=True, null=True)
    
    '''save image'''
    def save(self, *args, **kwargs):
        super(Object, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.object_name

"""
POI Model:  the position-of-interest. Different POI can be point to the save 
            object, or not point to any. 
    - longitude: longitude of the POI
    - latitude: latitude of the POI
    - location_name: name of the POI
    - object: point to an object
    - annotation: optional descriptions for the POI
"""
class POI(models.Model):
    longtitude = models.FloatField()
    latitude = models.FloatField()
    poi_name = models.CharField(max_length=60)
    
    object = models.ForeignKey(Object, blank=True, null=True)
    annotation = models.CharField(max_length=100, blank=True, null=True)
    
    def __unicode__(self):
        return self.poi_name
    
"""
Image Model: all the uploaded images from user
    - title: optional description for the image
    - object: point to an object
    - image_path: path to the image
    
    - azimuth
    - pitch
    - roll
    - longitude
    - latitude
    
    - match():  match the image against the database and return the 
                matched object name
"""    
class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    object_of_interest = models.ForeignKey(Object, null=True, blank=True)
    image_path = models.FileField(upload_to=content_file_name)
    
    azimuth = models.FloatField(blank=True, null=True)
    pitch = models.FloatField(blank=True, null=True)
    roll = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    
    '''save image'''
    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        
    def match(self):
        '''match the image against the database and return the matched class index'''
        img_dir = os.path.join(MEDIA_ROOT, self.image_path.name)
        idx, obj = Classifier(img_dir, 1)
        
        '''if matched to any image in the database, save the object'''
        if Object.objects.filter(object_name = obj).count() > 0:
            self.object_of_interest = Object.objects.get(object_name = obj)
            self.save()
        
        return obj
        
    def __unicode__(self):
        return self.image_path.name
    
    
    
#Content model: not finalize yet
# class Content(models.Model):
#     #each entry in the content table is related to a signle Obj-of-Int
#     object_of_interest = models.ForeignKey(Object)
#     #description
#     description = models.CharField(max_length=1000)
#     #url
#     url = models.CharField(max_length=200)
#     #model path
#     model_path = models.FileField(upload_to="content_model/")