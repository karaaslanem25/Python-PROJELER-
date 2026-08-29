# app.py

import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("📈 Canlı Borsa Dashboard")

# hisse seçimi
symbol = st.text_input("Hisse gir (örn: AAPL, TSLA, THYAO.IS)", "THYAO.IS")

# veri çek (son 1 gün - 1 dakikalık)
df = yf.download(symbol, period="1d", interval="1m")

if df.empty:
    st.error("Veri alınamadı. Hisse kodunu kontrol et.")
    st.stop()

# hareketli ortalama
df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

# AL / SAT sinyali
df["Signal"] = 0
df.loc[df["MA20"] > df["MA50"], "Signal"] = 1   # AL
df.loc[df["MA20"] < df["MA50"], "Signal"] = -1  # SAT

# son durum
last_signal = df["Signal"].iloc[-1]

if last_signal == 1:
    st.success("🟢 AL Sinyali")
elif last_signal == -1:
    st.error("🔴 SAT Sinyali")
else:
    st.warning("⚪ Bekle")

# grafik
fig, ax = plt.subplots(figsize=(10,5))

ax.plot(df.index, df["Close"], label="Fiyat")
ax.plot(df.index, df["MA20"], label="MA20")
ax.plot(df.index, df["MA50"], label="MA50")

ax.legend()
ax.set_title(symbol + " Canlı Grafik")

st.pyplot(fig)

# tablo
st.dataframe(df.tail(20))