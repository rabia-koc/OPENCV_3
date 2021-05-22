import cv2
import matplotlib.pyplot as plt

resim = cv2.imread("bookpage.jpg", 0)

ret, th = cv2.threshold(resim, 10, 255, cv2.THRESH_BINARY)  # basit treshold işlemi

thresh = cv2.adaptiveThreshold(resim, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 11, 2)
# thresh mean de: tüm matrixleri sırayla sıralıyor. küçükten büyüğe doğru. ortanca değer hangisiyse onu seçip kullanıyoruz.

# 2 değeri: tüm bu çarpma işlemi yapıldıktan sonra sabit değerden burada girdğimiz c değerini yani 2 çıkartıyor. mean_c yazma sebebimiz o.

thresh2 = cv2.adaptiveThreshold(resim, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)
# adaptive thresh gaussioanda bunları belli bir ağırlık değerleri olarak çarpıp matrixleri ona göre sonuç matrixi belirliyoruz.

"""
cv2.imshow("original resim", resim)
cv2.imshow("adaptive mean", thresh)
cv2.imshow("adaptive gaussion", thresh2)

cv2.waitKey()
cv2.destroyAllWindows()
"""
# matplotlib ile daha iyi göstermek için
plt.subplot(2, 2, 1), plt.imshow(resim, "gray"), plt.title("original image")
plt.subplot(2, 2, 2), plt.imshow(th, "gray"), plt.title("global threshold")
plt.subplot(2, 2, 3), plt.imshow(thresh, "gray"), plt.title("thresh mean")
plt.subplot(2, 2, 4), plt.imshow(thresh2, "gray"), plt.title("thresh2 gaussian")

plt.show()