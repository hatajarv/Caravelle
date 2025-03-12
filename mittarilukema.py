import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ------------------------------------
# 1. Mittausdata (kovakoodattu)
# ------------------------------------
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

# ------------------------------------
# 2. Huoltohistoria (kovakoodattu)
# ------------------------------------
# Alla on listattuna rivit, jotka mainitsit aiemmin.
# Sarakkeet: Päivämäärä, Liike, Kuvaus, Hinta
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
    {
        "Päivämäärä": "10.1.2025",
        "Liike": "TDI Tuning Finland Oy",
        "Kuvaus": "\"Jatkosäätö\"",
        "Hinta": 300
    },
    {
        "Päivämäärä": "9.1.2025",
        "Liike": "Motonet",
        "Kuvaus": "Puhaltimen moottori, ilmastointikompuran hihna",
        "Hinta": 125.85
    },
    {
        "Päivämäärä": "9.12.2024",
        "Liike": "Jyväskylän Auto-Startti",
        "Kuvaus": "D5WZ Eberi",
        "Hinta": 1550
    },
    {
        "Päivämäärä": "19.11.2024",
        "Liike": "Jyväskylän Auto-Startti",
        "Kuvaus": "Eber-sisäpuhalluksen kytkentä",
        "Hinta": 146
    },
    {
        "Päivämäärä": "15.11.2024",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Öljyjen vaihto, moottori, takaperä, laatikko",
        "Hinta": 325.62
    },
    {
        "Päivämäärä": "29.10.2024",
        "Liike": "Jyväskylän Auto-Startti",
        "Kuvaus": "Eber hehkutulpan vaihto",
        "Hinta": 112.2
    },
    {
        "Päivämäärä": "30.5.2024",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Takapyörän laakeri, Jarulevy taka, Jarrupala taka",
        "Hinta": 382.7
    },
    {
        "Päivämäärä": "7.6.2024",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Alapallonivel vasen etu",
        "Hinta": 64.6
    },
    {
        "Päivämäärä": "26.9.2023",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Öljynvaihto, ilman- ja polttoaineen suodattimet",
        "Hinta": 252.6
    },
    {
        "Päivämäärä": "18.11.2022",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Jakopää, vesipumppu",
        "Hinta": 579.2
    },
    {
        "Päivämäärä": "10.11.2023",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Alapallonivel oike, Rt-pää vas. Ulompi",
        "Hinta": 125.3
    },
    {
        "Päivämäärä": "20.11.2023",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Rt-sisäpää vasen",
        "Hinta": 75.3
    },
    {
        "Päivämäärä": "10.1.2025",
        "Liike": "A&H Nieminen",
        "Kuvaus": "Turbon ja suutinkärkien vaihto",
        "Hinta": 847
    },
    {
        "Päivämäärä": "12.11.2024",
        "Liike": "Fin-Turbo Oy",
        "Kuvaus": "Turbon muutostyö",
        "Hinta": 871
    }
]

df_huolto = pd.DataFrame(huolto_data)

# Muunnetaan päivämäärät dayfirst=True, jotta 29.1.2025 tulkitaan oikein
df_huolto["Päivämäärä"] = pd.to_datetime(df_huolto["Päivämäärä"], dayfirst=True, errors='coerce')
df_huolto = df_huolto.dropna(subset=["Päivämäärä"])  # poistetaan mahdolliset rivit, joissa päivämäärä ei kelpaa
df_huolto = df_huolto.sort_values("Päivämäärä")

# Interpoloidaan, jotta saadaan km-lukema kullekin huoltopäivälle
xp = df_measure['Päivämäärä'].map(lambda d: d.toordinal())
fp = df_measure['Mittarilukema']
df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))

# ------------------------------------
# 3. Sovelluksen otsikko ja esitykset
# ------------------------------------
st.title("VW Caravelle AYE-599 – Huoltohistoria ja Mittarilukema")

st.subheader("Huoltohistoria (taulukko)")
st.dataframe(df_huolto)

# Piirretään Altair-kuvaaja: sininen viiva = mittausdata, punaiset pisteet = huollot
tick_dates = [d.to_pydatetime() for d in pd.date_range(
    start=df_measure['Päivämäärä'].min(),
    end=df_measure['Päivämäärä'].max(),
    freq='2M'
)]
base = alt.Chart(df_measure).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä',
            axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
    y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
)
line = base.mark_line(color='blue')

points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
    x='Päivämäärä:T',
    y='Kilometrit:Q',
    tooltip=[
        'Päivämäärä:T',
        alt.Tooltip('Kilometrit:Q', format=",.0f"),
        'Liike',
        'Kuvaus',
        alt.Tooltip('Hinta:Q', format=",.2f")
    ]
)

service_chart = (line + points).properties(
    width=700,
    height=400,
    title="Huoltohistoria – Huoltojen lasketut kilometrit"
)

st.subheader("Huoltohistoria (kuvaaja)")
st.altair_chart(service_chart, use_container_width=True)

# ------------------------------------
# 4. Näytetään mittausdatan taulukko
# ------------------------------------
st.subheader("Mittarilukemien historia")
df_display = df_measure.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)

