import cv2
import numpy as np

img = cv2.imread("1.jpeg")
img_copy = img.copy()
gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY) # kopyalanan resmi gri renge dönüştürdük.
edges = cv2.Canny(gray, 30, 50) # kenar algılamak için canny kullandık.

# algılanmış kenarlar üzerinde çizgileri bulmak için:
lines = cv2.HoughLines(edges, 1, np.pi/180, 150)  # theresholdu düşürürsem daha çok çizgi belli olur.
"""
 1. paramere: kenarları algılanmış resmim
 2. parametre: rho; üçgendeki r değerinin çözünürlüğü
 3. parametre: theta'nın çözünürlüğünü vericez. her birine 1 derece vericez. yani 1 derecenin 180 tane dereceyi elde etmek istiyurum.
 4. parametre: threshold; ne kadar çok verirsek o kadar çizgi kesişir.
"""
"""
 bunu yaptıktan sonra çizgiler tespit edilmiş olucak.
 bu çizgiler bir dizi halinde bunun içinde değerleri var fakat bu değerler üzerinde çizgi çizme işlemi yapıcaz
 yapmadan önce kontrol etmemiz gerek. bunun içi boş mu dolu mu diye.
 çünkü kontrol etmezsek bir sonraki kısmıda işlem yaparken hata verecek içi nand değeri döndürdüğü için
"""

"""
 if type(lines) != type(None):
 bu şekilde kontrol etmek yerine şu şekilde kontrol ediyorum.
 buradaki her bir line'nı tek tek dönme işlemi yapıcam.
 resmin üzerine tek tek çizicem tüm resimleri.
"""
# lines'teki değerler none değilse burdaki işlemleri yapıyoruz.
# line içinde r ve theta değerleri var.
if not isinstance(lines, type(None)):
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho   # r.cos(theta)
            y0 = b*rho   # r.sin(theta)
            # çizgi çizmek için 2 noktaya ihtiyacımız var. yukarda bir nokta seçmem için x değeri azalması gerek.

            x1 = int(x0 + 1000*(-b))
            # 1000 ile çarpmamım sebeb: bir görüntüm var bu görüntünün pikselleri üzerinde bir çizgi çizeceğim ya
            # bu çizgi az verirsem mesala 100 verirsem ufak bir çizgi çizmiş olurum ve az uzaklaşmış olurum.
            # 1000 yazarsam çok uzaklaşmış olurum.
            # y1 verirken yukarı gitceğimiz için arttırmamız gerekiyor.
            y1 = int(y0 + 1000*(a))

            # şimdi aşağıda nokta belirlemek için x0' dan sağa doğru gitmemiz lazım. arttırmak için
            x2 = int(x0 - 1000*(-b))  # içi artı çıkar
            # y0' da aşağı indirmek için çıkarma işlemi yapıcaz.
            y2 = int(y0 - 1000*(a))  # y0 a'nın 1000 katı kadar azalmış olucak.

            # şimdi 2 nokta arasına çizgi çizmek için. kopyaladığım resmin üzerine çizicem.
            cv2.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2) # kalınlık:2, renk:kırmızı

cv2.imshow("original", img)
cv2.imshow("lines", img_copy)
cv2.imshow("edges", edges)  # KENAR BELİRLEDİĞİMİZ RESMİN GÖRÜNTÜSÜ

cv2.waitKey()
cv2.destroyAllWindows()
