import streamlit as st
import streamlit.components.v1 as components
import time

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Spel-AI Factory 5.0", page_icon="🎮", layout="centered")
st.title("🕹️ Aleos Lokala Spelstudio")
st.write("100% kraschsäker studio. Skriv ditt spelval nedan och lås fast spelmotorn!")

# Initiera chattminne och fastlåst spelstatus
if "messages" not in st.session_state:
    st.session_state.messages = []
if "valt_spel" not in st.session_state:
    st.session_state.valt_spel = None

# HUVUDÅTERSTÄLLARE
if st.button("🔴 🆕 Nollställ allt & starta ett helt nytt spel", use_container_width=True):
    st.session_state.messages = []
    st.session_state.valt_spel = None
    st.success("Spelstudion har nollställts!")
    time.sleep(0.4)
    st.rerun()

st.write("---")

# --- 2. HÄR VISAS DET GENERERADE SPELET ---

# === NYA SPELET: TURBASERAT PUSSEL (MONSTER TAR 2 STEG) ===
if st.session_state.valt_spel == "pussel":
    st.subheader("🧩 Låst Spelmotor: Turbaserat Labyrint-Pussel")
    st.caption("Du rör dig 1 steg -> Monstret (M) tar 2 steg mot dig! Hitta dörren (🚪)!")
    pussel_html = """
    <div style="text-align: center;">
        <canvas id="pusselCanvas" width="400" height="400" style="background: #0f0f1a; border: 3px solid #00ffcc; image-rendering: pixelated;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById("pusselCanvas"); const ctx = canvas.getContext("2d");
        const TILE_SIZE = 40; const GRID_SIZE = 10;
        let player = { x: 1, y: 1, level: 1 }; let monster = { x: 8, y: 8 }; let map = [];

        function genereraLabyrint() {
            for (let y = 0; y < GRID_SIZE; y++) {
                map[y] = [];
                for (let x = 0; x < GRID_SIZE; x++) {
                    if (x === 0 || x === GRID_SIZE - 1 || y === 0 || y === GRID_SIZE - 1) map[y][x] = 1;
                    else if ((x === 3 && y !== 2 && y !== 7) || (x === 6 && y !== 3 && y !== 6)) map[y][x] = 1;
                    else map[y][x] = 0;
                }
            }
            map[8][1] = 6; // Dörren 🚪
        }
        genereraLabyrint();

        function flyttaM() {
            let dx = player.x - monster.x; let dy = player.y - monster.y;
            let nX = monster.x + (dx !== 0 ? (dx > 0 ? 1 : -1) : 0);
            let nY = monster.y + (dx === 0 && dy !== 0 ? (dy > 0 ? 1 : -1) : 0);
            if (map[nY] && map[nY][nX] !== 1) { monster.x = nX; monster.y = nY; }
        }

        window.addEventListener("keydown", e => {
            let nX = player.x; let nY = player.y; let step = false;
            if (e.key === "ArrowLeft" || e.key === "a") { nX--; step = true; }
            if (e.key === "ArrowRight" || e.key === "d") { nX++; step = true; }
            if (e.key === "ArrowUp" || e.key === "w") { nY--; step = true; }
            if (e.key === "ArrowDown" || e.key === "s") { nY++; step = true; }

            if (step && map[nY] && map[nY][nX] !== 1) {
                player.x = nX; player.y = nY;
                if (map[player.y][player.x] === 6) {
                    player.level++; player.x = 1; player.y = 1; monster.x = 8; monster.y = 8;
                    alert("🎉 Level avklarad! Vidare till nästa!"); return;
                }
                flyttaM(); if (monster.x === player.x && monster.y === player.y) { alert("💀 Fångad! Startar om..."); player.x = 1; player.y = 1; monster.x = 8; monster.y = 8; return; }
                flyttaM(); if (monster.x === player.x && monster.y === player.y) { alert("💀 Fångad! Startar om..."); player.x = 1; player.y = 1; monster.x = 8; monster.y = 8; return; }
            }
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let y = 0; y < GRID_SIZE; y++) {
                for (let x = 0; x < GRID_SIZE; x++) {
                    if (map[y][x] === 1) { ctx.fillStyle = "#4a4a5a"; ctx.fillRect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1); }
                    else if (map[y][x] === 6) { ctx.fillStyle = "#00ffcc"; ctx.font = "22px Arial"; ctx.fillText("🚪", x*TILE_SIZE+8, y*TILE_SIZE+28); }
                    else { ctx.fillStyle = "#161626"; ctx.fillRect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE); }
                }
            }
            ctx.fillStyle = "#ff3333"; ctx.font = "bold 22px Courier"; ctx.fillText("M", monster.x*TILE_SIZE+12, monster.y*TILE_SIZE+28);
            ctx.fillStyle = "#00d2ff"; ctx.font = "bold 24px Arial"; ctx.fillText("@", player.x*TILE_SIZE+10, player.y*TILE_SIZE+28);
        }
        setInterval(draw, 50);
    </script>
    """
    components.html(pussel_html, height=430)

