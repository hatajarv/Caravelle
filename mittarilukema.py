import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def set_background():
    css = """
    <style>
    [data-testid="stAppViewContainer"]::before {
        content: "";
        background-image: url("https://lh3.googleusercontent.com/pw/AP1GczMebNg4BCFQefDWwx8k8fPHoQh3_oHA8TNKqVjGKjsOcKwsafnGn0AI_MtJ1k9andmNbzLmi2oZ9cFsNtFxM5fBI-47hmm4FsiTCbkJoN-WsBvmQFxt7jyRmXdSV-NzeBTr9wB8EJQw0VxaLC6HzN601g=w1836-h827-s-no-gm");
        background-size: 50%;
        background-position: top right;
        background-repeat: no-repeat;
        opacity: 0.5;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        z-index: -1;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Aseta taustakuva
set_background()

st.title("VW Caravelle AYE-599")

# Seuraavassa on esimerkkidataa ja muut sovelluksen osiot
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

first_date = df['Päivämäärä'].min()
last_date = df['Päivämäärä'].max()
total_km_driven = df.iloc[-1]['Mittarilukema'] - df.iloc[0]['Mittarilukema']
num_days = (last_date - first_date).days
daily_avg = total_km_driven / num_days
monthly_avg = daily_avg * 30
yearly_avg = daily_avg * 365

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

# Jäljempänä on muut osiot, esim. päivämäärähaku, ennustehaku, kuvaaja ja datataulukko…
# (Näitä osioita ei ole tässä päivitetty, mutta ne ovat samoja kuin aiemmassa koodissa.)
