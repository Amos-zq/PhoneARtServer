'''
Created on Apr 14, 2014

@author: yulu
'''
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse
import json

def responseJson(result):
    try:
        js = json.dumps(result, cls=DjangoJSONEncoder)
    except:
        js = serializers.serialize('json', result)
        
    return HttpResponse(js, content_type="application/json")


def fail():
    return responseJson({'status':'fail'})

def success():
    return responseJson({'status':'success'})

class AlreadyExistException(Exception):
    def __init__(self):
        pass 
    
    def __str__(self):
        return repr("Already Exist Exception")
    
class IncompleteParamException(Exception):
    def __init__(self):
        pass 
    
    def __str__(self):
        return repr("The parameter is incomplete")


class ParseException(Exception):
    def __init__(self):
        pass 
    
    def __str__(self):
        return repr("receipt parsing error")