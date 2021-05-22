import cv2

car_cascade = cv2.CascadeClassifier("cars.xml")
cam = cv2.VideoCapture("car1.avi")

def main():

    while cam.isOpened():

        ret, frame = cam.read()

        if not ret:
            print("done")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # videoyu griye çeviriyoruz.

        gray = cv2.equalizeHist(gray)
        # görüntünün daha da kontrastını arttırmak için ayrıntıları göstermek için yapılan bir işlem

        cars = car_cascade.detectMultiScale(gray, 1.1, 2)  # arabaları tespit ediyoruz.

        # arabadaki değerleri çekip çizdirme işlemi yapıcaz.
        for x, y, w, h in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
            frame[y:y + h, x:x + w, 2] = 255  # içini boyamak için bgr olarak düşündük.

        cv2.imshow("frame", frame)

        if cv2.waitKey(33) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


# neden def main() içine aldık. kod burda çalışıyor ama başka tarafta import edersek çalışmayack.
# bunun sayesinde eğer bir dosya import ediliyorsa buradaki ismi değiştiği için buarda if __name__ kısmına eşitlemediği için çalışmayacak.
# başka bir dosyada import ettiğim zaman maini çağırmadan bu kodlar çalışmayacak.