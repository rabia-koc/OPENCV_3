
import cv2
import numpy as np

cam = cv2.VideoCapture("vtest.avi")

tum_vucud = cv2.CascadeClassifier("haarcascade_fullbody.xml")
alt_vucud = cv2.CascadeClassifier("haarcascade_lowerbody.xml")
ust_vucud = cv2.CascadeClassifier("haarcascade_upperbody.xml")

ret, resim = cam.read()

# seçilen insanları çerveve içine eklemek için
detect = np.zeros((resim.shape[0], resim.shape[1], 3), np.uint8)
# 3 tane renk kanalından oluşuyor.
print(resim.shape)  # (576, 768, 3)

def nothing(x):
    pass

cv2.namedWindow("resim", cv2.WINDOW_NORMAL)   # trackbar için boş pencere oluşturduk.
cv2.createTrackbar("one_param", "resim", 0, 100, nothing)
cv2.createTrackbar("two_param", "resim", 0, 100, nothing)
cv2.createTrackbar("switch", "resim", 0, 1, nothing)

while cam.isOpened():
    
    detect[:] = 0  # her döngü tekrar başladığında temizleme işlemi
    
    if cv2.getTrackbarPos("switch", "resim") == 1:
        cv2.waitKey(1)
        continue
        
    ret, resim = cam.read()
    if not ret:
        print("done")
        break
    
    resim_gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)

    # vucutların içine gireceğimiz değerleri buradan çekecez.
    one_param = cv2.getTrackbarPos("one_param", "resim")/100+1.01
    # küçültme oranı
    # bunu çektiğim zaman bu değer 0'da gelebilir.farklı değerlerde gelebilir.
    # bunu önlemek için /100+1.01 bu işlemi de ekledik.

    # komşuluk değeri
    two_param = cv2.getTrackbarPos("two_param", "resim")+1
    
    print("ilk parametre: {}, ikinci parametre: {} ".format(
        one_param, two_param))
    
    vucudlar = tum_vucud.detectMultiScale(resim_gri, one_param, two_param, minSize=(40, 40), maxSize=(110, 110))

    alt_vucudlar = alt_vucud.detectMultiScale(resim_gri, one_param, two_param, minSize=(40, 40), maxSize=(80, 80))

    ust_vucudlar = ust_vucud.detectMultiScale(resim_gri, one_param, two_param, minSize=(40, 40), maxSize=(80, 80))

    # çizdirme işlemi için
    for x, y, w, h in vucudlar:
        detect[y:y+h, x:x+w] = resim[y:y+h, x:x+w]  # tüm respit edilen vucutları bu resmin içine ekleme işlemi
        cv2.rectangle(resim, (x, y), (x+w, y+h), (255, 0, 0), 3)
        resim[y:y+h, x:x+w, 0] = 255  # boyama işlemi için
    
    for x, y, w, h in alt_vucudlar:
        cv2.rectangle(resim, (x, y), (x+w, y+h), (0, 255, 0), 2)
        resim[y:y+h, x:x+w, 1] = 255
    
    for x, y, w, h in ust_vucudlar:
        cv2.rectangle(resim, (x, y), (x+w, y+h), (0, 0, 255), 2)
        resim[y:y+h, x:x+w, 2] = 255
    
    cv2.imshow("resim", resim)
    cv2.imshow("detect", detect)
    
    if cv2.waitKey(5) == ord("q"):
        print("by")
        break
    
cv2.destroyAllWindows()
cam.release()