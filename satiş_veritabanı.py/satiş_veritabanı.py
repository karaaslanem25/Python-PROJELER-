import sqlite3
import random
from datetime import datetime, timedelta


# ============================================================
# AYARLAR
# ============================================================

DB_NAME = "satis_veritabani.db"

MUSTERI_SAYISI = 1000
URUN_SAYISI = 100
SIPARIS_SAYISI = 20000

BASLANGIC_TARIHI = datetime(2023, 1, 1)
BITIS_TARIHI = datetime(2027, 12, 31)


# ============================================================
# GERÇEK HAYATTA KULLANILAN TÜRKÇE İSİMLER
# ============================================================

ADLAR = [
    "Ahmet",
    "Mehmet",
    "Mustafa",
    "Ali",
    "Hasan",
    "Hüseyin",
    "İbrahim",
    "Emre",
    "Burak",
    "Murat",
    "Can",
    "Cem",
    "Kerem",
    "Oğuz",
    "Onur",
    "Serkan",
    "Hakan",
    "Yusuf",
    "Ömer",
    "Enes",
    "Arda",
    "Berk",
    "Kaan",
    "Eren",
    "Mert",
    "Furkan",
    "Batuhan",
    "Umut",
    "Tolga",
    "Barış",
    "Ayşe",
    "Fatma",
    "Zeynep",
    "Elif",
    "Esra",
    "Merve",
    "Büşra",
    "Seda",
    "Derya",
    "Ece",
    "Ceren",
    "Selin",
    "İrem",
    "Sibel",
    "Özge",
    "Melis",
    "Bahar",
    "Damla",
    "Gizem",
    "Nehir"
]


SOYADLAR = [
    "Yılmaz",
    "Kaya",
    "Demir",
    "Şahin",
    "Çelik",
    "Yıldız",
    "Yıldırım",
    "Öztürk",
    "Aydın",
    "Özdemir",
    "Arslan",
    "Doğan",
    "Kılıç",
    "Aslan",
    "Çetin",
    "Kara",
    "Koç",
    "Kurt",
    "Özkan",
    "Şimşek",
    "Polat",
    "Erdoğan",
    "Aksoy",
    "Güneş",
    "Tekin",
    "Bulut",
    "Keskin",
    "Avcı",
    "Taş",
    "Kaplan",
    "Erdem",
    "Karaca",
    "Duman",
    "Acar",
    "Sarı",
    "Tunç",
    "Bozkurt",
    "Korkmaz",
    "Ünal",
    "Işık"
]


# ============================================================
# ŞEHİRLER
# ============================================================

SEHIRLER = [
    "İstanbul",
    "Ankara",
    "İzmir",
    "Bursa",
    "Antalya",
    "Adana",
    "Konya",
    "Gaziantep",
    "Kocaeli",
    "Mersin",
    "Kayseri",
    "Eskişehir",
    "Samsun",
    "Diyarbakır",
    "Trabzon"
]


# ============================================================
# KATEGORİLER
# ============================================================

KATEGORILER = [
    "Elektronik",
    "Bilgisayar",
    "Telefon",
    "Ev ve Yaşam",
    "Ofis",
    "Giyim",
    "Spor",
    "Kitap"
]


# ============================================================
# ÜRÜN İSİMLERİ
# ============================================================

URUNLER = [
    "Kablosuz Kulaklık",
    "Bluetooth Hoparlör",
    "Akıllı Saat",
    "Televizyon",
    "Dizüstü Bilgisayar",
    "Masaüstü Bilgisayar",
    "Gaming Laptop",
    "Tablet",
    "Monitör",
    "Klavye",
    "Mouse",
    "Web Kamera",
    "Mekanik Klavye",
    "USB Bellek",
    "Harici SSD",
    "Harici HDD",
    "Akıllı Telefon",
    "Telefon Kılıfı",
    "Şarj Adaptörü",
    "Powerbank",
    "Robot Süpürge",
    "Elektrikli Süpürge",
    "Kahve Makinesi",
    "Blender",
    "Airfryer",
    "Mikrodalga Fırın",
    "Çalışma Masası",
    "Ofis Sandalyesi",
    "Kitaplık",
    "Masa Lambası",
    "Sırt Çantası",
    "Spor Ayakkabı",
    "Koşu Bandı",
    "Yoga Matı",
    "Dambıl Seti",
    "Tişört",
    "Sweatshirt",
    "Mont",
    "Jean Pantolon",
    "Spor Çanta",
    "Roman",
    "Ders Kitabı",
    "Bilim Kitabı",
    "Tarih Kitabı",
    "Kişisel Gelişim Kitabı"
]


