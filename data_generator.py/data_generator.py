import sqlite3
import random
import time
from datetime import datetime
from faker import Faker
import pandas as pd

# Faker nesnesini Türkçe veri üretecek şekilde başlatıyoruz
fake = Faker('tr_TR')

# 1. SQLite Veritabanı Bağlantısı ve Tablo Oluşturma
def setup_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # E-ticaret log tablosunu oluşturuyoruz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_type TEXT,
            product_id INTEGER,
            product_category TEXT,
            price REAL,
            city TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# 2. Sentetik Veri Üretim Fonksiyonu
def generate_log_event():
    categories = ['Elektronik', 'Giyim', 'Ev & Yaşam', 'Kişisel Bakım', 'Spor & Outdoor']
    event_types = ['view', 'add_to_cart', 'purchase']
    # Olay ağırlıkları: %60 görüntüleme, %25 sepete ekleme, %15 satın alma
    event_weights = [0.60, 0.25, 0.15]
    
    cities = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Kocaeli', 'Gaziantep']
    
    event = random.choices(event_types, weights=event_weights)[0]
    category = random.choice(categories)
    
    # Fiyat belirlenmesi (sadece ürün görüntüleme/satın alma durumları için mantıklı fiyatlar)
    price_ranges = {
        'Elektronik': (500, 15000),
        'Giyim': (100, 2000),
        'Ev & Yaşam': (150, 5000),
        'Kişisel Bakım': (50, 800),
        'Spor & Outdoor': (200, 4000)
    }
    low, high = price_ranges[category]
    price = round(random.uniform(low, high), 2)
    
    log_data = {
        'user_id': random.randint(1000, 9999),
        'event_type': event,
        'product_id': random.randint(101, 200),
        'product_category': category,
        'price': price if event == 'purchase' else round(price * 0.1, 2), # Görüntülemede varsayılan değer
        'city': random.choice(cities),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return log_data

# 3. Gerçek Zamanlı Akış Simülasyonu
def start_streaming(total_records=500, delay_seconds=0.1):
    setup_database()
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print(f"Veri akışı başlatıldı. Toplam {total_records} log üretilecek...")
    
    for i in range(total_records):
        data = generate_log_event()
        
        cursor.execute('''
            INSERT INTO user_activity_logs (user_id, event_type, product_id, product_category, price, city, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['user_id'], data['event_type'], data['product_id'], data['product_category'], data['price'], data['city'], data['timestamp']))
        
        conn.commit()
        
        if (i + 1) % 50 == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {i + 1} adet log başarıyla aktarıldı.")
            
        time.sleep(delay_seconds) # Gerçek zamanlı akış hissi vermek için bekleme süresi
        
    conn.close()
    print("Veri akışı tamamlandı. 'ecommerce.db' dosyası hazır.")

if __name__ == '__main__':
    start_streaming(total_records=1000, delay_seconds=0.05)