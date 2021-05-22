import cv2
import matplotlib.pyplot as plt

resim = cv2.imread("bookpage.jpg",0)

thresh = cv2.adaptiveThreshold(resim, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 11, 2)

"""
 2. paramatre max değer
 eşik değerini kendisi belirleyecek ve belirlerken komşuluklardan faydalanacak, bizim belirlediğimiz matrix üzerinden komşuluk kuracak.
 4. sü hangi treshold türü ile yapacağım
 5.si matrix'in kaça kaçlık olacağı 11x11'lik, tek rakam olmak zorunda
 sonra bu matrix'i resim üzerinde gezdirme işlemi yapacak
 6.sı: c değeridir. gezdirme işlemi yaptıdığı zaman bir hesaplama yapıyor, bu hesaplama da normal çıkan değerin eksi ya da artı olarak bir toplam değerden çıkarma işlemi yapabiliyoruz.
"""

# matrix boyutunu artırarak daha okunaklı hale getirdik.
# bir değer belirlendi ve ondan 2 çıkartma işlemi yaptı.

cv2.imshow("original resim", resim)
cv2.imshow("adaptive ", thresh)

cv2.waitKey()
cv2.destroyAllWindows()

"""
komuşulukları kullanıyor, 
küçük küçük matrixler halinde işlem yaptığı için karanlık bölgede karanlık bir thresh değeri belirliyor
aydınlık bölgede aydınlık bir thresh değeri belirliyor
"""
