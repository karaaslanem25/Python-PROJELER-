from ursina import *
import random

app = Ursina()

# Pencere ve kamera ayarları
window.color = color.rgb(20, 20, 30)
camera.position = (0, 4, -12)
camera.rotation_x = 18

# Oyun Değişkenleri
lanes = [-2, 0, 2]  # 3 kulvar (sol, orta, sağ)
lane = 1            # Başlangıç kulvarı (orta)
speed = 15          # Koşu hızı
game_over = False

# Oyuncu (Karakter)
player = Entity(
    model='cube',
    color=color.orange,
    scale=(0.6, 0.9, 0.6),
    position=(lanes[lane], 0.5, -4),
    collider='box'
)

# Yol
road = Entity(
    model='cube',
    color=color.dark_gray,
    scale=(8, 0.2, 60),
    position=(0, 0, 15)
)

# Yol çizgileri
lines = [
    Entity(model='cube', color=color.white, scale=(0.1, 0.05, 3), position=(x, 0.1, z))
    for x in [-1, 1] for z in range(-10, 40, 6)
]

# Engeller Listesi
obstacles = []

def spawn_obstacle():
    if game_over: return
    obs = Entity(
        model='cube',
        color=color.red,
        scale=(0.9, 1.2, 0.9),
        position=(random.choice(lanes), 0.6, 45),
        collider='box'
    )
    obstacles.append(obs)
    invoke(spawn_obstacle, delay=1.2)

spawn_obstacle()

# Tuş Kontrolleri (A ve D ile şerit değiştirme)
def input(key):
    global lane
    if game_over: return
    if key == 'a' and lane > 0:
        lane -= 1
    elif key == 'd' and lane < 2:
        lane += 1

# Oyun Döngüsü (Her karede çalışır)
def update():
    global speed, game_over
    if game_over: return

    # Karakteri pürüzsüzce şeride kaydır
    player.x = lerp(player.x, lanes[lane], 8 * time.dt)
    
    # Hız zamanla artsın
    speed += time.dt * 0.1

    # Yol çizgilerini hareket ettir
    for line in lines:
        line.z -= speed * time.dt
        if line.z < -10:
            line.z += 50

    # Engelleri hareket ettir ve Çarpışma Testi
    for obs in obstacles[:]:
        obs.z -= speed * time.dt
        
        # Oyuncu ile engel çarpıştı mı?
        if player.intersects(obs).hit:
            game_over = True
            Text(text="GAME OVER!", origin=(0,0), scale=3, color=color.red, background=True)
            print("[OYUN BITTI] Çarptın!")

        # Ekran arkasında kalan engelleri sil
        if obs.z < -6:
            destroy(obs)
            obstacles.remove(obs)

app.run()