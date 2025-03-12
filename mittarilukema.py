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

# Käytetään suoraa URL:ia, jonka annoit
background_url = "https://lh3.googleusercontent.com/pw/AP1GczMebNg4BCFQefDWwx8k8fPHoQh3_oHA8TNKqVjGKjsOcKwsafnGn0AI_MtJ1k9andmNbzLmi2oZ9cFsNtFxM5fBI-47hmm4FsiTCbkJoN-WsBvmQFxt7jyRmXdSV-NzeBTr9wB8EJQw0VxaLC6HzN601g=w1836-h827-s-no-gm?authuser=0"
set_background_from_url(background_url)

st.title("VW Caravelle AYE-599")
st.write("Tämä on esimerkkisovellus, jossa taustakuva on haettu suoran URL:n avulla Google Photosista.")
