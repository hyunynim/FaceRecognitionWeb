# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse

import base64
import os
import random
import string
from urllib import parse

from . import FaceRecognition

# Create your views here.
def GetMainPage(_request):
    return render(_request, 'FaceRecognition/main.html')

def UploadPhoto(_request):
    resultString = ''
    if _request.method == "POST":
        name = str(_request.headers['ImageName'])

        decodedName = parse.unquote(name)

        rawData = str(_request.body)
        header, img = rawData.split(';base64,')
        filePath = decodedName + '.png'
        
        base64ToPng(img, 'tmp/', filePath)

        nameList = FaceRecognition.GetNameList('tmp/' + filePath)

        if not nameList:
            resultString = 'No faces image or not registered face'
        else:
            base64ToPng(img, 'img/', filePath)
            resultString = 'Hello ' + nameList[0]
        
        os.remove('tmp/' + filePath)
        context = {
            'result': resultString,
        }
        return JsonResponse(context)

def base64ToPng(_base64String, _root, _fileName):
    decodedData = base64.b64decode(_base64String)

    image = open(_root + _fileName,'wb') 
    image.write(decodedData)
    image.close()

#Make name randomly [A-z, a-z, 0-9]
def makeName(_len = 20):
    letterList = string.ascii_uppercase + string.ascii_lowercase + string.digits
    fileName = ''
    for i in range(_len):
        fileName += random.choice(letterList)
    return fileName