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

# CSS MEJORADO: Fondo Azul Marino, Marco Verde y Diseño Responsivo
css_chemita = """
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    .stDeployButton {display: none;}

    /* Fondo y Marco General */
    .stApp {
        max-width: 100%; 
        padding: 0; 
        background-color: #001F3F !important; /* Azul Marino */
    }
    .stApp > div {
        border: 8px solid #2ECC71 !important; /* Marco Verde */
        border-radius: 15px;
        overflow: hidden; 
        box-sizing: border-box; 
    }

    /* Contenedor principal */
    [data-testid="stBlock"] {
        padding: 15px;
    }

    /* --- ESTILO DEL BANNER DE IMAGEN --- */
    div[data-testid="stImageContainer"] {
        margin: 0 0 15px 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stImageContainer"] img {
        width: 100% !important; 
        height: auto !important; 
        max-height: 250px; 
        object-fit: cover !important; 
        border-radius: 10px; 
        border: 3px solid #2ECC71; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* Estilo de los mensajes - Fondo amarillo tenue */
    [data-testid="stChatMessage"] {
        background-color: #FFFDE0 !important; 
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: #333 !important; 
    }

    /* Entrada de Chat */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        padding-bottom: 10px;
    }
    [data-testid="stChatInput"] > div {
        border-radius: 25px;
        border: 2px solid #2ECC71 !important; 
        background-color: white !important;
        padding: 5px 15px !important;
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
        color: #FFE484; 
        font-size: clamp(2em, 6vw, 3.5em); 
        font-weight: bold;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .custom-subtitle-chemita {
        text-align: center;
        color: #FFE484;
        font-size: clamp(0.9em, 3vw, 1.2em); 
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Botones */
    .stButton button {
        background-color: #2ECC71 !important; 
        color: white !important;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        padding: 10px 15px;
        transition: transform 0.2s, background-color 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.03);
        background-color: #27AE60 !important; 
    }
</style>
"""
st.markdown(css_chemita, unsafe_allow_html=True)

# FUNCIÓN PARA MOSTRAR BANNER Y TÍTULO
def mostrar_titulo_chemita():
    if os.path.exists("chemita.png"):
        st.image("chemita.png", use_container_width=True)
    else:
        st.warning("🖼️ Falta subir el archivo 'chemita.png' a GitHub en la misma carpeta que app.py")
    
    st.markdown('<h1 class="custom-title-chemita">Chemita</h1>', unsafe_allow_html=True)
    st.markdown('<p class="custom-subtitle-chemita">✨ Tu amigo siempre útil y empático ✨</p>', unsafe_allow_html=True)

# PERSONALIDAD DE CHEMITA (ACTUALIZADA CON REGLA DE LONGITUD)
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
- **REGLA DE LONGITUD ESTRICTA:** Tus respuestas deben ser muy cortas y fáciles de leer para un niño. NUNCA escribas más de dos párrafos. Ve directo al punto con cariño.
"""

mostrar_titulo_chemita()

# CONEXIÓN CON GROQ USANDO SECRETS
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except KeyError:
    st.error("🚨 Error de configuración: No se encontró la API Key. Revisa tus Secrets en Streamlit Cloud.")
    st.stop()
except Exception as e:
    st.error(f"✨ ¡Oh no! Ocurrió un error de conexión: {e}")
    st.stop()

# --- FUNCIÓN DE VOZ (TEXT-TO-SPEECH) ---
def speak_js(text):
    """Inyecta JavaScript para hablar."""
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    js_code = f"""
    <div id="audio-trigger" style="height:0
