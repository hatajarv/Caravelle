import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# Funktio, joka laskee viikonloppujen ja arkipäivien lukumäärän kahden päivämäärän väliltä (mukaan lukien molemmat)
def count_weekend_weekday(start_date, end_date):
    weekend = 0
    weekday = 0
    d = start_date
    while d <= end_date:
        # Pythonissa: maanantai = 0, ..., sunnuntai = 6.
        if d.weekday() >= 4:  # perjantai (4), lauantai (5), sunnuntai (6)
            weekend += 1
        else:
            weekday += 1
        d += timedelta(days=1)
    return weekend, weekday

st.title("VW Caravelle AYE-599")

# Kovakoodattu data (mittauspäivämäärät ja mittarilukemat)
data = [
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

df = pd.DataFrame(data)
df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä'])
df = df.sort_values("Päivämäärä")

# Historiallisten tietojen laskenta
first_date = df['Päivämäärä'].min()
last_date = df['Päivämäärä'].max()
total_km_driven = df.iloc[-1]['Mittarilukema'] - df.iloc[0]['Mittarilukema']
num_days = (last_date - first_date).days
daily_avg = total_km_driven / num_days
monthly_avg = daily_avg * 30
yearly_avg = daily_avg * 365

# Polttoainekustannukset (oletus: 9 l/100km, diesel 1,70 €/l)
diesel_price = 1.70
monthly_fuel_cost = (monthly_avg / 100 * 9) * diesel_price
yearly_fuel_cost = (yearly_avg / 100 * 9) * diesel_price

info_text = f"""**Havaintojen ajanjakso:** {first_date.strftime('%d-%m-%Y')} - {last_date.strftime('%d-%m-%Y')}

**Ajetut kilometrit yhteensä:** {total_km_driven} km

**Päivittäinen keskiarvo:** {daily_avg:.1f} km/päivä  
**Kuukausittainen keskiarvo:** {monthly_avg:.1f} km/kk  
**Vuosittainen keskiarvo:** {yearly_avg:.1f} km/vuosi

**Kuukausittaiset polttoainekustannukset:** {monthly_fuel_cost:.2f} €/kk  
**Vuosittaiset polttoainekustannukset:** {yearly_fuel_cost:.2f} €/vuosi
"""
st.info(info_text)

# Päivämäärähaku (historialliset tiedot)
st.subheader("Päivämäärähaku")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="historical")
# Jos valittu päivä on historiallisen ajan sisällä, näytetään viimeisin mitattu arvo.
if pd.to_datetime(selected_date) <= last_date:
    filtered_df = df[df['Päivämäärä'] <= pd.to_datetime(selected_date)]
    total_km = filtered_df["Mittarilukema"].iloc[-1]
    selected_date_str = pd.to_datetime(selected_date).strftime("%d-%m-%Y")
    st.write(f"Ajettu kilometrejä {selected_date_str} mennessä: **{total_km} km**")
else:
    st.write("Valittu päivämäärä on viimeisimmän mittauksen jälkeen. Käytä ennustehakua.")

# Ennustehaku käyttäen weekend/weekday–painotettua mallia
# Lasketaan ensin kokonaiskilometrien erotus historiallisen ajanjakson aikana painotettuna
total_weekend, total_weekday = count_weekend_weekday(first_date, last_date)
overall_weekend_rate = (2/3 * total_km_driven) / total_weekend
overall_weekday_rate = (1/3 * total_km_driven) / total_weekday

st.subheader("Kilometrien ennustehaku")
prediction_date = st.date_input("Valitse ennustettava päivämäärä:", value=last_date, key="prediction")
if pd.to_datetime(prediction_date) <= last_date:
    # Jos ennustuspäivä on historiallisen ajan sisällä, näytetään mitattu arvo.
    predicted_km = df[df['Päivämäärä'] <= pd.to_datetime(prediction_date)].iloc[-1]['Mittarilukema']
else:
    # Tulevalle jaksolle lasketaan viikonloppu- ja arkipäivien lukumäärät
    future_start = last_date + timedelta(days=1)
    future_end = pd.to_datetime(prediction_date)
    future_weekend, future_weekday = count_weekend_weekday(future_start, future_end)
    predicted_additional_km = overall_weekend_rate * future_weekend + overall_weekday_rate * future_weekday
    predicted_km = df.iloc[-1]['Mittarilukema'] + predicted_additional_km

st.write(f"Ennustettu mittarilukema {pd.to_datetime(prediction_date).strftime('%d-%m-%Y')} on: **{int(predicted_km)} km**")

# Altair-kuvaaja
tick_dates = [d.to_pydatetime() for d in pd.date_range(start=first_date, end=last_date, freq='2M')]

st.subheader("Mittarilukeman kehitys")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
    y=alt.Y('Mittarilukema:Q', title='Mittarilukema', 
            scale=alt.Scale(domain=[145000, 250000]),
            axis=alt.Axis(values=list(range(145000, 250000+5000, 5000))))
).properties(
    width=700,
    height=400,
    title="Mittarilukeman kehitys ajan myötä"
)
st.altair_chart(chart, use_container_width=True)

# Näytetään lopuksi Excel-tiedoston sisältö taulukkona
st.subheader("Excel-tiedoston sisältö")
df_display = df.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)
