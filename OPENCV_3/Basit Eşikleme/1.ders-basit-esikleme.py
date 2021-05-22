import cv2
import mustafa

# resim okuma işlemi olucak ve içine resmin konumunu gir
resim = cv2.imread("kizkulesi.jpg",0) # siyah beyaz okumak için 0 koydum.

# threshold işlemi
ret, resim_thresh = cv2.threshold(resim, 182, 255, cv2.THRESH_BINARY)

"""
ilk paramatre kaynak isimli parametre yani resmim
2. parametre eşik değeri
3. parametre: max değer; 182' nin altında olan değerleri 0'a eşitlicek üstünde olan değerleri neye eşitliyim diyor.
4. parametre türünü belirledik.
Bu işlem bize 2 değer döndürücek.
ret değeri: 182 değerini döndürecek
resim_thresh: eşikleme yapılmış resmi döndürecek
"""
ret2, resim_thresh2 = mustafa.threshold(resim, 182, 255)

# resimlerin boyutlarıyla oynamak için
cv2.namedWindow("resim", cv2.WINDOW_NORMAL)
cv2.namedWindow("resim_thresh", cv2.WINDOW_NORMAL)
cv2.namedWindow("resim_thresh2", cv2.WINDOW_NORMAL)

cv2.imshow("resim",resim)
cv2.imshow("resim_thresh",resim_thresh)
cv2.imshow("resim_thresh2",resim_thresh2)
cv2.waitKey()
cv2.destroyAllWindows()