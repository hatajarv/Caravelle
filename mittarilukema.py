import streamlit as st
import pandas as pd
import altair as alt

st.title("VW Caravelle AYE-599")

# Excel-tiedostosta haettu data kovakoodattuna
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

# Muodostetaan DataFrame ja muunnetaan 'Päivämäärä'-sarake date-objekteiksi
df = pd.DataFrame(data)
df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä']).dt.date
df = df.sort_values("Päivämäärä")

# Lasketaan havaintoajalta ajetut kilometrit ja keskiarvot
first_date = df['Päivämäärä'].min()
last_date = df['Päivämäärä'].max()
total_km_driven = df.iloc[-1]['Mittarilukema'] - df.iloc[0]['Mittarilukema']
num_days = (last_date - first_date).days
daily_avg = total_km_driven / num_days
monthly_avg = daily_avg * 30
yearly_avg = daily_avg * 365

# Lasketaan polttoainekustannukset: 9l/100km ja diesel-hinnan oletusarvona 1,70 €/l.
diesel_price = 1.70  # €/l
monthly_fuel_cost = (monthly_avg / 100 * 9) * diesel_price
yearly_fuel_cost = (yearly_avg / 100 * 9) * diesel_price

# Näytetään infoikkuna
st.info(
    f"""**Havaintojen ajanjakso:** {first_date.strftime("%d-%m-%Y")} - {last_date.strftime("%d-%m-%Y")}

**Ajetut kilometrit yhteensä:** {total_km_driven} km

**Päivittäinen keskiarvo:** {daily_avg:.1f} km/päivä  
**Kuukausittainen keski
