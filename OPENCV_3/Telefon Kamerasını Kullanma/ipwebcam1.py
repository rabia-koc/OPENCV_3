import cv2

url = "http://192.168.1.105:8888/video"
cam = cv2.VideoCapture(url)

# kameram açılırsa döngüye gir
while cam.isOpened():
    ret, frame = cam.read() # kamreadan görüntü okuyacak
    # eğer buradaki kamera görüntüsü okunmuyorsa
    if not ret:
        print("kameradan görüntü okunamadı")

    cv2.imshow("görüntü", frame)   # görüntüyü gösteriyoruz.

    # koddan çıkmak için
    if cv2.waitKey(1) == ord("q"):
        break
cv2.destroyAllWindows()