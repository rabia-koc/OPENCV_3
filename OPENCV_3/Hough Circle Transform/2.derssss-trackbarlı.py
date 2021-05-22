# trackbarlı kullanım hali
import cv2
import numpy as np

image = cv2.imread('goz.jpg')
img_org = image.copy()
image = cv2.medianBlur(image,5)
# image = cv2.GaussianBlur(image, (7,7), 1.5)
img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.namedWindow("img",cv2.WINDOW_NORMAL)

font = cv2.FONT_HERSHEY_SIMPLEX

def nothing(x):
    pass


# dp = çözünürlüğün ters oranı
# min_dist = algılanan merkezler arası min mesafe

# min_dist = image.shape[0]/4
# param1 = 120
# param2 = 40
cv2.createTrackbar("min_dist", "image", 0, 500, nothing)
cv2.createTrackbar("param1", "image", 0, 500, nothing)
# cv2.createTrackbar("param2", "image", 0, 500, nothing)

# algılanan değerleerden hata alabiliriz onun için: try, except
while(1):
    img = img_org.copy()
    min_dist = cv2.getTrackbarPos("min_dist", "image") + 1
    param1 = cv2.getTrackbarPos("param1", "image") + 1
    # param2 = cv2.getTrackbarPos("param2","image") + 1
    
    print("min_dist: {}, param1: {}, param2: ".format(
        min_dist, param1))
    try:
        # daha küçük daireleri bulmak için. min_dist: daha fazla seçmek gerekecek görüntü büyüdüğü için
        # param2 değerlerinin artık sıfırın altında olması gerekiyor.
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT_ALT,
                                   1.5,
                                   min_dist, param1=param1,
                                   param2=0.85, 
                                   minRadius=0, maxRadius=0)
        # circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1,
        #                            min_dist, param1=param1,
        #                            param2=param2, 
        #                            minRadius=10, maxRadius=100)
    except Exception as e:
        print("hata: ", e)

        cv2.imshow("image", image)
        cv2.imshow("img", img)
        
        if cv2.waitKey(33) & 0xFF == ord("q"):
            break
        continue
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x, y, r in circles[0,:]:
            cv2.circle(img, (x, y), r, (0, 255, 0), 1)
            cv2.circle(img, (x, y), 1, (0, 0, 255), 1)
            
            cv2.putText(img, "r:"+str(r), (x+10, y+10),
                        font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        
    cv2.imshow("image",image)
    cv2.imshow("img",img)
    
    if cv2.waitKey(33) & 0xFF == ord("q"):
        break
    
cv2.destroyAllWindows()