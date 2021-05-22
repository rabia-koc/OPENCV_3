# -*- coding: utf-8 -*-
"""
@author: Mustafa Ünlü
@instagram: mmustafaunluu
@youtube: Kendi Çapında Mühendis
"""


import cv2
import numpy as np

cam = cv2.VideoCapture("car1.mp4")
sapma = 100
kernel = np.ones((3,3),dtype=np.uint8)
    
def crop_matris(img):
    x, y = img.shape[:2]
    value= np.array([
        [(sapma,x-sapma),(int((y*3.2)/8),int(x*0.6)),
         (int((y*5)/8),int(x*0.6)),(y,x-sapma)]],np.int32)
    return value
    
def crop_image(img, matris):
    x, y = img.shape[:2]
    mask = np.zeros(shape = (x, y), dtype=np.uint8)
    mask = cv2.fillPoly(mask, matris, 255)
    mask = cv2.bitwise_and(img, img, mask=mask)
    return mask

def filt(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.inRange(img, 150, 255)
    img = cv2.erode(img, kernel)
    img = cv2.dilate(img, kernel)
    img = cv2.medianBlur(img, 9)
    img = cv2.Canny(img, 40, 200)
    return img

def line_mean(lines):
    left = []
    right = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2-y1)/(x2-x1)
        if slope < -0.2:
            right.append((x1,y1,x2,y2))
        elif slope > 0.2:
            left.append((x1,y1,x2,y2))
        right_mean = np.mean(right, axis=0)
        left_mean = np.mean(left, axis=0)
        #burası 0'a bölme uyarısı verebilir!
    if not isinstance(right_mean, type(np.nan)):
        if not isinstance(left_mean, type(np.nan)):
            return right_mean, left_mean
        else:
            return right_mean, None
    else:
        if not isinstance(left_mean, type(np.nan)):
            return None, left_mean
        else:
            return None, None
        
def draw_line(img, line):
    line = np.int32(np.around(line))
    x1, y1, x2, y2 = line
    cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 10)
    return img

def draw_polylines(img, matris):
    dst = np.array([[matris[0][1,0],matris[0][1,1]],
                    [matris[0][0,0],matris[0][0,1]],
                    [matris[0][3,0],matris[0][3,1]],
                    [matris[0][2,0],matris[0][2,1]]],np.int32)
    cv2.polylines(img, [dst], True, (0,255,255), 2)
    return img


def pers(img, matris, resize_x=300, resize_y=200):
    x, y = img.shape[:2]
    src = np.float32([
        [matris[0][1,0],matris[0][1,1]],
        [matris[0][2,0],matris[0][2,1]],
        [matris[0][0,0],matris[0][0,1]],
        [matris[0][3,0],matris[0][3,1]]])
    dst = np.float32([
        [0,0],
        [y-1,0],
        [0,x-1],
        [y-1,x-1]])
    M = cv2.getPerspectiveTransform(src,dst)
    img_output = cv2.warpPerspective(img, M, (y,x))
    img_output = cv2.resize(img_output, (resize_x, resize_y))
    return img_output
    
    
while cam.isOpened():
    
    ret, image = cam.read()
    if not ret:
        print("bitti")
        break
    
    img_org = image.copy()
    
    matris = crop_matris(image)
    img = crop_image(image, matris)
    img_org[:200,300:600] = cv2.resize(img, (300,200))
    img = filt(img)
    
    lines = cv2.HoughLinesP(img, 1, np.pi/180, 20, 
                            minLineLength = 5, maxLineGap = 200)
    
    img_org[:200,:300] = pers(img_org, matris)
    image = draw_polylines(img_org, matris)
    
    if lines is not None:
        right_line, left_line = line_mean(lines)
        if right_line is not None:
            image = draw_line(image, right_line)
        if left_line is not None:
            image = draw_line(image, left_line)
        

    cv2.imshow("image",image)
    # cv2.imshow("img",img)
    
    key = cv2.waitKey(16) & 0xFF
    if key == ord("q"):
        print("kapatıldı")
        break


cam.release()
cv2.destroyAllWindows()