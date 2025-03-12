# --- Huoltohistorian osio ---
st.subheader("Huoltohistoria")

try:
    df_huolto = pd.read_excel("/mnt/data/AYE_599_huoltohistoria.xlsx")
    st.write("Huoltohistorian raakatiedot:")
    st.dataframe(df_huolto.head())
except Exception as e:
    st.error(f"Huoltohistorian tiedoston lukemisessa tapahtui virhe: {e}")
    df_huolto = pd.DataFrame()

if not df_huolto.empty:
    # Varmistetaan, että sarake "Päivämäärä" on olemassa
    if 'Päivämäärä' not in df_huolto.columns:
        st.error("Huoltohistoriassa ei löytynyt saraketta 'Päivämäärä'. Sarakkeiden nimet ovat: " + ", ".join(df_huolto.columns))
    else:
        df_huolto['Päivämäärä'] = pd.to_datetime(df_huolto['Päivämäärä'])
        df_huolto = df_huolto.sort_values("Päivämäärä")
        
        # Interpoloidaan odometrit huoltojen päivämäärien perusteella käyttäen historiallista mittausdataa
        xp = df['Päivämäärä'].map(lambda d: d.toordinal())
        fp = df['Mittarilukema']
        df_huolto['Kilometrit'] = df_huolto['Päivämäärä'].map(lambda d: np.interp(d.toordinal(), xp, fp))
        
        st.write("Huoltohistorian taulukko (sisältää lasketut kilometrit):")
        st.dataframe(df_huolto)
        
        # Piirretään Altair-kuvaaja, jossa näkyy mittarilukeman kehitys ja huoltojen merkinnät
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
