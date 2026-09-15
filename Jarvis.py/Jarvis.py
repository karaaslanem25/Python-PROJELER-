import sys
import threading
import time
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pythoncom
import win32com.client
from google import genai
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# ==========================================
# 1. GEMINI AI KURULUMU
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6LF-a44hjIOx4qyks7PZ-W358GtUvUsK6fPzOrwqY5cTQ"

client = genai.Client(api_key=GEMINI_API_KEY) 

def yapay_zekaya_sor(soru):
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',  # Doğru model ismi
            contents=f"Sen Jarvis adında yardımsever, samimi ve zeki bir sesli asistansın. "
                     f"Cevapların kısa, net ve konuşma diline uygun olsun (maksimum 2-3 cümle). "
                     f"Kullanıcının şu sözüne yanıt ver: {soru}"
        )
        return response.text
    except Exception as e:
        print(f"[Gemini API Hatası]: {e}")
        
        # Google servisi çökerse kilitlenmeyi önleyen yedek yanıt mekanizması
        soru_alt = soru.lower()
        if "merhaba" in soru_alt or "selam" in soru_alt:
            return "Merhaba efendim, Google servislerinde anlık bir aksama var ama sizi duyuyorum."
        elif "nasılsın" in soru_alt:
            return "Sistemlerim aktif ancak sunucu bağlantısını kontrol ediyorum."
        elif "saat kaç" in soru_alt:
            return f"Saat şu an {time.strftime('%H:%M')}"
        elif "adın ne" in soru_alt or "kimsin" in soru_alt:
            return "Ben sizin kişisel asistanınız Jarvis'im."
        else:
            return f"'{soru}' dediğinizi aldım efendim, ancak şu an sunucuya erişemiyorum."

# ==========================================
# 2. SESLENDİRME (Thread Güvenli Windows SAPI)
# ==========================================
def seslendir(metin):
    print(f"[Jarvis]: {metin}")
    try:
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(metin)
    except Exception as e:
        print(f"[Ses Konuşma Hatası]: {e}")
    finally:
        pythoncom.CoUninitialize()

# ==========================================
# 3. SES DİNLEME VE ANLAMA DÖNGÜSÜ
# ==========================================
def jarvis_dongusu():
    r = sr.Recognizer()
    sample_rate = 16000
    sure = 5  # Konuşma kaydı süresi (saniye)

    time.sleep(1)
    seslendir("Sistemler aktif, sizi dinliyorum.")

    while True:
        try:
            print("\n[Jarvis] Dinleniyor... (Şimdi konuşun)")
            
            kayit = sd.rec(int(sure * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()
            
            print("[Jarvis] Ses alındı, çözümleniyor...")
            
            audio_data = sr.AudioData(kayit.tobytes(), sample_rate, 2)
            komut = r.recognize_google(audio_data, language="tr-TR").lower()
            
            print(f"[Siz]: {komut}")
            
            yanit = yapay_zekaya_sor(komut)
            seslendir(yanit)

        except sr.UnknownValueError:
            print("[Jarvis] Ses algılanamadı, tekrar dinleniyor...")
        except sr.RequestError as e:
            print(f"[Jarvis Hata] Google Servis Hatası: {e}")
            seslendir("İnternet veya ses tanıma servisinde bağlantı sorunu var.")
        except Exception as e:
            print(f"[Jarvis Hata]: {e}")

# ==========================================
# 4. BAŞLATICI VEYA ARAYÜZ (GUI)
# ==========================================
class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Sesli Asistan")
        self.resize(300, 150)
        
        layout = QVBoxLayout()
        self.label = QLabel("Jarvis Dinliyor...", self)
        layout.addWidget(self.label)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ui = JarvisUI()
    ui.show()
    
    threading.Thread(target=jarvis_dongusu, daemon=True).start()
    
    sys.exit(app.exec_())