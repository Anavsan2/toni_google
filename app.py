import streamlit as st
from google import genai
from google.genai import types

# --- Configuración de la Página ---
st.set_page_config(page_title="Toni Image Generator", page_icon="💡")
st.title("💡 Toni Image Generator")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Gemini API Key:", type="password")

# --- Interfaz Principal ---
if api_key:
    try:
        # CORRECCIÓN: En la nueva SDK, el cliente se crea así
        client = genai.Client(api_key=api_key)

        st.subheader("Introduce 5 palabras clave:")
        col1, col2, col3 = st.columns(3)
        with col1:
            word1 = st.text_input("Palabra 1", value="Astronauta")
            word4 = st.text_input("Palabra 4", value="Galaxia")
        with col2:
            word2 = st.text_input("Palabra 2", value="Gato")
            word5 = st.text_input("Palabra 5", value="Neon")
        with col3:
            word3 = st.text_input("Palabra 3", value="Pizza")

        style = st.selectbox("Estilo:", ["Cyberpunk", "Realista", "Animé", "Óleo"])

        if st.button("Generar con Toni", use_container_width=True, type="primary"):
            prompt_final = f"A high-quality {style} image of {word1}, {word2}, {word3}, {word4}, {word5}"
            
            with st.spinner("Toni está trabajando..."):
                # Llamada usando la nueva sintaxis de la SDK
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=prompt_final,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"]
                    )
                )
                
                # Extraer e hidratar la imagen
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        st.image(part.inline_data.data, caption="¡Obra de Toni!")
                        st.download_button("Descargar", part.inline_data.data, "imagen.png")

    except Exception as e:
        st.error(f"Hubo un error: {e}")
else:
    st.info("Pon tu API Key en el lateral.")
