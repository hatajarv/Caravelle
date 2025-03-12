import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# Apufunktiot viikonloppupäivien ja arkipäivien laskemiseen
def count_weekend_days_detail(start_date, end_date):
    """Laskee päivät eriteltynä: perjantai, lauantai ja sunnuntai."""
    count_friday = 0
    count_saturday = 0
    count_sunday = 0
    d = start_date
    while d <= end_date:
        if d.weekday() == 4:  # perjantai
            count_friday += 1
        elif d.weekday() == 5:  # lauantai
            count_saturday += 1
        elif d.weekday() == 6:  # sunnuntai
            count_sunday += 1
        d += timedelta(days=1)
    return count_friday, count_saturday, count_sunday

def count_weekdays(start_date, end_date):
    """Laskee maanantaista torstaihin (0-3) päivien lukumäärän."""
    count = 0
    d = start_date
    while d <= end_date:
        if d.weekday() < 4:  # maanantai (0) - torstai (3)
            count += 1
        d += timedelta(days=1)
    return count

st.title("VW Caravelle AYE-599")

# Kovakoodattu historiallinen data
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

# Historialliset laskelmat
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

# Ennustehaku käyttäen painotettua mallia, jossa viikonlopun osuus jaetaan:
# Perjantai: 37,5%, Lauantai: 25%, Sunnuntai: 37,5%
st.subheader("Kilometrien ennustehaku (painotettu weekend/weekday)")
prediction_date = st.date_input("Valitse ennustettava päivämäärä:", value=last_date, key="prediction")
if pd.to_datetime(prediction_date) <= last_date:
    # Jos ennustuspäivä on historiallisen datan sisällä, näytetään mitattu arvo.
    predicted_km = df[df['Päivämäärä'] <= pd.to_datetime(prediction_date)].iloc[-1]['Mittarilukema']
else:
    # Ennustetaan tulevalle jaksolle: viimeisestä mittauspäivästä ennustettavaan päivämäärään.
    future_start = last_date + timedelta(days=1)
    future_end = pd.to_datetime(prediction_date)
    
    # Lasketaan tulevan jakson viikonloppupäivät eriteltynä perjantaille, lauantaille, sunnuntaille
    future_friday, future_saturday, future_sunday = count_weekend_days_detail(future_start, future_end)
    future_weekday = count_weekdays(future_start, future_end)
    
    # Historialliset viikonloppupäivät
    hist_friday, hist_saturday, hist_sunday = count_weekend_days_detail(first_date, last_date)
    # Historiallinen viikonloppujen osuus kilometreistä on 2/3 kokonaiskilometreistä.
    total_weekend_km = (2/3) * total_km_driven
    
    # Määritetään perjantai, lauantai, sunnuntai -nopeudet:
    # Perjantai: 37,5% osuus
    if hist_friday > 0:
        friday_rate = (0.375 * total_weekend_km) / hist_friday
    else:
        friday_rate = 0
    # Lauantai: 25% osuus
    if hist_saturday > 0:
        saturday_rate = (0.25 * total_weekend_km) / hist_saturday
    else:
        saturday_rate = 0
    # Sunnuntai: 37,5% osuus
    if hist_sunday > 0:
        sunday_rate = (0.375 * total_weekend_km) / hist_sunday
    else:
        sunday_rate = 0

    # Historiallinen arkipäivien (maanantai–torstai) osuus on 1/3 kokonaiskilometreistä.
    hist_weekday = count_weekdays(first_date, last_date)
    if hist_weekday > 0:
        weekday_rate = ((1/3) * total_km_driven) / hist_weekday
    else:
        weekday_rate = 0

    additional_km = (friday_rate * future_friday) + (saturday_rate * future_saturday) + (sunday_rate * future_sunday) + (weekday_rate * future_weekday)
    predicted_km = df.iloc[-1]['Mittarilukema'] + additional_km

st.write(f"Ennustettu mittarilukema {pd.to_datetime(prediction_date).strftime('%d-%m-%Y')} on: **{int(predicted_km)} km**")

# Voit lisätä myös muita osioita, kuten päivämäärähaku, kuvaaja ja datataulukko...
