import streamlit as st
import streamlit.components.v1 as components
import time

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Spel-AI Factory", page_icon="🎮", layout="centered")
st.title("🕹️ Aleos Spel-AI & Visuella Studio")
st.write("Skriv din spelidé, klicka på knappen för att generera och lås fast spelskärmen!")

# Initiera chattminne och fastlåst spelstatus
if "messages" not in st.session_state:
    st.session_state.messages = []
if "valt_spel" not in st.session_state:
    st.session_state.valt_spel = None

# NYÅTERSTÄLLNING: Denna raderar allt och låser upp spelväljaren
if st.button("🔴 🆕 Nollställ & Starta helt nytt spel", use_container_width=True):
    st.session_state.messages = []
    st.session_state.valt_spel = None
    st.success("Spelstudion har nollställts helt och hållet!")
    time.sleep(0.6)
    st.rerun()

st.write("---")

# --- 2. HÄR VISAS DET GENERERADE SPELET OCH LÅSER SIG KVAR ---
if st.session_state.valt_spel == "snake":
    st.subheader("🐍 Fastlåst Spelmotor: Retro Snake")
    st.caption("Spelet är låst på skärmen. Klicka på spelytan och styr med pilarna eller W,A,S,D!")
    snake_html = """
    <canvas id="snakeCanvas" width="400" height="300" style="background: #0a1c0a; display: block; margin: 0 auto; border: 3px solid #00ff00;"></canvas>
    <script>
        const canvas = document.getElementById("snakeCanvas"); const ctx = canvas.getContext("2d");
        let box = 20; let snake = [{x: 9*box, y: 7*box}]; let dir = "RIGHT";
        let food = {x: Math.floor(Math.random()*19)*box, y: Math.floor(Math.random()*14)*box}; let score = 0;
        window.addEventListener("keydown", e => {
            if((e.key==="ArrowLeft"||e.key==="a") && dir!=="RIGHT") dir = "LEFT";
            if((e.key==="ArrowRight"||e.key==="d") && dir!=="LEFT") dir = "RIGHT";
            if((e.key==="ArrowUp"||e.key==="w") && dir!=="DOWN") dir = "UP";
            if((e.key==="ArrowDown"||e.key==="s") && dir!=="UP") dir = "DOWN";
        });
        function draw() {
            ctx.fillStyle = "#0a1c0a"; ctx.fillRect(0,0,400,300);
            for(let i=0; i<snake.length; i++) { ctx.fillStyle = i===0 ? "#00ff00" : "#00aa00"; ctx.fillRect(snake[i].x, snake[i].y, box-2, box-2); }
            ctx.fillStyle = "#ff0000"; ctx.fillRect(food.x, food.y, box-2, box-2);
            let headX = snake[0].x; let headY = snake[0].y;
            if(dir==="LEFT") headX -= box; if(dir==="RIGHT") headX += box; if(dir==="UP") headY -= box; if(dir==="DOWN") headY += box;
            if(headX===food.x && headY===food.y) { score++; food = {x: Math.floor(Math.random()*19)*box, y: Math.floor(Math.random()*14)*box}; }
            else { snake.pop(); }
            let newHead = {x: headX, y: headY};
            if(headX<0||headX>=400||headY<0||headY>=300) { snake = [{x: 9*box, y: 7*box}]; dir="RIGHT"; score=0; }
            snake.unshift(newHead);
            ctx.fillStyle = "white"; ctx.font = "14px Arial"; ctx.fillText("Poäng: " + score, 15, 25);
        }
        setInterval(draw, 150);
    </script>
    """
    components.html(snake_html, height=330)

elif st.session_state.valt_spel == "dungeon":
    st.subheader("👾 Fastlåst Spelmotor: Dungeon Crawler")
    st.caption("Spelet är låst på skärmen. Styr hjälten (@) till skatterna (💰)!")
    dungeon_html = """
    <canvas id="gameCanvas" width="400" height="300" style="background: #1a0f00; display: block; margin: 0 auto; border: 3px solid #ffaa00;"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
        let p = {x: 2, y: 2}; let gold = {x: 6, y: 4}; let score = 0; const size = 30;
        window.addEventListener("keydown", e => {
            if(e.key === "ArrowLeft" || e.key === "a") p.x = Math.max(0, p.x - 1);
            if(e.key === "ArrowRight" || e.key === "d") p.x = Math.min(12, p.x + 1);
            if(e.key === "ArrowUp" || e.key === "w") p.y = Math.max(0, p.y - 1);
            if(e.key === "ArrowDown" || e.key === "s") p.y = Math.min(9, p.y + 1);
            if(p.x === gold.x && p.y === gold.y) { score += 100; gold.x = Math.floor(Math.random()*12); gold.y = Math.floor(Math.random()*9); }
        });
        function draw() {
            ctx.fillStyle = "#1a0f00"; ctx.fillRect(0, 0, 400, 300);
            ctx.fillStyle = "#ffaa00"; ctx.beginPath(); ctx.arc(gold.x*size+15, gold.y*size+15, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#00d2ff"; ctx.font = "20px Arial"; ctx.fillText("@", p.x*size+8, p.y*size+22);
            ctx.fillStyle = "white"; ctx.font = "14px Arial"; ctx.fillText("Guld: " + score + " 💰", 15, 25);
        }
        setInterval(draw, 100);
    </script>
    """
    components.html(dungeon_html, height=330)

