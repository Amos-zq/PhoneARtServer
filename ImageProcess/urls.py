'''
Created on Apr 14, 2014

@author: yulu
'''

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('ImageProcess.views', 
        url(r'^upload_image_for_match/?$', 'upload_image_for_match', name='upload_image_for_match'),
        url(r'^request_image_url/?$', 'request_image_url', name='request_image_url'),
)
