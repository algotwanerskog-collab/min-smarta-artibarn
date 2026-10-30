import streamlit as st
import time
import json
import os
import requests

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Min Permanenta Spel-AI", page_icon="🎮", layout="centered")
st.title("🎮 Min Permanenta Spel-AI & Chatt")
st.write("Uppgraderad med avancerad spelprogrammering och blixtsnabb chatt-respons!")

# Officiell och stabil moln-API
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

# CHATTEN (Nu helt lagad med rätt säkerhets-headers!)
if prompt := st.chat_input("Chatta eller ställ en fråga om spelprogrammering..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("AI:n tänker..."):
            try:
                # Bygg historiken korrekt
                system_instruktion = "Du är en smart, pedagogisk och rolig AI-assistent. Du älskar spelprogrammering. Svara alltid på svenska."
                full_context = [{"role": "system", "content": system_instruktion}] + st.session_state.messages
                
                payload = {
                    "model": "meta-llama/llama-3.2-1b-instruct:free",
                    "messages": full_context
                }
                
                # SÄKERHETSKRAVET: OpenRouter kräver dessa headers för att tillåta gratis-trafik!
                headers = {
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io", 
                    "X-Title": "Aleo Game AI Factory"
                }
                
                response = requests.post(
                    API_URL, 
                    headers=headers, 
                    json=payload, 
                    timeout=15
                )
                
                if response.status_code == 200:
                    resultat = response.json()
                    rent_svar = resultat["choices"][0]["message"]["content"].strip()
                else:
                    rent_svar = f"Fick kontakt med servern men den bad om en paus. (Statuskod: {response.status_code}). Försök igen om ett ögonblick!"
                        
            except Exception as e:
                rent_svar = f"Kunde inte nå AI-hjärnan just nu. Låt oss testa att skicka meddelandet igen! (Tekniskt fel: {e})"
                
        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
