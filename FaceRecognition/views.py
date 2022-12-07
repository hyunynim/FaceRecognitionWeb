from django.shortcuts import render
import base64
import random
import string
from urllib import parse

# Create your views here.
def GetMainPage(_request):
    return render(_request, 'FaceRecognition/main.html')

def UploadPhoto(_request):
    if _request.method == "POST":
        name = str(_request.headers['ImageName'])

        decodedName = parse.unquote(name)

        print(decodedName)
        rawData = str(_request.body)
        header, img = rawData.split(';base64,')
        base64ToPng(img, decodedName + '.png')

    #TODO: Upload result page
    return render(_request, 'FaceRecognition/main.html')

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