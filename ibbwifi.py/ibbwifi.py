import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 2023 başından 2027 sonuna kadar günlük tarih aralığı oluşturma
dates = pd.date_range(start="2023-01-01", end="2027-12-31", freq="D")
n_days = len(dates)

# 2. Gerçekçi veri simülasyonu (Trend + Mevsimsellik + Rastgelelik)
np.random.seed(42)

# Zamanla büyüyen kullanıcı trendi
trend = np.linspace(800, 3500, n_days)

# Yıllık ve haftalık kullanım dalgalanmaları
yearly_pattern = 400 * np.sin(2 * np.pi * dates.dayofyear / 365)
weekly_pattern = 150 * (dates.dayofweek >= 5) # Hafta sonu artışı

# Rastgele gürültü
noise = np.random.normal(0, 200, n_days)

# Toplam günlük yeni kullanıcı sayısı
subscribers = np.maximum(trend + yearly_pattern + weekly_pattern + noise, 100).astype(int)

# DataFrame oluşturma
df = pd.DataFrame({
    "Tarih": dates,
    "Yeni_Kullanici_Sayisi": subscribers
})

# CSV dosyası olarak kaydetme
df.to_csv("ibb_wifi_subscriber_2027.csv", index=False)
print("Veri seti oluşturuldu: 'ibb_wifi_subscriber_2027.csv'")

# 3. Görselleştirme (2027 Yılı Vurgulu)
plt.figure(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# Tüm veri çizimi
plt.plot(df["Tarih"], df["Yeni_Kullanici_Sayisi"], color="#0077b6", alpha=0.7, label="Günlük Yeni Kullanıcı")

# 2027 yılını belirginleştirmek için arka plan renklendirmesi
plt.axvspan(pd.Timestamp("2027-01-01"), pd.Timestamp("2027-12-31"), color="#ffb703", alpha=0.2, label="2027 Yılı Verisi")

plt.title("İBB WiFi Günlük Yeni Kullanıcı Verisi (2023 - 2027)", fontsize=14, fontweight="bold")
plt.xlabel("Tarih", fontsize=12)
plt.ylabel("Yeni Kullanıcı Sayısı", fontsize=12)
plt.legend(loc="upper left")
plt.tight_layout()

plt.show()