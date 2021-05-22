import cv2
import matplotlib.pyplot as plt
resim = cv2.imread("shape_noise.png", 0)  # gürültülü resim

# görüntünün gürültüden arındırılması için
blur = cv2.GaussianBlur(resim, (15, 15), 0)  # sigma değerini 0 olarak girdik.
# ilk paramtre resim ifadesi
# 2.si matrix değeri

# resmi thresholding yapmak için
# gürültüden arındırılan resmi, treshold yaptığımız yönteme gönderiyoruz.
ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Burda bir değer dönecek, bu dönen değere göre thresh değerimiz otomatik olarak seçilecek.
# oradaki 0 değeri yerine sistem otomatik bir değer seçer.
print(ret)  # seçtiği değeri görürüz

# histogram görseldeki renk kodlarının dağılımını gösteriyor
hist = resim.ravel()
print(hist)
# sıralanmış liste için çünkü resimi tek başına hist için giremeyiz bir grafiks alacağı için
plt.hist(resim.ravel(), 256)
# ilk parametreye ravel yazdık çünkü histogramda görüntülemek için sıralaması gerekiyor.
# 2. ci parametre bunların kaç tane old. yazmak gerekiyor.
plt.show()

#cv2.imshow("resim", resim)
#cv2.imshow("th", th)
#cv2.waitKey()
#cv2.destroyAllWindows()