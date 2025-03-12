import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

st.title("VW Caravelle AYE-599")

# ----------------------------
# Mittausdata (kovakoodattu)
measurement_data = [
    {"Päivämäärä": "2022-03-09", "Mittarilukema": 154029},
    {"Päivämäärä": "2022-03-22", "Mittarilukema": 154829},
    {"Päivämäärä": "2022-04-11", "Mittarilukema": 155695},
    {"Päivämäärä": "2023-10-12", "Mittarilukema": 183951},
    {"Päivämäärä": "2023-10-16", "Mittarilukema": 184667},
    {"Päivämäärä": "2024-03-02", "Mittarilukema": 193158},
    {"Päivämäärä": "2024-03-30", "Mittarilukema": 194698},
    {"Päivämäärä": "2024-10-29", "Mittarilukema": 198152},
    {"Päivämäärä": "2024-11-06", "Mittarilukema": 198850},
    {"Päivämäärä": "2024-11-16", "Mittarilukema": 200069},
    {"Päivämäärä": "2024-11-18", "Mittarilukema": 200221},
    {"Päivämäärä": "2024-11-20", "Mittarilukema": 200371},
    {"Päivämäärä": "2024-11-22", "Mittarilukema": 200807},
    {"Päivämäärä": "2024-12-09", "Mittarilukema": 201873},
    {"Päivämäärä": "2025-01-03", "Mittarilukema": 203245},
    {"Päivämäärä": "2025-01-06", "Mittarilukema": 203448},
    {"Päivämäärä": "2025-01-09", "Mittarilukema": 203711},
    {"Päivämäärä": "2025-03-11", "Mittarilukema": 207621}
]

df_measure = pd.DataFrame(measurement_data)
df_measure['Päivämäärä'] = pd.to_datetime(df_measure['Päivämäärä'])
df_measure = df_measure.sort_values("Päivämäärä")

# Lasketaan mittausdatan perustiedot
first_date = df_measure['Päivämäärä'].min()
last_date = df_measure['Päivämäärä'].max()
initial_value = df_measure.iloc[0]['Mittarilukema']
total_km_driven = df_measure.iloc[-1]['Mittarilukema'] - initial_value
num_days = (last_date - first_date).days
daily_avg = total_km_driven / num_days
monthly_avg = daily_avg * 30
yearly_avg = daily_avg * 365

st.info(f"""**Havaintojen ajanjakso:** {first_date.strftime('%d-%m-%Y')} - {last_date.strftime('%d-%m-%Y')}

**Ajetut kilometrit yhteensä:** {total_km_driven} km

**Päivittäinen keskiarvo:** {daily_avg:.1f} km/päivä  
**Kuukausittainen keskiarvo:** {monthly_avg:.1f} km/kk  
**Vuosittainen keskiarvo:** {yearly_avg:.1f} km/vuosi
""")

# ----------------------------
# Huoltohistoria: Luetaan Excel-tiedostosta
try:
    df_huolto = pd.read_excel("/mnt/data/AYE_599_huoltohistoria.xlsx")
    st.write("Huoltohistorian raakatiedot:")
    st.dataframe(df_huolto.head())
except Exception as e:
    st.error(f"Huoltohistorian tiedoston lukemisessa tapahtui virhe: {e}")
    df_huolto = pd.DataFrame()

# Jos huoltohistoriadataa löytyy, prosessoidaan se
if not df_huolto.empty:
    # Tarkistetaan, että sarake "Päivämäärä" on olemassa
    if 'Päivämäärä' not in df_huolto.columns:
        st.error("Huoltohistoriassa ei löytynyt saraketta 'Päivämäärä'. Löydetyt sarakkeet: " + ", ".join(df_huolto.columns))
    else:
        # Muutetaan huoltojen päivämäärät datetime-muotoon ja järjestetään data
        df_huolto['Päivämäärä'] = pd.to_datetime(df_huolto['Päivämäärä'])
        df_huolto = df_huolto.sort_values("Päivämäärä")
        
        # Interpoloidaan auton mittarilukemat huoltojen päivämäärien perusteella
        # Muutetaan mittausdatan päivämäärät ordinal-lukuihin
        xp = df_measure['Päivämäärä'].map(lambda d: d.toordinal())
        fp = df_measure['Mittarilukema']
        df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))
        
        st.write("Huoltohistorian taulukko (sisältää lasketut kilometrit):")
        st.dataframe(df_huolto)
        
        # Piirretään kuvaaja, jossa näkyy auton mittarilukemien kehitys (sininen viiva)
        # ja huoltojen merkinnät (punaiset pisteet)
        tick_dates = [d.to_pydatetime() for d in pd.date_range(start=first_date, end=last_date, freq='2M')]
        base = alt.Chart(df_measure).encode(
            x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
            y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
        )
        line = base.mark_line(color='blue')
        points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
            x='Päivämäärä:T',
            y='Kilometrit:Q',
            tooltip=['Päivämäärä:T', alt.Tooltip('Kilometrit:Q', format=",.0f")]
        )
        service_chart = (line + points).properties(
            width=700,
            height=400,
            title="Huoltohistoria – huoltojen lasketut kilometrit"
        )
        st.altair_chart(service_chart, use_container_width=True)
else:
    st.write("Huoltohistoriaa ei löytynyt.")

# ----------------------------
# Näytetään mittausdatan sisältö taulukkona
st.subheader("Mittarilukemien historia")
df_display = df_measure.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)
