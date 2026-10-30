import streamlit as st
import time
import random

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Spel-AI Factory", page_icon="🎮", layout="centered")
st.title("🎮 Aleos Spel-AI & Chat-Factory")
st.write("100% kraschsäker offline-motor med inbyggt spelsinne och blixtsnabba svar!")

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

# CHATTEN (Helt lokal, blixtsnabb och omöjlig att krascha!)
if prompt := st.chat_input("Chatta eller ställ en fråga om spelprogrammering..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Genererar spelsvar..."):
            time.sleep(0.5) # Simulerar lite betänketid för realism
            
            text_input = prompt.lower()
            
            # Smart logikmatris baserad på vad du faktiskt skriver!
            if "dungeon" in text_input or "crawler" in text_input:
                svar_alternativ = [
                    "En Dungeon-crawler är ett fantastiskt val! Vi kan bygga en karta som en 2D-matris där spelaren representeras av tecknet '@'. Ska vi börja med att koda spelarens rörelse eller generera rummen?",
                    "Spännande! För en Dungeon-crawler behöver vi ett rutnät av väggar (#) och golv (.). Vill du att vi lägger till fiender som jagar spelaren på kartan på en gång?",
                    "Riktigt coolt spelsystem! Vi kan skapa slumpmässiga grottrum. Vill du ha ett turordningsbaserat stridssystem när man stöter på monster?"
                ]
                rent_svar = random.choice(svar_alternativ)
                
            elif "hej" in text_input or "tjena" in text_input:
                svar_alternativ = [
                    "Tjena! Jag är din personliga spelprogrammerings-AI. Jag är redo att hjälpa dig att bygga legendariska spel. Vad vill du koda idag?",
                    "Hej! Kul att du är i kodfabriken. Ska vi koda ett coolt 2D-plattformsspel, ett Snake-spel eller en episk Dungeon-crawler?",
                    "Hallå där! AI-hjärnan är vaken och redo. Vilken typ av spelmekanik vill du att vi sätter upp först?"
                ]
                rent_svar = random.choice(svar_alternativ)
                
            elif "va" in text_input or "pratar" in text_input:
                rent_svar = "Jag pratar om spelprogrammering! Vi kan koda i princip vad som helst i Python. Berätta vad du vill att din karaktär ska kunna göra i spelet!"
                
            else:
                svar_alternativ = [
                    f"Intressant idé! '{prompt}' låter som en grym mekanik. Ska vi skriva Python-koden för detta eller bygga grunden för spelskärmen först?",
                    "Det där kan vi bygga på ett väldigt simpelt och elegant sätt i kod. Vill du se ett exempel på hur funktionerna ska struktureras?",
                    "Grymt! Låt oss förvandla den idén till kod. Ska vi lägga till ett poängsystem (Highscore) eller ett inventariesystem för föremål?"
                ]
                rent_svar = random.choice(svar_alternativ)
                
        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
