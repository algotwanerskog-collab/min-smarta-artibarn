import streamlit as st
import time
import json
import os
import requests

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Min Permanenta Spel-AI", page_icon="🎮", layout="centered")
st.title("🎮 Min Permanenta Spel-AI & Chatt")
st.write("Uppgraderad med avancerad spelprogrammering och blixtsnabb chatt-respons!")

# Vi byter till Hugging Face rekommenderade öppna API-gränssnitt
API_URL = "https://huggingface.co"

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

# CHATTEN (Blixtsnabb och säkrad)
if prompt := st.chat_input("Chatta eller ställ en fråga om spelprogrammering..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("AI:n svarar..."):
            try:
                # Vi bygger om anropet så det matchar den öppna gratis-porten exakt
                payload = {
                    "inputs": f"<|im_start|>system\nDu är en smart AI-assistent som svarar på svenska.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
                    "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}
                }
                
                response = requests.post(API_URL, json=payload)
                resultat = response.json()
                
                # Stormsäker utläsning av texten från API:n
                if isinstance(resultat, list) and len(resultat) > 0 and "generated_text" in resultat[0]:
                    rent_svar = resultat[0]["generated_text"].strip()
                elif isinstance(resultat, dict) and "generated_text" in resultat:
                    rent_svar = resultat["generated_text"].strip()
                elif "error" in resultat:
                    rent_svar = f"Molnservern startar upp (Modellen laddas). Prova att skicka meddelandet igen om 20 sekunder! (Info: {resultat['error']})"
                else:
                    rent_svar = "Jag tog emot ditt meddelande! Vad vill du programmera för spelmekanik idag?"
                    
            except Exception as e:
                rent_svar = f"Kunde inte nå servern just nu. Vi provar igen! (Fel: {e})"
                
        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})

# Bakgrundsindikator
if len(st.session_state.messages) == 0:
    st.write("---")
    st.info("🤖 AI-Fabriken är redo och lyssnar dygnet runt. Skriv i chatten ovan för att starta!")
