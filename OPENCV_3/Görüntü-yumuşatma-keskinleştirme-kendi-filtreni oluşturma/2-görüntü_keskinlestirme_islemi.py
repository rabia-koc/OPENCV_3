# KESKİNLEŞTİRME İŞLEMİ
# görüntülerdeki kenarları genişleştirmek için kullanılır.
import cv2
import numpy as np

img = cv2.imread("1..jpg")

# 3x3'lük bir kernel oluşturuyorum.
# keskinleştirmek için kullanılan bir matrix var onu kullandık.

filter = np. array([[-1, -1, -1],
                    [-1, 9, -1],
                    [-1, -1, -1]])

# çarpma işlemi yaparak fonksiyonu kullanıyoruz.
dst = cv2.filter2D(img, -1, filter)


cv2.imshow("img", img)
cv2.imshow("dst", dst)  # bulanık bir resim oluştu.

cv2.waitKey()
cv2.destroyAllWindows()