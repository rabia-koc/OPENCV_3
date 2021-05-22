import cv2
import numpy as np

img = cv2.imread("1..jpg")


# mexicanhat filtresi
#filter = np.array([[0,0,-1, 0,0],
#                    [0, -1,-2,-1,0],
#                    [-1,-2,16,-2,-1],
#                    [0,-1,-2,-1,0],
#                    [0,0,-1,0,0]])


# rastgele filtre oluşturdum. "dst = cv2.filter2D(img, -1, filter ) + 50" yani 50 yerine yazdığımız sayı ile parlaklık ayarı yaparız.
filter = np.array([[4,-3,-4],
                   [-5,7,-7],
                   [3,-2,-1]])


# çarpma işlemi yaparak fonksiyonu kullanıyoruz.
dst = cv2.filter2D(img, -1, filter) + 50


cv2.imshow("img", img)
cv2.imshow("dst", dst)  # bulanık bir resim oluştu.

cv2.waitKey()
cv2.destroyAllWindows()