import sqlite3
import random
import time
from datetime import datetime
from faker import Faker
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Veritabanını Hazırlama
def setup_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS kullanici_aktivite_loglari')
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

# 2. Sentetik Veri Üretimi
def log_olustur():
    kategoriler = ['Elektronik', 'Giyim', 'Ev & Yaşam', 'Kişisel Bakım', 'Spor & Outdoor']
    islem_turleri = ['goruntuleme', 'sepete_ekleme', 'satin_alma']
    islem_agirliklari = [0.60, 0.25, 0.15]
    sehirler = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Kocaeli', 'Gaziantep', 'Konya', 'Kayseri']
    
    islem = random.choices(islem_turleri, weights=islem_agirliklari)[0]
    kategori = random.choice(kategoriler)
    
    fiyat_araliklari = {
        'Elektronik': (1000, 20000),
        'Giyim': (150, 2500),
        'Ev & Yaşam': (200, 6000),
        'Kişisel Bakım': (50, 1000),
        'Spor & Outdoor': (300, 5000)
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

def veri_doldur(toplam_kayit=1000):
    setup_database()
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    for _ in range(toplam_kayit):
        data = log_olustur()
        cursor.execute('''
            INSERT INTO kullanici_aktivite_loglari 
            (kullanici_id, islem_turu, urun_id, urun_kategorisi, fiyat, sehir, zaman_damgasi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['kullanici_id'], data['islem_turu'], data['urun_id'], 
              data['urun_kategorisi'], data['fiyat'], data['sehir'], data['zaman_damgasi']))
    conn.commit()
    conn.close()
    print("Veri akışı tamamlandı, 1000 kayıt eklendi.")

# 3. Görselleştirme ve Dashboard Oluşturma
def dashboard_ciz():
    conn = sqlite3.connect('ecommerce.db')
    
    # Verileri Çekme
    df_sehir = pd.read_sql_query('''
        SELECT sehir, ROUND(SUM(fiyat), 2) AS toplam_ciro
        FROM kullanici_aktivite_loglari
        WHERE islem_turu = 'satin_alma'
        GROUP BY sehir
        ORDER BY toplam_ciro DESC
    ''', conn)

    df_kategori = pd.read_sql_query('''
        SELECT urun_kategorisi, ROUND(SUM(fiyat), 2) AS toplam_ciro
        FROM kullanici_aktivite_loglari
        WHERE islem_turu = 'satin_alma'
        GROUP BY urun_kategorisi
        ORDER BY toplam_ciro DESC
    ''', conn)

    df_islem = pd.read_sql_query('''
        SELECT islem_turu, COUNT(*) AS adet
        FROM kullanici_aktivite_loglari
        GROUP BY islem_turu
    ''', conn)
    conn.close()

    # Stil Ayarları
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(15, 8))
    fig.suptitle('E-Ticaret Veri Analitiği Dashboard', fontsize=18, fontweight='bold', y=0.98)

    # 1. Grafik: Şehir Bazlı Ciro (Sol Taraf - Yatay Çubuk)
    ax1 = plt.subplot(1, 2, 1)
    sns.barplot(data=df_sehir, x='toplam_ciro', y='sehir', color='#1f77b4', ax=ax1)
    ax1.set_title('Şehir Bazlı Toplam Ciro (₺)', fontsize=13, pad=10)
    ax1.set_xlabel('Toplam Ciro (₺)')
    ax1.set_ylabel('Şehir')

    # 2. Grafik: Kategori Ciro Dağılımı (Sağ Üst - Dikey Çubuk)
    ax2 = plt.subplot(2, 2, 2)
    sns.barplot(data=df_kategori, x='urun_kategorisi', y='toplam_ciro', color='#1f77b4', ax=ax2)
    ax2.set_title('Kategori Bazlı Ciro (₺)', fontsize=13, pad=10)
    ax2.set_xlabel('')
    ax2.set_ylabel('Ciro (₺)')
    plt.xticks(rotation=15)

    # 3. Grafik: Etkileşim Türleri (Sağ Alt - Donut/Halka Grafik)
    ax3 = plt.subplot(2, 2, 4)
    etiket_map = {'goruntuleme': 'Görüntüleme', 'sepete_ekleme': 'Sepete Ekleme', 'satin_alma': 'Satın Alma'}
    labels = [etiket_map.get(x, x) for x in df_islem['islem_turu']]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    ax3.pie(df_islem['adet'], labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    centre_circle = plt.Circle((0,0),0.60,fc='white')
    ax3.add_artist(centre_circle)
    ax3.set_title('Kullanıcı Etkileşim Türleri', fontsize=13, pad=10)

    # Yerleşim düzenleme ve Resmi Kaydetme
    plt.tight_layout()
    plt.savefig('dashboard_gorseli.png', dpi=300, bbox_inches='tight')
    print("Dashboard grafiği 'dashboard_gorseli.png' olarak kaydedildi!")
    plt.show()

if __name__ == '__main__':
    veri_doldur(1000)
    dashboard_ciz()