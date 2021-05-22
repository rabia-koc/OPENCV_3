import cv2
import numpy as np

img = cv2.imread("image_1.jpg")

print(img.shape)

rows, cols = img.shape[:2]

click_count = 0
a = []

# burda değiştirme işlemi yapmadığımız burda kalabilir.
dst_points = np.float32([
    [0, 0],
    [cols - 1, 0],
    [0, rows - 1],
    [cols - 1, rows - 1]])

cv2.namedWindow("img", cv2.WINDOW_NORMAL)  # pencere oluşturdum
cv2.namedWindow("output", cv2.WINDOW_NORMAL)


def draw(event, x, y, flags, param):
    global click_count, a
    # a değişkeni her tıkladığımda x,y koordinatlarına gelen sayıları a değişkenine atar.

    # 4 kez tıklama işlemi yapmışsam
    if click_count < 4:

        # çift tıklama fonksiyonu
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print(click_count)
            print(x, y)
            click_count += 1  # her tıklamada 1 artar.
            a.append((x, y))  # tıklanan değerleri a'ya ekliyoruz.
    else:

        # bütün tıklamanın değerleridir. x ve y bakımından
        src = np.float32([
            [a[0][0], a[0][1]],
            [a[1][0], a[1][1]],
            [a[2][0], a[2][1]],
            [a[3][0], a[3][1]]])

        click_count = 0  # çünkü her bir 4 tıklamadan sonra bitmesin kod tekrar işlemler yapabilelim diye
        a = []

        M = cv2.getPerspectiveTransform(src, dst_points)  # matrix oluşturduk.
        img_output = cv2.warpPerspective(img, M, (cols, rows))

        img_output = cv2.cvtColor(img_output, cv2.COLOR_BGR2GRAY) # GRİ TONA DÖNÜŞTÜ
        # eşikleme işlemi yapıldı.
        thresh = cv2.adaptiveThreshold(img_output, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY, 11, 4)

        cv2.imshow("output", thresh)

    pass


cv2.setMouseCallback("img", draw)

# tıklama işlemi yaptığım sürece resimleri göstermesini istedim.
while (1):
    cv2.imshow("img", img)
    # cv2.imshow("img_output",img_output)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
