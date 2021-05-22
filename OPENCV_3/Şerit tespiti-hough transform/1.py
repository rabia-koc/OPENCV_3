import cv2
import numpy as np

cam = cv2.VideoCapture("car1.mp4")
sapma = 100
kernel = np.ones((3, 3), dtype=np.uint8)


# kırpma işlemlerini bir fonksiyona atıyoruz. ilk başta kırpacağım alanın olduğu kısmı bana geri döndüren bir matris olarak döndüren bir şey yapmak istiyorum.
def crop_matris(img):
    x, y = img.shape[:2]  # resmin ilk 2 parametrisini aldık.
    value = np.array([
       [(sapma, x - sapma), (int((y * 3.2) / 8), int(x * 0.6)),
         (int((y * 5) / 8), int(x * 0.6)), (y, x - sapma)]], np.int32)
    return value
# ilk y yi düşünürsek sapma belirledik. ordan başlar. 2. kısımda x'te ful aşağı doğru ama sapma kadarda yukarı çıkması gerek.

# bir matris geriye döndürücez. ,
def crop_image(img, matris):
    # siyah bir mask oluşturucaz onun üzerine bu matrislerin olduğu kısmı beyaz olarak yerleştiricez.
    # mask'nin boyutunu da görselin boyutuyla oluşturduk.
    x, y = img.shape[:2]
    mask = np.zeros(shape=(x, y), dtype=np.uint8)
    # bu maske üzerine matrisi çizme işlemi oluşturucaz.
    mask = cv2.fillPoly(mask, matris, 255)   # ilk parametre: resim, 2.parametre: pointler noktalar, 3. parametre: renk
    mask = cv2.bitwise_and(img, img, mask=mask)   # mask'eyle görüntüyü çarpıp o kısmı alacağız.
    return mask


# parabolsigline kullanıcaz. ilk başta giderken siyah beyaz görüntü ve kenarları algılanmış görüntü gönderiyorduk normalde.
# parabolün içinde dahili vardı. ama parametreleri biz kendimiz ayarlıcaz.
# içine görsel gelicek ama görsel renkli bir görüntü. griye çeviricez.
def filt(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # griye çevirdikten sonra direk parlak kısımları kırpmak istiyoruz.
    img = cv2.inRange(img, 150, 255)  # 150 ile 255 arasında ise buranın 1 olmasını, değilse 0 olmasını sağlıcaz.
    img = cv2.erode(img, kernel)      # resimdeki küçük noktaları silmek için
    img = cv2.dilate(img, kernel)     # resmi büyültmek için
    img = cv2.medianBlur(img, 9)
    img = cv2.Canny(img, 40, 200)
    return img

# çizgi belirlerken çok fazla çizgi belirleyebilir. şeridi bir tane çizmek için:
# orada tüm belirlediği çizgilerin bir ortalamasını alıcaz, ortalama aldıktan sonra
# ortalaması alınmış bir tane çizgi koordinatları çıkıcak. sadece o çizgiyi çizicez.

def line_mean(lines):
    left = []
    right = []
    # her bir çizginin üzerinde gezme işlemi yapıcaz.
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2-y1)/(x2-x1)  # eğim belirledik. eğim bize bu çizginin sağa mı sola mı yatık olduğu bilgisini vericek.

        # çizgi tespit ederken çizgilerin yatay olanları da tespit edilecek.
        # yatay olanların değerleri de 0' a çok yakın çıkıcak. dolayısıyla 0' a yakın çıkarken
        # yatay olanları almak istemiyorum. belirli bir eğime sahip olanları almak istiyorum.
        # -0.2'den küçükleri ve 0.2'den büyükleri alarak bir eşik değeri belirlemiş oluruz.
        # bu eşik değerlerinin arasındakileri almıcaz. yatay çizgiler olduğu için.
        if slope < -0.2:
            # eğimi sola doğrudur bu da sağ şerit demektir.
            right.append((x1,y1,x2,y2))
        elif slope > 0.2:
            left.append((x1,y1,x2,y2))

        # toplanmış çizgiler var bu çizgiler üzerinde işlem yapıcaz.
        right_mean = np.mean(right, axis=0)
        left_mean = np.mean(left, axis=0)

        # çizgin ortalaması nan değer döndürebilir. o yüzden koruma koduyla geri döndürme işlemi yapıcaz.
        # burası 0'a bölme uyarısı verebilir!
        # türü nan değilse türü var demektir.
    if not isinstance(right_mean, type(np.nan)):
        if not isinstance(left_mean, type(np.nan)):
            return right_mean, left_mean
        # diyelim ki içinde left yok sadece right döndürecek
        else:
            return right_mean, None
        # right olmayabilir tekrar left sorgulucaz.
    else:
        if not isinstance(left_mean, type(np.nan)):
            return None, left_mean
        # tam aksi durum varsa 2'sinin none değer döndürdüğü durum olucak.
        else:
            return None, None

