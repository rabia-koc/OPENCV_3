import cv2
import numpy as np

img = cv2.imread("1..jpg")

"""
instagramda kullanılan bir filtre bu şekilde de yapılabilir ama  biz aynısını bir filtre ile gerçekleştiricez.
b, g, r = cv2.split(img)

r_new = r*0.393 + g*0.769 + b*0.189
g_new = .........
b_new = .......

dst = cv2.merge([b_new, g_new, r_new])
"""


filter = np.array([[0.272, 0.534, 0.131],
                   [0.349, 0.686, 0.168],
                   [0.393, 0.769, 0.189]])

# görüntümü oluşturduğum filtre ile renk kanallarıyla çarpma işlemi yapıcam.
dst = cv2.transform(img, filter)
# her bir renk kanalında işlem yapmak için bu fonk. kullanırız.

cv2.imshow("img", img)
cv2.imshow("dst", dst)  # bulanık bir resim oluştu.

cv2.waitKey()
cv2.destroyAllWindows()