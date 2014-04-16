import os
from django.db import models
from os.path import join
from PhoneARtDemo.settings import MEDIA_ROOT
from time import gmtime, strftime
from PatternRecognition.Classifier import * #import PatternRecognition package


# name the uploaded image with current time
def content_file_name(instance, filename):
    name = "img_" + strftime("%Y%m%d%H%M%S", gmtime())
    return os.path.join('images/', name)

# Create your models here
class POI(models.Model):
    #the geographic location of the position of interest
    longtitude = models.FloatField()
    latitude = models.FloatField()
    # name of the poi
    location_name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.location_name

class Object(models.Model):
    #each object is related to a Single POI
    poi = models.ForeignKey(POI)
    #name of the object
    object_name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.object_name
    
class Image(models.Model):
    #each image is related to a signle Object-of-Interest
    object_of_interest = models.ForeignKey(Object)
    
    #title
    title = models.CharField(max_length=60, blank=True, null=True)
    
    #image path
    image_path = models.FileField(upload_to=content_file_name)
    
    def save(self, *args, **kwargs):
        '''save image'''
        super(Image, self).save(*args, **kwargs)
        
    def match(self):
        '''match the image against the database and return the matched class index'''
        img_dir = os.path.join(MEDIA_ROOT, self.image_path.name)
        idx, class_folder = Classifier(img_dir, 1)
        
        return idx, class_folder
        
    def __unicode__(self):
        return self.image_path.name
    
#Content model: not finalize yet
class Content(models.Model):
    #each entry in the content table is related to a signle Obj-of-Int
    object_of_interest = models.ForeignKey(Object)
    #description
    description = models.CharField(max_length=1000)
    #url
    url = models.CharField(max_length=200)
    #model path
    model_path = models.FileField(upload_to="content_model/")