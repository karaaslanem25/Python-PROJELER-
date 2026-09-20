from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

# =========================================================
# MENÜ
# =========================================================

MENU = [
    ("Klasik Hamburger", 180),
    ("Cheeseburger", 200),
    ("Double Burger", 250),
    ("Tavuk Burger", 170),

    ("Margarita Pizza", 220),
    ("Karışık Pizza", 280),
    ("Sucuklu Pizza", 260),
    ("Tavuklu Pizza", 270),

    ("Spagetti Bolognese", 190),
    ("Fettuccine Alfredo", 210),
    ("Napoliten Makarna", 180),

    ("Izgara Tavuk", 230),
    ("Çıtır Tavuk", 220),
    ("Tavuk Şinitzel", 240),

    ("Sezar Salata", 160),
    ("Akdeniz Salata", 150),

    ("Patates Kızartması", 90),
    ("Soğan Halkası", 100),
    ("Mozzarella Stick", 130),

    ("Çikolatalı Sufle", 140),
    ("Cheesecake", 150),
    ("Tiramisu", 150),

    ("Kola", 50),
    ("Fanta", 50),
    ("Sprite", 50),
    ("Ayran", 40),
    ("Su", 25),
    ("Çay", 30),
    ("Türk Kahvesi", 70)
]


# =========================================================
# VERİTABANI
# =========================================================

