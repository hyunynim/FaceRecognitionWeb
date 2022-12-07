import face_recognition

import cv2
import numpy as np
import os

def getFileListFromPath(_path, _ext = '.png'):
    filePathList = []
    for (root, directories, files) in os.walk(_path):
        for file in files:
            filePath = os.path.join(root, file)
            if(filePath[-4:] == _ext):
                filePathList.append(filePath)
    return filePathList

def setRegisteredImage(_filePathList):
    faceEncodingList = []
    nameList = []
    for filePath in _filePathList:
        image = face_recognition.load_image_file(filePath)
        faceEncodingList.append(face_recognition.face_encodings(image)[0])

        rootDir, imageName = filePath.split('img/')
        name, ext = imageName.split('.png')
        nameList.append(name)

    return faceEncodingList, nameList


def GetNameList(_imagePath):
    registeredFileList = getFileListFromPath('img/')
    registeredFaceEncodingList, registeredNameList = setRegisteredImage(registeredFileList)

    image = cv2.imread(_imagePath)
    if image is None:
        return None

    #Use down-sampling image for faster face recognition processing
    #image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    #Convert BGR to RGB
    rgbImage = image[:, :, ::-1]

    faceLocationList = []
    faceEncodingList = []
    
    faceLocationList = face_recognition.face_locations(rgbImage)
    faceEncodingList = face_recognition.face_encodings(rgbImage, faceLocationList)

    faceNameList = []
    for faceEncoding in faceEncodingList:
        # See if the face is a match for the known face(s)
        matcheList = face_recognition.compare_faces(registeredFaceEncodingList, faceEncoding)
        name = "Unknown"

        faceDistanceList = face_recognition.face_distance(registeredFaceEncodingList, faceEncoding)
        bestMatchIndex = np.argmin(faceDistanceList)
        if matcheList[bestMatchIndex]:
            name = registeredNameList[bestMatchIndex]

        faceNameList.append(name)
    
    return faceNameList