# ============================================================
# VERİTABANI
# ============================================================

conn = sqlite3.connect(DB_NAME)

cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_keys = ON"
)


# ============================================================
# TABLOLARI OLUŞTUR
# ============================================================

cursor.executescript("""
DROP TABLE IF EXISTS siparis_detaylari;
DROP TABLE IF EXISTS siparisler;
DROP TABLE IF EXISTS urunler;
DROP TABLE IF EXISTS kategoriler;
DROP TABLE IF EXISTS musteriler;


CREATE TABLE musteriler (
    musteri_id INTEGER PRIMARY KEY AUTOINCREMENT,

    ad TEXT NOT NULL,

    soyad TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    sehir TEXT NOT NULL,

    kayit_tarihi TEXT NOT NULL,

    aktif INTEGER NOT NULL
);


CREATE TABLE kategoriler (
    kategori_id INTEGER PRIMARY KEY AUTOINCREMENT,

    kategori_adi TEXT NOT NULL UNIQUE
);


CREATE TABLE urunler (
    urun_id INTEGER PRIMARY KEY AUTOINCREMENT,

    kategori_id INTEGER NOT NULL,

    urun_adi TEXT NOT NULL,

    birim_fiyat REAL NOT NULL,

    stok_miktari INTEGER NOT NULL,

    FOREIGN KEY (kategori_id)
        REFERENCES kategoriler(kategori_id)
);


CREATE TABLE siparisler (
    siparis_id INTEGER PRIMARY KEY AUTOINCREMENT,

    musteri_id INTEGER NOT NULL,

    siparis_tarihi TEXT NOT NULL,

    durum TEXT NOT NULL,

    odeme_yontemi TEXT NOT NULL,

    FOREIGN KEY (musteri_id)
        REFERENCES musteriler(musteri_id)
);


CREATE TABLE siparis_detaylari (
    detay_id INTEGER PRIMARY KEY AUTOINCREMENT,

    siparis_id INTEGER NOT NULL,

    urun_id INTEGER NOT NULL,

    miktar INTEGER NOT NULL,

    birim_fiyat REAL NOT NULL,

    indirim_orani REAL NOT NULL,

    FOREIGN KEY (siparis_id)
        REFERENCES siparisler(siparis_id),

    FOREIGN KEY (urun_id)
        REFERENCES urunler(urun_id)
);


CREATE INDEX idx_siparis_tarihi
ON siparisler(siparis_tarihi);


CREATE INDEX idx_siparis_musteri
ON siparisler(musteri_id);


CREATE INDEX idx_detay_urun
ON siparis_detaylari(urun_id);
""")


# ============================================================
# TARİH ÜRETME
# ============================================================

def rastgele_tarih():

    fark = BITIS_TARIHI - BASLANGIC_TARIHI

    gun = random.randint(
        0,
        fark.days
    )

    tarih = (
        BASLANGIC_TARIHI
        + timedelta(days=gun)
    )

    return tarih.strftime("%Y-%m-%d")


# ============================================================
# KATEGORİLERİ EKLE
# ============================================================

for kategori in KATEGORILER:

    cursor.execute(
        """
        INSERT INTO kategoriler
        (kategori_adi)

        VALUES (?)
        """,
        (kategori,)
    )


# ============================================================
# MÜŞTERİLERİ OLUŞTUR
# ============================================================

kullanilan_emailler = set()

