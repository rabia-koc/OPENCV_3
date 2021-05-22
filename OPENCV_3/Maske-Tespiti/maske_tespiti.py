import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # yüz tespit için
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")   # ağız tespit için

org = (30, 30)
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
weared_mask = "Thank you for wearing MASK"
not_weared_mask = "Please wear MASK to defeat CORONA"

cap = cv2.VideoCapture(0)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("haydaa")
        
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # görüntüyü gri tonlamaya çevirdik.
    
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 7)
    """ birden fazla yüz olabilir. yüz seçmek için
        1. parametre: küçültme oranı
        2. parametre: doğruluk oranı"""

    """ boyutuna bakıyoruz. 0'a eşit ise hiçbir yüz bulunamadı demektir.
        org: koordinat demek
        color: beyaz, kalınlık:2"""
    if(len(faces) == 0):
        cv2.putText(frame, "No face found", org, fontFace, 
                    fontScale, (255, 255, 255), 2)
    # yüz tespit edilmişse:
    else:
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h),
                          (255, 0, 0), 2)
            # roi: kırpma işlemi, yüzümü kestik
            roi_gray = gray_image[y:y+h, x:x+w]
            mouth = mouth_cascade.detectMultiScale(roi_gray, 1.4, 15)  # kesilen yüz resmi içinde ağız seçiyor.

            i = 0 # birden fazla ağız seçtiği için yazdık.
            if(len(mouth) == 0):
                cv2.putText(frame, weared_mask, org, fontFace, fontScale, (0, 255, 0), 2, cv2.LINE_AA)
                # maske takılı, ağız bulunamadı.

            # maske takılı değilse, ağız bulundu. ağız işaretleme yaptık.
            else:
                cv2.putText(frame, not_weared_mask, org, fontFace, fontScale, (0, 0, 255), 4, cv2.LINE_AA)  # bir mesaj yazdık.
                for mx, my, mw, mh in mouth:
                    if i == 0:
                        i+=1  # böylece i sıfırın dışına çıktığı için tek bir tane ağız çizmiş olacak.
                        cv2.rectangle(frame, (mx+x, my+y), (mx+x+mw, my+y+mh), (0, 0, 255), 3)
                        """ koordinatlara 2. ve3. parametrelere x ve y ekledik. çünkü:
                            roi işleminde suratımın olduğu alanı kırpıyorum. Kırptığım alan üzerinde ağız buluyorum.
                            Mesala ağzımın koordinatı 30,100 olsun ama ana resimde yani büyük resimde çizdirdiğim için
                            büyük resimde 30,100 arka planda bi yere denk geliyor. Dolayısıyla, ana resimde yüzümü tespit ettiğim
                            x, y koordinatını ağzımı tespit ederken artı olarak eklersem koordinatlara otomatikman istediğim yere denk getirmiş olacağım."""
                    else:
                        pass
        
    cv2.imshow("Mask Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("by")
        break



cap.release()
cv2.destroyAllWindows()