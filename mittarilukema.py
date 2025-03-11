import streamlit as st
import pandas as pd
import altair as alt

st.title("Excel-tiedoston sisältö ja kilometrien seuranta")

# Kopioi Excel-tiedoston sisältö tähän. Esimerkin dataa voi muokata tarpeen mukaan.
data = [
    {"Päivämäärä": "2023-01-01", "Kilometrit": 1000},
    {"Päivämäärä": "2023-01-15", "Kilometrit": 1500},
    {"Päivämäärä": "2023-02-01", "Kilometrit": 2000},
    {"Päivämäärä": "2023-02-15", "Kilometrit": 2500},
    {"Päivämäärä": "2023-03-01", "Kilometrit": 3000},
    # Lisää rivejä Excel-tiedostosi mukaan...
]

# Muodostetaan DataFrame kovakoodatusta datasta
df = pd.DataFrame(data)
df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä'])
df = df.sort_values("Päivämäärä")

# Näytetään Excel-tiedoston sisältö
st.subheader("Excel-tiedoston sisältö")
st.dataframe(df)

# Piirretään viivakaavio Altairilla
st.subheader("Kilometrien kehitys")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä'),
    y=alt.Y('Kilometrit:Q', title='Kilometrit')
).properties(
    width=700,
    height=400,
    title="Kilometrien kehitys ajan myötä"
)
st.altair_chart(chart, use_container_width=True)

# Päivämäärähaku: käyttäjä voi valita päivämäärän ja nähdä siihen mennessä ajettujen kilometrien määrän.
st.subheader("Päivämäärähaku")
selected_date = st.date_input("Valitse päivämäärä:", value=df['Päivämäärä'].max())

# Suodatetaan tiedot siten, että näytetään vain ne rivit, joiden päivämäärä on valittua pienempi tai yhtä suuri.
filtered_df = df[df['Päivämäärä'] <= pd.to_datetime(selected_date)]

# Oletus: Excel-tiedostossa on kertymäkilometrilukema, jolloin käytetään viimeistä arvoa.
total_km = filtered_df["Kilometrit"].iloc[-1] if not filtered_df.empty else 0

st.write(f"Ajettu kilometrejä {selected_date} mennessä: **{total_km} km**")

