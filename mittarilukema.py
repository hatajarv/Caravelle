import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# Apufunktiot viikonloppupäivien ja arkipäivien laskemiseen
def count_weekend_days_detail(start_date, end_date):
    """
    Laskee päivät eriteltynä: perjantai, lauantai ja sunnuntai
    """
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
    """
    Laskee maanantaista torstaihin (0-3) päivien lukumäärän
    """
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

# Historiallisten tietojen laskenta
first_date = df['Päivämäärä'].min()
last_date = df['Päivämäärä'].max()
initial_value = df.iloc[0]['Mittarilukema']
total_km_driven = df.iloc[-1]['Mittarilukema'] - initial_value

# Näistä lasketaan peruskeskiarvot (tätä voidaan käyttää myös laskentapohjana)
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

# Lasketaan historiallisten tietojen painotukset käyttäen koko mittausjaksoa
# Oletus: 2/3 kokonaiskilometreistä kertyy viikonloppuina ja 1/3 arkipäivinä.
hist_friday, hist_saturday, hist_sunday = count_weekend_days_detail(first_date, last_date)
hist_weekend = hist_friday + hist_saturday + hist_sunday
total_weekend_km = (2/3) * total_km_driven
if hist_friday > 0:
    friday_rate = (0.375 * total_weekend_km) / hist_friday
else:
    friday_rate = 0
if hist_saturday > 0:
    saturday_rate = (0.25 * total_weekend_km) / hist_saturday
else:
    saturday_rate = 0
if hist_sunday > 0:
    sunday_rate = (0.375 * total_weekend_km) / hist_sunday
else:
    sunday_rate = 0

hist_weekday = count_weekdays(first_date, last_date)
if hist_weekday > 0:
    weekday_rate = ((1/3) * total_km_driven) / hist_weekday
else:
    weekday_rate = 0

# Yhtenäinen laskentamalli: Käytetään painotettua mallia sekä historiallisen datan haussa että ennusteessa
st.subheader("Päivämäärähaku ja ennuste (painotettu mallilla)")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="combined")
period_start = first_date
period_end = pd.to_datetime(selected_date)

# Lasketaan valitun ajanjakson pituus painotetulla mallilla
# Lasketaan ensin viikonloppupäivät eriteltynä
period_friday, period_saturday, period_sunday = count_weekend_days_detail(period_start, period_end)
period_weekday = count_weekdays(period_start, period_end)

# Ennustettu lisäkilometrimäärä kyseiselle ajanjaksolle
predicted_additional_km = (friday_rate * period_friday) + (saturday_rate * period_saturday) + (sunday_rate * period_sunday) + (weekday_rate * period_weekday)
predicted_km = initial_value + predicted_additional_km

st.write(f"Painotetun mallin mukaan valitun päivän ({pd.to_datetime(selected_date).strftime('%d-%m-%Y')}) arvioitu mittarilukema on: **{int(predicted_km)} km**")

# Altair-kuvaaja: Mittarilukeman kehitys
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
