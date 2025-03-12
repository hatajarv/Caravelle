import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# ---------------------------
# Apufunktiot viikonloppupäivien ja arkipäivien laskemiseen
def count_weekend_days_detail(start_date, end_date):
    """Laskee päivät eriteltynä: perjantai, lauantai ja sunnuntai"""
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
    """Laskee maanantaista torstaihin (0-3) päivien lukumäärän"""
    count = 0
    d = start_date
    while d <= end_date:
        if d.weekday() < 4:  # maanantai - torstai
            count += 1
        d += timedelta(days=1)
    return count

# ---------------------------
# Pääsovelluksen otsikko ja historiallinen mittausdata
st.title("VW Caravelle AYE-599")

# Kovakoodattu historiallinen mittausdata
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

# ---------------------------
# Lasketaan historiallisten tietojen painotukset
# Oletus: 2/3 kokonaiskilometreistä kertyy viikonloppuina ja 1/3 arkipäivinä.
hist_friday, hist_saturday, hist_sunday = count_weekend_days_detail(first_date, last_date)
total_weekend_km = (2/3) * total_km_driven

friday_rate = (0.375 * total_weekend_km) / hist_friday if hist_friday > 0 else 0
saturday_rate = (0.25 * total_weekend_km) / hist_saturday if hist_saturday > 0 else 0
sunday_rate = (0.375 * total_weekend_km) / hist_sunday if hist_sunday > 0 else 0

hist_weekday = count_weekdays(first_date, last_date)
weekday_rate = ((1/3) * total_km_driven) / hist_weekday if hist_weekday > 0 else 0

# ---------------------------
# Yhtenäinen malli: Painotettu malli, jota käytetään sekä historiallisen datan haussa että ennusteessa
st.subheader("Päivämäärähaku ja ennuste (painotettu malli)")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="combined")
period_start = first_date
period_end = pd.to_datetime(selected_date)

# Lasketaan valitun ajanjakson painotettu lisäkilometrimäärä
period_friday, period_saturday, period_sunday = count_weekend_days_detail(period_start, period_end)
period_weekday = count_weekdays(period_start, period_end)
predicted_additional_km = (friday_rate * period_friday) + (saturday_rate * period_saturday) + (sunday_rate * period_sunday) + (weekday_rate * period_weekday)
predicted_km = initial_value + predicted_additional_km

st.write(f"Painotetun mallin mukaan valitun päivän ({pd.to_datetime(selected_date).strftime('%d-%m-%Y')}) arvioitu mittarilukema on: **{int(predicted_km)} km**")

# ---------------------------
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

# ---------------------------
# Näytetään historiallinen mittausdata taulukkonaimport streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

# ---------------------------
# Apufunktiot viikonloppupäivien ja arkipäivien laskemiseen
def count_weekend_days_detail(start_date, end_date):
    """Laskee päivät eriteltynä: perjantai, lauantai ja sunnuntai"""
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
    """Laskee maanantaista torstaihin (0-3) päivien lukumäärän"""
    count = 0
    d = start_date
    while d <= end_date:
        if d.weekday() < 4:  # maanantai - torstai
            count += 1
        d += timedelta(days=1)
    return count

# ---------------------------
# Pääsovelluksen otsikko ja historiallinen mittausdata
st.title("VW Caravelle AYE-599")

# Kovakoodattu historiallinen mittausdata
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

# ---------------------------
# Lasketaan historiallisten tietojen painotukset
# Oletus: 2/3 kokonaiskilometreistä kertyy viikonloppuina ja 1/3 arkipäivinä.
hist_friday, hist_saturday, hist_sunday = count_weekend_days_detail(first_date, last_date)
total_weekend_km = (2/3) * total_km_driven

friday_rate = (0.375 * total_weekend_km) / hist_friday if hist_friday > 0 else 0
saturday_rate = (0.25 * total_weekend_km) / hist_saturday if hist_saturday > 0 else 0
sunday_rate = (0.375 * total_weekend_km) / hist_sunday if hist_sunday > 0 else 0

hist_weekday = count_weekdays(first_date, last_date)
weekday_rate = ((1/3) * total_km_driven) / hist_weekday if hist_weekday > 0 else 0

# ---------------------------
# Yhtenäinen malli: Painotettu malli, jota käytetään sekä historiallisen datan haussa että ennusteessa
st.subheader("Päivämäärähaku ja ennuste (painotettu malli)")
selected_date = st.date_input("Valitse päivämäärä:", value=last_date, key="combined")
period_start = first_date
period_end = pd.to_datetime(selected_date)

# Lasketaan valitun ajanjakson painotettu lisäkilometrimäärä
period_friday, period_saturday, period_sunday = count_weekend_days_detail(period_start, period_end)
period_weekday = count_weekdays(period_start, period_end)
predicted_additional_km = (friday_rate * period_friday) + (saturday_rate * period_saturday) + (sunday_rate * period_sunday) + (weekday_rate * period_weekday)
predicted_km = initial_value + predicted_additional_km

