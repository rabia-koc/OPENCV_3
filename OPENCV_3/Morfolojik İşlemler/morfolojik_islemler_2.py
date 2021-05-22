import cv2
import numpy as np
import matplotlib.pyplot as plt

resim = cv2.imread("opening.png", 0)


# erosion için numpy kütüphanesini ekledik ve kernel'e ihtiyacımız var.
kernel = np.ones((5, 5), np.uint8)
# matrix'in boyutu önemli sadece 1'leri aşındırır. genişletme , aşındırıp, büyültme, küçültme işlemlerini matrix yapar.
# içinde tamamı 1'lerden oluşuyor.
# data türü pozitif int sayılardan oluşuyor.

""" kerneli farklı değerlerde kullanmak için"""
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))  # yani bir yapılandırma elamanı oluştur diyoruz.
print(kernel)
# Bu 2 kernel normalde aynı şey

# bunu neden kullanırız. elips oluşturabiliriz.
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
print(kernel)

# çarpım oluşturabiliriz.
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
print(kernel)


# kernel ile morfolojik işlemleri yapıcaz.
erosion = cv2.erode(resim, kernel, iterations=1)
# iterations işlemi: tekrarlama işlemi yapar. kaç tekrarla yapacağımızı yazarız. 1 yazdık.
dilation = cv2.dilate(resim, kernel, iterations=1)

opening = cv2.morphologyEx(resim, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(resim, cv2.MORPH_CLOSE, kernel)
tophat = cv2.morphologyEx(resim, cv2.MORPH_TOPHAT, kernel)   # original resim ile opening farkını alıyor
blackhat = cv2.morphologyEx(resim, cv2.MORPH_BLACKHAT, kernel)   # original resim ile closing farkını alıyor
gradient = cv2.morphologyEx(resim, cv2.MORPH_GRADIENT, kernel)   # genişletme ve aşındırma işleminin farkını alıyor
"""
aralarındaki fark: OPEN dediğimiz işlemde ilk başta erosion işlemi yapıp erosion için uygulanmış resim üzerine dilation işlemi yapıyor.
yani önce aşındırma işlemi görüyor sonra genişleme işlemi görüyor.
o görselde aşındırma işlemi yapınca gürültülerden kurtuluyoruz ama ana görüntüde algılanma istediğimiz şey inceldiğinde 
tekrar kalınlaştırdığımızda dışardaki gürültüler gidiyor önceki incelttiğimiz ana nesnemiz eski boyutlarına geliyro.
"""


plt.subplot(241), plt.imshow(resim, "gray"), plt.title("orijinal")
plt.subplot(242), plt.imshow(erosion, "gray"), plt.title("erosion")
plt.subplot(243), plt.imshow(dilation, "gray"), plt.title("dilation")
plt.subplot(244), plt.imshow(opening, "gray"), plt.title("opening")
plt.subplot(245), plt.imshow(closing, "gray"), plt.title("closing")
plt.subplot(246), plt.imshow(tophat, "gray"), plt.title("tophat")
plt.subplot(247), plt.imshow(blackhat, "gray"), plt.title("blackhat")
plt.subplot(248), plt.imshow(gradient, "gray"), plt.title("gradient")

plt.show()

"""
asıl amacımız: içerdeki gürültüleri temizlemek istiyorsak = closing
dışardaki gürültüleri temizlemek istiyorsak = opening işlemini kullanırız.
"""
