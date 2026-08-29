import cv2
import numpy as np
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

canvas = None
kivilcimlar = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Neon izin zamanla kaybolması
    canvas = cv2.addWeighted(canvas, 0.92, np.zeros((h, w, 3), dtype=np.uint8), 0.08, 0)

    # Ten rengi tespiti (HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    alt_ten = np.array([0, 20, 70], dtype=np.uint8)
    ust_ten = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, alt_ten, ust_ten)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 4000:
            # En uç noktayı (parmak ucu) tespit et
            en_ust_nokta = tuple(max_contour[max_contour[:, :, 1].argmin()][0])
            px, py = en_ust_nokta

            # X konumuna göre renk
            hue = int((px / w) * 179)
            renk_hsv = np.uint8([[[hue, 255, 255]]])
            renk_bgr = cv2.cvtColor(renk_hsv, cv2.COLOR_HSV2BGR)[0][0]
            renk = (int(renk_bgr[0]), int(renk_bgr[1]), int(renk_bgr[2]))

            # Parmağın ucuna neon halka ve tuvala çizim
            cv2.circle(frame, (px, py), 15, renk, -1)
            cv2.circle(frame, (px, py), 25, (255, 255, 255), 2)
            cv2.circle(canvas, (px, py), 12, renk, -1)

            # Kıvılcımlar
            for _ in range(3):
                kivilcimlar.append({
                    "x": px,
                    "y": py,
                    "vx": random.randint(-8, 8),
                    "vy": random.randint(-8, 8),
                    "renk": renk,
                    "omur": 15
                })

    # Kıvılcımları Çiz
    yeni_kivilcimlar = []
    for k in kivilcimlar:
        k["x"] += k["vx"]
        k["y"] += k["vy"]
        k["omur"] -= 1
        if k["omur"] > 0:
            cv2.circle(frame, (k["x"], k["y"]), random.randint(2, 5), k["renk"], -1)
            yeni_kivilcimlar.append(k)
    kivilcimlar = yeni_kivilcimlar

    kombine = cv2.addWeighted(frame, 0.7, canvas, 1.0, 0)
    cv2.imshow("Serbest Neon El Oyunu", kombine)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()