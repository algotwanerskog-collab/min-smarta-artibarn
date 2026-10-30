import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import urllib.parse # Används för att säkert omvandla texten till en webblänk

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos AI Spel-Fabrik 4.1", page_icon="🔮", layout="centered")
st.title("🔮 Aleos Universella AI-Spelfabrik")
st.write("Skriv precis vilken spelidé som helst nedan, så kodar AI-hjärnan hela spelskärmen live från grunden!")

# Initiera spelsessionen i minnet
if "genererad_kod" not in st.session_state:
    st.session_state.genererad_kod = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# HUVUDÅTERSTÄLLARE
if st.button("🔴 🆕 Starta helt nytt spel / Nollställ", use_container_width=True):
    st.session_state.genererad_kod = None
    st.session_state.messages = []
    st.success("Spelstudion har nollställts!")
    time.sleep(0.4)
    st.rerun()

st.write("---")

# --- 2. HÄR RITAS DITT UNIKA AI-GENERERADE SPEL UT LIVE ---
if st.session_state.genererad_kod:
    st.subheader("🎮 Din Genererade Spelmotor (Spelbar live):")
    components.html(st.session_state.genererad_kod, height=450, scrolling=True)
else:
    st.info("🤖 Ingen aktiv spelmotor än. Skriv din idé nedan och klicka på 'Generera Spel' för att starta!")

st.write("---")

# --- 3. INPUT OCH SMART CHATT SOM FÖRSVINNER ALDRIG ---
st.write("### 📸 Visuell insamling och analys:")
bild_instruktion = st.text_input("Beskriv din bild-scanning eller spelskärm här (valfritt):")

# Visa tidigare chattmeddelanden
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Textinmatning + Kolumn-tvåa för knapp bredvid
chatt_spår, knapp_spår = st.columns(2)

with chatt_spår:
    input_text = st.text_input("Skriv din exakta spelidé här:", key="user_input_field")

with knapp_spår:
    st.write(" ") # Justering
    generera_klick = st.button("🤖 Generera Spel", use_container_width=True)

# BEARBETNING: Skickar din unika idé via ett säkert GET-anrop
if generera_klick and input_text:
    final_prompt = input_text
    if bild_instruktion:
        final_prompt = f"[Visuell scanning: {bild_instruktion}] " + final_prompt
        
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    
    with st.spinner("AI-hjärnan kodar ditt unika spel... Detta kan ta upp till 30 sekunder..."):
        try:
            system_prompt = (
                "You are an expert 2D game developer. Write a complete, working, single-file HTML game "
                "using HTML5 <canvas> and <script> JavaScript. Use beautiful neon colors, custom pixel-like graphics, "
                "and full keyboard controls (W,A,S,D / Arrows). Implement ALL specific rules, mechanics, scoring systems, "
                "and winning/losing conditions requested by the user. "
                "Return ONLY the raw HTML/JS code. Do NOT wrap your answer in markdown codeblocks like html."
            )
            
            # SÄKRARE GET-METOD: Vi bakar in systeminstruktionerna och din idé direkt i webbadressen
            kodad_system = urllib.parse.quote(system_prompt)
            kodad_prompt = urllib.parse.quote(final_prompt)
            
            # Vi bygger den perfekta API-länken som tar emot text direkt
            länk = f"https://pollinations.ai{kodad_system}/prompt/{kodad_prompt}"
            
            # Vi gör ett GET-anrop istället för POST för att slippa 405-fel!
            response = requests.get(länk, timeout=45)
            
            if response.status_code == 200:
                genererad_text = response.text.strip()
                
                # Städa bort eventuella råa markdown-block om AI:n lade till dem ändå
                if "html" in genererad_text:
                    genererad_text = genererad_text.split("html")[-1].split("").strip()
                elif "" in genererad_text:
                    genererad_text = genererad_text.split("")[-1].split("```").strip()
                
                st.session_state.genererad_kod = genererad_text
                svar = "🔮 *Spel framgångsrikt skapat!* AI-hjärnan har byggt hela källkoden live utifrån dina instruktioner. Testa spelskärmen högst upp!"
            else:
                svar = f"Kunde inte nå AI-servern just nu (Kod: {response.status_code}). Försök igen om ett ögonblick!"
        except Exception as e:
            svar = f"Ett fel uppstod vid kodningen: {e}"
            
    st.session_state.messages.append({"role": "assistant", "content": svar})
    st.rerun()