for i in range(MUSTERI_SAYISI):

    ad = random.choice(ADLAR)

    soyad = random.choice(SOYADLAR)

    sehir = random.choice(SEHIRLER)

    # Aynı isimden birçok kişi olabilir.
    # Email benzersiz olacak şekilde ID ekliyoruz.
    email = (
        ad.lower()
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("ü", "u")
        .replace("ş", "s")
        .replace("ö", "o")
        .replace("ç", "c")
        + "."
        +
        soyad.lower()
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("ü", "u")
        .replace("ş", "s")
        .replace("ö", "o")
        .replace("ç", "c")
        +
        str(i + 1)
        +
        "@example.com"
    )

    kayit_tarihi = rastgele_tarih()

    aktif = random.choices(
        [0, 1],
        weights=[10, 90]
    )[0]

    cursor.execute(
        """
        INSERT INTO musteriler
        (
            ad,
            soyad,
            email,
            sehir,
            kayit_tarihi,
            aktif
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ad,
            soyad,
            email,
            sehir,
            kayit_tarihi,
            aktif
        )
    )


# ============================================================
# ÜRÜNLERİ OLUŞTUR
# ============================================================

for i in range(URUN_SAYISI):

    kategori_id = random.randint(
        1,
        len(KATEGORILER)
    )

    urun_adi = random.choice(URUNLER)

    # Aynı ürün isminden tekrar gelebileceği için
    # ürün numarası ekleniyor.
    urun_adi = (
        urun_adi
        + " "
        + str(i + 1)
    )

    fiyat = round(
        random.uniform(100, 25000),
        2
    )

    stok = random.randint(
        10,
        1000
    )

    cursor.execute(
        """
        INSERT INTO urunler
        (
            kategori_id,
            urun_adi,
            birim_fiyat,
            stok_miktari
        )

        VALUES (?, ?, ?, ?)
        """,
        (
            kategori_id,
            urun_adi,
            fiyat,
            stok
        )
    )


# ============================================================
# SİPARİŞLER
# ============================================================

DURUMLAR = [
    "Tamamlandı",
    "Hazırlanıyor",
    "Kargoda",
    "İptal"
]

DURUM_AGIRLIKLARI = [
    75,
    10,
    10,
    5
]

ODEME_YONTEMLERI = [
    "Kredi Kartı",
    "Banka Kartı",
    "Havale",
    "Dijital Cüzdan"
]


for i in range(SIPARIS_SAYISI):

    musteri_id = random.randint(
        1,
        MUSTERI_SAYISI
    )

    tarih = rastgele_tarih()

    durum = random.choices(
        DURUMLAR,
        weights=DURUM_AGIRLIKLARI
    )[0]

    odeme = random.choice(
        ODEME_YONTEMLERI
    )

    cursor.execute(
        """
        INSERT INTO siparisler
        (
            musteri_id,
            siparis_tarihi,
            durum,
            odeme_yontemi
        )

        VALUES (?, ?, ?, ?)
        """,
        (
            musteri_id,
            tarih,
            durum,
            odeme
        )
    )


# ============================================================
# SİPARİŞ DETAYLARI
# ============================================================

urun_listesi = cursor.execute(
    """
    SELECT
        urun_id,
        birim_fiyat

    FROM urunler
    """
).fetchall()


siparis_listesi = cursor.execute(
    """
    SELECT
        siparis_id

    FROM siparisler
    """
).fetchall()


for (siparis_id,) in siparis_listesi:

    urun_sayisi = random.randint(
        1,
        5
    )

    secilen_urunler = random.sample(
        urun_listesi,
        urun_sayisi
    )

    for urun_id, fiyat in secilen_urunler:

        miktar = random.randint(
            1,
            5
        )

        indirim = random.choice(
            [0, 0, 0, 5, 10]
        )

        cursor.execute(
            """
            INSERT INTO siparis_detaylari
            (
                siparis_id,
                urun_id,
                miktar,
                birim_fiyat,
                indirim_orani
            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                siparis_id,
                urun_id,
                miktar,
                fiyat,
                indirim
            )
        )


