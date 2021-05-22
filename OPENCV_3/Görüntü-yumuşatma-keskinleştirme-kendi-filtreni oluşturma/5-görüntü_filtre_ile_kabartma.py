
import cv2
import numpy as np


img = cv2.imread("1..jpg")



filter = np.array([[0, 1, 0],
                   [0, 0, 0],
                   [0, -1, 0]])

dst = cv2.filter2D(img, -1, filter) + 64  # karanlığı gidermek için 64 ekledik.

cv2.imshow("img", img)
cv2.imshow("dst", dst)
cv2.waitKey()

cv2.destroyAllWindows()