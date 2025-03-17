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

# ------------------------------------
# 2. Huoltohistoria
# Yritetään lukea Excel-tiedosto; jos sitä ei löydy, käytetään fallback-dataa.
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
xp = df['Päivämäär
