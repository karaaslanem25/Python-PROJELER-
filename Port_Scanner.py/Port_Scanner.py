import concurrent.futures
import socket
import time
import requests

# Kontrol edilecek hedef ağ veya IP listesi (Yalnızca yetkiniz dâhilindeki cihazlar)
TARGET_HOSTS = [
    "127.0.0.1",
    "localhost"
]

# Kontrol edilecek servis portları (80: HTTP, 443: HTTPS, 22: SSH)
CHECK_PORTS = [80, 443, 22]

def check_tcp_port(ip, port, timeout=1.5):
    """
    Belirtilen IP ve Port üzerindeki servisin erişilebilirliğini test eder.
    """
    start_time = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            latency = (time.time() - start_time) * 1000
            if result == 0:
                return port, True, round(latency, 2)
    except Exception:
        pass
    return port, False, None

def inspect_host(host):
    """
    Bir ana bilgisayarın (host) port durumlarını ve erişim süresini raporlar.
    """
    print(f"\n[*] Sunucu Kontrol Ediliyor: {host}")
    open_services = []
    
    for port in CHECK_PORTS:
        _, is_open, latency = check_tcp_port(host, port)
        if is_open:
            open_services.append((port, latency))
            print(f"  [+] Port {port:<5} -> AÇIK | Yanıt Süresi: {latency} ms")
        else:
            print(f"  [-] Port {port:<5} -> KAPALI / Yanıt Yok")

    return host, open_services

def main():
    print("=== Sistem ve Servis Sağlık Durumu Taraması ===")
    
    # Eşzamanlı (Concurrent) iş parçacıkları ile sistem analizi
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(inspect_host, TARGET_HOSTS))

    print("\n" + "="*45)
    print("Tarama Tamamlandı.")

if __name__ == "__main__":
    main()