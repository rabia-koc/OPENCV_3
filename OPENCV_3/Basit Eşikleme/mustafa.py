
# eğer bizim verdiğimiz thresh değerinden yüksek bir değer varsa maxval eşitle
# eğer yoksa 0'a eşitle
#   THRES_BINARY
# dst(x, y) = { maxval     if src(x, y) > thresh
#             {  0         otherwise

# bunları kullanıcı olarak girerek threshold işlemini döndürücez.
def threshold(src, thresh, maxval):
    """
    Bu fonksiyon ile basit eşikleme işlemi yapılabir.
    src = image
    thresh = 0...255
    maxval = 0...255
    """
    img = src.copy()  # resmi kopyaladık. çünkü ilerde ana resmi kullanırken bir değişiklik olmaması için

    # img'in tüm değerleri pikselleri üzerinde gezmek için;
    # shape'nin ilk 2 terimini alıyorum.
    rows, cols = img.shape[:2]
    for i in range(rows):
        for j in range(cols):
            if img[i, j] < thresh:
                img[i, j] = 0
            else:
                img[i ,j] = maxval
        """
         bu resmin satır ve sutünlarının geldiğimdeki piksel değeri benim verdiğim thresh değerinden küçükse bunu o pikseldeki bu değeri 0 yap,
         eğer büyükse pikseldeki bu değeri benim verdiğim max değer yap.
         bunu yaptıktan sonra benim bu değeri geri döndürmem gerekiyor.
        """
    return thresh, img