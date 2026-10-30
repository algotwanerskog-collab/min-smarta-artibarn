import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# 1. DESIGN OCH SIKT
st.set_page_config(page_title="Aleos AI Spel-Fabrik", page_icon="🕹️", layout="centered")
st.title("🕹️ Aleos Äkta AI Spel-Fabrik")
st.write("Skriv precis hur du vill att spelet ska fungera, så kodar AI-hjärnan det live åt dig!")

# Officiell och stabil gratis-API för Qwen-modellen
API_URL = "https://huggingface.co"

# Initiera spelsessionen
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

# --- 2. HÄR RITAS AI:NS EGEN GENERERADE KOD UT LIVE ---
if st.session_state.genererad_kod:
    st.subheader("🎮 Din Genererade Spelmotor (Spelbar live):")
    # Vi bäddar in AI:ns egna JavaScript- och Canvas-kod direkt i gränssnittet
    components.html(st.session_state.genererad_kod, height=450, scrolling=True)
else:
    st.info("🤖 Ingen aktiv spelmotor än. Skriv instruktioner nedan och klicka på 'Generera Spel' för att låta AI:n koda bakgrunden och logiken!")

st.write("---")

# --- 3. INPUT OCH SMART CHATT SOM ALLTID LIGGER KVAR ---
st.write("### 📸 Visuell insamling och analys:")
bild_instruktion = st.text_input("Beskriv din bild-scanning eller spelskärm här (t.ex. gråa väggar, monster, guld):")

# Visa tidigare chattmeddelanden
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Textinmatning + Genereraknapp sida vid sida med den fixade kolumn-tvåan!
chatt_spår, knapp_spår = st.columns(2)

with chatt_spår:
    input_text = st.text_input("Berätta för AI:n vad du vill bygga eller ändra:", key="user_input_field")

with knapp_spår:
    st.write(" ") # Justering
    generera_klick = st.button("🤖 Generera Spel", use_container_width=True)

# BEARBETNING: När användaren klickar på knappen
if generera_klick and input_text:
    final_prompt = input_text
    if bild_instruktion:
        final_prompt = f"[Visuell scanning: {bild_instruktion}] " + final_prompt
        
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    
    with st.spinner("AI-hjärnan kodar ditt spel från grunden..."):
        try:
            # Vi instruerar modellen att skriva komplett, snygg HTML5/Canvas-kod baserat på din prompt
            system_prompt = (
                "Du är en expert på spelprogrammering. Skriv ett komplett, spelbart 2D-spel i ett enda HTML-block "
                "med <canvas> och <script>. Använd snygg pixel-grafik, färgade bakgrunder, och implementera "
                "all mekanik som användaren ber om (kontroller, väggar, fiender, guld, siktlinje). "
                "Svara ENDAST med HTML-koden, inkludera inga förklaringar."
            )
            
            payload = {
                "inputs": f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{final_prompt}<|im_end|>\n<|im_start|>assistant\n",
                "parameters": {"max_new_tokens": 1000, "temperature": 0.3}
            }
            
            response = requests.post(API_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                resultat = response.json()
                genererad_text = ""
                
                if isinstance(resultat, list) and len(resultat) > 0 and "generated_text" in resultat[0]:
                    genererad_text = resultat[0]["generated_text"].strip()
                elif isinstance(resultat, dict) and "generated_text" in resultat:
                    genererad_text = resultat["generated_text"].strip()
                
                # Om modellen spottar ur sig kodblock, städa bort dem så att Streamlit kan köra koden rent
                if "html" in genererad_text:
                    genererad_text = genererad_text.split("html")[-1].split("")[0].strip()
                elif "" in genererad_text:
                    genererad_text = genererad_text.split("")[-1].split("")[0].strip()
                
                if genererad_text.startswith("<"):
                    st.session_state.genererad_kod = genererad_text
                    svar = "⚔️ *Spel framgångsrikt genererat av AI:n!* Jag har skrivit koden baserat på dina exakta instruktioner. Spela det högst upp på skärmen!"
                else:
                    st.session_state.genererad_kod = """
                    <div style="background:#111;color:#ff5500;padding:20px;text-align:center;font-family:Arial;">
                        <h3>🤖 AI-Spelmotorn laddas...</h3>
                        <p>Servern håller på att starta upp modellen. Skicka ditt meddelande en gång till om 15 sekunder så byggs spelet!</p>
                    </div>
                    """
                    svar = "Modellen startar upp i molnet. Prova att klicka på knappen igen om några sekunder!"
            else:
                svar = f"Kunde inte nå AI-hjärnan just nu (Status: {response.status_code}). Vi provar igen!"
        except Exception as e:
            svar = f"Ett nätverksfel uppstod, men koden är säkrad. Testa igen! (Info: {e})"
            
    st.session_state.messages.append({"role": "assistant", "content": svar})
    st.rerun()
