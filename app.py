import streamlit as st
import time
import random

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Spel-AI Factory", page_icon="🕹️", layout="centered")
st.title("🕹️ Aleos Universella Spel-AI")
st.write("Skriv vilket spel du vill bygga, så genererar motorn rätt Python-kod direkt!")

# Initiera chattminne och spelstatus
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HÄR ÄR DE TVÅ SEPARATA KNAPPARNA HÖGST UPP ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🆕 Starta nytt spel", use_container_width=True):
        st.session_state.messages = []
        st.success("AI-Fabriken är nollställd för ett helt nytt spel!")
        time.sleep(0.6)
        st.rerun()

with col2:
    if st.button("🧹 Rensa chattminne", use_container_width=True):
        st.session_state.messages = []
        st.success("Chattsträngen har städats rent!")
        time.sleep(0.6)
        st.rerun()

# Visa chattbubblor
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CHATTEN (Dynamisk kodgenerator för ALLA typer av spel)
if prompt := st.chat_input("Vilket sorts spel eller vilken mekanik vill du koda?"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Bearbetar instruktioner..."):
            time.sleep(0.4)
            
            text_input = prompt.lower()
            rent_svar = ""

            # --- NY FUNKTION: Känner av frågor om VAR koden ska läggas in ---
            if "vart" in text_input or "var " in text_input or "hur" in text_input or "sätta" in text_input:
                rent_svar = """Du ska klistra in och köra all spelkod i *Google Colab* eller *Kaggle Notebooks*! 

*Så här gör du steg-för-steg:*
1. Kopiera kodblocket från appen (rutan som börjar med class ...).
2. Gå till din flik i Google Colab eller öppna en ny Notebook på Kaggle.
3. Skapa en ny kodcell genom att klicka på *+ Kod* (eller + Code).
4. Klistra in koden där och klicka på den runda *Play-knappen* (\u25b6).

Då startar spelet direkt i textformat under rutan! Vilken typ av spelkod vill du att jag genererar åt dig nu?"""

            # --- KATAGORI 1: RYMDSPEL / SKJUTA (Space Invaders) ---
            elif "rymd" in text_input or "skjut" in text_input or "laser" in text_input:
                rent_svar = """Här är grundkoden för ett *Rymd-skjutspel (Space Shooter)* i Python! Det innehåller ett skepp som kan flytta sig och skjuta laser.

python
class Rymdskepp:
    def __init__(self, namn):
        self.namn = namn
        self.x = 0
        self.skott = []

    def flytta(self, riktning):
        if riktning == "vänster": self.x -= 1
        elif riktning == "höger": self.x += 1
        print(f"🚀 {self.namn} flyttade till position X: {self.x}")

    def skjut_laser(self):
        self.skott.append(f"Laser_{len(self.skott) + 1}")
        print(f"🔥 PIIIIW! Laser avfyrad från position {self.x}!")

# --- TESTA RYMDMEKANIKEN ---
player = Rymdskepp("Alfa-1")
player.flytta("höger")
player.skjut_laser()

Kopiera detta till Colab/Kaggle för att köra det! Skriv *'nytt spel'* eller tryck på knappen högst upp för att byta genre."""

            # --- KATEGORI 2: BILSPEL / RACING ---
            elif "bil" in text_input or "race" in text_input or "kör" in text_input:
                rent_svar = """Här är Python-koden för ett *Racingspel / Bilmekanik* som hanterar hastighet, acceleration och bromsning!

python
class Racerbil:
    def __init__(self, modell):
        self.modell = modell
        self.hastighet = 0

    def gasa(self):
        self.hastighet += 20
        print(f"🏎‍🟀 {self.modell} accelererar! Hastighet: {self.hastighet} km/h")

    def bromsa(self):
        self.hastighet = max(0, self.hastighet - 30)
        print(f"🛑 Bromsar! Hastighet nu: {self.hastighet} km/h")

# --- TESTA BILEN ---
bil = Racerbil("Turbo-X")
bil.gasa()
bil.gasa()
bil.bromsa()

Kopiera detta till Colab/Kaggle för att köra det! Skriv *'nytt spel'* eller tryck på knappen högst upp för att byta genre."""

            # --- KATEGORI 3: PLATFORM / HOPP (Mario-stil) ---
            elif "plattform" in text_input or "hopp" in text_input or "mario" in text_input:
                rent_svar = """Här är fysik-motor i miniformat för ett *Plattformsspel* som hanterar gravitation och hopp!

python
class PlattformSpelare:
    def __init__(self):
        self.y = 0
        self.på_marken = True

    def hoppa(self):
        if self.på_marken:
            self.y += 10
            self.på_marken = False
            print(f"🦘 HOPP! Spelaren hoppade upp till höjd Y: {self.y}")
        else:
            print("❌ Kan inte hoppa i luften!")

    def uppdatera_gravitation(self):
        if not self.på_marken:
            self.y = 0
            self.på_marken = True
            print("🌍 Faller ner till marken igen (Y: 0)")

# --- TESTA HOPPMETODEN ---
hero = PlattformSpelare()
hero.hoppa()
hero.uppdatera_gravitation()

Kopiera detta till Colab/Kaggle för att köra det! Skriv *'nytt spel'* eller tryck på knappen högst upp för att byta genre."""

            # --- KATEGORI 4: DUNGEON CRAWLER / SKATTER ---
            elif "dungeon" in text_input or "crawler" in text_input or "skatt" in text_input or "inventarie" in text_input:
                rent_svar = """Här är koden för ett *Äventyrsspel / Dungeon crawler* med fungerande inventarie och skattsystem!

python
class Spelare:
    def __init__(self, namn):
        self.namn = namn
        self.guld = 0
        self.inventarie = []

    def plocka_upp_skatt(self, sak, värde):
        self.inventarie.append(sak)
        self.guld += värde
        print(f"🎒 {self.namn} hittade {sak}! (+{raw_guld:=värde} guld)")

hero = Spelare("Aleo")
hero.plocka_upp_skatt("Magisk diamant", 100)

Kopiera detta till Colab/Kaggle för att köra det! Skriv *'nytt spel'* eller tryck på knappen högst upp för att byta genre."""

            # --- STANDARD / ALLMÄNT ---
            else:
                rent_svar = f"""Jag är redo! Berätta vilket spel du vill sätta upp basen för. 
                
Välj mellan att skriva *'bilspel', *'rymdspel'*, *'plattformsspel'* eller *'dungeon-crawler'* så spottar jag ur mig koden direkt! Du kan också fråga mig *'vart ska jag sätta koden'** för att få instruktioner."""

        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
