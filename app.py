import streamlit as st
from google import genai
from google.genai import types

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Toni Image Gen", page_icon="🎨", layout="centered")

st.title("🎨 Toni Image Generator")
st.markdown("Genera arte digital a partir de 5 conceptos usando **Imagen 3**.")

# --- 2. SIDEBAR PARA CREDENCIALES ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Gemini API Key:", type="password")
    st.info("Consíguela en [Google AI Studio](https://aistudio.google.com/)")
    st.divider()
    st.caption("Versión: Toni v2.0 - Google Cloud Connected")

# --- 3. INTERFAZ DE USUARIO ---
if api_key:
    try:
        # Inicialización del cliente con la nueva SDK
        client = genai.Client(api_key=api_key)

        st.subheader("Toni necesita 5 palabras clave:")
        
        # Grid de 5 inputs
        c1, c2 = st.columns(2)
        with c1:
            w1 = st.text_input("Palabra 1", placeholder="Ej: Gato")
            w2 = st.text_input("Palabra 2", placeholder="Ej: Neón")
            w3 = st.text_input("Palabra 3", placeholder="Ej: Cyberpunk")
        with c2:
            w4 = st.text_input("Palabra 4", placeholder="Ej: Espacio")
            w5 = st.text_input("Palabra 5", placeholder="Ej: Realista")

        style = st.selectbox("Elige un acabado artístico:", 
                           ["Digital Art", "Oil Painting", "Cinematic Photo", "Sketch", "3D Render"])

        if st.button("🚀 ¡Generar Imagen con Toni!", use_container_width=True, type="primary"):
            if all([w1, w2, w3, w4, w5]):
                # Unimos las palabras en un prompt potente
                user_prompt = f"{w1}, {w2}, {w3}, {w4}, {w5}. Style: {style}. High resolution, 4k, masterpiece."
                
                with st.spinner("Toni está dibujando... (esto tarda unos 10 segundos)"):
                    try:
                        # LLAMADA AL MODELO IMAGEN 3
                        response = client.models.generate_content(
                            model="imagen-3.0-generate-001", 
                            contents=user_prompt,
                            config=types.GenerateContentConfig(
                                response_modalities=["IMAGE"]
                            )
                        )
                        
                        # Extraer la imagen de la respuesta
                        image_found = False
                        for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                img_data = part.inline_data.data
                                st.image(img_data, caption="Generado por Toni", use_container_width=True)
                                
                                # Botón de descarga
                                st.download_button(
                                    label="💾 Descargar Obra",
                                    data=img_data,
                                    file_name="toni_art.png",
                                    mime="image/png",
                                    use_container_width=True
                                )
                                image_found = True
                        
                        if not image_found:
                            st.error("La IA no devolvió una imagen. Puede ser por filtros de seguridad.")

                    except Exception as e:
                        if "400" in str(e):
                            st.error("❌ Error 400: Tu API Key puede no tener acceso a 'Imagen 3' todavía.")
                            st.info("Prueba en AI Studio a habilitar el modelo de generación de imágenes.")
                        else:
                            st.error(f"Error técnico: {e}")
            else:
                st.warning("⚠️ Toni necesita las 5 palabras para trabajar correctamente.")

    except Exception as e:
        st.error(f"Error al conectar con Google: {e}")
else:
    st.warning