def draw_line(img, line):
    # içeri gelen resmin line'nı küsüratını yuvarlayalım.
    # türünü de int32 yaptık çünkü resmin içindeki koordiantları 1000'ne binlik bir resim olabilir.
    line = np.int32(np.around(line))
    x1, y1, x2, y2 = line   # line'nın içinden koordinatları çekiyoruz.
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 10)  # kalınlık 10
    return img

# görselin üzerine biz nereyi çiziyorsak o alanı keselim.
# hangi alana baktığımızı bir çokgen çizerek yani görüntünün üzerinde hangi alanda çizgi arıyorsak oraya çokgen çizelim.
# içine gelen matrisin değerlerine göre tekrar matris oluşturuyoruz.
def draw_polylines(img, matris):
    dst = np.array([[matris[0][1, 0], matris[0][1, 1]],
                    [matris[0][0, 0], matris[0][0, 1]],
                    [matris[0][3, 0], matris[0][3, 1]],
                    [matris[0][2, 0], matris[0][2, 1]]], np.int32)
    cv2.polylines(img, [dst], True, (0, 255, 255), 2)   # oluşturduğumuz matrisi de oraya bir şekil çizmek için kullanıyoruz.
    return img


def pers(img, matris, resize_x=300, resize_y=200):
    x, y = img.shape[:2]

    # kaynak pointleridir. belirli noktalardan kesme işlemi olacağı için koordinatları gerekiyor.
    src = np.float32([
        [matris[0][1, 0], matris[0][1, 1]],
        [matris[0][2, 0], matris[0][2, 1]],
        [matris[0][0, 0], matris[0][0, 1]],
        [matris[0][3, 0], matris[0][3, 1]]])

    # oluşacak resmin koordinatları
    dst = np.float32([
        [0, 0],
        [y-1, 0],
        [0, x-1],
        [y-1, x-1]])

    M = cv2.getPerspectiveTransform(src, dst)  # pointlerle bir matris oluşturduk.
    img_output = cv2.warpPerspective(img, M, (y, x))
    # oluşan resmi resmin sol üst köşesine yerleştireceğimiz için boyutlarının küçülmesi gerek.
    img_output = cv2.resize(img_output, (300, 200))
    return img_output

while cam.isOpened():
    ret, image = cam.read()
    if not ret:
        print("bitti")
        break

    img_org = image.copy()

    matris = crop_matris(image)  # matrisi elde ettik. elde ettiğimiz matrisi crop_image içine göndericez. orda da bize resim geriye döndürecek.
    img = crop_image(image, matris)
    img_org[:200, 300:600] = cv2.resize(img, (300, 200))
    img = filt(img)  # kenarları algıladık.

    # kenarları algılanan kısımda çizgi tespiti yapabiliriz.
    # 2. parametre: r değeri çözünürlük, 3. theta, 4. threshold değeri, 5. min uzunluk,
    # 6. pikseller arası boşlukların ne kadar fazla olursa bir çizgi olarak algılanmasını sağlıyor.
    lines = cv2.HoughLinesP(img, 1, np.pi / 180, 20,
                            minLineLength=5, maxLineGap=200)

    img_org[:200, :300] = pers(img_org, matris)  # persin içine gönderdik.

    image = draw_polylines(img_org, matris)  # şekli kırpma işlemi yapacağımız için içine saf resim lazım.


    # eğer çizgiler varsa;
    if lines is not None:
        # burda sol ve sağ çizgiler ortalaması alınmış olarak bize gelecek.
        # bu geldikten sonra çizme işlemini yapıcaz.
        right_line, left_line = line_mean(lines)
        # none dönmemişse çizme işlemi yap. image resmimize çizme işlemi yap.
        if right_line is not None:
            image = draw_line(image, right_line)  # ana resmimimiz üzerinde yani image
        if left_line is not None:
            image = draw_line(image, left_line)

    cv2.imshow("image", image)
    #cv2.imshow("img", img)


    key = cv2.waitKey(16) & 0xFF
    # videom: 60 fps. 1 saniyede 60 tane var demektir. 1/60 = 16 ms bekleme süresi olmuş oluyor.
    if key == ord("q"):
        print("kapatıldı")
        break

cam.release()
cv2.destroyAllWindows()