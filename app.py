import streamlit as st
import streamlit.components.v1 as components
import time

# 1. DESIGN OCH STRUKTUR
st.set_page_config(page_title="Aleos Visuella Spelstudio", page_icon="🕹️", layout="centered")
st.title("🕹️ Aleos Visuella Spelstudio")
st.write("Välj ett spel nedan för att generera en visuell spelbakgrund och spela direkt på skärmen!")

# Initiera chattminne och vald spelmotor
if "valt_spel" not in st.session_state:
    st.session_state.valt_spel = None

# --- KNAPPAR FÖR ATT VÄLJA OCH GENERERA SPEL ---
st.write("### 🛠️ Generera och starta en spelmotor:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Rymd-Shooter", use_container_width=True):
        st.session_state.valt_spel = "rymd"
with col2:
    if st.button("🏎‍🟀 Bil-Racing", use_container_width=True):
        st.session_state.valt_spel = "bil"
with col3:
    if st.button("👾 Dungeon Crawler", use_container_width=True):
        st.session_state.valt_spel = "dungeon"

# --- 2. HÄR GENERERAS DE FAKTISKA SPELEN MED BAKGRUND OCH GRAFIK ---

# === MOTOR 1: RYMD-SHOOTER ===
if st.session_state.valt_spel == "rymd":
    st.subheader("🌌 Visuell Spelmotor: Space Shooter")
    st.info("Klicka på spelskärmen. Använd VÄNSTER/HÖGER pilspår (eller A/D) för att styra och BLANKSTEG för att skjuta laser!")
    
    rymd_html = """
    <canvas id="gameCanvas" width="400" height="400" style="background: #050510; display: block; margin: 0 auto; border: 3px solid #39ff14;"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let playerX = 180;
        let lasers = [];
        let keys = {};

        window.addEventListener("keydown", e => { keys[e.key] = true; if(e.key === " ") lasers.push({x: playerX + 17, y: 350}); });
        window.addEventListener("keyup", e => keys[e.key] = false);

        function update() {
            if (keys["ArrowLeft"] || keys["a"]) playerX = Math.max(0, playerX - 5);
            if (keys["ArrowRight"] || keys["d"]) playerX = Math.min(360, playerX + 5);
            lasers.forEach(l => l.y -= 7);
            lasers = lasers.filter(l => l.y > 0);
        }

        function draw() {
            // Rita stjärnbakgrund
            ctx.fillStyle = "#050510";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            for(let i=0; i<15; i++) ctx.fillRect((i*27)%400, (i*53)%400, 2, 2);

            // Rita laserskott
            ctx.fillStyle = "#ff0055";
            lasers.forEach(l => ctx.fillRect(l.x, l.y, 4, 15));

            // Rita Rymdskeppet (Grönt neon-skepp)
            ctx.fillStyle = "#39ff14";
            ctx.fillRect(playerX, 360, 40, 20);
            ctx.fillRect(playerX + 15, 345, 10, 15);
        }

        function loop() { update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
    """
    components.html(rymd_html, height=430)

# === MOTOR 2: BIL-RACING ===
elif st.session_state.valt_spel == "bil":
    st.subheader("🏁 Visuell Spelmotor: Neon Racing")
    st.info("Klicka på spelskärmen. Håll inne UPPÅTPIL (eller W) för att accelerera din racerbil på banan!")
    
    bil_html = """
    <canvas id="gameCanvas" width="400" height="400" style="background: #111; display: block; margin: 0 auto; border: 3px solid #ff0055;"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let speed = 0;
        let carY = 300;
        let keys = {};

        window.addEventListener("keydown", e => keys[e.key] = true);
        window.addEventListener("keyup", e => keys[e.key] = false);

        function update() {
            if (keys["ArrowUp"] || keys["w"]) speed = Math.min(8, speed + 0.1);
            else speed = Math.max(0, speed - 0.1);
            carY -= speed * 0.2;
            if(carY < -40) carY = 400;
        }

        function draw() {
            ctx.fillStyle = "#111";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            # Spelbakgrund: Grå Racingbana med linjer
            ctx.fillStyle = "#333";
            ctx.fillRect(100, 0, 200, 400);
            ctx.strokeStyle = "white";
            ctx.setLineDash([20, 20]);
            ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(200, 400); ctx.stroke();

            # Rita Racerbilen (Neonrosa sportbil)
            ctx.fillStyle = "#ff0055";
            ctx.fillRect(185, carY, 30, 50);
            ctx.fillStyle = "black";
            ctx.fillRect(180, carY+5, 5, 10); ctx.fillRect(215, carY+5, 5, 10);
            ctx.fillRect(180, carY+35, 5, 10); ctx.fillRect(215, carY+35, 5, 10);
        }

        function loop() { update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
    """
    components.html(bil_html, height=430)

# === MOTOR 3: DUNGEON CRAWLER ===
elif st.session_state.valt_spel == "dungeon":
    st.subheader("👾 Visuell Spelmotor: Dungeon Crawler")
    st.info("Klicka på spelskärmen. Använd PILTANGENTERNA (W,A,S,D) för att styra hjälten (@) till skatterna (💰)!")
    
    dungeon_html = """
    <canvas id="gameCanvas" width="400" height="400" style="background: #1a0f00; display: block; margin: 0 auto; border: 3px solid #ffaa00;"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let p = {x: 2, y: 2};
        let gold = {x: 6, y: 5};
        let score = 0;
        const size = 40;

        window.addEventListener("keydown", e => {
            if(e.key === "ArrowLeft" || e.key === "a") p.x = Math.max(0, p.x - 1);
            if(e.key === "ArrowRight" || e.key === "d") p.x = Math.min(9, p.x + 1);
            if(e.key === "ArrowUp" || e.key === "w") p.y = Math.max(0, p.y - 1);
            if(e.key === "ArrowDown" || e.key === "s") p.y = Math.min(9, p.y + 1);
            
            if(p.x === gold.x && p.y === gold.y) {
                score += 100;
                gold.x = Math.floor(Math.random() * 10);
                gold.y = Math.floor(Math.random() * 10);
            }
        });

        function draw() {
            // Grottbakgrund (Rutnät)
            ctx.fillStyle = "#1a0f00"; ctx.fillRect(0, 0, 400, 400);
            ctx.strokeStyle = "#2b1a04";
            for(let i=0; i<10; i++) {
                for(let j=0; j<10; j++) ctx.strokeRect(i*size, j*size, size, size);
            }

            // Rita guldskatten (Guldcirkel)
            ctx.fillStyle = "#ffaa00";
            ctx.beginPath(); ctx.arc(gold.x*size+20, gold.y*size+20, 12, 0, Math.PI*2); ctx.fill();

            // Rita Spelaren (Ljusblå hjälte)
            ctx.fillStyle = "#00d2ff";
            ctx.font = "24px Arial";
            ctx.fillText("@", p.x*size+12, p.y*size+28);

            // Poängräknare
            ctx.fillStyle = "white"; ctx.font = "16px Arial";
            ctx.fillText("Guld: " + score + " 💰", 15, 30);
        }

        setInterval(draw, 100);
    </script>
    """
    components.html(dungeon_html, height=430)

else:
    st.info("Klicka på en av knapparna högst upp för att rita upp spelbakgrunden och generera spelmotorn!")
