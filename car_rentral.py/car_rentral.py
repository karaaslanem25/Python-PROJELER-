import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

st.set_page_config(page_title="Canlı Trafik İzleme Paneli", layout="wide")

st.title("🚦 Canlı Şehir Trafik ve Sinyalizasyon Paneli")
st.caption("Sensörlerden gelen anlık veri akışı simülasyonu")

# Metrik kartları için alanlar
col1, col2, col3, col4 = st.columns(4)

with col1:
    m1 = st.empty()
with col2:
    m2 = st.empty()
with col3:
    m3 = st.empty()
with col4:
    m4 = st.empty()

st.divider()

# Grafik alanları
g1, g2 = st.columns(2)
with g1:
    st.subheader("Anlık Araç Yoğunluğu")
    chart_area = st.empty()

with g2:
    st.subheader("Kavşak Sinyal Durumları")
    status_area = st.empty()

# Veri depolama (Son 20 saniye)
history_df = pd.DataFrame(columns=["Zaman", "Kavsak_A", "Kavsak_B", "Kavsak_C", "Kavsak_D"])

# Canlı Döngü
for i in range(100):
    current_time = time.strftime("%H:%M:%S")
    
    # Anlık rastgele (canlı sensör benzeri) veri üretimi
    k_a = np.random.randint(10, 85)
    k_b = np.random.randint(5, 60)
    k_c = np.random.randint(20, 95)
    k_d = np.random.randint(15, 40)
    
    # Metrikleri güncelleme
    m1.metric("Kavşak A (Merkez)", f"{k_a} Araç", delta=f"{np.random.randint(-5, 6)} Araç")
    m2.metric("Kavşak B (Meydan)", f"{k_b} Araç", delta=f"{np.random.randint(-5, 6)} Araç")
    m3.metric("Kavşak C (Sahil)", f"{k_c} Araç", delta=f"{np.random.randint(-5, 6)} Araç")
    m4.metric("Kavşak D (Otoban)", f"{k_d} Araç", delta=f"{np.random.randint(-5, 6)} Araç")
    
    # Veri geçmişini güncelle
    new_row = pd.DataFrame([{
        "Zaman": current_time,
        "Kavsak_A": k_a,
        "Kavsak_B": k_b,
        "Kavsak_C": k_c,
        "Kavsak_D": k_d
    }])
    history_df = pd.concat([history_df, new_row]).tail(15)
    
    # Çizgi Grafik Güncelleme
    fig_line = px.line(
        history_df, 
        x="Zaman", 
        y=["Kavsak_A", "Kavsak_B", "Kavsak_C", "Kavsak_D"],
        markers=True,
        labels={"value": "Yoğunluk", "variable": "Kavşak"}
    )
    chart_area.plotly_chart(fig_line, use_container_width=True)
    
    # Işık Durumu (En yoğun kavşağa yeşil yakma mantığı)
    densities = {"Kavşak A": k_a, "Kavşak B": k_b, "Kavşak C": k_c, "Kavşak D": k_d}
    max_k = max(densities, key=densities.get)
    
    status_df = pd.DataFrame([
        {"Kavşak": k, "Yoğunluk": v, "Durum": "🟢 YEŞİL (Öncelikli)" if k == max_k else "🔴 KIRMIZI"}
        for k, v in densities.items()
    ])
    
    status_area.dataframe(status_df, use_container_width=True)
    
    time.sleep(1)