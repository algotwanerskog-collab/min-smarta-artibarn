import streamlit as st
import time
import random

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Universella Spel-AI", page_icon="🕹️", layout="centered")
st.title("🕹️ Aleos Universella Spel-AI")
st.write("Skriv vilken typ av spel eller mekanik du vill bygga, så genererar motorn rätt Python-kod direkt!")

# Initiera chattminne
if "messages" not in st.session_state:
    st.session_state.messages = []

# Knapp för att rensa minnet
if st.button("🔄 Starta nytt spel / Rensa minne"):
    st.session_state.messages = []
    st.success("Appen är återställd och redo för ett nytt spel!")
    time.sleep(0.5)
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
        with st.spinner("Analyserar speltyp och bygger kod..."):
            time.sleep(0.5)
            
            text_input = prompt.lower()
            rent_svar = ""

            # --- KATAGORI 1: RYMDSPEL / SKJUTA (Space Invaders / Asteroids) ---
            if "rymd" in text_input or "skjut" in text_input or "laser" in text_input:
                rent_svar = """Här är grundkoden för ett *Rymd-skjutspel (Space Shooter)* i Python! Det innehåller ett skepp som kan flytta sig i X-led och skjuta laserskott.

python
class Rymdskepp:
    def __init__(self, namn):
        self.namn = namn
        self.x = 0
        self.skott = []

    def flytta(self, riktning):
        if riktning == "vänster":
            self.x -= 1
        elif riktning == "höger":
            self.x += 1
        print(f"🚀 {self.namn} flyttade till position X: {self.x}")

    def skjut_laser(self):
        laser_id = len(self.skott) + 1
        self.skott.append(f"Laser_{laser_id}")
        print(f"🔥 PIIIIW! Laser skickad från position {self.x}! (Aktiva skott på skärmen: {len(self.skott)})")

# --- TESTA RYMDMEKANIKEN ---
player = Rymdskepp("Alfa-1")
player.flytta("höger")
player.skjut_laser()

Vill du lägga till kod för *fiende-skepp* som spawnar från taket eller ett *liv-system* till ditt rymdspel?"""

            # --- KATEGORI 2: BILSPEL / RACING / HASTIGHET ---
            elif "bil" in text_input or "race" in text_input or "kör" in text_input:
                rent_svar = """Här är Python-koden för ett *Racingspel / Bilmekanik*. Den hanterar hastighet, acceleration, bromsning och växling!

python
class Racerbil:
    def __init__(self, modell):
        self.modell = modell
        self.hastighet = 0
        self.växel = 1

    def gasa(self):
        self.hastighet += 20
        if self.hastighet > 60 and self.växel == 1:
            self.växel = 2
        print(f"🏎‍🟀 {self.modell} accelererar! Hastighet: {self.hastighet} km/h (Växel: {self.växel})")

    def bromsa(self):
        self.hastighet = max(0, self.hastighet - 30)
        print(f"🛑 Bromsar! Hastighet nu: {self.hastighet} km/h")

# --- TESTA BILEN ---
min_bil = "Turbo-X"
bil = Racerbil(min_bil)
bil.gasa()
bil.gasa()
bil.bromsa()

Vill du bygga ut detta med en *bana med varvtider* eller *hinder på vägen*?"""

            # --- KATEGORI 3: PLATFORM / HOPP / RÖRELSE (Mario-stil) ---
            elif "plattform" in text_input or "hopp" in text_input or "mario" in text_input:
                rent_svar = """Här är en fysik-motor i miniformat för ett *Plattformsspel*! Den hanterar gravitation och hopp-logik.

python
class PlattformSpelare:
    def __init__(self):
        self.y = 0 # Marknivå
        self.står_på_marken = True

    def hoppa(self):
        if self.står_på_marken:
            self.y += 10
            self.står_på_marken = False
            print(f"🦘 HOPP! Spelaren hoppade upp till höjd Y: {self.y}")
        else:
            print("❌ Kan inte hoppa i luften!")

    def uppdatera_gravitation(self):
        if not self.står_på_marken:
            self.y = 0
            self.står_på_marken = True
            print("🌍 Gravitationen drog ner spelaren till marken igen (Y: 0)")

# --- TESTA HOPPMETODEN ---
hero = PlattformSpelare()
hero.hoppa()
hero.hoppa() # Testar dubbelhopp (ska nekas)
hero.uppdatera_gravitation()

Vill du lägga till *plattformar i luften* eller *fiender (Goombas)* man kan hoppa på?"""

            # --- KATEGORI 4: DUNGEON CRAWLER / RPG / INVENTARIE (Det vi körde innan) ---
            elif "dungeon" in text_input or "crawler" in text_input or "rpg" in text_input or "skatt" in text_input or "inventarie" in text_input:
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
        print(f"🎒 {self.namn} hittade {sak}! (+{värde} guld)")

    def sälj_allt(self):
        print(f"⚖️ Säljer {len(self.inventarie)} föremål för totalt {self.guld} guld!")
        self.inventarie.clear()

hero = Spelare("Aleo")
hero.plocka_upp_skatt("Magisk dryck", 50)
hero.sälj_allt()

Vill du ha kod för en *slumpmässig grott-karta* eller ett *stridssystem med bossar*?"""

            # --- STANDARD / ALLMÄNT (Om du skriver något helt annat) ---
            else:
                rent_svar = f"""Jag fattar! Du vill programmera något som har med *'{prompt}'* och spelutveckling att göra. 

För att ge dig exakt rätt Python-kod, berätta: Är det ett *bilspel, ett **rymdspel, ett **plattformsspel* eller en *dungeon-crawler* du vill sätta upp basen för? Skriv ditt val i chattrutan nedan så spottar jag ur mig koden direkt!"""

        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
