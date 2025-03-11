import pandas as pd
import streamlit as st
from datetime import datetime

# Syötetyt tiedot
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

# Käyttäjä valitsee päivämäärän
user_date = st.date_input("Valitse päivämäärä")

# Tarkistetaan lähin mittarilukema
df_filtered = df[df['Päivämäärä'] <= user_date]

if not df_filtered.empty:
    latest_km = df_filtered.iloc[-1]['Mittarilukema']
    st.success(f"📅 Mittarilukema {user_date}: **{latest_km} km**")
else:
    st.warning("⚠️ Ei tietoa valitusta päivämäärästä.")

# Näytetään taulukko
st.subheader("📊 Kaikki mittarilukemat")
st.dataframe(df)
