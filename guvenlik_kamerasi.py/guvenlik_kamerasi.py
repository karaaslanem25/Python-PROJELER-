import cv2
import numpy as np
import winsound  # Windows dahili ses sistemi (Linux/Mac için os.system veya pygame kullanılabilir)
import datetime

# Kamerayı başlat (0: Varsayılan bilgisayar kamerası)
cap = cv2.VideoCapture(0)

# Hareket algılama hassasiyeti (Piksel farkı eşiği)
SENSITIVITY = 5000 

print("Kamera başlatıldı. Çıkmak için 'q' tuşuna basın.")

while cap.isOpened():
    # Kare 1 ve Kare 2'yi oku (Hareket kıyası için)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    if not ret:
        break

    # İki kare arasındaki farkı bul
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        # Belirli bir alandan büyük hareketler için
        if cv2.contourArea(contour) < SENSITIVITY:
            continue

        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # Hareket eden bölgeye kırmızı kutu çiz
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if motion_detected:
        # Zaman damgası ve Uyarı Yazısı
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame1, f"HAREKET ALGILANDI! [{time_str}]", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # Bip Sesi Çal (Frekans: 2500Hz, Süre: 200ms)
        winsound.Beep(2500, 200)

    # Görüntüyü ekrana bas
    cv2.imshow("Güvenlik Kamerası", frame1)

    # 'q' tuşuna basınca kapat
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()