import cv2
import numpy as np

img = cv2.imread("digits.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# DATAMIZI HAZIRLIYORUZ

# soldan sağa doğru 100 tane veri olduğu için 100'e böldük ve her bir verimi listelemiş olduk.
cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]  # her bir sayı için 5 tane bölme var. 10 tane verim var. 5x10:50
x = np.array(cells)  # listeyi matris yaptık.

train = x[:, :90].reshape(-1, 400).astype(np.float32)
# baştan 90'na kadar böldük. reshapede ilk kısmı öncekiyle aynı kalsın, 2. kısmı: 20x20=400 yaparak düzleştiriyor.
# x'in içinde 4500 tane 20x20'lik görsel var. 4500 aynı kalsın diğer kısmı 20x20'liği düzleştir.
# 500 tane test verimiz kalır.
test = x[:, 90:100].reshape(-1, 400).astype(np.float32)

# 0'dan 10'na kadar oluşturacağımız için bir liste hazırladık. bu listeyle verilerimi yapıcam.
k = np.arange(10)

# yanıtları döndürmek için: her bir değer için 250 tane oluşturmasını söylüyoruz.
# yukardan aşağı sıralaması için reshape yaptık.
train_responses = np.repeat(k, 450).reshape(-1, 1)  # 4500 olduğu için 4500/10:450 yazdık.

# test_responses = train_responses.copy()  # 2'sini yarı yarıya böldüğümüzde böyle de yapabiliriz.
test_responses = np.repeat(k, 50).reshape(-1, 1)  # geriye 500 tane kaldığı için 500/10:50 yazdık.

# DATA KAYIT ETME
np.savez("knn_data.npz", train_data=train, train_label=train_responses)
# hangi isimlerle kayıt edeceğimizi yazdık.

# DATA OKUMA
with np.load("knn_data.npz") as data:
    print(data.files)
    train = data["train_data"]
    train_responses = data["train_label"]


# EĞİTİM

knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_responses)
ret, results, neighbours, distance = knn.findNearest(test, 5)  # 2500 tane data üzerinde yapıcaz.

matches = test_responses == results  # true false yanıtlarının olduğu bir liste döner.
correct = np.count_nonzero(matches)  # sadece true olanları sayar.
accuracy = correct*100.0 / results.size  # burdan oranını buluruz. adedine böldük.
# böyle yaparak doğruluğu buluruz.
print("accuracy: ", accuracy)
# test datalarım azaldı, traindatalarım büyüdüğü zaman doğruluk daha da arttı.

# Eğitilen modeli kayıt etmek
knn.save('KNN_Trained_Model.yml')

# modeli okuma
knn = cv2.ml.KNearest_load('KNN_Trained_Model.yml')

# Kendimiz Test Edelim

def test(img):
    img = cv2.medianBlur(img, 21)  # 21 size değeri
    img = cv2.dilate(img, np.ones((15, 15), np.uint8))
    cv2.imshow("img", img)
    img = cv2.resize(img, (20, 20)).reshape(-1, 400).astype(np.float32)
    # resmi 20'ye 20'ye çevirip daha sonra resmi reshape yap.
    ret, results, neighbours, distance = knn.findNearest(img, 5)  # resmi yerleştirip sonucu alabilirim.

    # tahmin yaptıktan sonra img2 içine yazıyoruz. return değerini yazıyoruz.
    cv2.putText(img2, str(int(ret)), (100, 300), font, 10, 255, 4, cv2.LINE_AA)
    return ret


cizim = False
mod = False
xi, yi = -1, -1
font = cv2.FONT_HERSHEY_SIMPLEX
img = np.ones((400, 400), np.uint8)

def draw(event, x, y, flags, param):
    global cizim, xi, yi, mod
    
    if event == cv2.EVENT_LBUTTONDOWN:
        xi, yi = x, y
        cizim = True
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if cizim:
            if mod:
                cv2.circle(img, (x, y), 10, 255, -1)  # renkli görüntü olmadığı için 255 yaptık.
            else:
                cv2.rectangle(img, (xi, yi), (x, y), 255, -1)
        else:
            pass
    
    elif event == cv2.EVENT_LBUTTONUP:
        cizim = False

    # resmimi tekrar sıfırlaması için
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        img[:, :] = 0


cv2.namedWindow("paint")
cv2.setMouseCallback("paint", draw)

while(1):
    img2 = np.ones((400, 400), np.uint8)  # remin sürekli yenilenmesi için buraya yazdık.
    key = cv2.waitKey(33) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("m"):
        mod = not mod

    print(test(img))
    cv2.imshow("paint", img)
    cv2.imshow("result", img2)
    
cv2.destroyAllWindows()





