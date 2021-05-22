import cv2
import matplotlib.pyplot as plt

# resim okuma işlemi olucak ve içine resmin konumunu gir
resim = cv2.imread("gradient.jpg",0) # siyah beyaz okumak için 0 koydum.

# threshold işlemi
_, resim_thresh1 = cv2.threshold(resim, 182, 255, cv2.THRESH_BINARY)  # 182'nin altında olanları sıfır yapıyor.

_, resim_thresh2 = cv2.threshold(resim, 182, 255, cv2.THRESH_BINARY_INV) # terslenmiş hali. 182'nin üstünde olanları sıfır(255) yapıyor.

_, resim_thresh3 = cv2.threshold(resim, 182, 255, cv2.THRESH_TRUNC) #  Kes anlamı olan hali
# 182'nin üstü olan yerleri 255 yapmış, altında olan yerleri ise önceki hali ile bırakmış kesmiş

_, resim_thresh4 = cv2.threshold(resim, 182, 255, cv2.THRESH_TOZERO)
# 1822nin altında olanları 0 yapmış, üstünde olanları aynı bırakmış

_, resim_thresh5 = cv2.threshold(resim, 182, 255, cv2.THRESH_TOZERO_INV)
# tozero'nun terslenmiş hali

resimler = [resim, resim_thresh1, resim_thresh2, resim_thresh3, resim_thresh4, resim_thresh5]

basliklar = ["original resim", "binary", "binary_inv", "trunc", "to_zero", "to_zero_inv"]
for i in range(6):
    plt.subplot(2, 3, i+1)
    plt.imshow(resimler[i], "gray")
    plt.title(basliklar[i])

plt.show()