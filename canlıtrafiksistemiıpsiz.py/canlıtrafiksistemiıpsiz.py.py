import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

# =========================
# 🔴 CANLI VERİ SİMÜLASYONU
# =========================

def generate_traffic_data():
    times = []
    values = []

    for i in range(30):  # 30 saniyelik simülasyon
        current_time = datetime.now().strftime("%H:%M:%S")
        intensity = np.random.randint(10, 120)

        times.append(current_time)
        values.append(intensity)

        # anlık durum
        if intensity > 90:
            print(f"🚨 YOĞUN TRAFİK | {current_time} | {intensity}")
        elif intensity > 60:
            print(f"⚠️ ORTA TRAFİK | {current_time} | {intensity}")
        else:
            print(f"🟢 AKICI | {current_time} | {intensity}")

        time.sleep(1)

    return pd.DataFrame({
        "time": times,
        "intensity": values
    })


# =========================
# 📊 ANALİZ
# =========================

def analyze(df):
    print("\n📊 ORTALAMA TRAFİK:", df["intensity"].mean())
    print("🚦 EN YOĞUN ZAMAN:", df.loc[df["intensity"].idxmax(), "time"])


# =========================
# 📈 GRAFİK
# =========================

def plot(df):
    plt.figure(figsize=(12,5))
    plt.plot(df["time"], df["intensity"], marker="o")

    plt.title("Canlı Trafik Yoğunluğu Simülasyonu")
    plt.xlabel("Zaman")
    plt.ylabel("Yoğunluk")
    plt.xticks(rotation=45)
    plt.grid()

    plt.tight_layout()
    plt.show()


# =========================
# 🚀 ANA ÇALIŞTIRMA
# =========================

df = generate_traffic_data()
analyze(df)
plot(df)