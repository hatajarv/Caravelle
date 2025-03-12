import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# ----------------------------
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
        if d.weekday() < 4:  # maanantai - torstai
            count += 1
        d += timedelta(days=1)
    return count

# ----------------------------
st.title("VW Caravelle AYE-599 – Huoltohistoria ja Mittarilukemat")

# ------------------------------------
# 1. Mittausdata (kovakoodattu)
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

# Päivitetty polttoaineen hinta: 1,85 €/l
diesel_price = 1.85
monthly_fuel_cost = (monthly_avg / 100 * 9) * diesel_price
yearly_fuel_cost = (yearly_avg / 100 * 9) * diesel_price

# ------------------------------------
# 2. Huoltohistoria (kovakoodattu lähdedata)
huolto_data = [
    {"Päivämäärä": "29.1.2025", "Liike": "TDI Tuning Finland OY", "Kuvaus": "Nopeusanturin vaihto, Vikadiagnostiikka", "Hinta": 949},
    {"Päivämäärä": "14.11.2024", "Liike": "Disel Service", "Kuvaus": "Bosio PP 764 suuttimet", "Hinta": 301.45},
    {"Päivämäärä": "10.1.2025", "Liike": "Motonet", "Kuvaus": "Lämmityslaitteen kenno", "Hinta": 38.9},
    {"Päivämäärä": "10.1.2025", "Liike": "TDI Tuning Finland Oy", "Kuvaus": "Jatkosäätö", "Hinta": 300},
    {"Päivämäärä": "9.1.2025", "Liike": "Motonet", "Kuvaus": "Puhaltimen moottori, ilmastointikompuran hihna", "Hinta": 125.85},
    {"Päivämäärä": "9.12.2024", "Liike": "Jyväskylän Auto-Startti", "Kuvaus": "D5WZ Eberi", "Hinta": 1550},
    {"Päivämäärä": "19.11.2024", "Liike": "Jyväskylän Auto-Startti", "Kuvaus": "Eber-sisäpuhalluksen kytkentä", "Hinta": 146},
    {"Päivämäärä": "15.11.2024", "Liike": "A&H Nieminen", "Kuvaus": "Öljyjen vaihto, moottori, takaperä, laatikko", "Hinta": 325.62},
    {"Päivämäärä": "29.10.2024", "Liike": "Jyväskylän Auto-Startti", "Kuvaus": "Eber hehkutulpan vaihto", "Hinta": 112.2},
    {"Päivämäärä": "30.5.2024", "Liike": "A&H Nieminen", "Kuvaus": "Takapyörän laakeri, Jarulevy taka, Jarrupala taka", "Hinta": 382.7},
    {"Päivämäärä": "7.6.2024", "Liike": "A&H Nieminen", "Kuvaus": "Alapallonivel vasen etu", "Hinta": 64.6},
    {"Päivämäärä": "26.9.2023", "Liike": "A&H Nieminen", "Kuvaus": "Öljynvaihto, ilman- ja polttoaineen suodattimet", "Hinta": 252.6},
    {"Päivämäärä": "18.11.2022", "Liike": "A&H Nieminen", "Kuvaus": "Jakopää, vesipumppu", "Hinta": 579.2},
    {"Päivämäärä": "10.11.2023", "Liike": "A&H Nieminen", "Kuvaus": "Alapallonivel oike, Rt-pää vas. Ulompi", "Hinta": 125.3},
    {"Päivämäärä": "20.11.2023", "Liike": "A&H Nieminen", "Kuvaus": "Rt-sisäpää vasen", "Hinta": 75.3},
    {"Päivämäärä": "10.1.2025", "Liike": "A&H Nieminen", "Kuvaus": "Turbon ja suutinkärkien vaihto", "Hinta": 847},
    {"Päivämäärä": "12.11.2024", "Liike": "Fin-Turbo Oy", "Kuvaus": "Turbon muutostyö", "Hinta": 871}
]
df_huolto = pd.DataFrame(huolto_data)
df_huolto["Päivämäärä"] = pd.to_datetime(df_huolto["Päivämäärä"], dayfirst=True, errors='coerce')
df_huolto = df_huolto.dropna(subset=["Päivämäärä"])
df_huolto = df_huolto.sort_values("Päivämäärä")

# Interpoloidaan huoltojen päivämäärien perusteella odometrit
xp = df_measure['Päivämäärä'].map(lambda d: d.toordinal())
fp = df_measure['Mittarilukema']
df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))

