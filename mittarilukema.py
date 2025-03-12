import streamlit as st

def set_background_from_url(image_url):
    css = f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Käytä tätä URL-osoitetta taustakuvana.
background_url = "https://photos.google.com/share/AF1QipOVowZZb_maS58LNHPglNoYOULe1wvGiT-hSk86mXh74F0uTwN2ztS0NBPKjUBaxw/photo/AF1QipNoG-e1CfydT0yCj2ILGABd_JqTYacPDsxUoenW?key=TTJLY3ZEME90cTFHVGlucW5IUkVvUjBEX0JoQzVB"
set_background_from_url(background_url)

st.title("VW Caravelle AYE-599")
st.write("Tämä on esimerkkisovellus, jossa taustakuva on haettu Google Photos -linkin kautta.")
