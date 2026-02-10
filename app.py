import streamlit as st
from google import genai
from google.genai import types
import base64

# --- Configuración de la Página ---
st.set_page_config(page_title="Toni Image Generator", page_icon="💡", layout="centered")
st.title("💡 Toni Image Generator")
st.markdown("Crea imágenes a partir de 5 palabras con Gemini 2.0 Flash")

# --- Sidebar para la Configuración ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    st.info("Asegúrate que tu API Key tiene permisos para generación de imágenes.")

# --- Interfaz Principal ---
if api_key:
    # Inicializamos el cliente de Gemini
    genai.configure(api_key=api_key) # Se configura globalmente
    # Puedes especificar el modelo aquí si quieres, aunque generate_content puede tomarlo.
    # model = genai.GenerativeModel("gemini-1.5-flash") # No se usará para imágenes directamente aquí.

    st.subheader("Introduce 5 palabras clave:")

    # Inputs para las 5 palabras clave
    col1, col2, col3 = st.columns(3)
    with col1:
        word1 = st.text_input("Palabra 1", value="ciudad")
        word4 = st.text_input("Palabra 4", value="misteriosa")
    with col2:
        word2 = st.text_input("Palabra 2", value="futurista")
        word5 = st.text_input("Palabra 5", value="luna")
    with col3:
        word3 = st.text_input("Palabra 3", value="coches voladores")

    # Selector de estilo
    st.subheader("Elige un estilo:")
    style = st.radio(
        "Estilo de la imagen:",
        ["Fotorrealista", "Dibujo Animado", "Pintura al Óleo", "Cyberpunk", "Pixel Art", "Fantasia"],
        horizontal=True,
        index=0 # Estilo por defecto
    )

    if st.button("Generar con Toni", use_container_width=True, type="primary"):
        # Unimos las 5 palabras clave para formar la descripción
        keywords_description = f"{word1}, {word2}, {word3}, {word4}, {word5}"
        
        # Creamos el prompt completo para la IA
        full_prompt = f"A high-quality {style} image of {keywords_description}. Professional lighting, detailed."
        
        # Pequeña validación
        if not all([word1, word2, word3, word4, word5]):
            st.warning("Por favor, introduce las 5 palabras clave.")
        else:
            with st.spinner("Toni está pintando tu obra maestra..."):
                try:
                    # Llamada al modelo multimodal para generación de imágenes
                    # Usamos el cliente directamente y especificamos el modelo en la llamada
                    response = genai.GenerativeModel("gemini-2.0-flash").generate_content( # O "gemini-1.5-flash" si prefieres el de texto
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["IMAGE"]
                        )
                    )
                    
                    found_image = False
                    # Acceder a la imagen generada (puede venir en diferentes formatos)
                    if response.candidates:
                        for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                image_bytes = part.inline_data.data
                                st.image(image_bytes, caption=f"Keywords: {keywords_description} - Estilo: {style}", use_container_width=True)
                                
                                # Botón de descarga
                                st.download_button(
                                    label="Descargar Imagen",
                                    data=image_bytes,
                                    file_name=f"toni_gen_{style.lower().replace(' ', '_')}.png",
                                    mime="image/png",
                                    use_container_width=True
                                )
                                found_image = True
                                break # Solo necesitamos una imagen

                    if not found_image:
                        st.warning("Toni no pudo generar la imagen. Revisa las palabras clave o los filtros de seguridad de la IA.")

                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Asegúrate de que tu API Key es correcta y tiene acceso a la generación de imágenes.")
else:
    st.info("Introduce tu API Key en la barra lateral para empezar a generar imágenes con Toni.")

# --- Información Adicional (Footer) ---
st.markdown("---")
st.markdown("Desarrollado con Streamlit y Google Gemini.")