st.write(f"Painotetun mallin mukaan valitun päivän ({pd.to_datetime(selected_date).strftime('%d-%m-%Y')}) arvioitu mittarilukema on: **{int(predicted_km)} km**")

# ---------------------------
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

# ---------------------------
# Näytetään historiallinen mittausdata taulukkona
st.subheader("Excel-tiedoston sisältö (Mittarilukemat)")
df_display = df.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)

# ---------------------------
# Huoltohistorian osio
st.subheader("Huoltohistoria")

# Luetaan huoltohistoria Excel-tiedostosta (oletetaan tiedoston poluksi /mnt/data/AYE_599_huoltohistoria.xlsx)
try:
    df_huolto = pd.read_excel("/mnt/data/AYE_599_huoltohistoria.xlsx")
except Exception as e:
    st.error(f"Huoltohistorian tiedoston lukemisessa tapahtui virhe: {e}")
    df_huolto = pd.DataFrame()  # tyhjä DataFrame

if not df_huolto.empty:
    # Oletetaan, että huoltohistoriassa on ainakin sarake "Päivämäärä"
    df_huolto['Päivämäärä'] = pd.to_datetime(df_huolto['Päivämäärä'])
    df_huolto = df_huolto.sort_values("Päivämäärä")
    
    # Lasketaan interpoloidut odometrit huoltojen päivämäärien perusteella
    # Muutetaan historiallisten mittausten päivämäärät ordinal-lukuihin
    xp = df['Päivämäärä'].map(lambda d: d.toordinal())
    fp = df['Mittarilukema']
    
    # Lisää huoltohistoriaan sarake "Kilometrit" käyttäen lineaarista interpolointia
    df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))
    
    st.write("Huoltohistorian taulukko (sisältää lasketut kilometrit):")
    st.dataframe(df_huolto)
    
    # Piirretään Altair-kuvaaja, jossa näkyy historiallinen mittarilukema ja huoltojen merkinnät
    base = alt.Chart(df).encode(
        x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
        y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
    )
    line = base.mark_line(color='blue')
    points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
        x='Päivämäärä:T',
        y='Kilometrit:Q',
        tooltip=['Päivämäärä:T', alt.Tooltip('Kilometrit:Q', format=",.0f")]
    )
    service_chart = (line + points).properties(
        width=700,
        height=400,
        title="Huoltohistoria – huoltojen lasketut kilometrit"
    )
    st.altair_chart(service_chart, use_container_width=True)
else:
    st.write("Huoltohistoriaa ei löytynyt.")

st.subheader("Excel-tiedoston sisältö (Mittarilukemat)")
df_display = df.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))
st.dataframe(df_display)

# ---------------------------
# Huoltohistorian osio
st.subheader("Huoltohistoria")

# Luetaan huoltohistoria Excel-tiedostosta (oletetaan tiedoston poluksi /mnt/data/AYE_599_huoltohistoria.xlsx)
try:
    df_huolto = pd.read_excel("/mnt/data/AYE_599_huoltohistoria.xlsx")
except Exception as e:
    st.error(f"Huoltohistorian tiedoston lukemisessa tapahtui virhe: {e}")
    df_huolto = pd.DataFrame()  # tyhjä DataFrame

if not df_huolto.empty:
    # Oletetaan, että huoltohistoriassa on ainakin sarake "Päivämäärä"
    df_huolto['Päivämäärä'] = pd.to_datetime(df_huolto['Päivämäärä'])
    df_huolto = df_huolto.sort_values("Päivämäärä")
    
    # Lasketaan interpoloidut odometrit huoltojen päivämäärien perusteella
    # Muutetaan historiallisten mittausten päivämäärät ordinal-lukuihin
    xp = df['Päivämäärä'].map(lambda d: d.toordinal())
    fp = df['Mittarilukema']
    
    # Lisää huoltohistoriaan sarake "Kilometrit" käyttäen lineaarista interpolointia
    df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))
    
    st.write("Huoltohistorian taulukko (sisältää lasketut kilometrit):")
    st.dataframe(df_huolto)
    
    # Piirretään Altair-kuvaaja, jossa näkyy historiallinen mittarilukema ja huoltojen merkinnät
    base = alt.Chart(df).encode(
        x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y', values=tick_dates)),
        y=alt.Y('Mittarilukema:Q', title='Mittarilukema')
    )
    line = base.mark_line(color='blue')
    points = alt.Chart(df_huolto).mark_point(color='red', size=100).encode(
        x='Päivämäärä:T',
        y='Kilometrit:Q',
        tooltip=['Päivämäärä:T', alt.Tooltip('Kilometrit:Q', format=",.0f")]
    )
    service_chart = (line + points).properties(
        width=700,
        height=400,
        title="Huoltohistoria – huoltojen lasketut kilometrit"
    )
    st.altair_chart(service_chart, use_container_width=True)
else:
    st.write("Huoltohistoriaa ei löytynyt.")
