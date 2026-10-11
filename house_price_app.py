import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Ames Konut Fiyat Tahmin Uygulaması",
    page_icon="🏠",
    layout="centered",
)

# Eğitilmiş modeli ve sütunları yükleme
@st.cache_resource
def load_model():
  model = joblib.load("house_price_model.pkl")
  model_columns = joblib.load("model_columns.pkl")
  return model, model_columns


model, model_columns = load_model()

st.title("🏠 Ames Konut Fiyat Tahmin Sistemi")
st.write(
    "Bu uygulama, ev özelliklerini kullanarak konut satış fiyatını (`SalePrice`)"
    " tahmin eder."
)

st.sidebar.header("Ev Özellikleri (Girdiler)")

# Kullanıcıdan temel ve en önemli özellikleri almak için arayüz elemanları
overall_qual = st.sidebar.slider(
    "Genel Kalite (Overall Qual) (1-10)", 1, 10, 6
)
gr_liv_area = st.sidebar.number_input(
    "Yaşam Alanı Metrekaresi (Gr Liv Area)",
    min_value=300,
    max_value=5000,
    value=1500,
)
garage_cars = st.sidebar.selectbox("Garaj Araç Kapasitesi (Garage Cars)", [0, 1, 2, 3, 4])
garage_area = st.sidebar.number_input(
    "Garaj Alanı (Garage Area)", min_value=0, max_value=1500, value=400
)
total_bsmt_sf = st.sidebar.number_input(
    "Toplam Bodrum Alanı (Total Bsmt SF)",
    min_value=0,
    max_value=3000,
    value=800,
)
year_built = st.sidebar.number_input(
    "İnşa Yılı (Year Built)", min_value=1800, max_value=2026, value=2003
)

# Tahmin butonu
if st.sidebar.button("Fiyatı Tahmin Et"):
  # Boş bir veri çerçevesi oluşturalım (model sütunlarına tam uyumlu olması için)
  input_data = pd.DataFrame(0, index=[0], columns=model_columns)

  # Kullanıcıdan alınan temel sayısal değerleri yerleştirelim
  if "Overall Qual" in input_data.columns:
    input_data["Overall Qual"] = overall_qual
  if "Gr Liv Area" in input_data.columns:
    input_data["Gr Liv Area"] = gr_liv_area
  if "Garage Cars" in input_data.columns:
    input_data["Garage Cars"] = garage_cars
  if "Garage Area" in input_data.columns:
    input_data["Garage Area"] = garage_area
  if "Total Bsmt SF" in input_data.columns:
    input_data["Total Bsmt SF"] = total_bsmt_sf
  if "Year Built" in input_data.columns:
    input_data["Year Built"] = year_built

  # Tahmin yapma
  prediction = model.predict(input_data)[0]

  st.success(f"### Tahmini Konut Fiyatı: ${prediction:,.2f}")
  st.balloons()