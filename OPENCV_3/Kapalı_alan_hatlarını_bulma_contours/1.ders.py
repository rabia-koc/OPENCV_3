"""
contour: kapalı bir cismin çevresindeki noktalardır.
bunu kullanmak için binary bir resme ihtiyacımız var.
onun üzerinde daha doğru sonuçlar elde ediyoruz. yani 0 ve 1'lerden oluşan resim.
buradaki maske üzerinde kullanıcaz.
"""

import cv2
import numpy as np
from random import randint as rnd  # color için
camera = cv2.VideoCapture(0)  # kameradan görüntü alacğım için kamera belirledim.


def nothing(x):
    pass

cv2.namedWindow("frame")
cv2.createTrackbar("H1", "frame", 0, 359, nothing)  # renk değiştirmek için
cv2.createTrackbar("H2", "frame", 0, 359, nothing)
cv2.createTrackbar("S1", "frame", 0, 255, nothing)
cv2.createTrackbar("S2", "frame", 0, 255, nothing)
cv2.createTrackbar("V1", "frame", 0, 255, nothing)
cv2.createTrackbar("V2", "frame", 0, 255, nothing)
# 1.si ismi
# 2.si hangi pencerede olacağı
# 3., 4. 0 ile 359 değerleri arasında
# 4.sü fonk. ismi

kernel = np.ones((5, 5, ), np.uint8)  # morfoloik için
font = cv2.FONT_HERSHEY_SIMPLEX

# ret değişkenini kullanmıyacğım için alt tire koydum.
# kodun yavaş olmasını engeller.
while camera.isOpened():
    _, frame = camera.read()

    # üzerinde oynama yapacağım için önce farklı bir isimle kaydediyorum.
    img = frame.copy()

    # okuduğum resmi HSV'ye dönüştürme
    # frame bizim resmimiz.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2'ye bölme sebebi opencv de 180 değerini kullanıyor
    # değerleri okuyoruz.
    H1 = int(cv2.getTrackbarPos("H1", "frame") / 2)
    H2 = int(cv2.getTrackbarPos("H2", "frame") / 2)
    S1 = cv2.getTrackbarPos("S1", "frame")
    S2 = cv2.getTrackbarPos("S2", "frame")
    V1 = cv2.getTrackbarPos("V1", "frame")
    V2 = cv2.getTrackbarPos("V2", "frame")

    # bir nesneyi tespit etmek için kullandık, renkleri yakalamak için.
    lower = np.array([H1, S1, V1])  # tek tek h s v ye tekabül eder
    upper = np.array([H2, S2, V2])

    # opencv kütüphanesinde renk değerleri en fazla 180'ne kadar ayarlanmış
    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # bunu yaptığım zaman görüntüyü renkli de görebileceğim
    # hangi renkleri geçirdiğim belli olur.
    res = cv2.bitwise_and(frame, frame, mask=mask)

                                             # 3. parametre sadece köşesi olan cisimleri alıyor avantajlı ve bellekte daha az yer kaplıyor.
                                             # 2. parametredeki cv2.RETR_TREE: tüm konrolü alıyor.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 2 tane parametre döndürüyor.
    # contours : çevre noktalarımızı döndürüyor. algıladığı nesnenin köşe noktalarını
    # veya dış çeperindeki noktaları bir liste halinde tutuyor.
    # 2. değer ise hiyerarşi onunla alakalı 4 tane bilgiyi üzerine tutuyor.

    # burda contoursları kullanarak normal orijnal görüntü üzerine şekil çizmek istiyorum.
    # enumerate yöntemi ile buradaki contoursların içindekileri cnt olarak içine atıcam.
    # burada tespit ettiğim her nesneyi her çevresi olan bir kapalı alana sahip şeyi göstermek istemiyorum.
    # onun için bir alan kullanıcam. belli bir alanın üstünü alıcam, belli bir aralıkta olanları alıcam, diğerlerini gösttermek istemiyorum.

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        # bunun içine aldığım koordinatı gönderiyorum. ve alanı hesaplanacak.
        # buradaki alana göre eğer mesala algılanan obje 100x100 pixel ise alanı 10000px^2 olcaktır.
        # biz burada alanı sadece 200-50000 arasında olan nesneler algılansın diye böyle bir kod yazdık.
        if area > 50000 or area < 200:
            continue

        # buradaki nesnelerin x, y koordinatlarını ve genişliklik ve yükseklik değerlerini bulmak istiyorum.
        x, y, w, h = cv2.boundingRect(cnt)
        print(x, y, w, h)

        color = (rnd(0, 256), rnd(0, 256), rnd(0, 256))  # renkler her seferinde rastgele olarak belirlenmiş olacak.
        """
        # koyduğumuz koordinatlar eğer elips oluşturmayacak koordinatlarsa hata verir o yüzden;
        try:
            ellipse = cv2.fitEllipse(cnt)
            cv2.ellipse(img, ellipse, color, -1)  # çizim için. 2. paramtre ellipse merkezi kendisi ayarlar. kalınlık:-1
        except cv2.error as e:
            print("opps:", e)
        """


        """
        # buradaki bulduğum şeyleri çizdiricem. İlk başta çizeceğim yer lazım.
        # img koyduk çünkü çizim yaparken sıkıntı oluşurmaması için.
        # burda oluşurulan i contoursId için
        # kalınlığı 6 yaptık. sonra -1 verdik içini doldurması için
        # yazı tipini girdik.
        # SONRA HİYERARŞİ İÇİNE GÖNDERDİK."""

        cv2.drawContours(img, contours, i, color, 6, cv2.LINE_8, hierarchy, 0)
        # bunu kullanmadan da çizebiliriz.
        # sonra belirlediğimiz nesnenin çevresini bulup üzerine çizme işlemi yapıcak.

        text = str((w, h))  # genişlik ve uzunluk olarak ayarladık.
        #text = str((x, y))

        # koordinatları resmin üzerine yazmak için
        cv2.putText(img, text, (x, y), font, 1, color, 2)  # kalınlık:2, fountscale:1


    cv2.imshow("frame", frame)
    # cv2.imshow("hsv", mask)
    cv2.imshow("res", res)
    cv2.imshow("img", img)

    if cv2.waitKey(5) == ord("q"):
        break

cv2.destroyAllWindows()
