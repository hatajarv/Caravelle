import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Mittausdata kovakoodattuna
measurement_data = [
    # ... (kuten aiemmin) ...
]
df_measure = pd.DataFrame(measurement_data)
df_measure['Päivämäärä'] = pd.to_datetime(df_measure['Päivämäärä'])
df_measure = df_measure.sort_values("Päivämäärä")

# Huoltohistoria kovakoodattuna
huolto_data = [
    {
        "Päivämäärä": "29.1.2025",
        "Liike": "TDI Tuning Finland OY",
        "Kuvaus": "Nopeusanturin vaihto, Vikadiagnostiikka",
        "Hinta": 949
    },
    {
        "Päivämäärä": "14.11.2024",
        "Liike": "Disel Service",
        "Kuvaus": "Bosio PP 764 suuttimet",
        "Hinta": 301.45
    },
    {
        "Päivämäärä": "10.1.2025",
        "Liike": "Motonet",
        "Kuvaus": "Lämmityslaitteen kenno",
        "Hinta": 38.9
    },
    # ... jatka kaikki rivit ...
]
df_huolto = pd.DataFrame(huolto_data)
df_huolto["Päivämäärä"] = pd.to_datetime(df_huolto["Päivämäärä"], dayfirst=True)
df_huolto = df_huolto.sort_values("Päivämäärä")

# Interpoloidaan
xp = df_measure['Päivämäärä'].map(lambda d: d.toordinal())
fp = df_measure['Mittarilukema']
df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))

st.title("VW Caravelle AYE-599")

# Näytetään huoltohistoria taulukkona
st.subheader("Huoltohistoria")
st.dataframe(df_huolto)

# Piirretään kuvaaja
base = alt.Chart(df_measure).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä'),
    y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
)
line = base.mark_line(color='blue')

points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
    x='Päivämäärä:T',
    y='Kilometrit:Q',
    tooltip=['Päivämäärä:T', alt.Tooltip('Kilometrit:Q', format=",.0f"), 'Kuvaus']
)

service_chart = (line + points).properties(
    width=700,
    height=400,
    title="Huoltohistoria – huoltojen lasketut kilometrit"
)

st.altair_chart(service_chart, use_container_width=True)
