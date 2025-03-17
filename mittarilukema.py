import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# Ladataan huoltohistoria Excelistä
def load_maintenance_data(file_path):
    df_huolto = pd.read_excel(file_path)
    df_huolto['Päivämäärä'] = pd.to_datetime(df_huolto['Päivämäärä'], dayfirst=True, errors='coerce')
    df_huolto = df_huolto.dropna(subset=['Päivämäärä'])
    df_huolto = df_huolto.sort_values('Päivämäärä')
    return df_huolto

# Ladataan huoltohistoria
file_path = "/mnt/data/AYE_599_huoltohistoria.xlsx"
df_huolto = load_maintenance_data(file_path)

# Kovakoodattu historiallinen data
data = [
    {"Päivämäärä": "2022-03-09", "Mittarilukema": 154029},
    {"Päivämäärä": "2022-03-22", "Mittarilukema": 154829},
    {"Päivämäärä": "2022-04-11", "Mittarilukema": 155695},
    {"Päivämäärä": "2022-05-10", "Mittarilukema": 156912},
    {"Päivämäärä": "2022-11-04", "Mittarilukema": 167026},
    {"Päivämäärä": "2022-11-09", "Mittarilukema": 167086},
    {"Päivämäärä": "2023-11-16", "Mittarilukema": 186769},
    {"Päivämäärä": "2025-03-11", "Mittarilukema": 207621}
]

df = pd.DataFrame(data)
df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä'])
df = df.sort_values("Päivämäärä")

# Lasketaan interpolaatio huoltojen kohdalle
xp = df['Päivämäärä'].map(lambda d: d.toordinal())
fp = df['Mittarilukema']
df_huolto['Mittarilukema'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))

# Lasketaan huoltokustannusten yhteenvedot
maintenance_total = df_huolto["Hinta"].sum()
maintenance_start = df_huolto["Päivämäärä"].min()
maintenance_end = df_huolto["Päivämäärä"].max()
maintenance_period_days = (maintenance_end - maintenance_start).days

if maintenance_period_days > 0:
    monthly_maintenance_cost = maintenance_total / (maintenance_period_days / 30)
    yearly_maintenance_cost = maintenance_total / (maintenance_period_days / 365)
else:
    monthly_maintenance_cost = yearly_maintenance_cost = 0

# Näytetään huoltohistorian tiedot taulukkona, vain päivämäärät ja mittarilukemat
st.subheader("Huoltohistorian kilometrilukemat")
st.dataframe(df_huolto[['Päivämäärä', 'Mittarilukema']])

# Lisätään huoltohistorian kuvaaja
st.subheader("Huoltojen kehitys mittarilukeman suhteen")
base = alt.Chart(df).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä'),
    y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
)
line = base.mark_line(color='blue')
points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
    x='Päivämäärä:T',
    y='Mittarilukema:Q',
    tooltip=['Päivämäärä:T', 'Mittarilukema:Q']
)
service_chart = (line + points).properties(
    width=700,
    height=400,
    title="Huoltohistoria – Huoltojen lasketut kilometrit"
)
st.altair_chart(service_chart, use_container_width=True)
