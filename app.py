import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Chemita | Amigo Joséfino",
    page_icon="chemita.png",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# CSS CON FONDO AZUL MARINO Y MARCO VERDE
css_chemita = """
<style>
    /* Ocultar elementos de Streamlit y configurar layout */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    .stApp {max-width: 100%; padding: 0; background-color: #001F3F !important;} /* Azul Marino */
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}

    /* Green Frame around the main content container and everything inside */
    .stApp > div {
        border: 10px solid #2ECC71 !important; /* Green Frame */
        border-radius: 15px;
        overflow: hidden; /* Prevent content bleeding */
        box-sizing: border-box; /* Include border in width */
    }

    /* Main container padding inside the frame */
    [data-testid="stBlock"] {
        padding: 20px;
    }

    /* Estilo de los mensajes - Fondo amarillo tenue */
    [data-testid="stChatMessage"] {
        background-color: #FFFDE0 !important; /* Pale Yellow / Amarillo Tenue */
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        color: #333 !important; /* Text color for contrast */
    }

    /* Re-style chat input for navy theme */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
    }
    [data-testid="stChatInput"] > div {
        border-radius: 30px;
        border: 2px solid #2ECC71 !important; /* Green border for input */
        background-color: white !important;
        padding-right: 15px !important;
    }
    [data-testid="stChatInput"] input {
        color: #333 !important;
    }
    [data-testid="stChatInputSubmit"] {
        color: #2ECC71 !important;
    }

    /* Título personalizado */
    .custom-title-chemita {
        text-align: center;
        color: #FFE484; /* Yellow title text */
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0;
    }
    .custom-subtitle-chemita {
        text-align: center;
        color: #FFE484;
        font-size: 1.2em;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Botones estilo Josefin */
    .stButton button {
        background-color: #2ECC71 !important; /* Green button */
        color: white !important;
        font-weight: bold;
        border-radius: 30px;
        border: none;
        transition: transform 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.05);
        background-color: #27AE60 !important; /* Slightly darker green */
    }

    /* Assistant vs. User Border styles, keeping asymmetry but using green/navy */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        border-left: 10px solid #2ECC71; /* Green border for Chemita */
    }
    [data-testid="stChatMessage"][data-testid*="user"] {
        border-right: 10px solid #004080; /* Brighter navy border for user */
    }
</style>
"""
st.markdown(css_chemita, unsafe_allow_html=True)

# FUNCIÓN PARA MOSTRAR IMAGEN Y TÍTULO DE CHEMITA
def mostrar_titulo_chemita():
    # Centered layout using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("chemita.png"):
            st.image("chemita.png", width=200) # Muestra la imagen si existe y arregla el aviso de Streamlit
        else:
            st.warning("🖼️ Falta subir el archivo 'chemita.png' a GitHub")
    
    # Title and subtitle HTML
    st.markdown('<h1 class="custom-title-chemita">Chemita</h1>', unsafe_allow_html=True)
    st.markdown('<p class="custom-subtitle-chemita">✨ Tu amigo siempre útil y empático ✨</p>', unsafe_allow_html=True)

# PERSONALIDAD DE CHEMITA - TUTOR INFANTIL JOSEFINO
SYSTEM_PROMPT = """Eres CHEMITA, un amigo virtual empático, saludable y lleno de energía creado especialmente para niños.

**TU PERSONALIDAD Y VALORES (JOSEFINOS):**
- Tu lema de vida es: "¡Adelante, siempre adelante!"
- Tu misión diaria es: "¡Hacer siempre y en todo lo mejor!"
- Sigues las enseñanzas de San José, por lo que eres trabajador, amable y noble.
- Eres una persona muy activa y buscas "estar siempre útilmente ocupada" de forma positiva.

**TUS INTERESES:**
- ¡Te encanta el deporte! (Fútbol, natación, correr, etc.) y siempre animas a los niños a moverse.
- ¡Te apasiona el arte! (Dibujo, música, teatro) y valoras la creatividad.
- Estás al día con los programas y series de moda saludables para niños (menciónalos de forma general y empática, ej: "¡Esa serie es increíble!").

**CÓMO INTERACTÚAS:**
1. **Empatía ante todo:** Comprendes profundamente los sentimientos de los niños. Usas frases como: "Entiendo que te sientas así", "No te preocupes, juntos lo resolvemos".
2. **Motivación Josefinos:** Usas tu lema: "¡Tú puedes hacerlo! ¡Recuerda hacer siempre lo mejor!" y "¡Adelante siempre adelante!".
3. **Lenguaje amigable:** Hablas de forma clara, directa y divertida para niños. Usas emojis variados (🏃‍♂️⚽🎨📺✨😊).
4. **Guía Activa:** No das respuestas directas. Haces preguntas como: "¿Y si lo intentamos de esta manera?", "¿Qué crees que pasaría si...?".
5. **Enfoque Saludable:** Relacionas tus respuestas con hábitos saludables (hacer ejercicio, comer bien, descansar).

**REGLAS IMPORTANTES:**
- NUNCA desmoralizas a un niño.
- Mantienes un tono positivo y constructivo.
- Promueves el trabajo duro y la perseverancia (hacer lo mejor).
- Conviertes los "errores" en oportunidades de aprendizaje para "adelante siempre adelante".
"""

# Mostrar título en la parte superior
mostrar_titulo_chemita()

# CONEXIÓN CON GROQ USANDO SECRETS
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception as e:
    st.error("✨ ¡Oh no! Chemita necesita su 'llave' de conexión. Por favor configura la API key en los Secrets de Streamlit.")
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
        hablar();
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
    bienvenida = "✨ ¡Hola! ¡Soy Chemita! Tu amigo siempre útil, empático y saludable. ¡Adelante siempre adelante! ¿Qué quieres preguntar hoy? 😊⚽🎨"
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
        with st.spinner("✨ Chemita está pensando en lo mejor..."):
            try:
                mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=mensajes_api,
                    stream=True,
                    temperature=0.7, # Adjusted slightly lower for a healthy, empathetic tone
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.last_response = response
            except Exception as e:
                st.error(f"✨ Ups... Chemita tuvo un problema: {str(e)}")

# --- INTERFAZ DE USUARIO ---

# 1. Entrada de Texto
placeholder_text = "✏️ Escribe tu pregunta... ¡Adelante, Chemita te ayuda! 😊🏃‍♂️"
if prompt := st.chat_input(placeholder_text):
    procesar_respuesta(prompt)

# 2. Botones de acción
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col2:
    if st.button("🔊 Escuchar a Chemita", use_container_width=True):
        if st.session_state.last_response:
            speak_js(st.session_state.last_response)
        else:
            speak_js("✨ ¡Hola! Pregúntame algo y te ayudaré")
with col3:
    if st.button("🔄 Empezar de nuevo", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.rerun()
