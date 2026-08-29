import random

# =====================================================================
# 1. TAKIMLAR, ÜLKELERİ VE TORBALAR (36 TAKIMLI YENİ ŞAMPİYONLAR LİGİ)
# =====================================================================
TAKIMLAR_BILGI = {
    # 1. Torba
    "Real Madrid": "İspanya", "Manchester City": "İngiltere", "Bayern München": "Almanya", 
    "PSG": "Fransa", "Liverpool": "İngiltere", "Inter": "İtalya", 
    "Dortmund": "Almanya", "RB Leipzig": "Almanya", "Barcelona": "İspanya",
    
    # 2. Torba
    "Bayer Leverkusen": "Almanya", "Atlético Madrid": "İspanya", "Atalanta": "İtalya", 
    "Juventus": "İtalya", "Benfica": "Portekiz", "Arsenal": "İngiltere", 
    "Club Brugge": "Belçika", "Shakhtar Donetsk": "Ukrayna", "AC Milan": "İtalya",
    
    # 3. Torba
    "Galatasaray": "Türkiye", "Feyenoord": "Hollanda", "Sporting CP": "Portekiz", 
    "PSV Eindhoven": "Hollanda", "GNK Dinamo": "Hırvatistan", "Salzburg": "Avusturya", 
    "Lille": "Fransa", "Crvena zvezda": "Sırbistan", "Celtic": "İskoçya",
    
    # 4. Torba
    "Fenerbahçe": "Türkiye", "Beşiktaş": "Türkiye", "Slovan Bratislava": "Slovakya", 
    "Monaco": "Fransa", "Sparta Praha": "Çekya", "Aston Villa": "İngiltere", 
    "Bologna": "İtalya", "Girona": "İspanya", "Stuttgart": "Almanya"
}

TORBALAR = {
    "1. Torba": ["Real Madrid", "Manchester City", "Bayern München", "PSG", "Liverpool", "Inter", "Dortmund", "RB Leipzig", "Barcelona"],
    "2. Torba": ["Bayer Leverkusen", "Atlético Madrid", "Atalanta", "Juventus", "Benfica", "Arsenal", "Club Brugge", "Shakhtar Donetsk", "AC Milan"],
    "3. Torba": ["Galatasaray", "Feyenoord", "Sporting CP", "PSV Eindhoven", "GNK Dinamo", "Salzburg", "Lille", "Crvena zvezda", "Celtic"],
    "4. Torba": ["Fenerbahçe", "Beşiktaş", "Slovan Bratislava", "Monaco", "Sparta Praha", "Aston Villa", "Bologna", "Girona", "Stuttgart"]
}

# =====================================================================
# 2. KURA SIMÜLASYONU MOTORU
# =====================================================================
def kura_simulasyonu():
    eslesmeler = {takim: [] for takim in TAKIMLAR_BILGI.keys()}

    for torba_adi, takimlar in TORBALAR.items():
        for takim in takimlar:
            takim_ulke = TAKIMLAR_BILGI[takim]
            
            for hedef_torba_adi, hedef_torba_takimlari in TORBALAR.items():
                mevcut_rakip_isimleri = [r['takim'] for r in eslesmeler[takim]]
                
                # Kurallar: Kendisi olamaz, aynı ülke takımı olamaz, önceden seçilmiş olamaz
                uygun_adaylar = [
                    t for t in hedef_torba_takimlari 
                    if t != takim 
                    and TAKIMLAR_BILGI[t] != takim_ulke 
                    and t not in mevcut_rakip_isimleri
                ]
                
                # Aday kalmama durumunda güvenlik eşleşmesi
                if len(uygun_adaylar) < 2:
                    uygun_adaylar = [t for t in hedef_torba_takimlari if t != takim and t not in mevcut_rakip_isimleri]

                secilenler = random.sample(uygun_adaylar, 2)
                
                eslesmeler[takim].append({"takim": secilenler[0], "saha": "Ev Sahibi", "torba": hedef_torba_adi})
                eslesmeler[takim].append({"takim": secilenler[1], "saha": "Deplasman", "torba": hedef_torba_adi})

    return eslesmeler

# =====================================================================
# 3. KURALARI ÇALIŞTIR VE EKRANA YAZDIR
# =====================================================================
kura_sonuclari = kura_simulasyonu()

print("=" * 65)
print("🏆 UEFA ŞAMPİYONLAR LİGİ KURA ÇEKİM SİMÜLASYONU 🏆")
print("=" * 65)

# Türk Takımlarının Fikstürü
turk_takimlari = ["Galatasaray", "Fenerbahçe", "Beşiktaş"]

for tt in turk_takimlari:
    print(f"\n🇹🇷 {tt.upper()} FİKSTÜRÜ ({TAKIMLAR_BILGI[tt]}):")
    print("-" * 55)
    for idx, mac in enumerate(kura_sonuclari[tt], 1):
        rakip_ulke = TAKIMLAR_BILGI[mac['takim']]
        print(f"{idx}. Maç: {mac['takim']} ({rakip_ulke}) - [{mac['saha']}] -> ({mac['torba']})")

# Diğer Takımları Arama Alanı
while True:
    print("\n" + "=" * 55)
    secim = input("Fikstürünü görmek istediğiniz takımı yazın (Çıkış için 'q'): ").strip()
    if secim.lower() == 'q':
        break
    
    bulunanlar = [t for t in kura_sonuclari.keys() if secim.lower() in t.lower()]
    
    if bulunanlar:
        secilen_takim = bulunanlar[0]
        print(f"\n📌 {secilen_takim.upper()} FİKSTÜRÜ ({TAKIMLAR_BILGI[secilen_takim]}):")
        print("-" * 55)
        for i, mac in enumerate(kura_sonuclari[secilen_takim], 1):
            rakip_ulke = TAKIMLAR_BILGI[mac['takim']]
            print(f"{i}. Maç: {mac['takim']} ({rakip_ulke}) - [{mac['saha']}] -> ({mac['torba']})")
    else:
        print("⚠️ Takım bulunamadı! Lütfen geçerli bir takım adı girin.")