"""
Dilation: Bir görüntüdeki nesnelerin sınırlarına piksel ekler.
Erosion: Bir görüntüdeki nesnelerin sınırlarındaki pikselleri kaldırır. gürültü gidermek için.
Opening: Önce erosion uygulanır ardından dilation uygulanır.
Closing: Önce dilation uygulanır ardından erosion uygulanır.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

resim = cv2.imread("2-dilation.png", 0)

# treshold işlemi de uygulanabilir.
_, resim = cv2.threshold(resim, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU )
# threshold neden kullandık? gri bir resim vardı onu siyah ve beyazlardan oluşan bir resim haline getirmek için.

# erosion için numpy kütüphanesini ekledik ve kernel'e ihtiyacımız var.
kernel = np.ones((7, 7), np.uint8)
# matrix'in boyutu önemli sadece 1'leri aşındırır. genişletme , aşındırıp, büyültme, küçültme işlemlerini matrix yapar.
# içinde tamamı 1'lerden oluşuyor.
# data türü pozitif int sayılardan oluşuyor.

# kernel ile morfolojik işlemleri yapıcaz.
erosion = cv2.erode(resim, kernel, iterations=1)
# iterations işlemi: tekrarlama işlemi yapar. kaç tekrarla yapacağımızı yazarız. 1 yazdık.
dilation = cv2.dilate(resim, kernel, iterations=1)

#cv2.imshow("original", resim)
#cv2.imshow("erosion", erosion)
#cv2.imshow("dilation", dilation)
#cv2.waitKey()
#cv2.destroyAllWindows()

plt.subplot(131), plt.imshow(resim, "gray"), plt.title("orijinal")
plt.subplot(132), plt.imshow(erosion, "gray"), plt.title("erosion")
plt.subplot(133), plt.imshow(dilation, "gray"), plt.title("dilation")

plt.show()

"""
sonuç: erosion işleminden sonra ortadaki beyaz kısım küçüldü.
dilation işleminden sonra ortadaki beyaz kısım büyüdü.
erosion işleminde beyaz kısımlar küçüldüğü için siyah kısım büyüdü.
"""