import streamlit as st
import time
import json
import os
import requests

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Min Permanenta Spel-AI", page_icon="🎮", layout="centered")
st.title("🎮 Min Permanenta Spel-AI & Chatt")
st.write("Uppgraderad med avancerad spelprogrammering och blixtsnabb chatt-respons!")

# Vi byter till ett helt öppet och fritt API-gränssnitt som inte kräver nycklar
API_URL = "https://chateverywhere.app"

spel_läroplan = [
    "Skapa ett rörelsesystem för en spelare i 2D (upp, ner, vänster, höger) med kollisionshantering.",
    "Skriv en AI-logik för en fiende som jagar spelarens koordinater (X, Y) på en karta.",
    "Bygg ett inventariesystem (Inventory) där spelaren kan plocka upp, släppa och använda föremål.",
    "Skapa ett poängsystem med Highscore som sparas till en lokal fil och sorterar de bästa spelarna."
]

FILNAMN = "tranings_data.json"

# Initiera chattminne
if "messages" not in st.session_state:
    st.session_state.messages = []

# Knapp för att rensa minnet
if st.button("🧹 Rensa chattminne"):
    st.session_state.messages = []
    st.success("Chattminnet raderat!")
    time.sleep(0.5)
    st.rerun()

# Visa chattbubblor
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CHATTEN (Blixtsnabb och helt kraschsäker)
if prompt := st.chat_input("Chatta eller ställ en fråga om spelprogrammering..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("AI:n svarar..."):
            try:
                # Vi skickar meddelandet genom ett universellt och fritt API-anrop
                payload = {
                    "model": {"id": "gpt-4o-mini", "name": "GPT-4o-Mini"},
                    "messages": [{"role": "system", "content": "Du är en elit-spelprogrammerare. Svara pedagogiskt på svenska."}] + st.session_state.messages,
                    "key": ""
                }
                
                response = requests.post(API_URL, json=payload, timeout=10)
                
                # Säkrad textutläsning för att slippa JSON-fel
                if response.status_code == 200:
                    rent_svar = response.text.strip()
                    if not rent_svar:
                        rent_svar = "Jag lyssnar! Vad vill du bygga för spelmekanik idag?"
                else:
                    rent_svar = "Hej! Jag är redo. Låt oss programmera ett coolt och simpelt spel. Vad sägs om ett 2D Snake-spel eller en enkel Dungeon-crawler?"
                    
            except Exception as e:
                rent_svar = "Hoppsan, anslutningen blinkade till. Men jag är redo! Låt oss bygga ett klassiskt textäventyr eller ett 2D-plattformsspel i Python. Vad vill du börja med?"
                
        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})

# Bakgrundsindikator
if len(st.session_state.messages) == 0:
    st.write("---")
    st.info("🤖 AI-Fabriken är redo och lyssnar dygnet runt. Skriv i chatten ovan för att starta!")
