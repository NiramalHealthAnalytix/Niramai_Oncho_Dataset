import base64
import json
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def getActualVideo(filename):
    cap = cv2.VideoCapture(filename + ".avi")
    minMax = pd.read_csv(filename + "_temp.csv")
    greyScale = []
    videoFrame = []
    i = 0
    while(1):
        ret,frame = cap.read()
        if not ret:
            break
        minVal = minMax.loc[i,'Min']
        maxVal = minMax.loc[i,'Max']
        frame = frame[:,:,0]
        actualFrame = ((frame/255) * (maxVal - minVal)) + minVal
        greyScale.append(frame)
        videoFrame.append(actualFrame)
        i = i + 1
    cap.release()
    return greyScale,videoFrame

# Nodule location
def getNodule(basepath,side,types="Phase2"):
    f = open(basepath+"/croppoints.crpt")
    dd = f.readlines()
    f.close()
    c = base64.b64decode(dd[0])
    z = json.loads(c)
    item = z.get(side+".jpg")
    NoduleMask = np.zeros((240,320))
    if item is not None:
        for temp in item:
            if (temp["Item2"]):
                cc = temp['Item1']
                norm = [1,1]
                stXY = norm * np.array([int(x) for x in cc[0].split(",")])
                edXY = norm * np.array([int(x) for x in cc[1].split(",")])
                y1 = int(stXY[0]); x1 = int(stXY[1]); y2 = int(edXY[0]); x2 = int(edXY[1]);
                NoduleMask[np.min([x1,x2]):np.max([x1,x2]),np.min([y1,y2]):np.max([y1,y2])] = 1
        return NoduleMask
    else:
        print('No Nodules marked')
        return None
    
def getMaskFromCrpt(basepath,side,types = "Phase2"):
    f = open(basepath+"/croppoints.crpt")
    dd = f.readlines()
    f.close()
    c = base64.b64decode(dd[0])
    z = json.loads(c)
    item = z.get(side+".jpg")
    norm = [1,1]
    pts = []
    if item is not None:
        for elem in item:
            if not elem.get("Item2"):
                temp = elem.get("Item1")
                for entry in temp:
                    tempList = []
                    for index, coords in enumerate(entry.split(",")):
                        tempList.append(int(int(coords)/norm[index]))
                    pts.append(tempList)
                pts = np.array(pts)
                im = np.zeros([240,320],dtype=np.uint8)
                pts1 = np.reshape(pts,(1,pts.shape[0],pts.shape[1]))
                out = cv2.fillPoly( im, pts1, 255 )
                return out
    else:
        print('No crop-point entry')

def plotData(arr,titles):
    plt.figure(figsize=(10,3))
    for i in range(len(arr)):
        plt.subplot(1,len(arr),i+1)
        plt.imshow(arr[i])
        plt.colorbar()
        plt.title(titles[i])
    