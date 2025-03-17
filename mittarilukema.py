import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta
import os

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
        if d.weekday() == 4:
            count_friday += 1
        elif d.weekday() == 5:
            count_saturday += 1
        elif d.weekday() == 6:
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

st.title("VW Caravelle AYE-599 (versio 2.2)")

# ------------------------------------
# 1. Mittausdata (kovakoodattu uusilla mittausarvoilla)
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

**Päivittäinen keskiarvo:** {int(daily_avg)} km/päivä  
**Kuukausittainen keskiarvo:** {int(monthly_avg)} km/kk  
**Vuosittainen keskiarvo:** {int(yearly_avg)} km/vuosi

**Kuukausittaiset polttoainekustannukset:** {monthly_fuel_cost:.2f} €/kk  
**Vuosittaiset polttoainekustannukset:** {yearly_fuel_cost:.2f} €/vuosi
"""

# ------------------------------------
# 2. Huoltohistoria
# Yritetään lukea Excel-tiedosto; jos sitä ei löydy, fallback-dataa käytetään.
file_path = "/mnt/data/AYE_599_huoltohistoria.xlsx"
if os.path.exists(file_path):
    try:
        df_huolto = pd.read_excel(file_path)
    except Exception as e:
        st.error(f"Virhe Excel-tiedoston lukemisessa: {e}")
        df_huolto = pd.DataFrame()
else:
    st.warning("Excel-tiedostoa ei löytynyt, käytetään fallback-dataa.")
    fallback_data = [
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
    df_huolto = pd.DataFrame(fallback_data)
    df_huolto["Päivämäärä"] = pd.to_datetime(df_huolto["Päivämäärä"], dayfirst=True, errors='coerce')
    df_huolto = df_huolto.dropna(subset=["Päivämäärä"])
    df_huolto = df_huolto.sort_values("Päivämäärä")
    
# Interpoloidaan huoltojen päivämäärien perusteella mittarilukemat
xp = df['Päivämäärä'].map(lambda d: d.toordinal())
fp = df['Mittarilukema']
df_huolto['Mittarilukema'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))
# Muutetaan interpoloidut mittarilukemat kokonaisluvuiksi
df_huolto['Mittarilukema'] = df_huolto['Mittarilukema'].astype(int)

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

# ------------------------------------
# 3. Infolaatikko – Mittausdata & Huoltokulut
info_text_full = info_text
if not df_huolto.empty:
    info_text_full += (
        f"""\n\n**Huoltohistorian kustannukset:**\n- Yhteensä: {maintenance_total:.2f} €\n- Kuukausittainen keskiarvo: {monthly_maintenance_cost:.2f} €/kk\n- Vuosittainen keskiarvo: {yearly_maintenance_cost:.2f} €/vuosi"""
    )
else:
    info_text_full += "\n\nHuoltohistoriaa ei löytynyt."
st.info(info_text_full)

# ------------------------------------
# 4. Yhtenäinen malli: Päivämäärähaku ja ennuste (painotettu malli)
st.subheader("Päivämäärähaku ja ennuste (painotettu malli)")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="combined")
period_start = first_date
period_end = pd.to_datetime(selected_date)

def calc_period_counts(start, end):
    fri, sat, sun = count_weekend_days_detail(start, end)
    wd = count_weekdays(start, end)
    return fri, sat, sun, wd

period_friday, period_saturday, period_sunday, period_weekday = calc_period_counts(period_start, period_end)
# Historiallisten tietojen painotukset: oletus, että 2/3 kokonaiskilometreistä kertyy viikonloppuina ja 1/3 arkipäivinä.
hist_friday, hist_saturday, hist_sunday = count_weekend_days_detail(first_date, last_date)
total_weekend_km = (2/3) * total_km_driven
friday_rate = (0.375 * total_weekend_km) / hist_friday if hist_friday > 0 else 0
saturday_rate = (0.25 * total_weekend_km) / hist_saturday if hist_saturday > 0 else 0
sunday_rate = (0.375 * total_weekend_km) / hist_sunday if hist_sunday > 0 else 0
hist_weekday = count_weekdays(first_date, last_date)
weekday_rate = ((1/3) * total_km_driven) / hist_weekday if hist_weekday > 0 else 0

predicted_additional_km = (
    (friday_rate * period_friday) +
    (saturday_rate * period_saturday) +
    (sunday_rate * period_sunday) +
    (weekday_rate * period_weekday)
)
predicted_km = initial_value + predicted_additional_km
st.write(f"Painotetun mallin mukaan valitun päivän ({period_end.strftime('%d-%m-%Y')}) arvioitu mittarilukema on: **{int(predicted_km)} km**")

# ------------------------------------
# 5. Altair-kuvaaja: Mittarilukeman kehitys
tick_dates = [d.to_pydatetime() for d in pd.date_range(start=first_date, end=last_date, freq='2M')]
st.subheader("Mittarilukeman kehitys ajan myötä")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X(
        'Päivämäärä:T',
        title='Päivämäärä',
        axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)
    ),
    y=alt.Y(
        'Mittarilukema:Q',
        title='Mittarilukema',
        scale=alt.Scale(domain=[145000, 250000]),
        axis=alt.Axis(values=list(range(145000, 250000+5000, 5000)))
    ),
    tooltip=[alt.Tooltip('Mittarilukema:Q', format=",.0f")]
).properties(width=700, height=400, title="Mittarilukeman kehitys ajan myötä")
st.altair_chart(chart, use_container_width=True)

# ------------------------------------
# 6. Näytetään mittausdatan taulukko
st.subheader("Mittaushistoria")
df_display = df.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)

# ------------------------------------
# 7. Huoltohistorian osio: Näytetään taulukko, jossa Päivämäärä, Liike, Kuvaus ja interpoloitu Mittarilukema
st.subheader("Huoltohistoria – mitä huoltoja kunakin ajankohtana on tehty")
if not df_huolto.empty:
    # Muotoillaan huoltohistorian päivämäärät ilman kellonaikaa
    df_huolto['Päivämäärä'] = df_huolto['Päivämäärä'].dt.strftime("%d-%m-%Y")
    st.dataframe(df_huolto[['Päivämäärä', 'Liike', 'Kuvaus', 'Mittarilukema']])
else:
    st.write("Huoltohistoriaa ei löytynyt.")
