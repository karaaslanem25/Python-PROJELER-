from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ZaferBayramiProjesi:

  def __init__(self):
    self.bugun = datetime.now()
    self.mesaj = (
        "30 Ağustos Zafer Bayramı Kutlu Olsun! Ne Mutlu Türküm Diyene 🇹🇷"
    )

  def bayram_kutlama_banneri(self):
    """Konsol ekranına şık ve dikkat çekici bir kutlama banner'ı basar."""
    print("*" * 65)
    print(f"* {self.mesaj} *")
    print("*" * 65)
    print(f"Sistem Tarihi: {self.bugun.strftime('%d.%m.%Y')}\n")

  def tarihi_veri_analizi(self):
    """Tarihsel verileri Pandas kullanarak simüle eder ve özetler."""
    # Tarihsel olayları ve katılım/etki verilerini temsil eden örnek veri seti
    veri = {
        "Yil": [1922, 1926, 1930, 1950, 1980, 2020, 2026],
        "Etkinlik_Turu": [
            "Büyük Taarruz Zaferi",
            "İlk Resmi Kutlama",
            "Anıtsal Adımlar",
            "Gelenekselleşme",
            "Modern Kutlamalar",
            "Dijital/Kapsamlı",
            "104. Yıl Coşkusu",
        ],
        "KatilimEndeksi": [85, 90, 92, 95, 97, 99, 100],
    }

    df = pd.DataFrame(veri)

    print("--- 30 AĞUSTOS TARİHSEL ETKİ VE KUTLAMA ENDEKSİ ---")
    print(df.to_string(index=False))
    print("-" * 50)
    return df

  def bayram_grafigi_cizdir(self, df):
    """Kutlama ve katılım endeksini grafikleştirerek görselleştirir."""
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(10, 5))

    # Çizgi grafik ile yıllara göre katılım/coşku artışı
    plt.plot(
        df["Yil"],
        df["KatilimEndeksi"],
        marker="o",
        color="crimson",
        linewidth=3,
        markersize=8,
    )
    plt.title(
        "30 Ağustos Zafer Bayramı Kutlama ve Coşku Endeksi (Yıllara Göre)",
        fontsize=13,
        fontweight="bold",
    )
    plt.xlabel("Yıllar", fontsize=11)
    plt.ylabel("Coşku / Katılım Seviyesi", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Grafiği kaydetme
    dosya_adi = "30_agustos_zafer_bayrami.png"
    plt.savefig(dosya_adi, dpi=300, bbox_inches="tight")
    print(
        f"\n[BILGI] Anlamlı grafik '{dosya_adi}' adıyla başarıyla kaydedildi."
    )
    plt.show()


# ==========================================
# PROJEYİ ÇALIŞTIRMA KISMI
# ==========================================
if __name__ == "__main__":
  zafer_projesi = ZaferBayramiProjesi()

  # Adımları sırasıyla çalıştır
  zafer_projesi.bayram_kutlama_banneri()
  analiz_df = zafer_projesi.tarihi_veri_analizi()
  zafer_projesi.bayram_grafigi_cizdir(analiz_df)