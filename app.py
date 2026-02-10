import streamlit as st
from google import genai
from google.genai import types

# --- CONFIGURACIÓN ESTÉTICA ---
st.set_page_config(page_title="Toni AI Art", page_icon="🎨", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4285F4; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 Toni AI: Generador de Conceptos")
st.write("Introduce 5 palabras y Toni creará una visión artística para ti.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 Conexión")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.info("Obtén tu clave en [Google AI Studio](https://aistudio.google.com/)")
    st.divider()
    st.caption("Toni v3.0 - Intelligent Fallback Mode")

# --- LÓGICA PRINCIPAL ---
if api_key:
    try:
        client = genai.Client(api_key=api_key)

        # Formulario de palabras clave
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                w1 = st.text_input("Palabra 1", "Bosque")
                w2 = st.text_input("Palabra 2", "Cristal")
            with col2:
                w3 = st.text_input("Palabra 3", "Futuro")
                w4 = st.text_input("Palabra 4", "Luz")
            with col3:
                w5 = st.text_input("Palabra 5", "Noche")
                style = st.selectbox("Estilo", ["Cyberpunk", "Óleo", "Minimalista", "Épico"])

        if st.button("🚀 Generar con Toni"):
            prompt_final = f"Vision of {w1}, {w2}, {w3}, {w4}, {w5} in {style} style."
            
            with st.spinner("Toni está creando..."):
                try:
                    # INTENTO 1: Generar imagen real
                    response = client.models.generate_content(
                        model="imagen-3.0",
                        contents=prompt_final,
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                    )
                    
                    # Si llega aquí, mostramos la imagen
                    img_found = False
                    for part in response.candidates[0].content.parts:
                        if part.inline_data:
                            st.image(part.inline_data.data, caption="Obra generada por Toni", use_container_width=True)
                            st.download_button("Descargar Imagen", part.inline_data.data, "toni_art.png")
                            img_found = True
                    
                    if not img_found: raise Exception("No image in response")

                except Exception as e:
                    # PLAN B: Si la imagen falla, Toni genera Arte Conceptual
                    st.warning("🔄 Modo Imagen no disponible en esta región. Activando 'Toni Artista Conceptual'...")
                    
                    fallback_prompt = f"""
                    Actúa como Toni, un artista conceptual de élite. 
                    Basado en estas 5 palabras: {w1}, {w2}, {w3}, {w4}, {w5} y el estilo {style}:
                    1. Describe la 'Obra Maestra' que pintarías (3 frases intensas).
                    2. Crea una representación visual usando únicamente Emojis y símbolos ASCII.
                    """
                    
                    res = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=fallback_prompt
                    )
                    
                    st.subheader("🖼️ Visión Artística")
                    st.markdown(f"> {res.text}")
                    st.balloons()

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.info("Introduce tu API Key en la izquierda para despertar a Toni.")
