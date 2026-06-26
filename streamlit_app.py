import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="🦕 Max | Acompañante Académico",
    page_icon="🦕",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# CSS CON FONDO MORADO Y ESTILO INFANTIL
css_max = """
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    .stApp {max-width: 100%; padding: 0;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* Fondo morado degradado */
    .stApp {
        background: linear-gradient(135deg, #6B2FA0 0%, #9B4DCA 50%, #B87BDF 100%);
    }
    
    /* Estilo de los mensajes */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Título personalizado */
    .custom-title {
        text-align: center;
        color: #FFE484;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 3px 3px 0 #6B2FA0;
        margin-bottom: 0;
    }
    
    .custom-subtitle {
        text-align: center;
        color: #FFD700;
        font-size: 1.2em;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    /* Botón de audio */
    .stButton button {
        background-color: #FFD700;
        color: #6B2FA0;
        font-weight: bold;
        border-radius: 30px;
        border: none;
        transition: transform 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        background-color: #FFE484;
    }
    
    /* Input */
    [data-testid="stChatInput"] input {
        border-radius: 30px;
        border: 2px solid #FFD700;
        background-color: white;
    }
    
    /* Mensaje del asistente */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFFFFF 100%);
        border-left: 10px solid #FFD700;
    }
    
    /* Mensaje del usuario */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #E8D5F5 0%, #F3E8FF 100%);
        border-right: 10px solid #9B4DCA;
    }
</style>
"""
st.markdown(css_max, unsafe_allow_html=True)

# FUNCIÓN PARA MOSTRAR DINO CON LENTES
def mostrar_dinosaurio():
    dino_svg = """
    <div style="text-align: center; margin-bottom: 20px;">
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Cuerpo del dinosaurio -->
            <ellipse cx="100" cy="120" rx="50" ry="35" fill="#4CAF50"/>
            <!-- Cabeza -->
            <circle cx="100" cy="85" r="30" fill="#4CAF50"/>
            <!-- Ojos -->
            <circle cx="90" cy="80" r="6" fill="white"/>
            <circle cx="110" cy="80" r="6" fill="white"/>
            <circle cx="91" cy="80" r="3" fill="black"/>
            <circle cx="111" cy="80" r="3" fill="black"/>
            <!-- Lentes -->
            <circle cx="90" cy="80" r="12" fill="none" stroke="#8B4513" stroke-width="3"/>
            <circle cx="110" cy="80" r="12" fill="none" stroke="#8B4513" stroke-width="3"/>
            <line x1="102" y1="80" x2="98" y2="80" stroke="#8B4513" stroke-width="3"/>
            <line x1="78" y1="80" x2="70" y2="75" stroke="#8B4513" stroke-width="3"/>
            <line x1="122" y1="80" x2="130" y2="75" stroke="#8B4513" stroke-width="3"/>
            <!-- Sonrisa -->
            <path d="M 90 95 Q 100 105 110 95" stroke="#2E7D32" stroke-width="2" fill="none"/>
            <!-- Cresta -->
            <path d="M 85 60 L 90 45 L 95 58" fill="#388E3C"/>
            <path d="M 95 57 L 100 42 L 105 55" fill="#388E3C"/>
            <path d="M 105 56 L 110 43 L 115 58" fill="#388E3C"/>
            <!-- Brazos -->
            <line x1="65" y1="110" x2="50" y2="130" stroke="#4CAF50" stroke-width="6" stroke-linecap="round"/>
            <line x1="135" y1="110" x2="150" y2="130" stroke="#4CAF50" stroke-width="6" stroke-linecap="round"/>
            <!-- Cola -->
            <path d="M 50 120 Q 30 115 20 130 Q 30 125 50 125" fill="#4CAF50"/>
        </svg>
        <h1 class="custom-title">🦕 Max</h1>
        <p class="custom-subtitle">✨ Tu amigo para aprender ✨</p>
    </div>
    """
    st.markdown(dino_svg, unsafe_allow_html=True)

