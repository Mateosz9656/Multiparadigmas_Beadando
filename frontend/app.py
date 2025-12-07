import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"
st.set_page_config(layout="wide")


def fetch_current_data(city_name: str):

    endpoint = f"{BACKEND_URL}/weather/fetch/{city_name}"
    try:
        response = requests.post(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Hiba az aktuális adat lekérésekor: {e}")
        return None


def fetch_all_history_data():

    endpoint = f"{BACKEND_URL}/weather/history"
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return []


st.title("☀️ Python Időjárás Alkalmazás")
st.header("Mikroszerviz Architektúra Bemutató")
st.subheader("Kézi mentés")
st.info("A háttérben fut egy automatikus mentés 1 óránként minden megyeszékhelyre!")
city_options = [
    "Budapest",
    "Békéscsaba",
    "Debrecen",
    "Eger",
    "Győr",
    "Kaposvár",
    "Kecskemét",
    "Miskolc",
    "Nyíregyháza",
    "Pécs",
    "Salgótarján",
    "Szeged",
    "Szekszárd",
    "Székesfehérvár",
    "Szolnok",
    "Szombathely",
    "Tatabánya",
    "Veszprém",
    "Zalaegerszeg",
]
selected_city = st.selectbox("Válassz várost kézi mentéshez:", city_options)
if st.button(f"Mentés MOST: {selected_city}"):
    with st.spinner(f"Lekérés és mentés a Backendbe ({selected_city})..."):
        current_weather = fetch_current_data(selected_city)
        if current_weather:
            st.success(f"Sikeres kézi mentés: {current_weather['city']}")
st.divider()
st.header("Időjárás Történet (Minden város)")
if st.button("Diagram Frissítése"):
    st.cache_data.clear()
history_data = fetch_all_history_data()
if history_data:
    df = pd.DataFrame(history_data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.subheader("Hőmérséklet alakulása (Összesített)")
    fig = px.line(
        df.sort_values(by="timestamp"),
        x="timestamp",
        y="temperature_c",
        color="city",
        title="Hőmérséklet adatpontok városonként",
        symbol="city",
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Nyers adatok táblázata"):
        st.dataframe(df, use_container_width=True)
else:
    st.info(
        "Még nincs mentett adat az adatbázisban. Várj az automatikus mentésre, vagy ments kézzel!"
    )
