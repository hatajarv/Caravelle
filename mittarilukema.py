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

# Muodostetaan DataFrame ja muunnetaan 'Päivämäärä'-sarake pd.Timestamp-objekteiksi
df = pd.DataFrame(data)
df['Päivämäärä'] = pd.to_datetime(df['Päivämäärä'])
df = df.sort_values("Päivämäärä")

# Lasketaan havaintoajalta ajetut kilometrit ja keskiarvot
first_date = df['Päivämäärä'].min()
last_date = df['Päivämäärä'].max()
total_km_driven = df.iloc[-1]['Mittarilukema'] - df.iloc[0]['Mittarilukema']
num_days = (last_date - first_date).days
daily_avg = total_km_driven / num_days
monthly_avg = daily_avg * 30
yearly_avg = daily_avg * 365

# Lasketaan polttoainekustannukset:
# Oletus: 9 l/100 km kulutus ja dieselpolttoaineen hinta 1,70 €/l.
diesel_price = 1.70  # €/l
monthly_fuel_cost = (monthly_avg / 100 * 9) * diesel_price
yearly_fuel_cost = (yearly_avg / 100 * 9) * diesel_price

# Infoikkuna
info_text = (
    f"""**Havaintojen ajanjakso:** {first_date.strftime('%d-%m-%Y')} - {last_date.strftime('%d-%m-%Y')}
    
**Ajetut kilometrit yhteensä:** {total_km_driven} km
    
**Päivittäinen keskiarvo:** {daily_avg:.1f} km/päivä  
**Kuukausittainen keskiarvo:** {monthly_avg:.1f} km/kk  
**Vuosittainen keskiarvo:** {yearly_avg:.1f} km/vuosi
    
**Kuukausittaiset polttoainekustannukset:** {monthly_fuel_cost:.2f} €/kk  
**Vuosittaiset polttoainekustannukset:** {yearly_fuel_cost:.2f} €/vuosi"""
)
st.info(info_text)

# Päivämäärähaku
st.subheader("Päivämäärähaku")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date)
filtered_df = df[df['Päivämäärä'] <= pd.to_datetime(selected_date)]
total_km = filtered_df["Mittarilukema"].iloc[-1] if not filtered_df.empty else 0
selected_date_str = pd.to_datetime(selected_date).strftime("%d-%m-%Y")
st.write(f"Ajettu kilometrejä {selected_date_str} mennessä: **{total_km} km**")

# Valmista tick-arvot x-akselille (päivämäärät 2 kuukauden välein)
tick_dates = list(pd.date_range(start=first_date, end=last_date, freq='2M'))

# Kuvaaja
st.subheader("Mittarilukeman kehitys")
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
        axis=alt.Axis(values=list(range(145000, 250000 + 5000, 5000)))
    )
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
