import time
import cv2
import numpy as np
from PIL import ImageGrab

# Arka plan çıkarıcı (Hareketli araçları algılar)
object_detector = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=40
)

print(
    "1. Tarayıcınızdan istediğiniz kamera yayınını açın ve ekranınızda görünür yapın."
)
print("2. Başlatmak için bu terminale gelip ENTER'a basın...")
input()

print("\nAraç/Hareket takibi başladı. Durdurmak için 'q' tuşuna basın.")

while True:
    # Tüm ekranın anlık görüntüsünü al
    screenshot = ImageGrab.grab()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Hareket maskesi oluştur ve gürültüleri temizle
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    # Kontur tespiti
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    arac_sayisi = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Belli bir piksellerden büyük hareketli alanları araç olarak kabul et
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            arac_sayisi += 1 

    # Anlık araç sayısını yazdır
    cv2.putText(
        frame,
        f"Tespit Edilen Hareketli Arac: {arac_sayisi}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

    # İşlenen görüntüyü göster
    resized = cv2.resize(frame, (960, 540))
    cv2.imshow("Canli Arac Sayim Penceresi", resized)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()