import cv2
import numpy as np

# DATA HAZIRLAMA
# hafrleri sayıya dönüştürücez. ascii table yazıp o siteye giriyoruz. tabloda;
# A büyük harfi 65'e tekabül ediyor. 1 1 artıyor geri kalanı.
# 1 1 arttığı için bunların hepsini okuyim 65 çıkartıyim. A sıfır olur. B:1, C: 2 olur böyle artar.
# sayılara dönüştürmüş oluruz.
# 2 yöntem var. 1.si:
# veri türünü str verdik, ayıracı virgülle olduğu için okurken virgülle ayrıldığını söylüyoruz.
"""
data = np.loadtxt("letter-recognition.data", dtype="str", delimiter=",")

# içi string olarak yer aldığı için düzenlemem gerek onun içinde bir döngü gerek.
# ilk indisini ve içinde ne olduğu değerini döndürücez.
for i, k in enumerate(data[:, 0]):
    data[:, 0][i] = ord(k)-65  # her birinde hangi indise denk geliyorsa buranın içinde dönen k değerini
    # ord ile yazınca ascii kodu decimale çevirecek yani k daki harf T (ilk indis) kaça denk geliyorsa
    # bundan -65 yaparsak 0'dan başlayıp dizmiş olucaz. A da sıfır olmuş oldu.
data = np.float32(data)  # türünü de değiştirdik.
"""

# 2. yöntem: kısa yolu
# converters ile dönüştürme işlemi yapıcaz .
# x harf olarak
data = np.loadtxt("letter-recognition.data", dtype="float32", delimiter=",",
                  converters={0: lambda x: ord(x)-65})

# datanın ilk sütunu harfleri içeriyor. diğerleri bunun özelliklerini içeriyor.
# datayı 2'ye böldük.
train, test = np.vsplit(data, 2)
# ilk sütun cevapları almak için. 1.sütundan itibaren bölüyoruz.
train_responses, trainData = np.hsplit(train, [1])
# aynısını test verileri içinde yaptık.
test_responses, testData = np.hsplit(test, [1])


# EĞİTİM

knn = cv2.ml.KNearest_create()
knn.train(trainData, cv2.ml.ROW_SAMPLE, train_responses)


# TEST
ret, results, neighbours, distance = knn.findNearest(testData, 5)

matches = test_responses == results
correct = np.count_nonzero(matches)
accuracy = correct*100.0 / results.size

print("accuracy: ", accuracy)  # doğruluk oranını verdi.