def veritabani():

    conn = sqlite3.connect("restoran.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS siparisler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT,
            telefon TEXT,
            adres TEXT,
            urunler TEXT,
            toplam INTEGER,
            odeme TEXT,
            not_bilgisi TEXT,
            tarih TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# ANA SAYFA HTML
# =========================================================

ANA_SAYFA = """

<!DOCTYPE html>

<html lang="tr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Lezzet Durağı</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family: Arial, sans-serif;

    background: #f4f4f4;

    color: #333;
}

header {

    background: linear-gradient(
        135deg,
        #b22222,
        #e63946
    );

    color: white;

    text-align: center;

    padding: 35px;
}

header h1 {

    margin: 0;

    font-size: 40px;
}

header p {

    font-size: 18px;
}

.container {

    max-width: 1100px;

    margin: auto;

    padding: 25px;
}

h2 {

    color: #b22222;

    margin-top: 35px;
}

.menu {

    display: grid;

    grid-template-columns:
    repeat(
        auto-fit,
        minmax(220px, 1fr)
    );

    gap: 20px;
}

.urun {

    background: white;

    padding: 20px;

    border-radius: 15px;

    box-shadow:
        0 3px 10px
        rgba(0,0,0,0.1);
}

.urun h3 {

    margin-top: 0;

    color: #b22222;
}

.fiyat {

    font-size: 20px;

    font-weight: bold;
}

.adet {

    width: 80px;

    padding: 10px;

    border: 1px solid #ccc;

    border-radius: 6px;
}

.form {

    background: white;

    padding: 30px;

    margin-top: 40px;

    border-radius: 15px;

    box-shadow:
        0 3px 10px
        rgba(0,0,0,0.1);
}

label {

    display: block;

    font-weight: bold;

    margin-top: 15px;

    margin-bottom: 5px;
}

input,
textarea,
select {

    width: 100%;

    padding: 13px;

    border: 1px solid #ccc;

    border-radius: 7px;

    font-size: 15px;
}

textarea {

    min-height: 100px;

    resize: vertical;
}

button {

    width: 100%;

    margin-top: 25px;

    padding: 16px;

    background: #b22222;

    color: white;

    border: none;

    border-radius: 8px;

    font-size: 18px;

    cursor: pointer;
}

button:hover {

    background: #8b1a1a;
}

footer {

    margin-top: 50px;

    padding: 25px;

    text-align: center;

    background: #222;

    color: white;
}

</style>

</head>


<body>


<header>

<h1>🍽️ LEZZET DURAĞI</h1>

<p>Online Restoran Sipariş Sistemi</p>

</header>


<div class="container">


<form method="POST"
      action="/siparis">


<h2>🍔 Burgerler</h2>

<div class="menu">

{% for i in range(0,4) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🍕 Pizzalar</h2>

<div class="menu">

{% for i in range(4,8) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🍝 Makarnalar</h2>

<div class="menu">

{% for i in range(8,11) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🍗 Tavuklar</h2>

<div class="menu">

{% for i in range(11,14) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🥗 Salatalar</h2>

<div class="menu">

{% for i in range(14,16) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🍟 Atıştırmalıklar</h2>

<div class="menu">

{% for i in range(16,19) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🍰 Tatlılar</h2>

<div class="menu">

{% for i in range(19,22) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<h2>🥤 İçecekler</h2>

<div class="menu">

{% for i in range(22,29) %}

<div class="urun">

<h3>
{{ menu[i][0] }}
</h3>

<p class="fiyat">
{{ menu[i][1] }} TL
</p>

<label>Adet</label>

<input
    class="adet"
    type="number"
    min="0"
    value="0"
    name="urun{{ i }}"
>

</div>

{% endfor %}

</div>


<div class="form">

<h2>👤 Müşteri Bilgileri</h2>


<label>Ad Soyad</label>

<input
    type="text"
    name="ad_soyad"
    placeholder="Örn: Ahmet Yılmaz"
    required
>


<label>Telefon</label>

<input
    type="tel"
    name="telefon"
    placeholder="05XX XXX XX XX"
    required
>


<label>Adres</label>

<textarea
    name="adres"
    placeholder="Teslimat adresiniz"
    required
></textarea>


<label>Ödeme Yöntemi</label>

<select name="odeme">

<option>
Kapıda Nakit
</option>

<option>
Kapıda Kart
</option>

</select>


<label>Sipariş Notu</label>

<textarea
    name="not_bilgisi"
    placeholder="Örn: Soğansız olsun."
></textarea>


<button type="submit">

🛒 SİPARİŞİ VER

</button>


</div>


</form>


</div>


<footer>

Lezzet Durağı © 2026

</footer>


</body>

</html>

"""


# =========================================================
# BAŞARILI SAYFASI
# =========================================================

BASARILI = """

<!DOCTYPE html>

<html lang="tr">

<head>

<meta charset="UTF-8">

<title>Sipariş Alındı</title>

<style>

body {

    font-family: Arial;

    background: #f4f4f4;

    text-align: center;

    padding-top: 100px;
}

.box {

    background: white;

    max-width: 500px;

    margin: auto;

    padding: 40px;

    border-radius: 15px;

    box-shadow:
        0 5px 20px
        rgba(0,0,0,.15);
}

h1 {

    color: green;
}

.toplam {

    color: #b22222;

    font-size: 25px;

    font-weight: bold;
}

a {

    display: inline-block;

    margin-top: 20px;

    padding: 12px 25px;

    background: #b22222;

    color: white;

    text-decoration: none;

    border-radius: 7px;
}

</style>

</head>

<body>

<div class="box">

<h1>✅ Sipariş Alındı!</h1>

<h2>
{{ ad_soyad }}
</h2>

<p>
Siparişiniz başarıyla oluşturuldu.
</p>

<p class="toplam">
Toplam: {{ toplam }} TL
</p>

<a href="/">
Yeni Sipariş
</a>

</div>

</body>

</html>

"""


# =========================================================
# ADMİN PANELİ
# =========================================================

ADMIN = """

<!DOCTYPE html>

<html lang="tr">

<head>

<meta charset="UTF-8">

<title>Admin Paneli</title>

<style>

body {

    font-family: Arial;

    background: #f4f4f4;

    margin: 0;

    padding: 30px;
}

h1 {

    color: #b22222;
}

.siparis {

    background: white;

    padding: 25px;

    margin-bottom: 20px;

    border-radius: 12px;

    box-shadow:
        0 3px 10px
        rgba(0,0,0,.1);
}

.toplam {

    color: green;

    font-size: 22px;

    font-weight: bold;
}

.urunler {

    background: #eee;

    padding: 15px;

    border-radius: 7px;
}

</style>

</head>

<body>

<h1>
📋 Gelen Siparişler
</h1>


{% for siparis in siparisler %}

<div class="siparis">

<h2>
🧾 Sipariş #{{ siparis[0] }}
</h2>

<p>
<b>👤 Müşteri:</b>
{{ siparis[1] }}
</p>

<p>
<b>📞 Telefon:</b>
{{ siparis[2] }}
</p>

<p>
<b>📍 Adres:</b>
{{ siparis[3] }}
</p>

<p>
<b>🍔 Ürünler:</b>
</p>

<div class="urunler">
{{ siparis[4] }}
</div>

<p class="toplam">
💰 {{ siparis[5] }} TL
</p>

<p>
<b>💳 Ödeme:</b>
{{ siparis[6] }}
</p>

<p>
<b>📝 Not:</b>
{{ siparis[7] or "Not yok" }}
</p>

<p>
<b>🕐 Tarih:</b>
{{ siparis[8] }}
</p>

</div>

{% else %}

<h2>
Henüz sipariş yok.
</h2>

{% endfor %}


</body>

</html>

"""


# =========================================================
# ANA SAYFA
# =========================================================

@app.route("/")
def ana_sayfa():

    return render_template_string(
        ANA_SAYFA,
        menu=MENU
    )


# =========================================================
# SİPARİŞ AL
# =========================================================

@app.route(
    "/siparis",
    methods=["POST"]
)
def siparis():

    ad_soyad = request.form.get(
        "ad_soyad"
    )

    telefon = request.form.get(
        "telefon"
    )

    adres = request.form.get(
        "adres"
    )

    odeme = request.form.get(
        "odeme"
    )

    not_bilgisi = request.form.get(
        "not_bilgisi"
    )


    toplam = 0

    urunler = []


    for i, urun in enumerate(MENU):

        adet = request.form.get(
            f"urun{i}",
            "0"
        )

        try:

            adet = int(adet)

        except:

            adet = 0


        if adet > 0:

            isim = urun[0]

            fiyat = urun[1]

            ara_toplam = (
                fiyat * adet
            )

            toplam += ara_toplam

            urunler.append(
                f"{isim} x {adet} = {ara_toplam} TL"
            )


    if not urunler:

        return """

        <h2>
        En az bir ürün seçmelisiniz.
        </h2>

        <a href="/">
        Geri dön
        </a>

        """


    urunler_text = "\n".join(
        urunler
    )


    tarih = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )


    conn = sqlite3.connect(
        "restoran.db"
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        INSERT INTO siparisler

        (
            ad_soyad,
            telefon,
            adres,
            urunler,
            toplam,
            odeme,
            not_bilgisi,
            tarih
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (
            ad_soyad,
            telefon,
            adres,
            urunler_text,
            toplam,
            odeme,
            not_bilgisi,
            tarih
        )
    )


    conn.commit()

    conn.close()


    return render_template_string(
        BASARILI,
        ad_soyad=ad_soyad,
        toplam=toplam
    )


# =========================================================
# ADMİN
# =========================================================

@app.route("/admin")
def admin():

    conn = sqlite3.connect(
        "restoran.db"
    )

    cursor = conn.cursor()


    cursor.execute(
        """

        SELECT *

        FROM siparisler

        ORDER BY id DESC

        """
    )


    siparisler = cursor.fetchall()

    conn.close()


    return render_template_string(
        ADMIN,
        siparisler=siparisler
    )


# =========================================================
# ÇALIŞTIR
# =========================================================

if __name__ == "__main__":

    veritabani()

    print("")
    print("================================")
    print("   🍽️ LEZZET DURAĞI")
    print("================================")
    print("")
    print("Müşteri:")
    print("http://127.0.0.1:5000")
    print("")
    print("Admin:")
    print("http://127.0.0.1:5000/admin")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
