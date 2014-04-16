'''
Created on Apr 14, 2014

@author: yulu
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ImageProcess.views', 
        url(r'^upload_file/?$', 'upload_file', name='upload_file'),
)
