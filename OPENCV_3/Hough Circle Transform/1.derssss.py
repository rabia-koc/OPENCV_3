"""
Bu derste daireleri tespit etmeye çalışıcaz.
"""

"""
Hough dönüşümü sırasında görüntümüzü geniş bir alana dönüştürüyoruz.
daire bulmaya çalışırken 3 boyutlu parametreler gerkiyor.
merkez koordinatları x ve y olarak ve yarıçap gerekiyor.
dönüşüm sırasında girdiği görüntümüzdeki her bir kenar pikseli pikselin uzanabileceği tüm 
olası çemberleri oyluyor. yabir bir oylama işlemi yapıyor. çevresini çizicek sınırları bulmak için oylama yapıyor.
bu oylamayı 3 boyutlu matrix içindeki çoklu değerleri arttırma olarak düşünebiliriz.
oylar verildikten sonra bu matrix içindeki en yüksek değeri arıyoruz ve daire merkezine ve yarıçapını okuyoruz.
matrix ne kadar büyükse yani giriş resmimize kıyasla ne kadar büyükse, dp ne kadar küçükse matrix o kadar büyük oluyor.
oylamamızın çözünürlüğüde o kadar yüksek olur. 
çözünürlük ne kadar yüksekse daire tespitide o kadar doğru olacaktır.
bununla birlikte tespit ne kadar doğru olursa örneğin biraz bozulmuş dairelerin gözden kaçırma veya büyük kenarlı daire yerine 
birden fazla daire tespit etme gibi olasılıklarda yükselir
"""

import cv2
import numpy as np

image = cv2.imread('ay.jpg')
img = image.copy()  # resmin üzerine çizme işlemi yapacağım için kopyasını aldım.
image = cv2.medianBlur(image, 5)

# image = cv2.GaussianBlur(image, (7,7), 1.5)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # gri tonlamaya çevirdik.

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.namedWindow("img", cv2.WINDOW_NORMAL)

# belirlediğim daireleri HoughCircle içinde bulucam
min_dist = image.shape[0]/8
param1 = 100
param2 = 50
circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1,
                           min_dist, param1=param1, param2=param2,
                           minRadius=0, maxRadius=0)
"""
 2. parametre: method
 3. parametre: dp; çözünürlüğün ters oranı
 4. parametre: mindist; algılanan merkezler arası min mesafe
 5. parametre: param1; üst eşiği kendimiz giriyoruz. alt eşiği otomatik olarak kendisi belirliyor
 6. parametre: param2; merkez algılama eşiği. eşik ne kadar düşükse o kadar daire algılanacak, 
 ne kadar yüksekse de potansiyel olarak o kadar fazla daire geriye döndürecek bize
 minRadius ve maxRadiusta algıladığımız dairenin min ve max yarıçapıdır.
 0 olarak girersek sıfır olarak girersek otomatik bir sınırlama koymamış oluruz. kendisi her şeyi buluyor.
 maxRadius' a -1 değeri girersek: çevredeki çizen daireyi çizmez sadece merkezini bulur .
 minRadius=5, maxRadius=70 ' te verebiliriz.
"""
"""
şimdi daireler hazır. daireleri çizme işlemi yapıcaz ama bu dairelerin içinde dönen değerler
3 tane değer döndürüyor: x,y,r . buradaki değerlerde float türünde döndürüyor. onun için bunları ortalama bir değere yuvarlamamız gerek.
"""

circles = np.uint16(np.around(circles))
"""
 buranın sonucu yuvarlanmış olarak dönecek. dönen değerin türünü de  değiştirdik.
 şimdi şu şekilde dönüyor bu:
 matrixin değerleri mesala 5 tane şey aldı ya 1 5 3 olarak gelir buradaki değerler yani boyutu.
"""

# işlemleri yaparken bir kontrol kodu koyucam.
# circles'lerin içi boş değilse işlem yap.
if circles is not None:
    for x, y, r in circles[0, :]:   # 0. indeksinden tamamını al. yoksa burda hata alırım. yani x,y,r değerleri dönmez.
        cv2.circle(img, (x, y), r, (0, 255, 0), 3)  # renk: yeşil
        cv2.circle(img, (x, y), 1, (0, 0, 255), 5)   # merkez noktasını çizmek için

cv2.imshow("image", image)
cv2.imshow("img", img)


cv2.waitKey(0)
cv2.destroyAllWindows()