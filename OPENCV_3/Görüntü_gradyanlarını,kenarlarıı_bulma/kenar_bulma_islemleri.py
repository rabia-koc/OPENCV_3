"""
kenar algılama: bir resimdeki nesnelerin sınırlarını bulmak için kullanılan bir teknikir.
ve çıktı olarak bize içinin 0 ve 1'lerden oluşan binarry bir resim verir.
genellikle bu kenarları belirtmek için siyah bir arka plan kullanırız.
ön planları da beyaz olur. kenar çizgileri beyaz olarak gözükür.
burada kenar algılamak için yüsek geçiren filtre kulanılır.
mesela piksel değerleri soldan sağa doğru 10-20-15-25 gidiyor ya
bir anda 150-200 geçtiği anda orda sert bir geçiş varya o sert geçişin olduğu yer kenardır diye düşünebiliriz.
yüksek geçiş filtresi: yüksek frekanslı içeriğin geçmesine ve düşük frekanslı içeriğin blok olmasına silinmesini sağlıyor.
kenarları yüksek frekanslı içeriklerdir.
kenar tespitinde bu kenarları korumak ve diğer her şeyi atmak, çıkarmak, silmek isiyoruz.
bu nedenle yüksek geçişli filtre kullanıyoruz. onun için de bir kernel oluşturucaz.
ilk başta sobel dediğimiz filtreyi görücez.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("1.jpeg", 0)
"""
 sobel operatörleri ortak bir gaussian filtresi kullanır ve farklılaştırma işlemi alır.
 bu nedenle gürültüye karşı daha dayanıklıdır.
 bir türev alma işlemi yapar. türev alırken de dikey ve yatay olarak türünü belirtebiliyoruz.
 kullanacağı kernel sayesinde matrix'in boyutlarını da biz belirtebiliyoruz.
"""
sobelX = cv2.Sobel(img, -1, 1, 0, ksize = 5)  # ksize'leri(matrix) tek sayı olarak giriyoruz.
# sobelX1 = cv2.Sobel(img, -1, 1, 0, ksize = -1) # ksize'yi -1 yaparsak
sobelY = cv2.Sobel(img, -1, 0, 1, ksize = 5)
# 2. parametre derinlik,
# 3. parametre: dx; x'teki kenarları bulmak için 1
# 4. parametre: dy; y'deki kenarları bulmak için 1
# 5. parametre 5x5'lik bir kernelsize ve tek sayı olarak giriyoruz.
# sobel = cv2.Sobel(img, -1, 1, 1, ksize = 5) # x ve y de ortak olarak kenar algılama olucak.

"""
neden derinliğe -1 verdik?
matrix'in sonucu pozitif çıkmayabilir. yani burda bir türev alma işlemi uygulanıyor ve 
türevde aşağı doğru bakanlar pozitif, yukarı doğru bakanlar negatif sonuç değer veriyor. 
fakat biz burda kullanırken pozitifleri almış oluyoruz.
dolayısıyla biz burda aslında aşağı bakan kısmı görmemiş oluyoruz.
bunu görmek istersek:
derinlik olarak -1 yazdığımız zaman orjinalindeki derinliği neyse poziif int sayılar neyse ona dönüştürüp elde ettiriyor.
orjinal görüntüm pozitif int sayılar olmasaydı derinliğe cv2.CV_8U yazdığım zaman yine aynı şekilde pozitif int sayıları elde edicem.
sobelX2 = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize = 5)
bunu yağtığımız zaman eğimi eksi olanları göremiyoruz onun yerine cv2.CV_64F kullanırsam eksi pikselleri de görürüz.
bunu kullandığımız zaman eğimi farklı olan pikselleri de bulduk.
bunun mutlak değerini alıcam, eksilerden kurtulucam.
mutlak değerini aldıktan sonra da bu değerler 255 üstünde ya yine pozitif int sayılar olsun 8 bitlik diye belirledik.
"""
sobelX2 = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = 5)
sobelX2 = np.absolute(sobelX2)
sobelX2 = np.uint8(sobelX2)

"""
laplacian türev alırken sobel filtresini kullanarak türev alma işlemi yapıyor ona göre kenar belirliyor.
"""
laplacian = cv2.Laplacian(img, -1)
# burda ayarlamaları kendimiz yapamıyoruz ama güzel sonuç verdi.
# ksize de ekleyebiliriz.


"""
canny: 4 tane aşamadan oluşuyor. 1. aşama olarak: 5x5'lik bir gaussian filtre uyguluyor.
gürültüleri gideriyor. daha sonra görüntünün yoğunluk grandyantını buluyor. yani düzleştiren görüntü
daha sonra yatay yönde ve dikey yönde 1. türevi elde etmek için bir sobel çekirdeğiyle filtreleniyor.
bu filtreleme işleminden sonra 3. aşamaya geçiliyor: max olmayanı sıfırlama yöntemi kullanıyor.
yani bu grandyant belirlenen görüntü de kenar oluşturabilmek için oluşturulmasını istenmeyen pikselleri kaldırmak için tam bir görüntü taraması yapılıyor.
bunun için her pikselin eğim yönünde yerel bir max olup olmadığına bakıyor.
kenar olması muhtemel her yerleri alıyor onun dışındakileri de siliyor.
daha sonra 4. aşamaya geçiyor: histerezis eğrisi denilen bir yöntem kullanılıyor.
hangi kenarların gerçekten kenar olup olmadığına karar veriliyor. bunun için min ve max değerleri biz kendimiz veriyoruz.
max değerden yüksek grandyat yoğunluğa sahip olan tüm kenarlar kesinlikle kenar sonucu çıkıyor.
min değerin altındaki kenarlar ise kesinlikle kenar değildir.
bu iki eşik arasında kalanlar bağlantılara göre kenar olup olmadığı belirleniyor.
bütün bu 4 aşamayı tek satırla yapıyoruz.
"""
canny = cv2.Canny(img, 200, 210)
# 2. parametre min değer
# 3. parametre max değer
# 200'ün altındaki hiçbir şeyi alma, 210'ün üsndeki her şeyi kenar olarak algıla
# bu ikisinin arasında kalan 10 tane değer eğer üsttteki kenara bağlanıyorsa
# 210'nun üstündeki grandayanta olan kısma da bağlanıyorsa kenar olarak algılamaya devam et demiş oluyoruz.

plt.subplot(2, 3, 1), plt.imshow(img, "gray"), plt.title("original")
plt.subplot(2, 3, 2), plt.imshow(sobelX, "gray"), plt.title("sobelX")
plt.subplot(2, 3, 3), plt.imshow(sobelY, "gray"), plt.title("sobelY")
# plt.subplot(2, 3, 4), plt.imshow(sobel, "gray"), plt.title("sobel")
plt.subplot(2, 3, 4), plt.imshow(sobelX2, "gray"), plt.title("sobelX2")  # daha fazla kenar algılamış oldu.
# plt.subplot(2, 3, 6), plt.imshow(sobelX1, "gray"), plt.title("sobelX1")
plt.subplot(2, 3, 5), plt.imshow(laplacian, "gray"), plt.title("laplacian")
plt.subplot(2, 3, 6), plt.imshow(canny, "gray"), plt.title("canny")  #

plt.show()