# === DET GAMLA SPELET: DUNGEON CRAWLER MED HP ===
elif st.session_state.valt_spel == "dungeon":
    st.subheader("👾 Låst Spelmotor: Pixel RPG Crawler")
    st.caption("Styr hjälten (@). Besegra Zombies (Z) och samla guld!")
    dungeon_html = """
    <div style="text-align: center;">
        <canvas id="rpgCanvas" width="400" height="400" style="background: #0d0d0d; border: 3px solid #ff5500; image-rendering: pixelated;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById("rpgCanvas"); const ctx = canvas.getContext("2d");
        const TILE_SIZE = 40; const GRID_SIZE = 10;
        let player = { x: 1, y: 1, gold: 0, hp: 5 }; let map = [];
        for(let y=0; y<GRID_SIZE; y++){ map[y]=[]; for(let x=0; x<GRID_SIZE; x++) map[y][x] = (x===0||x===9||y===0||y===9||(y===5&&x!==5)) ? 1 : 0; }
        map[8][8] = 3; map[2][7] = 4;
        window.addEventListener("keydown", e => {
            let nX = player.x; let nY = player.y;
            if(e.key==="ArrowLeft"||e.key==="a") nX--; if(e.key==="ArrowRight"||e.key==="d") nX++;
            if(e.key==="ArrowUp"||e.key==="w") nY--; if(e.key==="ArrowDown"||e.key==="s") nY++;
            if(map[nY] && map[nY][nX] !== 1) {
                if(map[nY][nX]===4) { player.gold+=10; map[nY][nX]=0; }
                if(map[nY][nX]===3) { player.gold+=20; map[nY][nX]=0; }
                player.x = nX; player.y = nY;
            }
        });
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for(let y=0; y<GRID_SIZE; y++){
                for(let x=0; x<GRID_SIZE; x++){
                    let dist = Math.sqrt(Math.pow(x-player.x,2)+Math.pow(y-player.y,2));
                    if(dist>3){ ctx.fillStyle="#000"; ctx.fillRect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE); continue; }
                    if(map[y][x]===1){ ctx.fillStyle="#3a3a3a"; ctx.fillRect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE-1,TILE_SIZE-1); }
                    else { ctx.fillStyle="#1c120c"; ctx.fillRect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE); }
                    if(map[y][x]===3){ ctx.fillStyle="#ffa"; ctx.font="20px Arial"; ctx.fillText("🎁", x*TILE_SIZE+10, y*TILE_SIZE+28); }
                    if(map[y][x]===4){ ctx.fillStyle="#0f0"; ctx.font="20px Arial"; ctx.fillText("Z", x*TILE_SIZE+14, y*TILE_SIZE+28); }
                }
            }
            ctx.fillStyle="#00d2ff"; ctx.font="24px Arial"; ctx.fillText("@", player.x*TILE_SIZE+10, player.y*TILE_SIZE+28);
            ctx.fillStyle="white"; ctx.font="14px Arial"; ctx.fillText("Guld: " + player.gold + " 💰", 15, 25);
        }
        setInterval(draw, 50);
    </script>
    """
    components.html(dungeon_html, height=430)

else:
    st.info("🤖 AI-Fabriken är redo. Skriv vilken spelidé du vill starta nedan!")

st.write("---")

# --- 3. INPUT RADER ---
st.write("### 📸 Visuell insamling:")
bild_instruktion = st.text_input("Beskriv din scanning här (valfritt):")

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

chatt_spår, knapp_spår = st.columns(2)
with chatt_spår:
    input_text = st.text_input("Skriv din spelidé här:", key="user_input_field")
with knapp_spår:
    st.write(" ")
    generera_klick = st.button("🤖 Generera Spel", use_container_width=True)

if generera_klick and input_text:
    st.session_state.messages.append({"role": "user", "content": input_text})
    text_analys = input_text.lower()
    
    # Här väljer den rätt spel baserat på din text helt lokalt!
    if "pussel" in text_analys or "labyrint" in text_analys or "steg" in text_analys:
        st.session_state.valt_spel = "pussel"
        svar = "🧩 *Turbaserat Pusselspel laddat!* Monstret (M) rör sig 2 steg när du tar 1. Styr överst på skärmen!"
    elif "dungeon" in text_analys or "crawler" in text_analys or "skat" in text_analys or "zombie" in text_analys:
        st.session_state.valt_spel = "dungeon"
        svar = "⚔️ *RPG Dungeon Crawler laddat!* Grottan och guldjakt aktiverad överst på skärmen."
    else:
        svar = "Hittade inte speltypen. Skriv ordet 'pussel' för pussel-labyrinten eller 'dungeon' för RPG-grottan!"

    st.session_state.messages.append({"role": "assistant", "content": svar})
    st.rerun()
