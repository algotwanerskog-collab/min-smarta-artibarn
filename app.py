import streamlit as st
import streamlit.components.v1 as components
import time

# 1. DESIGN OCH CONFIG
st.set_page_config(page_title="Aleos Avancerade Spelstudio 3.0", page_icon="⚔️", layout="centered")
st.title("🕹️ Aleos Avancerade Spelstudio")
st.write("Genererar avancerade spelsystem med pixel-grafik, vägg-kollisioner, dörrhål och HP-strider!")

# Initiera chattminne och fastlåst spelstatus
if "messages" not in st.session_state:
    st.session_state.messages = []
if "valt_spel" not in st.session_state:
    st.session_state.valt_spel = None

# DEN STORA HUVUDÅTERSTÄLLAREN
if st.button("🔴 🆕 Nollställ allt & starta ett helt nytt spel", use_container_width=True):
    st.session_state.messages = []
    st.session_state.valt_spel = None
    st.success("Spelstudion har nollställts!")
    time.sleep(0.4)
    st.rerun()

st.write("---")

# --- 2. DEN INTERAKTIVA SPELMOTORN MED EXAKT DINA REGLER ---
if st.session_state.valt_spel == "dungeon":
    st.subheader("👾 Aktiverat RPG: Pixel Dungeon Level-Crawler")
    st.caption("Styr med W,A,S,D eller PILARNA. Du har 5 HP, Zombies har 2 HP. Hitta hålet i väggen (🚪) för att klara leveln!")
    
    pixel_rpg_html = """
    <div style="text-align: center;">
        <canvas id="rpgCanvas" width="400" height="400" style="background: #0d0d0d; border: 3px solid #ff5500; image-rendering: pixelated;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById("rpgCanvas");
        const ctx = canvas.getContext("2d");
        const TILE_SIZE = 40;
        const GRID_SIZE = 10;

        let player = { x: 1, y: 1, gold: 0, hp: 5, kills: 0, level: 1 };
        let map = [];

        // Genererar en stor spelplan dynamiskt med rum, väggar och ett hål ut (dörr 6)
        function genereraKarta() {
            for (let y = 0; y < GRID_SIZE; y++) {
                map[y] = [];
                for (let x = 0; x < GRID_SIZE; x++) {
                    if (x === 0 || x === GRID_SIZE - 1 || y === 0 || y === GRID_SIZE - 1) {
                        map[y][x] = 1; // Ytterväggar
                    } else if (y === 5 && x !== 5) {
                        map[y][x] = 1; // Skiljevägg mellan rum
                    } else {
                        map[y][x] = 0; // Golv
                    }
                }
            }
            // Placera ut dörrhålet i väggen längst ner till nästa level!
            map[8][9] = 6; 
            
            // Placera ut kistor (3) och Zombies med HP (kod 4 = Zombie)
            map[2][7] = 3; map[7][2] = 3;
            map[3][4] = 4; map[6][7] = 4;
            map[7][8] = 5; // Slutboss 👹
        }

        // Håll koll på fiendernas unika HP (Zombies har 2 HP, Boss har mer)
        let zombieHP = {"3_4": 2, "6_7": 2};
        let bossHP = 5;

        genereraKarta();

        window.addEventListener("keydown", e => {
            if (player.hp <= 0) return;
            
            let nextX = player.x;
            let nextY = player.y;

            if (e.key === "ArrowLeft" || e.key === "a") nextX--;
            if (e.key === "ArrowRight" || e.key === "d") nextX++;
            if (e.key === "ArrowUp" || e.key === "w") nextY--;
            if (e.key === "ArrowDown" || e.key === "s") nextY++;

            // KOLLISION & SIKTLINJE: Stoppar rörelse genom solida väggar
            if (map[nextY] && map[nextY][nextX] !== undefined && map[nextY][nextX] !== 1) {
                let cell = map[nextY][nextX];
                
                // MÖTE MED ZOMBIE (2 HP)
                if (cell === 4) {
                    let key = nextX + "_" + nextY;
                    zombieHP[key]--;
                    player.hp--; // Spelaren tappar HP i striden
                    
                    if (zombieHP[key] <= 0) {
                        player.kills++;
                        player.gold += Math.floor(Math.random() * 20) + 1; // 1-20 Guld per monster!
                        map[nextY][nextX] = 0;
                    }
                    return;
                }
                // MÖTE MED BOSS 👹
                else if (cell === 5) {
                    bossHP--;
                    player.hp -= 2;
                    if (bossHP <= 0) {
                        player.gold += 50;
                        player.kills += 5;
                        map[nextY][nextX] = 0;
                    }
                    return;
                }
                // PLOCKA UPP KISTA 🎁
                else if (cell === 3) {
                    player.gold += 15;
                    map[nextY][nextX] = 0;
                }
                // HÅL I VÄGGEN / NÄSTA LEVEL 🚪
                else if (cell === 6) {
                    player.level++;
                    player.hp = 5; // Återställ HP vid ny bana
                    genereraKarta();
                    player.x = 1; player.y = 1;
                    return;
                }

                player.x = nextX;
                player.y = nextY;
            }
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (player.hp <= 0) {
                ctx.fillStyle = "red"; ctx.font = "bold 30px Arial";
                ctx.fillText("GAME OVER 💀", 100, 200);
                return;
            }

            for (let y = 0; y < GRID_SIZE; y++) {
                for (let x = 0; x < GRID_SIZE; x++) {
                    let tile = map[y][x];
                    let dist = Math.sqrt(Math.pow(x - player.x, 2) + Math.pow(y - player.y, 2));

                    // FOG OF WAR: Man ser inte genom väggar längre än 3 rutor bort
                    if (dist > 3) {
                        ctx.fillStyle = "#000000"; ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
                        continue;
                    }

                    if (tile === 1) {
                        ctx.fillStyle = "#3a3a3a"; // Grå pixelvägg
                        ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1);
                    } else {
                        ctx.fillStyle = "#1c120c"; // Mörkt grottgolv
                        ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
                    }

                    // Föremål
                    if (tile === 3) {
                        ctx.fillStyle = "#ffaa00"; ctx.font = "20px Arial"; ctx.fillText("🎁", x * TILE_SIZE + 10, y * TILE_SIZE + 28);
                    } else if (tile === 4) {
                        ctx.fillStyle = "#00ff00"; ctx.font = "bold 20px Courier"; ctx.fillText("Z", x * TILE_SIZE + 14, y * TILE_SIZE + 28);
                    } else if (tile === 5) {
                        ctx.fillStyle = "#ff0000"; ctx.font = "22px Arial"; ctx.fillText("👹", x * TILE_SIZE + 8, y * TILE_SIZE + 28);
                    } else if (tile === 6) {
                        ctx.fillStyle = "#00ffcc"; ctx.font = "22px Arial"; ctx.fillText("🚪", x * TILE_SIZE + 8, y * TILE_SIZE + 28);
                    }
                }
            }

            // Rita spelare och HP-text ovanför huvudet exakt som du bad om!
            ctx.fillStyle = "#00d2ff"; ctx.font = "bold 24px Arial";
            ctx.fillText("@", player.x * TILE_SIZE + 10, player.y * TILE_SIZE + 28);
            
            ctx.fillStyle = "#ff5555"; ctx.font = "bold 11px Arial";
            ctx.fillText(player.hp + " HP", player.x * TILE_SIZE + 6, player.y * TILE_SIZE + 8);

            // Övre UI-panelen
            ctx.fillStyle = "white"; ctx.font = "14px Arial";
            ctx.fillText("Level: " + player.level, 15, 25);
            ctx.fillText("HP: " + player.hp + "/5 ❤️", 90, 25);
            ctx.fillText("Guld: " + player.gold + " 💰", 180, 25);
        }

        setInterval(draw, 50);
    </script>
    """
    components.html(pixel_rpg_html, height=430)