conn.commit()


# ============================================================
# ÖRNEK MÜŞTERİLERİ GÖSTER
# ============================================================

print("\n")
print("=" * 65)
print("ÖRNEK MÜŞTERİLER")
print("=" * 65)

ornekler = cursor.execute(
    """
    SELECT
        musteri_id,
        ad,
        soyad,
        email,
        sehir

    FROM musteriler

    LIMIT 15
    """
).fetchall()


for musteri in ornekler:

    print(
        f"{musteri[0]:4} | "
        f"{musteri[1]:10} "
        f"{musteri[2]:15} | "
        f"{musteri[3]:35} | "
        f"{musteri[4]}"
    )


# ============================================================
# ANALİZ 1
# YILLARA GÖRE SİPARİŞ
# ============================================================

print("\n")
print("=" * 65)
print("YILLARA GÖRE SİPARİŞ SAYISI")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        substr(siparis_tarihi, 1, 4) AS yil,
        COUNT(*) AS siparis_sayisi

    FROM siparisler

    GROUP BY yil

    ORDER BY yil
    """
).fetchall()


for yil, sayi in sonuclar:

    print(
        f"{yil}: {sayi:,} sipariş"
    )


# ============================================================
# ANALİZ 2
# YILLIK CİRO
# ============================================================

print("\n")
print("=" * 65)
print("YILLIK CİRO")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        substr(
            s.siparis_tarihi,
            1,
            4
        ) AS yil,

        ROUND(
            SUM(
                sd.miktar
                * sd.birim_fiyat
                * (
                    1
                    - sd.indirim_orani / 100
                )
            ),
            2
        ) AS ciro

    FROM siparisler s

    JOIN siparis_detaylari sd
        ON s.siparis_id =
           sd.siparis_id

    WHERE s.durum != 'İptal'

    GROUP BY yil

    ORDER BY yil
    """
).fetchall()


for yil, ciro in sonuclar:

    print(
        f"{yil}: {ciro:,.2f} TL"
    )


# ============================================================
# ANALİZ 3
# EN ÇOK HARCAYAN MÜŞTERİLER
# ============================================================

print("\n")
print("=" * 65)
print("EN ÇOK HARCAYAN 10 MÜŞTERİ")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        m.ad,
        m.soyad,

        ROUND(
            SUM(
                sd.miktar
                * sd.birim_fiyat
                * (
                    1
                    - sd.indirim_orani / 100
                )
            ),
            2
        ) AS toplam_harcama

    FROM musteriler m

    JOIN siparisler s
        ON m.musteri_id =
           s.musteri_id

    JOIN siparis_detaylari sd
        ON s.siparis_id =
           sd.siparis_id

    WHERE s.durum != 'İptal'

    GROUP BY
        m.musteri_id

    ORDER BY
        toplam_harcama DESC

    LIMIT 10
    """
).fetchall()


for ad, soyad, harcama in sonuclar:

    print(
        f"{ad} {soyad}: "
        f"{harcama:,.2f} TL"
    )


# ============================================================
# ANALİZ 4
# ŞEHİRLERE GÖRE CİRO
# ============================================================

print("\n")
print("=" * 65)
print("ŞEHİRLERE GÖRE CİRO")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        m.sehir,

        ROUND(
            SUM(
                sd.miktar
                * sd.birim_fiyat
                * (
                    1
                    - sd.indirim_orani / 100
                )
            ),
            2
        ) AS ciro

    FROM musteriler m

    JOIN siparisler s
        ON m.musteri_id =
           s.musteri_id

    JOIN siparis_detaylari sd
        ON s.siparis_id =
           sd.siparis_id

    WHERE s.durum != 'İptal'

    GROUP BY m.sehir

    ORDER BY ciro DESC
    """
).fetchall()


for sehir, ciro in sonuclar:

    print(
        f"{sehir}: "
        f"{ciro:,.2f} TL"
    )


# ============================================================
# ANALİZ 5
# EN ÇOK SATAN ÜRÜNLER
# ============================================================

