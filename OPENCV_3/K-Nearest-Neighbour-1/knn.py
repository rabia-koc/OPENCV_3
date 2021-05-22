# KNN
# K-Nearest Neighbour Algorithm
# K En Yakın Komşu Algoritması

import cv2
import numpy as np
from matplotlib import pyplot as plt

# eğitim dataları
# 0'dan başla 100'e kadar
# 25 tane içinde x ve y bulunan data var.
trainData = np.random.randint(0, 100, (25, 2)).astype(np.float32)

# cevaplar: 0 ile 2 arasında kırmızı ya da mavi sınıfımız var.
# 25 tane olucak ve 1 boyuttur. ya 0'dır ya 1'dir.
responses = np.random.randint(0, 2, (25, 1)).astype(np.float32)

# traindata içinde responsesleri döndürücek ve neye eşitse o renktir.
# ravel ekleyince soldan sağa doğru sıralanmış oldu yani tek bir satırda.
red = trainData[responses.ravel() == 0]
blue = trainData[responses.ravel() == 1]

# bu verileri çizdirmek için
# x:0 için y lerde 1 için yazdık.
# boyut: 80
plt.scatter(red[:, 0], red[:, 1], 80, 'r', '^',
            label="red-0", alpha=0.4)
plt.scatter(blue[:, 0], blue[:, 1], 80, 'b', 'o',
            label="blue-1", alpha=0.4)

# yeni bir veri getirdik.
# boyut 1 tane
new_data = np.random.randint(0, 100, (1, 2)).astype(np.float32)

plt.scatter(new_data[:, 0], new_data[:, 1], 80, 'g', 's',
            label="new", alpha=1)

# bir tane K' ya en yakın sınıf algoritmasını, en yakın komşu algoritmasını oluşturmasını söylüyoruz.
knn = cv2.ml.KNearest_create()

# traindatadan eğitilecek
# 2. parametre: bu verilerin nasıl sıralandığı: buradaki örneklerimin satırlarda sıralandığını söylüyoruz.
# 3. parametre: her bir verinin gerçek sınıfını yazmak gerekiyor.
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

# bu model üzerinde yeni datamızın tahminini yaptırıcaz.
# k değerini 3 verdik.
# burda 4 tane parametre döndürüyor.
ret, results, neighbours, distance = knn.findNearest(new_data, 3)

# bu 4 değere göre burada yazdırma işlemi yapıyoruz.
# ret: hangi sınıfa ait olduğunu söylüyor.
# result: bunların liste halleri mesela 0. sınıfa ait olmuş olduğunu veren liste.
# neighbours: en yakın komşular. k'yı 3 verdiğimiz için 3 tane en yakın komşu sıralandı.
# distance: 3 tane sınıfın mesafeleri
print("*"*40)
print("""
      ret: {}
      results: {}
      neighbours: {}
      distance: {}
      """.format(ret, results, neighbours, distance))
print("*"*40)

plt.legend()  # labellerin gözükmesi için.
plt.show()