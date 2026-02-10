import streamlit as st
from google import genai
from google.genai import types
import time # Para el manejo de esperas

st.set_page_config(page_title="Toni AI Art", page_icon="🎨")

# --- ESTILOS ---
st.markdown("<style>.stButton>button { background-color: #4285F4; color: white; }</style>", unsafe_allow_html=True)

st.title("🎨 Toni AI: Generador de Conceptos")

with st.sidebar:
    st.header("🔑 Conexión")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.caption("Si ves un error 429, Toni reintentará automáticamente.")

if api_key:
    client = genai.Client(api_key=api_key)

    col1, col2, col3 = st.columns(3)
    with col1:
        w1, w2 = st.text_input("P1", "Nieve"), st.text_input("P2", "Neon")
    with col2:
        w3, w4 = st.text_input("P3", "Silencio"), st.text_input("P4", "Robot")
    with col3:
        w5 = st.text_input("P5", "Azul")
        style = st.selectbox("Estilo", ["Cyberpunk", "Minimalista", "Épico"])

    if st.button("🚀 Generar con Toni"):
        prompt_final = f"Vision of {w1}, {w2}, {w3}, {w4}, {w5} in {style} style."
        
        # --- LÓGICA DE REINTENTO (RETRY LOGIC) ---
        max_retries = 3
        retry_delay = 5 # segundos entre intentos
        success = False

        with st.spinner("Toni está procesando..."):
            for i in range(max_retries):
                try:
                    # Intento de generación (Imagen o Texto)
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", # Usamos este para asegurar rapidez
                        contents=f"Describe una obra de arte basada en: {prompt_final} y haz un dibujo ASCII."
                    )
                    st.subheader("🖼️ Visión Artística de Toni")
                    st.markdown(f"> {response.text}")
                    st.balloons()
                    success = True
                    break # Salimos del bucle si funciona

                except Exception as e:
                    if "429" in str(e):
                        st.warning(f"⚠️ Servidores ocupados. Reintento {i+1}/{max_retries} en {retry_delay}s...")
                        time.sleep(retry_delay)
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if not success:
                st.error("❌ Google está muy saturado ahora mismo. Prueba de nuevo en un minuto.")

else:
    st.info("Introduce tu API Key para despertar a Toni.")
