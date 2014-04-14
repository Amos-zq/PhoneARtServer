'''
Created on Apr 14, 2014

@author: yulu
'''

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()