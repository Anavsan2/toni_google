import streamlit as st
from google import genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Toni Fútbol Club", page_icon="⚽")
st.title("⚽ Toni Fútbol Chatbot")
st.markdown("¡Pregúntame lo que quieras sobre ligas, jugadores o historia del fútbol!")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Gemini API Key:", type="password")
    st.info("Consíguela gratis en [Google AI Studio](https://aistudio.google.com/)")

# --- LÓGICA DEL CHAT ---
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # Inicializar el historial del chat si no existe
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mostrar mensajes previos del chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input del usuario
        if prompt := st.chat_input("¿Quién ganó el mundial de 2010?"):
            # Mostrar mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generar respuesta de Toni
            with st.chat_message("assistant"):
                # Instrucción secreta para que siempre hable de fútbol
                full_query = f"Eres Toni, un experto en fútbol. Responde de forma breve y divertida: {prompt}"
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=full_query
                    )
                    respuesta_texto = response.text
                    st.markdown(respuesta_texto)
                    
                    # Guardar respuesta
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                
                except Exception as e:
                    if "429" in str(e):
                        st.error("Saturación: Espera 10 segundos y pregunta de nuevo.")
                    else:
                        st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.warning("👈 Pon tu API Key en el lateral para empezar el partido.")
