import sqlite3
import random
import time
from datetime import datetime
from faker import Faker

fake = Faker('tr_TR')

def setup_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Eski tabloyu silip Türkçe sütunlarla baştan oluşturuyoruz
    cursor.execute('DROP TABLE IF EXISTS kullanıcı_aktivite_logları')
    cursor.execute('''
        CREATE TABLE kullanıcı_aktivite_logları (
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

def generate_log_event():
    categories = ['Elektronik', 'Giyim', 'Ev & Yaşam', 'Kişisel Bakım', 'Spor & Outdoor']
    # İşlem türlerini Türkçe yapıyoruz
    event_types = ['goruntuleme', 'sepete_ekleme', 'satin_alma']
    event_weights = [0.60, 0.25, 0.15]
    cities = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Kocaeli', 'Gaziantep']
    
    event = random.choices(event_types, weights=event_weights)[0]
    category = random.choice(categories)
    
    price_ranges = {
        'Elektronik': (500, 15000),
        'Giyim': (100, 2000),
        'Ev & Yaşam': (150, 5000),
        'Kişisel Bakım': (50, 800),
        'Spor & Outdoor': (200, 4000)
    }
    low, high = price_ranges[category]
    price = round(random.uniform(low, high), 2)
    
    return {
        'kullanici_id': random.randint(1000, 9999),
        'islem_turu': event,
        'urun_id': random.randint(101, 200),
        'urun_kategorisi': category,
        'fiyat': price if event == 'satin_alma' else round(price * 0.1, 2),
        'sehir': random.choice(cities),
        'zaman_damgasi': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def start_streaming(total_records=1000, delay_seconds=0.01):
    setup_database()
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    for i in range(total_records):
        data = generate_log_event()
        cursor.execute('''
            INSERT INTO kullanıcı_aktivite_logları (kullanici_id, islem_turu, urun_id, urun_kategorisi, fiyat, sehir, zaman_damgasi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['kullanici_id'], data['islem_turu'], data['urun_id'], data['urun_kategorisi'], data['fiyat'], data['sehir'], data['zaman_damgasi']))
        conn.commit()
        time.sleep(delay_seconds)
        
    conn.close()
    print("Türkçe veri akışı tamamlandı!")

if __name__ == '__main__':
    start_streaming()