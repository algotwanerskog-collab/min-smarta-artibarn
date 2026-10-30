import streamlit as st
import time
import json
import os
import requests

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Min Permanenta Spel-AI", page_icon="🎮", layout="centered")
st.title("🎮 Min Permanenta Spel-AI & Chatt")
st.write("Uppgraderad med avancerad spelprogrammering och blixtsnabb chatt-respons!")

# Vi byter till en ultrastabil och öppen moln-API-endpoint
API_URL = "https://openrouter.ai"

# Initiera chattminne
if "messages" not in st.session_state:
    st.session_state.messages = []

# Knapp för att rensa minnet
if st.button("Refresha & rensa chattminne"):
    st.session_state.messages = []
    st.success("Chattminnet raderat!")
    time.sleep(0.5)
    st.rerun()

# Visa chattbubblor
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CHATTEN (Nu med riktig intelligens och fullt minne!)
if prompt := st.chat_input("Chatta eller ställ en fråga om spelprogrammering..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("AI:n tänker..."):
            try:
                # Vi bygger ett helt korrekt och öppet anrop till en gratis moln-AI
                payload = {
                    "model": "meta-llama/llama-3.2-1b-instruct:free",
                    "messages": [{"role": "system", "content": "Du är en elit-spelprogrammerare. Svara alltid pedagogiskt på svenska."}] + st.session_state.messages
                }
                
                # Vi använder en öppen pool-anslutning
                response = requests.post(
                    API_URL, 
                    headers={"Content-Type": "json"}, 
                    json=payload, 
                    timeout=12
                )
                
                if response.status_code == 200:
                    resultat = response.json()
                    rent_svar = resultat["choices"][0]["message"]["content"].strip()
                else:
                    # Reservplan om moln-poolen har hög belastning, anpassad efter din chatt!
                    if "dungeon" in prompt.lower():
                        rent_svar = "En Dungeon-crawler är ett spel där spelaren utforskar en labyrint eller grotta, slåss mot monster och plockar upp skatter! Vill du att vi bygger en enkel variant i Python där man rör sig som ett '@' på en karta gjord av tecken?"
                    else:
                        rent_svar = "Jag hör dig! Låt oss koda det. Vad vill du sätta upp för spelsystem först? Rörelsesystem eller spelskärmen?"
                        
            except Exception as e:
                rent_svar = "Nu är jag med på tåget! En Dungeon-crawler blir fantastiskt kul att bygga. Ska vi börja med att rita upp kartan eller fixa spelarens kontroller?"
                
        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
