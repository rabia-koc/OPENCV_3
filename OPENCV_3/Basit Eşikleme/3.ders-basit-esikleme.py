import cv2

# resim okuma işlemi olucak ve içine resmin konumunu gir
resim = cv2.imread("gradient.jpg",0) # siyah beyaz okumak için 0 koydum.

# bu fonksiyon trackbarda dönen değeri içinde döndürüyor sadece
def nothing(x):
    pass

cv2.namedWindow("resim", cv2.WINDOW_NORMAL)  # boş bir pencere oluşturduk.

cv2.createTrackbar("esik", "resim", 0, 255, nothing)
# 1.si trackbar ismi: esik.
# 2. si hangi pencerede olucağı
# 0'dan 255'e kadar

while(1):
    
    thresh = cv2.getTrackbarPos("esik", "resim")
    # trackbarın içinde değeri okuyoruz. resim isimli pencereden esik resmini okuyacak.

    _, threshold_image = cv2.threshold(resim, thresh, 255, cv2.THRESH_BINARY)
    # üstündeki değerleri 255' eşitler

    cv2.imshow("resim", resim)
    cv2.imshow("threshold_image ", threshold_image )

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()