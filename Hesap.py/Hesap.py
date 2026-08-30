import tkinter as tk
from tkinter import messagebox

# Ana pencereyi oluşturuyoruz
pencere = tk.Tk()
pencere.title("Pratik Hesap Makinesi")
pencere.geometry("300x400")
pencere.config(bg="#222222")

# Ekran (Giriş kutusu)
giris = tk.Entry(pencere, font=("Arial", 20), justify="right", bg="#333333", fg="white", bd=0)
giris.pack(fill="x", padx=15, pady=20, ipady=10)

# Butona basıldığında ekrana yazdırma fonksiyonu
def tikla(deger):
    giris.insert(tk.END, deger)

# Temizleme fonksiyonu
def temizle():
    giris.delete(0, tk.END)

# Hesaplama fonksiyonu
def hesapla():
    try:
        sonuc = eval(giris.get())
        temizle()
        giris.insert(0, str(sonuc))
    except Exception:
        messagebox.showerror("Hata", "Geçersiz İşlem!")

# Tuş takımını yerleştireceğimiz alan
tuslar_cercevesi = tk.Frame(pencere, bg="#222222")
tuslar_cercevesi.pack()

# Buton tasarımı ve yerleşimi
butonlar = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('+', 4, 2), ('=', 4, 3)
]

for (text, satir, sutun) in butonlar:
    if text == '=':
        b = tk.Button(tuslar_cercevesi, text=text, width=5, height=2, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=hesapla)
    elif text == 'C':
        b = tk.Button(tuslar_cercevesi, text=text, width=5, height=2, font=("Arial", 12, "bold"), bg="#f44336", fg="white", command=temizle)
    else:
        b = tk.Button(tuslar_cercevesi, text=text, width=5, height=2, font=("Arial", 12, "bold"), bg="#444444", fg="white", command=lambda t=text: tikla(t))
    
    b.grid(row=satir, column=sutun, padx=5, pady=5)

pencere.mainloop()