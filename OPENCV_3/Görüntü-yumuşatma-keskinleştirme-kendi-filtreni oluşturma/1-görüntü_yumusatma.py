import cv2
import numpy as np

img = cv2.imread("1..jpg")

# avearing filter için 5x5'lik matrix'le oluştuğu için 25'e böldük.
# kernel = np.ones((5,5), np.float32) / 25
""" 
biz resimde her pikseli 25'e bölüyoruz ya sonuçlar float veri türünde olabilir,
onun için float32 yazdık.
sonuçlar float veri türünde oluşacağından görüntü ile kernel çarpımının sonucunda 
bizim görüntümüzün veri türünün eski halini alması için parametre olarak -1 giriyoruz.
böylece float32 olan veri türü uınt8 veri türüne dönüştürerek sonuç elde ediliyor.
"""
# hedef görüntüm
# dst = cv2.filter2D(img, -1, kernel )
# 2. derinlik

# kendi kernel'imizi oluşturup çarpma işlemi yapıyoruz ya bunun yerine opencv'nin kendi direk kullanacabileceğimiz fonksiyonu var.
# dst = cv2.blur(img, (5,5))
"""
tüm pikseller üzerinde gerçekleşiyor. hiç bir şeyi almıyor komşuluk değeri vs.
her yeri eşit şekilde bulanıklaştırıyor.
bunun yerine Gauissian filter kullanabiliriz.
komşuluk değerlerine dayanan bir filtreleme yöntemi.
"""
#dst = cv2.GaussianBlur(img, (5,5), 0 )
# 3. parametreye 0 yazınca standart sapmayı kendisi ayarlıcak.
# keskin kenarlar keskin kalmaya devam ederken yumuşak kenarları daha da yumuşattı.
# tüm resim aşırı bir şekilde yumuşamıyor. komşulara göre işlem yapıldığı için bölgesel olarak kenarları korunuyor.

# median blur : genelde gürültüleri gidermek içn kullanılıyor.
dst = cv2.medianBlur(img, 7)  # direk 5 yazdık yani (5,5) anlamı


cv2.imshow("img", img)
cv2.imshow("dst", dst)  # bulanık bir resim oluştu.

cv2.waitKey()
cv2.destroyAllWindows()