import cv2
import matplotlib.pyplot as plt

resim = cv2.imread("shape_noise.png", 0)

# NORMAL BİR THRESHOLDİNG İŞLEMİ
_, th1 = cv2.threshold(resim, 127, 255, cv2.THRESH_BINARY)   # 127'nin altındakileri 0 yapıyor.

# Otsu's thresholding
_, th2 = cv2.threshold(resim, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# otsu'nun dezevantajı: resimlerdeki gürültüdür. gürültülü bir görselde thresholding işlemi yaptığımız zaman hiç iyi bir sonuç çıkmıyor.
# onun için blur yöntemini kullandık.

# blur yapıldıktan sonra thresholding işlemi
blur = cv2.GaussianBlur(resim, (15, 15), 0)
_, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# gürültüyü azaltarak ortalama değeri seçip altını 0 üstünü 255 olarak ayarlıyor

# 3'nün karşılaştırılması

plt.subplot(3, 3, 1), plt.imshow(resim, "gray"), plt.title("original resim")
plt.subplot(3, 3, 2), plt.hist(resim.ravel(), 256), plt.title("histogram")
plt.subplot(3, 3, 3), plt.imshow(th1, "gray"), plt.title("th1")

plt.subplot(3, 3, 4), plt.imshow(resim, "gray"), plt.title("original resim")
plt.subplot(3, 3, 5), plt.hist(resim.ravel(), 256), plt.title("histogram")
plt.subplot(3, 3, 6), plt.imshow(th2, "gray"), plt.title("th2")

plt.subplot(3, 3, 7), plt.imshow(blur, "gray"), plt.title("blur ")
plt.subplot(3, 3, 8), plt.hist(blur.ravel(), 256), plt.title("histogram")
plt.subplot(3, 3, 9), plt.imshow(th3, "gray"), plt.title("th3")

plt.show()