else:
    st.info("🤖 AI-Fabriken är redo. Skriv ordet 'dungeon' i chattrutan nedan och klicka på knappen för att starta!")

st.write("---")

# --- 3. KONTROLLER OCH CHATT ---
st.write("### 📸 Visuell insamling och analys:")
bild_instruktion = st.text_input("Beskriv din bild-scanning här:")

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

chatt_spår, knapp_spår = st.columns(2)
with chatt_spår:
    input_text = st.text_input("Prata med AI:n eller begär uppdateringar:", key="user_input_field")
with knapp_spår:
    st.write(" ")
    generera_klick = st.button("🤖 Generera Spel", use_container_width=True)

if generera_klick and input_text:
    final_prompt = input_text
    if bild_instruktion: final_prompt = f"[Visuell scanning: {bild_instruktion}] " + final_prompt
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    
    text_analys = input_text.lower()
    if "dungeon" in text_analys or "crawler" in text_analys or "skat" in text_analys or "zombie" in text_analys:
        st.session_state.valt_spel = "dungeon"
        svar = "⚔️ *Det avancerade RPG-spelet är laddat!* Spelplanen är jättestor, dina HP syns över @, Zombies tar 2 smällar och letar efter dörrhålet (🚪) i väggen för att klättra till Level 2!"
    else:
        svar = "Registrerat! Skriv ordet 'dungeon' för att ladda in pixel-världen överst."
    
    st.session_state.messages.append({"role": "assistant", "content": svar})
    st.rerun()
