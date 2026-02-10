import streamlit as st
from google import genai
from google.genai import types

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Toni Fútbol Club", page_icon="⚽")
st.title("⚽ Toni Fútbol Chatbot")
st.markdown("¡Ahora con conexión a Google para resultados en vivo!")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Gemini API Key:", type="password")
    st.info("Consíguela en [Google AI Studio](https://aistudio.google.com/)")

# --- LÓGICA DEL CHAT ---
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("¿Cuándo juega el Madrid el próximo partido?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    # CONFIGURACIÓN CLAVE: Activamos Google Search
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction="Eres Toni, un experto en fútbol. Usa Google Search para dar respuestas actualizadas sobre calendarios y resultados.",
                            tools=[types.Tool(google_search=types.GoogleSearch())] # <--- HERRAMIENTA DE BÚSQUEDA
                        )
                    )
                    
                    respuesta_texto = response.text
                    st.markdown(respuesta_texto)
                    
                    # Guardar respuesta
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                
                except Exception as e:
                    st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.warning("👈 Pon tu API Key en el lateral para empezar.")
