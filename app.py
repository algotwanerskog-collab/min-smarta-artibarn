import streamlit as st
import streamlit.components.v1 as components
import time

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Spel-AI Factory", page_icon="🎮", layout="centered")
st.title("🕹️ Aleos Spel-AI & Visuella Studio")
st.write("Skriv vad du vill bygga eller ladda upp instruktioner, så genereras de kompakta spelmotorerna live här på skärmen!")

# Initiera chattminne och spelstatus
if "messages" not in st.session_state:
    st.session_state.messages = []
if "valt_spel" not in st.session_state:
    st.session_state.valt_spel = None

# Knappar för städning högst upp
col1, col2 = st.columns(2)
with col1:
    if st.button("🆕 Starta helt nytt spel", use_container_width=True):
        st.session_state.messages = []
        st.session_state.valt_spel = None
        st.success("Spelstudion återställd!")
        time.sleep(0.4)
        st.rerun()
with col2:
    if st.button("🧹 Töm chatten", use_container_width=True):
        st.session_state.messages = []
        st.success("Chatten rensad!")
        time.sleep(0.4)
        st.rerun()

# --- 2. KÖR DE VISUELLA SPELMOTORERNA HÄR (Om ett spel är aktivt) ---
if st.session_state.valt_spel == "snake":
    st.subheader("🐍 Visuell Spelmotor: Retro Snake")
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
    st.subheader("👾 Visuell Spelmotor: Dungeon Crawler")
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
    st.subheader("🏎‍🟀 Visuell Spelmotor: Neon Racer")
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

st.write("---")

# --- 3. DESSA TEXTRUTOR LIGGER NU HELT FRISTÅENDE OCH FÖRSVINNER ALDRIG ---
st.write("### 📸 Visuell insamling och analys:")
bild_instruktion = st.text_input("Beskriv din visuella scanning eller spelskärm här:")

# Visa tidigare konversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CHATT-INPUT (Ligger alltid kvar längst ner på skärmen!)
if prompt := st.chat_input("Vilket spel eller vilken mekanik vill du generera nu?"):
    if bild_instruktion:
        prompt = f"[Visuell observation: {bild_instruktion}] " + prompt
        
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        text_input = prompt.lower()
        
        if "snake" in text_input or "orm" in text_input or "grön" in text_input:
            st.session_state.valt_spel = "snake"
            rent_svar = "🐍 *Retro Snake aktiverat!* Spelsidan har uppdaterats högst upp. Klicka på spelskärmen och styr ormen!"
        elif "skat" in text_input or "dungeon" in text_input or "crawler" in text_input:
            st.session_state.valt_spel = "dungeon"
            rent_svar = "👾 *Dungeon Crawler aktiverat!* Grottbakgrunden har ritats upp ovanför. Styr @ och samla guld!"
        elif "bil" in text_input or "race" in text_input or "kör" in text_input:
            st.session_state.valt_spel = "bil"
            rent_svar = "🏎‍🟀 *Neon Racer aktiverat!* Racingbanan ligger laddad högst upp. Håll inne W eller UPPÅTPIL för att gasa!"
        else:
            rent_svar = f"Registrerat! Skriv *'snake', *'dungeon'* eller *'bilspel'** i rutan nedan så ritar jag upp rätt grafik direkt ovanför chatten!"

        st.markdown(rent_svar)
        st.session_state.messages.append({"role": "assistant", "content": rent_svar})
