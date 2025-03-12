import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Asetetaan taustakuva käyttäen body-elementtiä
st.markdown(
    """
    <style>
    body {
        background-image: url("https://lh3.googleusercontent.com/pw/AP1GczMebNg4BCFQefDWwx8k8fPHoQh3_oHA8TNKqVjGKjsOcKwsafnGn0AI_MtJ1k9andmNbzLmi2oZ9cFsNtFxM5fBI-47hmm4FsiTCbkJoN-WsBvmQFxt7jyRmXdSV-NzeBTr9wB8EJQw0VxaLC6HzN601g=w1836-h827-s-no-gm");
        background-size: 50%;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        /* Voit lisätä läpinäkyvyyttä, mutta silloin se vaikuttaa myös teksteihin:
        opacity: 0.5;
        */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("VW Caravelle AYE-599")
st.write("Sovelluksen muu sisältö tulee tähän.")

# Esimerkkidata ja muut osiot, kuten info, päivämäärähaku, ennustehaku, kuvaaja ja datataulukko

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

# Muut sovelluksen osiot jatkuu tästä...
# (Voit lisätä infoikkunan, päivämäärähakun, ennustehakun, kuvaajan ja datataulukon koodisi mukaan)
st.write("Tässä esimerkissä näkyy sovelluksen muu sisältö, mutta taustakuva pitäisi nyt näkyä koko taustalla.")