print("\n")
print("=" * 65)
print("EN ÇOK SATAN 10 ÜRÜN")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        u.urun_adi,

        SUM(
            sd.miktar
        ) AS satilan_adet

    FROM siparis_detaylari sd

    JOIN urunler u
        ON sd.urun_id =
           u.urun_id

    JOIN siparisler s
        ON sd.siparis_id =
           s.siparis_id

    WHERE s.durum != 'İptal'

    GROUP BY
        u.urun_id

    ORDER BY
        satilan_adet DESC

    LIMIT 10
    """
).fetchall()


for urun, adet in sonuclar:

    print(
        f"{urun}: "
        f"{adet:,} adet"
    )


# ============================================================
# ANALİZ 6
# KATEGORİ BAZINDA CİRO
# ============================================================

print("\n")
print("=" * 65)
print("KATEGORİ BAZINDA CİRO")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        k.kategori_adi,

        ROUND(
            SUM(
                sd.miktar
                * sd.birim_fiyat
                * (
                    1
                    - sd.indirim_orani / 100
                )
            ),
            2
        ) AS ciro

    FROM siparis_detaylari sd

    JOIN urunler u
        ON sd.urun_id =
           u.urun_id

    JOIN kategoriler k
        ON u.kategori_id =
           k.kategori_id

    JOIN siparisler s
        ON sd.siparis_id =
           s.siparis_id

    WHERE s.durum != 'İptal'

    GROUP BY
        k.kategori_id

    ORDER BY ciro DESC
    """
).fetchall()


for kategori, ciro in sonuclar:

    print(
        f"{kategori}: "
        f"{ciro:,.2f} TL"
    )


# ============================================================
# ANALİZ 7
# ÖDEME YÖNTEMLERİ
# ============================================================

print("\n")
print("=" * 65)
print("ÖDEME YÖNTEMLERİ")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        odeme_yontemi,
        COUNT(*) AS siparis_sayisi

    FROM siparisler

    GROUP BY
        odeme_yontemi

    ORDER BY
        siparis_sayisi DESC
    """
).fetchall()


for odeme, sayi in sonuclar:

    print(
        f"{odeme}: "
        f"{sayi:,} sipariş"
    )


# ============================================================
# ANALİZ 8
# SİPARİŞ DURUMLARI
# ============================================================

print("\n")
print("=" * 65)
print("SİPARİŞ DURUMLARI")
print("=" * 65)

sonuclar = cursor.execute(
    """
    SELECT
        durum,
        COUNT(*) AS adet

    FROM siparisler

    GROUP BY durum

    ORDER BY adet DESC
    """
).fetchall()


for durum, adet in sonuclar:

    print(
        f"{durum}: "
        f"{adet:,}"
    )


# ============================================================
# GENEL İSTATİSTİK
# ============================================================

print("\n")
print("=" * 65)
print("VERİTABANI ÖZETİ")
print("=" * 65)

musteri_sayisi = cursor.execute(
    "SELECT COUNT(*) FROM musteriler"
).fetchone()[0]

urun_sayisi = cursor.execute(
    "SELECT COUNT(*) FROM urunler"
).fetchone()[0]

siparis_sayisi = cursor.execute(
    "SELECT COUNT(*) FROM siparisler"
).fetchone()[0]

detay_sayisi = cursor.execute(
    "SELECT COUNT(*) FROM siparis_detaylari"
).fetchone()[0]


print(
    f"Müşteri sayısı       : {musteri_sayisi:,}"
)

print(
    f"Ürün sayısı          : {urun_sayisi:,}"
)

print(
    f"Sipariş sayısı       : {siparis_sayisi:,}"
)

print(
    f"Sipariş detay sayısı : {detay_sayisi:,}"
)


# ============================================================
# VERİTABANINI KAPAT
# ============================================================

conn.close()

print("\n")
print("=" * 65)
print("İŞLEM TAMAMLANDI")
print("=" * 65)

print(
    f"Veritabanı dosyası: {DB_NAME}"
)
