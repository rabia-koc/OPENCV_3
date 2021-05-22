import cv2
import numpy as np

cam = cv2.VideoCapture(0)

# görüntü üzerinde eşikleme için lazım.
# bir nesneyi tespit etmek için kullandık, renkleri yakalamak için.
lower = np.array([75, 88, 120]) # h'leri 2'ye böldük çünkü 360 olarak hesaplandığından
upper = np.array([117, 250, 255])

"""bir tane resmi görüntü açıldığında background olarak belirliyorum. çünkü arka plan görüntüsü lazım
örneğin çantayı kaldırdığım zaman arkasının gözükmesi için boş bir görüntü almam gerekiyor."""
_, background = cam.read()

kernel = np.ones((3, 3), np.uint8)  # görüntümün içindeki büyütüyor.
kernel2 = np.ones((11, 11), np.uint8)  # dışardaki gürültüleri gideriyor.
kernel3 = np.ones((15, 15), np.uint8)

# kameram açılırsa oku
while(cam.isOpened()):
    _, frame = cam.read()

# bu görüntüyü yeşil algılamam için:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

# gürültülerden kurtulmak için maskelenmiş görüntüye işlem uyguladık.
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2)
    mask = cv2.dilate(mask, kernel3, iterations=1)

    #mask'yi 2 türlü kullanmam gerekiyor.
    mask_not = cv2.bitwise_not(mask) # çantamın 0 olduğu yerdir
    # siyahlar beyaz, beyazlar siyah olsun. terslenmiş görüntü yani.

    """
     orjinal görüntüde çantayı gösterdiğim zaman arka plan görüntüsü istiyordum.
     çantamı algıladığım zaman oluşan maske de çanta 1 olarak gözüküyor.
     1 olan yerleri background ile çarparsam sadece çantanın olduğu kısım 1 olarak kalır.
     arka planlar ise 0 olarak kalır.
     böylece arka plan görüntümün renkli kısmını alabilirim.
     """
    bg = cv2.bitwise_and(background, background, mask=mask)

    # orjinal görüntü içinde aynı işlemi uygularız.
    fg = cv2.bitwise_and(frame, frame, mask=mask)  # nesnenin yani çantanın renkli diğer tarfların sıyah olduğu görüntü.

    # bu görüntüleri üst üste birleştirme işlemi yapar.
    dst = cv2.addWeighted(bg, 1, fg, 1, 0)  # toplam parlaklık için sıfır verdik.

#  orjinal resmim ile son 3 resmimi yan yana görüntüleyebilirim.
    dst = np.vstack((frame, dst))  # dikey olarak birleştirdi.

    cv2.imshow("original", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("dst", dst)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()