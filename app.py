import streamlit as st
import torch
import time
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# 1. SÄTT UPP APPENS DESIGN (ChatGPT-stil)
st.set_page_config(page_title="Min AI-App", page_icon="🤖", layout="centered")
st.title("🤖 Min AI-App med raderbart minne")
st.write("Den här appen körs helt gratis dygnet runt i molnet och dör aldrig!")

# 2. LADDA AI-HJÄRNAN STABILT I MOLNET
@st.cache_resource
def ladda_ai_modell():
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    # Använd snabb och minnessnål laddning för moln-CPU
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True)
    return tokenizer, model

try:
    tokenizer, model = ladda_ai_modell()
except Exception as e:
    st.error(f"Kunde inte ladda AI-modellen: {e}")

# 3. INITIERA CHATTMINNE
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. SKAPA EN KNAPP FÖR ATT RADERA MINNET MANUELLT
if st.button("🧹 Rensa chattminne"):
    st.session_state.messages = []
    st.success("Chattminnet har raderats helt! Vi börjar om på ett nytt blankt blad.")
    time.sleep(1)
    st.rerun()

# 5. VISA TIDIGARE MEDDELANDEN I CHATTBUBBLOR
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. INPUT-RUTA FÖR ATT CHATTA (Precis som på ChatGPT)
if prompt := st.chat_input("Skriv något till din AI..."):
    
    # Kolla om användaren skriver rensa direkt i textrutan
    if prompt.strip().lower() in ["rensa", "radera", "clear"]:
        st.session_state.messages = []
        st.success("Chattminnet har raderats helt!")
        time.sleep(1)
        st.rerun()

    # Visa det du precis skrev i en bubbla
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Spara ditt meddelande i minnesbanken
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generera AI:ns svar baserat på hela minnet
    with st.chat_message("assistant"):
        system_instruktion = "Du är en smart AI-assistent. Svara på svenska. Kom ihåg tidigare meddelanden."
        
        # Bygg ihop hela historiken till modellen
        full_context = [{"role": "system", "content": system_instruktion}] + st.session_state.messages
        
        # Gör om till AI-format
        text = tokenizer.apply_chat_template(full_context, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text], return_tensors="pt")
        
        # Tänk-snurra medan molnservern räknar ut svaret
        with st.spinner("AI:n tänker..."):
            ids = model.generate(
                **inputs, 
                max_new_tokens=300, 
                do_sample=True, 
                temperature=0.7
            )
            fullt_svar = tokenizer.decode(ids, skip_special_tokens=True)
            rent_svar = fullt_svar.split("assistant\n")[-1].strip()
            
        # Visa svaret på skärmen
        st.markdown(rent_svar)
        
        # Spara AI:ns egna svar i minnet så den kommer ihåg vad den själv sagt
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