elif st.session_state.valt_spel == "bil":
    st.subheader("🏎‍🟀 Fastlåst Spelmotor: Neon Racer")
    st.caption("Spelet är låst på skärmen. Håll inne UPPÅTPIL eller W för att köra!")
    bil_html = """
    <canvas id="gameCanvas" width="400" height="300" style="background: #111; display: block; margin: 0 auto; border: 3px solid #ff0055;"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
        let speed = 0; let carY = 200; let keys = {};
        window.addEventListener("keydown", e => keys[e.key] = true);
        window.addEventListener("keyup", e => keys[e.key] = false);
        function update() {
            if (keys["ArrowUp"] || keys["w"]) speed = Math.min(8, speed + 0.1); else speed = Math.max(0, speed - 0.1);
            carY -= speed * 0.3; if(carY < -50) carY = 300;
        }
        function draw() {
            ctx.fillStyle = "#111"; ctx.fillRect(0, 0, 400, 300);
            ctx.fillStyle = "#333"; ctx.fillRect(120, 0, 160, 300);
            ctx.fillStyle = "#ff0055"; ctx.fillRect(185, carY, 30, 50);
            ctx.fillStyle = "white"; ctx.font = "14px Arial"; ctx.fillText("Fart: " + Math.round(speed*10) + " km/h 🏎‍🟀", 15, 25);
        }
        function loop() { update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
    """
    components.html(bil_html, height=330)
else:
    st.info("🤖 Ingen aktiv spelmotor. Fyll i rutorna nedan och klicka på 'Generera Spel' för att starta!")

st.write("---")

# --- 3. KONTROLLER OCH CHATT ---
st.write("### 📸 Visuell insamling och analys:")
bild_instruktion = st.text_input("Beskriv din visuella scanning eller spelskärm här:")

# Visa chattmeddelanden
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Vi skapar en snygg inmatningsrad med Textfält + Generera-knapp sida vid sida
chatt_spår, knapp_spår = st.columns([4, 1])

with chatt_spår:
    input_text = st.text_input("Fyll i din spelidé eller prata med AI:n här:", key="user_input_field")

with knapp_spår:
    st.write(" ") # Justering
    generera_klick = st.button("🤖 Generera Spel", use_container_width=True)

# PROCESSOR: Körs när du klickar på den nya genereraknappen eller trycker enter
if generera_klick and input_text:
    final_prompt = input_text
    if bild_instruktion:
        final_prompt = f"[Visuell scanning: {bild_instruktion}] " + final_prompt
        
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    
    text_analys = input_text.lower()
    
    # Här scannar vi orden och sätter fast rätt spel i minnet!
    if "snake" in text_analys or "orm" in text_analys or "grön" in text_analys:
        st.session_state.valt_spel = "snake"
        svar = "🐍 *Spel genererat och låst: Retro Snake!* Spelskärmen har fixerats högst upp och kommer stanna kvar tills du nollställer."
    elif "skat" in text_analys or "dungeon" in text_analys or "crawler" in text_analys or "boss" in text_analys:
        st.session_state.valt_spel = "dungeon"
        svar = "👾 *Spel genererat och låst: Dungeon Crawler!* Grottan har fixerats högst upp och kommer stanna kvar tills du nollställer."
    elif "bil" in text_analys or "race" in text_analys or "kör" in text_analys:
        st.session_state.valt_spel = "bil"
        svar = "🏎‍🟀 *Spel genererat och låst: Neon Racer!* Banan har fixerats högst upp och kommer stanna kvar tills du nollställer."
    else:
        svar = f"Registrerat! Om du vill låsa fast en visuell skärm, se till att skriva *'snake', *'dungeon'* eller *'bilspel'** på raden och klicka på knappen!"

    st.session_state.messages.append({"role": "assistant", "content": svar})
    st.rerun()
