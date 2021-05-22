"""
1. derste yaptığımız şeyi yani threshold değerini elimizle oynayarak sonuçların nasıl değişeceğini görelim.
trackbar oluşturarak yapıcaz.
"""

import cv2
import numpy as np

img = cv2.imread("1.jpeg")
img_copy = img.copy()
gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)  # kopyalanan resmi gri renge dönüştürdük.
edges = cv2.Canny(gray, 30, 50)  # kenar algılamak için canny kullandık.

def nothing(x):
    pass

cv2.namedWindow("trackbar", cv2.WINDOW_AUTOSIZE)  # trackbar için önce boş bir çerçeve oluşturuyoruz.
cv2.createTrackbar("threshold", "trackbar", 0, 300, nothing)
"""
 boş bir çerveve üzerine trackbar yerleştiriyoruz.
 1. trcakbar ismi
 2. hangi çerçevede olacağı
 0'dan 300'e kadar
"""


# trackbarı oluşturğumuz görselde çerçevede lines içine değeri girmek istiyoruz onun için while döngüsüne aldık.
while(1):

    img_copy = img.copy()
    # çizgileri tespit etmeden önce trackbardan değerleri çekmemiz gerekiyor.
    threshold = cv2.getTrackbarPos("threshold", "trackbar")+1  # sıfırdan başyamaz o yüzden artı 1 ekledik.
    print(threshold)

    """
     bir başka yöntemi
     1. resmimiz
     2. çözünürlük
     3. theta
     4. thereshold değeri
     5. bir çizgi oluşturmak için min nokta sayısı
     6. aynı çizgide dikkate alınacak 2 nokta arasındaki max boşluk yani tespit ettiğimiz pikseller arasında boşluklar olabilir.
     buradaki boşlukların kaç piksele kadar göz ardı edilebileceği"""

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, 20, 0)
    # 20 pikselden az olanları çizgi olarak saymıyor.
    # 0 yazarsak tüm çizgileri çizmiş oldu.

    if not isinstance(lines, type(None)):
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)  # yeşil renk

    """
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold)
    if not isinstance(lines, type(None)):
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho

                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)
    """

    cv2.imshow("trackbar", img_copy)


    if cv2.waitKey(33) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
