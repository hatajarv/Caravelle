import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from datetime import datetime

# --- 📌 Syötetyt tiedot ---
data = {
    "Päivämäärä": ["20.11.2024", "9.12.2024", "18.11.2024", "12.10.2023", "16.10.2023", "11.4.2022", 
                    "22.3.2022", "9.3.2022", "2.3.2024", "30.3.2024", "6.11.2024", "16.11.2024", 
                    "22.11.2024", "3.1.2025", "6.1.2025", "9.1.2025", "19.3.2025"],
    "Mittarilukema": [200371, 201873, 200221, 183951, 184667, 155695, 154829, 154029, 
                       193158, 194698, 198850, 200069, 200807, 203245, 203448, 203711, 207621]
}

# Muunna päivämäärät oikeaan muotoon
data['Päivämäärä'] = [datetime.strptime(date, "%d.%m.%Y") for date in data['Päivämäärä']]

# Luo DataFrame ja järjestä päivämäärän mukaan
df = pd.DataFrame(data)
df.sort_values('Päivämäärä', inplace=True)

# --- STREAMLIT WEB-SOVELLUS ---
st.title("🚗 Auton mittarilukemat ajan myötä")

st.write("Syötä päivämäärä ja tarkista mittarilukema siihen mennessä.")

# 🔹 Käyttäjä valitsee päivämäärän
user_date = st.date_input("Valitse päivämäärä")

# Muunna käyttäjän syöttämä päivämäärä oikeaan muotoon
user_date = datetime.combine(user_date, datetime.min.time())

# 🔹 Suodata aiempien päivämäärien mittarilukemat
df_filtered = df[df['Päivämäärä'] <= user_date]

# 🔹 Näytä viimeisin mittarilukema käyttäjän valitsemasta päivämäärästä
if not df_filtered.empty:
    latest_km = df_filtered.iloc[-1]['Mittarilukema']
    st.success(f"📅 Mittarilukema {user_date.strftime('%d.%m.%Y')}: **{latest_km} km**")
else:
    st.warning("⚠️ Ei tietoa valitusta päivämäärästä.")

# --- 📊 PIIRRÄ KUVAJA ---
st.subheader("📈 Kilometrilukeman kehitys")
fig = px.line(df, x='Päivämäärä', y='Mittarilukema', markers=True, title="Kilometrilukemat ajan myötä")
st.plotly_chart(fig)

# --- 🔮 TULEVAISUUDEN ARVIOINTI ---
st.subheader("🔮 Ennusta kilometrilukema tulevaisuuteen")

# Muunna päivämäärät numeeriseen muotoon ennustamista varten
df['Päivämäärä_ordinal'] = df['Päivämäärä'].map(datetime.toordinal)

# Lineaarinen regressio (ennusteen laskeminen)
z = np.polyfit(df['Päivämäärä_ordinal'], df['Mittarilukema'], 1)
p = np.poly1d(z)

# Käyttäjä syöttää tulevaisuuden päivämäärän
future_date = st.date_input("Valitse tuleva päivämäärä")
future_date_ordinal = datetime.combine(future_date, datetime.min.time()).toordinal()

# Lasketaan ennustettu kilometrilukema
predicted_km = p(future_date_ordinal)
st.info(f"📅 Arvioitu mittarilukema {future_date.strftime('%d.%m.%Y')}: **{int(predicted_km)} km**")

# --- 📊 PIIRRÄ KUVAJA ENNUSTEELLA ---
fig2 = px.line(df, x='Päivämäärä', y='Mittarilukema', markers=True, title="Kilometrilukemat + ennuste")
fig2.add_scatter(x=[future_date], y=[predicted_km], mode='markers', marker=dict(color='red', size=10), name="Ennuste")
st.plotly_chart(fig2)

# --- 📋 Näytetään taulukko ---
st.subheader("📊 Kaikki mittarilukemat")
st.dataframe(df[['Päivämäärä', 'Mittarilukema']])