# ------------------------------------
# 3. Infolaatikko – Mittausdata & Huoltokulut
# ------------------------------------
info_text = f"""**Havaintojen ajanjakso:** {first_date.strftime('%d-%m-%Y')} - {last_date.strftime('%d-%m-%Y')}

**Ajetut kilometrit yhteensä:** {total_km_driven} km

**Päivittäinen keskiarvo:** {daily_avg:.1f} km/päivä  
**Kuukausittainen keskiarvo:** {monthly_avg:.1f} km/kk  
**Vuosittainen keskiarvo:** {yearly_avg:.1f} km/vuosi

**Kuukausittaiset polttoainekustannukset:** {monthly_fuel_cost:.2f} €/kk  
**Vuosittaiset polttoainekustannukset:** {yearly_fuel_cost:.2f} €/vuosi
"""

# Lasketaan huoltokulut, jos huoltohistoriaa löytyy
if not df_huolto.empty:
    maintenance_total = df_huolto["Hinta"].sum()
    maintenance_start = df_huolto["Päivämäärä"].min()
    maintenance_end = df_huolto["Päivämäärä"].max()
    maintenance_period_days = (maintenance_end - maintenance_start).days
    if maintenance_period_days > 0:
        monthly_maintenance_cost = maintenance_total / (maintenance_period_days / 30)
        yearly_maintenance_cost = maintenance_total / (maintenance_period_days / 365)
    else:
        monthly_maintenance_cost = yearly_maintenance_cost = 0
    info_text += f"""

**Huoltohistorian kustannukset:**
- Yhteensä: {maintenance_total:.2f} €
- Kuukausittainen keskiarvo: {monthly_maintenance_cost:.2f} €/kk
- Vuosittainen keskiarvo: {yearly_maintenance_cost:.2f} €/vuosi
"""
st.info(info_text)

# ------------------------------------
# 4. Yhtenäinen malli: Päivämäärähaku ja ennuste (painotettu malli)
# ------------------------------------
st.subheader("Päivämäärähaku ja ennuste (painotettu malli)")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="combined")
period_start = first_date
period_end = pd.to_datetime(selected_date)

def calc_period_counts(start, end):
    fri, sat, sun = count_weekend_days_detail(start, end)
    wd = count_weekdays(start, end)
    return fri, sat, sun, wd

period_friday, period_saturday, period_sunday, period_weekday = calc_period_counts(period_start, period_end)
predicted_additional_km = (friday_rate * period_friday) + (saturday_rate * period_saturday) + (sunday_rate * period_sunday) + (weekday_rate * period_weekday)
predicted_km = initial_value + predicted_additional_km
st.write(f"Painotetun mallin mukaan valitun päivän ({pd.to_datetime(selected_date).strftime('%d-%m-%Y')}) arvioitu mittarilukema on: **{int(predicted_km)} km**")

# ------------------------------------
# 5. Altair-kuvaaja: Mittarilukeman kehitys
# ------------------------------------
tick_dates = [d.to_pydatetime() for d in pd.date_range(start=first_date, end=last_date, freq='2M')]
st.subheader("Mittarilukeman kehitys")
chart = alt.Chart(df_measure).mark_line(point=True).encode(
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

# ------------------------------------
# 6. Näytetään mittausdatan taulukko
# ------------------------------------
st.subheader("Mittarilukemien historia")
df_display = df_measure.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)

# ------------------------------------
# 7. Huoltohistorian osio: Taulukko ja kuvaaja
# ------------------------------------
st.subheader("Huoltohistoria")
if not df_huolto.empty:
    st.dataframe(df_huolto)
    
    base = alt.Chart(df_measure).encode(
        x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
        y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
    )
    line = base.mark_line(color='blue')
    points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
        x='Päivämäärä:T',
        y='Kilometrit:Q',
        tooltip=['Päivämäärä:T', alt.Tooltip('Kilometrit:Q', format=",.0f"), 'Liike', 'Kuvaus', alt.Tooltip('Hinta:Q', format=",.2f")]
    )
    service_chart = (line + points).properties(
        width=700,
        height=400,
        title="Huoltohistoria – Huoltojen lasketut kilometrit"
    )
    st.altair_chart(service_chart, use_container_width=True)
else:
    st.write("Huoltohistoriaa ei löytynyt.")
