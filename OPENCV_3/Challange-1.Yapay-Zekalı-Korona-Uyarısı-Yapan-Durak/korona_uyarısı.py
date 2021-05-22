import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")


korona = cv2.imread("aa.png")
yazi_maskeli = cv2.imread("yazi.png")
yazi_maskesiz = cv2.imread("yazi2.png")

korona_gray = cv2.cvtColor(korona, cv2.COLOR_BGR2GRAY)  # renkli resmi gri yaptık.
ret, mask = cv2.threshold(korona_gray, 5, 255, cv2.THRESH_BINARY)
# gri görüntüyü eşik değerinden geçirdik. 5'in altındaki değerler 0 oldu. yani siyah.


cv2.namedWindow("Mask Detection")

cam = cv2.VideoCapture(0)

cam_x, cam_y = int(cam.get(3)), int(cam.get(4))
# kameramın boyutlarını get ile almış oldum. float döndükleri için int yaptık.

cerceve = np.zeros((cam_y+200, cam_x, 3), np.uint8)
""" resmimi yerleştirmek için boş bir çerçeveye ihtiyacım var. 3 renk kanalına sahip olduğunu da yazık.
    kamera boyutumla aynı siyah boş bir çerçeve oluştu.
    kamera görüntümü 640,480 olarak varsaydım. yukardan aşağısı 680 boyutunda olucak.
    bu yüzden alt tarafta 200'lük fazlalık olucak. onu da y kısmına ekledik.
    artık kamera görüntümüzden 200 piksel daha fazla olan bir çerçevemiz var.
    çerçeveni 200 piksel olan kısmına yazılar gelecek.
    yazıların boyutlarını ayarladık."""

yazi_maskeli = cv2.resize(yazi_maskeli, (cam_x, 200))
yazi_maskesiz = cv2.resize(yazi_maskesiz, (cam_x, 200))

while cam.isOpened():
    ret, frame = cam.read()
    video = frame.copy()
    
    if not ret:
        print("haydaa")

    """ boş çerçevenin alt tarafına maskeli olan resim otomatik olarak yerleşecek sürekli bir
        döngü halinde hep çıkacak, eğer maskesiz insan varsa değişecek. """
    cerceve[-200:, :] = yazi_maskeli
    cerceve[:-200, :] = video
    
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 7)
    
    if(len(faces) == 0):
        print("no face found")
    else:
        for x, y, w, h in faces:
            roi_gray = gray_image[y:y+h, x:x+w]
            roi = frame[y:y+h, x:x+w]
            
            mouth = mouth_cascade.detectMultiScale(roi_gray, 1.4, 15)
            
            if(len(mouth) == 0):
                print("maske takılı")
            else:
                print("maskenizi takın")
                cerceve[-200:, :] = yazi_maskesiz
                dsize = (w, h)
                # yüzün değerleri değiştiği için buradaki korona resmimde boyutların değişmesi gerek.
                # buradaki mask'enin boyutları da sürekli değişmesi gerek.
                
                korona_resize = cv2.resize(korona, dsize)
                # renkli resmi kullanacağımız için tekrar boyutunu boyutlandırmak gerekiyor.
                # yüzün boyutuna göre görsel otomatik boyutlanacak.

                mask_resize = cv2.resize(mask, dsize)
                mask_inv = cv2.bitwise_not(mask_resize)  # mask' ede 0'ları 1, 1'leri 0 yaptık.
                
                
                img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
                # yüzümüzün olduğu renkli kısım: roi
                # mask'nin terslenmiş halini çarpıyoruz.

                img2_fg = cv2.bitwise_and(korona_resize, korona_resize, mask=mask_resize)  # koronanın tekrar boyutlandırılmış hali.
                
                toplam = cv2.add(img1_bg, img2_fg)  # ikisini topladık.
                
                video[y:y+h, x:x+w] = toplam  # ana görsel üzerinde yüzün olduğu kısma ekleme yaptık.
                
                cerceve[:-200, :] = video    # yazılı kısma ekleme işlemi yaptık.
                
                
    cv2.imshow("Mask Detection", cerceve)
    
    if cv2.waitKey(33) & 0xFF == ord("q"):
        print("by")
        break



cam.release()
cv2.destroyAllWindows()