"""
HAAR CASCADE CLASSIFIERS:
Beyaz tüm pikseller toplanır,
Siyah kısımlardan çıkarılır,
Bu değer eşiği geçiyorsa nesne vardır.
Positive image(face) asıl eğiteceğimiz yani modeli eğiteceğimiz nesnenin olduğu şey.
Negative image(background) ile topladıktan sonra bir eğitim işlemi gerçekleştiriliyor.
daha sonra sınıflandırma işlemi yapıyoruz. bize bir cascade dosyası oluşturuyor.
bu dosyayı artık kullanarak istediğimiz şekilde test işlemlerini tespit işlemlerini gerçekleştirebiliyoruz.
"""

import cv2

# bu bize bunun bir nesnesini oluşturucak.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # yüz için
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")                   # göz için

img = cv2.imread("yuz.JPG")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# resimde birden fazla yüz olabilir.
faces = face_cascade.detectMultiScale(img_gray, 1.3, 10)
# 2. parametre: scaleFactor; küçültme oranı gibi
# 3. parametre: minNeighbors; doğrulama değeri gibi. ne kadar azsa o kadar çok yüz tespiti olur.

# tespit edilen yüzlerin faces isimli değişkenin içine koordinatları geliyor.
# x, y yüzümün köşe noktası
# 2.parametre: x ve y noktamız
# 3. parametre: nerede biteceği
# renk: mavi, kalınlık: 3
for x, y, w, h in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

    # yüzümün olduğu kısımdaki gözü kırpmak için
    roi_gray = img_gray[y:y + h, x:x + w]

    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 20)

    # gözler için çizme işlemi
    for ex, ey, ew, eh in eyes:
        cv2.rectangle(img, (ex + x, ey + y), (ex + ew + x, ey + eh + y), (0, 255, 0), 2)
        # 2. parametre: kırpma işlemini yaptık ya bu kırpılmış img aslında baktığımız zaman x, y olarak yani
        # kırpılmış resim üzerinde göz algılandığı zaman verilen x, y ana resmimizin x y sinde kırpılmış, eksilmiş hali.
        # dolayısıyla ana resmin x ve y koordinatlarınıda eklememiz gerek.

cv2.imshow("img", img)
cv2.waitKey()
cv2.destroyAllWindows()