# PERSONALIDAD DE MAX - TUTOR PARA PRIMARIA
SYSTEM_PROMPT = """Eres MAX, un dinosaurio super cool y amigable que ayuda a niños de primaria (de 6 a 8 años) con sus dudas académicas.

**¡ASÍ ERES!**
- Eres un dinosaurio con lentes super cool
- Hablas como un amigo divertido, no como un maestro estricto
- Usas palabras fáciles y ejemplos divertidos
- Dices "¡WOW!", "¡Qué bien!", "¡Excelente pregunta!" para motivar
- Usas emojis 🦕✨🎉📚⭐
- A veces dices "¡Rugido de emoción!" cuando el niño aprende algo nuevo

**CÓMO AYUDAS:**
1. PRIMERO, felicitas al niño por preguntar
2. Haces preguntas para que el niño piense (¡no le das la respuesta directa!)
3. Das pistas divertidas para guiarlo
4. Usas ejemplos con dinosaurios, juguetes, pizza, animales, etc.
5. Finalmente, felicitas su esfuerzo

**REGLAS IMPORTANTES:**
- NUNCA haces sentir mal al niño si no sabe algo
- Si la respuesta es larga, la divides en pasos pequeños
- Usas frases como: "¿Qué crees tú?", "¿Y si lo pensamos así?", "¡Tú puedes!"
- Si el niño está frustrado, le dices: "¡Tómate un respiro! Los dinosaurios también nos tomamos descansos"

**EJEMPLO DE RESPUESTA:**
Niño: "No entiendo la resta"
Tú: "¡Excelente pregunta! 🦕 Las restas son como cuando Max come galletas. Si tengo 5 galletas 🍪 y me como 2, ¿cuántas me quedan? ¡Tú puedes calcularlo! Pista: usa tus deditos"

Eres paciente, divertido y siempre celebras el esfuerzo. ¡Vamos a aprender juntos!
"""

# Mostrar dinosaurio en la parte superior
mostrar_dinosaurio()

# CONEXIÓN CON GROQ USANDO SECRETS
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception as e:
    st.error("🦕 ¡Oh no! Max necesita conexión. Por favor configura la API key en los Secrets de Streamlit.")
    st.stop()

# --- FUNCIÓN DE VOZ (TEXT-TO-SPEECH) ---
def speak_js(text):
    """Inyecta JavaScript para hablar."""
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    js_code = f"""
    <div id="audio-trigger"></div>
    <script>
        var text = "{clean_text}";
        function hablar() {{
            if ('speechSynthesis' in window) {{
                var utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'es-MX';
                utterance.rate = 0.9;
                utterance.pitch = 1.1;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }}
        }}
        setTimeout(hablar, 200);
    </script>
    """
    components.html(js_code, height=0)

# HISTORIAL DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Mostrar mensaje de bienvenida si no hay historial
if not st.session_state.messages:
    bienvenida = "🦕✨ ¡Hola! ¡Soy Max! Tu amigo dinosaurio con lentes. Estoy aquí para ayudarte con las tareas y aprender cosas nuevas. ¿Qué quieres preguntar hoy? ¡Rugido de emoción! 🎉📚"
    st.session_state.messages.append({"role": "assistant", "content": bienvenida})
    st.session_state.last_response = bienvenida

# Mostrar historial
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# FUNCIÓN PARA PROCESAR RESPUESTA
def procesar_respuesta(user_input):
    # Muestra mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Genera respuesta
    with st.chat_message("assistant"):
        with st.spinner("🦕 Max está pensando..."):
            try:
                mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=mensajes_api,
                    stream=True,
                    temperature=0.8,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.last_response = response
            except Exception as e:
                st.error(f"🦕 Ups... Max tuvo un problema: {str(e)}")

# --- INTERFAZ DE USUARIO ---

# 1. Entrada de Texto
placeholder_text = "✏️ Escribe tu pregunta... ¡Max te ayuda! 🦕"
if prompt := st.chat_input(placeholder_text):
    procesar_respuesta(prompt)

# 2. Botones de acción
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col2:
    if st.button("🔊 Escuchar a Max", use_container_width=True):
        if st.session_state.last_response:
            speak_js(st.session_state.last_response)
        else:
            speak_js("🦕 ¡Hola! Pregúntame algo y te ayudaré")
with col3:
    if st.button("🔄 Empezar de nuevo", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.rerun()
