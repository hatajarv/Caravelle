import streamlit as st
import pandas as pd
import altair as alt

# Ladataan Excel-tiedosto. Varmista, että Excel-tiedoston nimi ja sarakeotsikot ovat oikein.
@st.cache_data
def load_data():
    # Muuta polku tarvittaessa, jos Excel-tiedosto ei sijaitse samassa kansiossa
    df = pd.read_excel("Caravelle AYE-599 kilometrit.xlsx")
    # Oletetaan, että tiedostossa on sarakkeet "Päivämäärä" ja "Kilometrit".
    df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä'])
    return df

df = load_data()
df = df.sort_values("Päivämäärä")

st.title("Kilometrien Seuranta")

# Piirretään käyrä Altair-kirjaston avulla
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

# Päivämäärähaku: käyttäjä voi valita päivämäärän ja nähdä, kuinka monta kilometriä on ajettu siihen mennessä.
st.subheader("Päivämäärähaku")
selected_date = st.date_input("Valitse päivämäärä:", value=df['Päivämäärä'].max())

# Suodatetaan data siihen päivämäärään mennessä olevat merkinnät
filtered_df = df[df['Päivämäärä'] <= pd.to_datetime(selected_date)]

# Jos data sisältää päivittäisiä ajomääriä, summataan ne yhteen.
# Jos tiedot ovat kertyviä (eli jokaisessa rivissä on kokonaiskilometrilukema), käytä sen sijaan:
# total_km = filtered_df["Kilometrit"].iloc[-1] if not filtered_df.empty else 0
total_km = filtered_df["Kilometrit"].sum() if not filtered_df.empty else 0

st.write(f"Ajettu kilometrejä {selected_date} mennessä: **{total_km} km**")
