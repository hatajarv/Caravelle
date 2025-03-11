import streamlit as st
import pandas as pd
import altair as alt

st.title("Kilometrien seuranta")

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

# Luodaan kopio datasta, jossa päivämäärä esitetään muodossa DD-MM-YYYY (näyttöä varten)
df_display = df.copy()
df_display['Päivämäärä'] = df_display['Päivämäärä'].apply(lambda d: d.strftime("%d-%m-%Y"))

st.subheader("Excel-tiedoston sisältö")
st.dataframe(df_display)

st.subheader("Mittarilukeman kehitys")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('Päivämäärä:T', title='Päivämäärä', axis=alt.Axis(format='%d-%m-%Y')),
    y=alt.Y('Mittarilukema:Q', title='Mittarilukema', scale=alt.Scale(domain=[140000, 300000]))
).properties(
    width=700,
    height=400,
    title="Mittarilukeman kehitys ajan myötä"
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Päivämäärähaku")
# Käyttäjä voi valita päivämäärän; arvo on edelleen date-objekti
selected_date = st.date_input("Valitse päivämäärä:", value=df['Päivämäärä'].max())
filtered_df = df[df['Päivämäärä'] <= selected_date]
total_km = filtered_df["Mittarilukema"].iloc[-1] if not filtered_df.empty else 0

# Muotoillaan valittu päivämäärä DD-MM-YYYY-muotoon
selected_date_str = selected_date.strftime("%d-%m-%Y")
st.write(f"Ajettu kilometrejä {selected_date_str} mennessä: **{total_km} km**")
