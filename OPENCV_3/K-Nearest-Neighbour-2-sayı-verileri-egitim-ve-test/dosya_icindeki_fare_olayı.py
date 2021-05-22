# ilk başta biz fareye tıkladığımızda bir şekil çizicez.
# basılı tutduğumuz süre boyunca bir çizim işlemi olucak.
# bunun için çizim isimli değişken oluşturduk.
# başta False dedik. Böylece tıkladığı zaman sadece false true olucak
# elimi çektiğimde tekrar false dönecek. çünkü ekrana bişeyler çizilmesin diye

import cv2
import numpy as np

cizim = False
mod = False
xi, yi = -1, -1  # başlangıç koordinatlarım


def draw(event, x, y, flags, param):
    global cizim, xi, yi, mod

    # sol click tuşum basılı ise x ve y kooardinatlarını başlangıç olarak sabitliyor.
    if event == cv2.EVENT_LBUTTONDOWN:
        xi, yi = x, y  # koordinatlar
        cizim = True

    # mouse hareketlerini görmek için
    elif event == cv2.EVENT_MOUSEMOVE:
        if cizim == True:
            # mod true olunca daire çizsin
            if mod:
                cv2.circle(img, (x, y), 2, (100, 50, 0), -1)
            # mod false olunca çokgen çizsin
            else:
                cv2.rectangle(img, (xi, yi), (x, y), (0, 0, 255), -1)
        else:
            pass

    # fareden elimi kaldırdığım anda olayı anlaması için
    elif event == cv2.EVENT_LBUTTONUP:
        cizim = False
        if mod:
            cv2.circle(img, (x, y), 2, (100, 50, 0), -1)
        # mod false olunca çokgen çizsin
        else:
            cv2.rectangle(img, (xi, yi), (x, y), (0, 0, 255), -1)


img = np.ones((512, 512, 3), np.uint8)

cv2.namedWindow("paint")

cv2.setMouseCallback("paint", draw)

while (1):
    cv2.imshow("paint", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
        # m'ye basıldığında mod değişikliği yapmasını sağlıyoruz..
    if cv2.waitKey(1) & 0xFF == ord("m"):
        mod = not mod

cv2.destroyAllWindows()