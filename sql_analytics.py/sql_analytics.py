import sqlite3
import random
import time
from datetime import datetime
from faker import Faker
import pandas as pd

# 1. Türkçe Faker Nesnesi
fake = Faker('tr_TR')

def veritabanini_hazirla():
    """Veritabanı bağlantısını kurar ve tabloyu sıfırdan oluşturur."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Varsa eski tabloyu temizliyoruz
    cursor.execute('DROP TABLE IF EXISTS kullanici_aktivite_loglari')
    
    # Yeni Türkçe tablo yapısı
    cursor.execute('''
        CREATE TABLE kullanici_aktivite_loglari (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER,
            islem_turu TEXT,
            urun_id INTEGER,
            urun_kategorisi TEXT,
            fiyat REAL,
            sehir TEXT,
            zaman_damgasi DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def log_olustur():
    """Rastgele ve gerçekçi bir e-ticaret hareket verisi üretir."""
    kategoriler = ['Elektronik', 'Giyim', 'Ev & Yaşam', 'Kişisel Bakım', 'Spor & Outdoor']
    islem_turleri = ['goruntuleme', 'sepete_ekleme', 'satin_alma']
    # Ağırlıklar: %60 görüntüleme, %25 sepete ekleme, %15 satın alma
    islem_agirliklari = [0.60, 0.25, 0.15]
    sehirler = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Kocaeli', 'Gaziantep']
    
    islem = random.choices(islem_turleri, weights=islem_agirliklari)[0]
    kategori = random.choice(kategoriler)
    
    fiyat_araliklari = {
        'Elektronik': (500, 15000),
        'Giyim': (100, 2000),
        'Ev & Yaşam': (150, 5000),
        'Kişisel Bakım': (50, 800),
        'Spor & Outdoor': (200, 4000)
    }
    alt, ust = fiyat_araliklari[kategori]
    fiyat = round(random.uniform(alt, ust), 2)
    
    return {
        'kullanici_id': random.randint(1000, 9999),
        'islem_turu': islem,
        'urun_id': random.randint(101, 200),
        'urun_kategorisi': kategori,
        'fiyat': fiyat if islem == 'satin_alma' else round(fiyat * 0.1, 2),
        'sehir': random.choice(sehirler),
        'zaman_damgasi': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def veri_akisini_baslat(toplam_kayit=1000):
    """Veritabanına log verilerini ekler."""
    veritabanini_hazirla()
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print(f"--- 1. ADIM: {toplam_kayit} Adet Log Üretiliyor ve Veritabanına Aktarılıyor... ---")
    
    for i in range(toplam_kayit):
        data = log_olustur()
        cursor.execute('''
            INSERT INTO kullanici_aktivite_loglari 
            (kullanici_id, islem_turu, urun_id, urun_kategorisi, fiyat, sehir, zaman_damgasi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['kullanici_id'], data['islem_turu'], data['urun_id'], 
              data['urun_kategorisi'], data['fiyat'], data['sehir'], data['zaman_damgasi']))
        
    conn.commit()
    conn.close()
    print("Veri üretimi ve aktarımı tamamlandı!\n")

def sql_analizlerini_calistir():
    """Veritabanındaki veriler üzerinden analitik SQL sorgularını çalıştırır."""
    conn = sqlite3.connect('ecommerce.db')
    
    print("=" * 60)
    print("--- 2. ADIM: ANALİTİK SQL SORGULARI VE SONUÇLARI ---")
    print("=" * 60)

    # 1. Şehir Bazlı Ciro Dağılımı
    print("\n1. ŞEHR BAZLI TOPLAM CİRO VE İŞLEM SAYILARI:")
    query_sehir = '''
        SELECT 
            sehir AS Şehir, 
            ROUND(SUM(fiyat), 2) AS Toplam_Ciro_TL,
            COUNT(*) AS Toplam_Satış_Adedi
        FROM kullanici_aktivite_loglari
        WHERE islem_turu = 'satin_alma'
        GROUP BY sehir
        ORDER BY Toplam_Ciro_TL DESC;
    '''
    df_sehir = pd.read_sql_query(query_sehir, conn)
    print(df_sehir.to_string(index=False))

    # 2. Kategori Performansı
    print("\n" + "-" * 60)
    print("2. KATEGORİ PERFORMANSI VE DÖNÜŞÜM METRİKLERİ:")
    query_kategori = '''
        SELECT 
            urun_kategorisi AS Kategori,
            COUNT(CASE WHEN islem_turu = 'goruntuleme' THEN 1 END) AS Görüntüleme,
            COUNT(CASE WHEN islem_turu = 'sepete_ekleme' THEN 1 END) AS Sepete_Ekleme,
            COUNT(CASE WHEN islem_turu = 'satin_alma' THEN 1 END) AS Satın_Alma,
            ROUND(SUM(CASE WHEN islem_turu = 'satin_alma' THEN fiyat ELSE 0 END), 2) AS Toplam_Ciro_TL
        FROM kullanici_aktivite_loglari
        GROUP BY urun_kategorisi
        ORDER BY Toplam_Ciro_TL DESC;
    '''
    df_kategori = pd.read_sql_query(query_kategori, conn)
    print(df_kategori.to_string(index=False))

    # 3. Müşteri Dönüşüm Oranı (Conversion Rate)
    print("\n" + "-" * 60)
    print("3. GENEL MÜŞTERİ DÖNÜŞÜM ORANI (CONVERSION RATE):")
    query_donusum = '''
        SELECT 
            COUNT(DISTINCT kullanici_id) AS Toplam_Tekil_Ziyaretçi,
            COUNT(DISTINCT CASE WHEN islem_turu = 'satin_alma' THEN kullanici_id END) AS Satın_Alan_Müşteri,
            ROUND(
                (CAST(COUNT(DISTINCT CASE WHEN islem_turu = 'satin_alma' THEN kullanici_id END) AS FLOAT) / 
                COUNT(DISTINCT kullanici_id)) * 100, 2
            ) AS Dönüşüm_Oranı_Yüzde
        FROM kullanici_aktivite_loglari;
    '''
    df_donusum = pd.read_sql_query(query_donusum, conn)
    print(df_donusum.to_string(index=False))

    conn.close()

# Ana Akış
if __name__ == '__main__':
    veri_akisini_baslat(toplam_kayit=1000)
    sql_analizlerini_calistir()