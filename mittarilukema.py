import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# ----------------------------
# Apufunktiot viikonloppupäivien ja arkipäivien laskemiseen
def count_weekend_days_detail(start_date, end_date):
    """
    Laskee päivät eriteltynä: perjantai, lauantai ja sunnuntai.
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
    Laskee maanantaista torstaihin (0-3) päivien lukumäärän.
    """
    count = 0
    d = start_date
    while d <= end_date:
        if d.weekday() < 4:
            count += 1
        d += timedelta(days=1)
    return count

st.title("VW Caravelle AYE-599")

# ------------------------------------
# 1. Mittausdata (kovakoodattu)
# Uudet mittausarvot lisätty:
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

# Historiallisten tietojen laskenta
first_date = df['Päivämäärä'].min()
last_date = df['Päivämäärä'].max()
initial_value = df.iloc[0]['Mittarilukema']
total_km_driven = df.iloc[-1]['Mittarilukema'] - initial_value

num_days = (last_date - first_date).days
daily_avg = total_km_driven / num_days
monthly_avg = daily_avg * 30
yearly_avg = daily_avg * 365

# Päivitetty polttoaineen hinta: 1,85 €/l
diesel_price = 1.85
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

# ------------------------------------
# 2. Huoltohistoria (Excel-tiedosto)
# Ladataan huoltohistoria Excelistä. Tiedostossa on sarakkeet: Päivämäärä, Liike, Kuvaus, Hinta.
def load_maintenance_data(file_path):
    df_h = pd.read_excel(file_path)
    df_h['Päivämäärä'] = pd.to_datetime(df_h['Päivämäärä'], dayfirst=True, errors='coerce')
    df_h = df_h.dropna(subset=['Päivämäärä'])
    df_h = df_h.sort_values('Päivämäärä')
    return df_h

file_path = "/mnt/data/AYE_599_huoltohistoria.xlsx"
df_huolto = load_maintenance_data(file_path)

# Interpoloidaan huoltojen päivämäärien perusteella mittarilukemat
xp = df['Päivämäärä'].map(lambda d: d.toordinal())
fp = df['Mittarilukema']
df_huolto['Mittarilukema'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))

# Näytetään huoltohistorian taulukko: vain Päivämäärä ja interpoloitu Mittarilukema
st.subheader("Huoltohistorian kilometrilukemat")
st.dataframe(df_huolto[['Päivämäärä', 'Mittarilukema']])

# ------------------------------------
# 3. Yhtenäinen malli: Päivämäärähaku ja ennuste (painotettu malli)
st.subheader("Päivämäärähaku ja ennuste (painotettu malli)")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="combined")
period_start = first_date
period_end = pd.to_datetime(selected_date)

def calc_period_counts(start, end):
    fri, sat, sun = count_weekend_days_detail(start, end)
    wd = count_weekdays(start, end)
    return fri, sat, sun, wd

period_friday, period_saturday, period_sunday, period_weekday = calc_period_counts(period_start, period_end)
# Oletus: 2/3 kokonaiskilometreistä kertyy viikonloppuina ja 1/3 arkipäivinä.
hist_friday, hist_saturday, hist_sunday = count_weekend_days_detail(first_date, last_date)
total_weekend_km = (2/3) * total_km_driven
friday_rate = (0.375 * total_weekend_km) / hist_friday if hist_friday > 0 else 0
saturday_rate = (0.25 * total_weekend_km) / hist_saturday if hist_saturday > 0 else 0
sunday_rate = (0.375 * total_weekend_km) / hist_sunday if hist_sunday > 0 else 0
hist_weekday = count_weekdays(first_date, last_date)
weekday_rate = ((1/3) * total_km_driven) / hist_weekday if hist_weekday > 0 else 0

predicted_additional_km = (friday_rate * period_friday) + (saturday_rate * period_saturday) + (sunday_rate * period_sunday) + (weekday_rate * period_weekday)
predicted_km = initial_value + predicted_additional_km
st.write(f"Painotetun mallin mukaan valitun päivän ({period_end.strftime('%d-%m-%Y')}) arvioitu mittarilukema on: **{int(predicted_km)} km**")

# ------------------------------------
# 4. Altair-kuvaaja: Mittarilukeman kehitys
tick_dates = [d.to_pydatetime() for d in pd.date_range(start=first_date, end=last_date, freq='2M')]
st.subheader("Mittarilukeman kehitys")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
    y=alt.Y('Mittarilukema:Q', title='Mittarilukema', scale=alt.Scale(domain=[145000, 250000]), 
            axis=alt.Axis(values=list(range(145000, 250000+5000, 5000))))
).properties(width=700, height=400, title="Mittarilukeman kehitys ajan myötä")
st.altair_chart(chart, use_container_width=True)

# ------------------------------------
# 5. Näytetään mittausdata taulukkona
st.subheader("Mittaushistoria")
df_display = df.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)
