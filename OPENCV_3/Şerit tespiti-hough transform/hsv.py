# -*- coding: utf-8 -*-
"""
@author: Mustafa Ünlü
@instagram: mmustafaunluu
@youtube: Kendi Çapında Mühendis
"""


import cv2
import numpy as np

cam = cv2.VideoCapture("car1.mp4")
kernel = np.ones((3,3), np.uint8)

def crop_ver(image, sapma=100):
    x,y = image.shape[:2]
    value= np.array([
        [(sapma,x-sapma),(int((y*3.2)/8),int(x*0.6)),
         (int((y*5)/8),int(x*0.6)),(y,x-sapma)]],np.int32)
    return value

def crop_al(image, value):
    x,y = image.shape[:2]
    mask = np.zeros(shape = (x, y), dtype=np.uint8)
    mask = cv2.fillPoly(mask, value, 255)   
    masked = cv2.bitwise_and(image, image, mask=mask)
    # cv2.imshow("masked",masked)
    return masked

def edge_filtre(image):
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.medianBlur(image, 9)
    # image = cv2.GaussianBlur(image, (25,25), 2)
    image = cv2.Canny(image,10,50)

    # cv2.imshow("canny",image)
    return image
    
def hough(image, threshold=20):
    left_av = []
    right_av = []
    lines = cv2.HoughLines(image, 1, np.pi/180, 
                           threshold)
    if not isinstance(lines, type(None)):
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                
                x1 = int(x0 + 10000*(-b))
                y1 = int(y0 + 10000*(a))
                x2 = int(x0 - 10000*(-b))
                y2 = int(y0 - 10000*(a))
                
                slope = (y2-y1)/(x2-x1)

                if slope > 0.2:
                    right_av.append((x1,y1,x2,y2))
                elif slope < -0.2:
                    left_av.append((x1,y1,x2,y2))
                    
        right_avg = np.average(right_av, axis=0)
        left_avg = np.average(left_av, axis=0)
        
        if not isinstance(right_avg, type(np.nan)):
            if not isinstance(left_avg, type(np.nan)):
                return right_avg, left_avg
            else:
                return right_avg, None
        else:
            if not isinstance(left_avg, type(np.nan)):
                return None, left_avg
            else:
                return None,None
    else:
        return None, None

def draw_line(image, lines):
    img = image.copy()
    x,y = image.shape[:2]
    crop_img = image[0:int(x*0.6),:]
    
    lines = np.int0(np.around(lines))
    if lines is not None:
        x1, y1, x2, y2 = lines
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 10)
        
    img[0:int(x*0.6),:] = crop_img
    
    return img
    
while cam.isOpened():
    ret, img_org = cam.read()
    if not ret:
        break
    
    img = img_org.copy()
    
    value = crop_ver(img)
    img = crop_al(img, value)
    
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    lower = np.array([0,0,160])
    upper = np.array([180,45,255])
    
    mask = cv2.inRange(img_hsv,lower,upper)
    cv2.imshow("mask",mask)
    res = cv2.bitwise_and(img,img,mask=mask)
    
    edges = edge_filtre(res)
    right_lines, left_lines = hough(edges)
    
    zeros = np.zeros_like(img)
    if left_lines is not None:
        zeros = draw_line(zeros, left_lines)
        img_org = cv2.addWeighted(img_org,1,zeros,1,0)
    if right_lines is not None:
        zeros = draw_line(zeros, right_lines)
        img_org = cv2.addWeighted(img_org,1,zeros,1,0)

    cv2.imshow("img_org",img_org)
    
    if cv2.waitKey(16) == ord("q"):
        break


cv2.destroyAllWindows()