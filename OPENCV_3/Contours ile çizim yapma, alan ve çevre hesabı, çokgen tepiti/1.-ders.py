
import cv2
import numpy as np
from random import randint as rnd

camera = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow("frame")
cv2.createTrackbar("H1", "frame", 0, 359, nothing)
cv2.createTrackbar("H2", "frame", 0, 359, nothing)
cv2.createTrackbar("S1", "frame", 0, 255, nothing)
cv2.createTrackbar("S2", "frame", 0, 255, nothing)
cv2.createTrackbar("V1", "frame", 0, 255, nothing)
cv2.createTrackbar("V2", "frame", 0, 255, nothing)

kernel = np.ones((7, 7), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

paint = np.ones((480, 640, 3), np.uint8)*255
# boş bir sayfa oluşturuyoruz. beyaz boş bir sayfa oldu. (480, 640, 3): boyutları.
# boyuta 3 yazınca bgr kullanacağımızı söylemiş oluyoruz.
paint = cv2.flip(paint, 1)  # kamera yerini değişitirmek için

while camera.isOpened():
    
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)  # frame için de kamera yerini değiştirdik.
    img = frame.copy()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    H1 = int(cv2.getTrackbarPos("H1", "frame") / 2)
    H2 = int(cv2.getTrackbarPos("H2", "frame") / 2)
    S1 = cv2.getTrackbarPos("S1", "frame")
    S2 = cv2.getTrackbarPos("S2", "frame")
    V1 = cv2.getTrackbarPos("V1", "frame")
    V2 = cv2.getTrackbarPos("V2", "frame")
    lower = np.array([H1, S1, V1])
    upper = np.array([H2, S2, V2])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    # hiyerarşi kullanmadık gerek yok.
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 50000 or area < 200:
            continue

        # buradaki x, y sol üst köşedeki pikselini gösteriyor.
        x, y, w, h = cv2.boundingRect(cnt)  # tespit edilen şeklin koordinatlarını buluruz.
        print(x, y, w, h)
        
        color = (rnd(0, 256), rnd(0, 256), rnd(0, 256))

        """
        # bu içinde matematiksel hesaplarla bir ağırlık merkezi vs. oluşturan parametreler döndürüyor.
        # merkez noktası için:
        # m10 yazan x'lerdeki parametrem bölü tüm alana bölüyorum.
        # y koordinatım içinde m01 bölü tüm alan
        # x ve y deki merkez noktalarını vermiş olucak.
        M = cv2.moments(cnt)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00'])) # burda circle olmasının önemi yok direk olarak merkezi buluyoruz.
        """

        # çevreyi bulmaya yarıyan bir fonksiyon: perimeter
        # 1. parametre: koordinattlarım
        # 2. parametre: kapalı bir cisim mi açık bir cisim mi? (kapalı:True)
        perimeter = cv2.arcLength(cnt, True)
        # ne kadar piksel varsa çevre uzunluğu için sayıyor. çıkıntıları da alıyor.
        # tum uzaklığı en geniş uzaklığı alıyor. nerde pikselde sıkıntı varsa alıyor.
        # bunu saymaması için: aşağıdaki işlemi yapıyoruz. yani yaklaştırmak gibi. içeriye en dış çizgiyi bulmak için kullanılıyor.


        epsilon = 0.015*perimeter      # çevre uzunluğumu 0.15 ile çarptık. bu şekilde daha geniş çapta tam dışını, çevresini dolanacak şekilde ayarlamış olurum.
        approx = cv2.approxPolyDP(cnt, epsilon, True)  # bunu yaptığım zaman en dışı çevreleyen koordinatları verecek bana
        
        cv2.drawContours(img, [approx], -1, (0, 0, 0), 15)
        # approx'ı çizeriz. liste olarak vermediği için kapalı paranteze alırız.
        # rengi de siyah yaptık.


        # convexhul: cismin en dıştaki kısımları birbirine düz çizgilerle bağlıyor
        hull = cv2.convexHull(cnt)
        cv2.drawContours(img, [hull], -1, (255, 255, 255), 8)


        # buradaki benim alanımın içinde kapsayan min circle çiz demek istiyor.
        # x,y koordinatlarını ve yarıçapını verecek.
        (x2, y2), radius = cv2.minEnclosingCircle(cnt)  # burda circle olarak merkez buluyoruz.
        center2 = (int(x2), int(y2))  # float olmaması için

        # buraya int(radius) yazdık çünkü float tipinde gelebilir ondan.
        cv2.circle(img, center2, int(radius), (0, 255, 0), -1)  # yeşil renk
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)    # yarıçap: 5, renk: kırmızı, kalınlık: içi dolu
       # cv2.circle(img, center, 5, (0,0,255), -1) # merkez noktası içinde yaptık.
        cv2.drawContours(img, contours, i, color, 4)
        
        cv2.circle(paint, center2, 15, color, -1)
        # boş beyaz sayfada yapıyoruz. Bu işlemi yaptığımızda sürekli olarak yazacağı için bunu bir yerde sıfırlayıp tekrar temiz hale getirmek gerek.


    # köşe sayısını tespit ettmek için:
        if len(approx) == 3:
            cv2.putText(img, "ucgen", (x, y), font, 1, 0, 2)
        elif len(approx) == 4:
            cv2.putText(img, "dortgen", (x, y), font, 1, 0, 2)
        elif len(approx) == 5:
            cv2.putText(img, "besgen", (x, y), font, 1, 0, 2)
        elif 6 < len(approx) < 11:
            cv2.putText(img, "cokgen", (x, y), font, 1, 0, 2)
        else:
            cv2.putText(img, "daire", (x, y), font, 1, 0, 2)
        
    cv2.imshow("frame", frame)
    cv2.imshow("res", res)
    cv2.imshow("img", img)
    cv2.imshow("paint", paint)

    # temizleme işlemi için: cv2.circle(paint, center2, 15, color, -1)
    key = cv2.waitKey(5)
    
    if key == ord("q"):
        break
    elif key == ord("e"):
        paint[:] = 255    # klavyede tekrar e tuşuna başmışsam benim paintimi tekrar beyaz hale getirsin.
    
camera.release()  # kamerayı yeniliyoruz
cv2.destroyAllWindows()