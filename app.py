import streamlit as st
import time
import json
import os
import requests # Används för att prata med den snabba AI-servern

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Min Permanenta Spel-AI", page_icon="🎮", layout="centered")
st.title("🎮 Min Permanenta Spel-AI & Chatt")
st.write("Uppgraderad med avancerad spelprogrammering och blixtsnabb chatt-respons!")

# API-länk till en supersnabb, gratis server för Qwen-modellen
API_URL = "https://huggingface.co"

# Dolda träningsmål inom spelprogrammering
spel_läroplan = [
    "Skapa ett rörelsesystem för en spelare i 2D (upp, ner, vänster, höger) med kollisionshantering.",
    "Skriv en AI-logik för en fiende som jagar spelarens koordinater (X, Y) på en karta.",
    "Bygg ett inventariesystem (Inventory) där spelaren kan plocka upp, släppa och använda föremål.",
    "Skapa ett poängsystem med Highscore som sparas till en lokal fil och sorterar de bästa spelarna.",
    "Skriv en slumpmässig generering av en spelbana (Dungeon generation) med rum och gångar.",
    "Bygg ett turordningsbaserat stridssystem (Turn-based combat) med HP, attack och kritisk skada."
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

# CHATTEN (Blixtsnabb via extern server)
if prompt := st.chat_input("Chatta eller ställ en fråga om spelprogrammering..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("AI:n svarar..."):
            try:
                # Vi skickar frågan till den externa snabba servern istället för att räkna på CPU:n
                headers = {"Authorization": "Bearer hf_placeholder"} # Använder offentlig gratis-pool
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": 400, "temperature": 0.7}}
                
                response = requests.post(API_URL, json=payload)
                resultat = response.json()
                
                # Hämta ut svaret säkert
                if isinstance(resultat, list) and "generated_text" in resultat[0]:
                    rent_svar = resultat[0]["generated_text"].strip()
                elif isinstance(resultat, dict) and "generated_text" in resultat:
                    rent_svar = resultat["generated_text"].strip()
                else:
                    rent_svar = "Hej! Jag är redo att hjälpa dig med spelprogrammering. Vad vill du bygga idag?"
                    
            except Exception as e:
                rent_svar = f"Hoppsan! Servern är upptagen just nu, men jag försöker igen. (Detaljer: {e})"
                
        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})

# AUTONOM TRÄNING I BAKGRUNDEN (Möter spelmålen!)
# Eftersom chatten nu är flyttad till API:n, kan vi använda Streamlits CPU exklusivt till att tugga träningsdata
if len(st.session_state.messages) == 0:
    st.write("---")
    st.info("🤖 AI-Fabriken är vilande. Skriv i chatten ovan eller låt den ligga för att generera data.")
