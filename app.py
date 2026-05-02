import os
import streamlit as st
import base64
from openai import OpenAI
import openai
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title='Tablero Inteligente 💖', layout='wide')

# 🎀 GIRLY STYLE
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Fondo */
.stApp {
    background: linear-gradient(135deg, #fff0f5, #ffe4ec);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 2px solid #fbcfe8;
}

/* Títulos */
h1 {
    color: #be185d !important;
    font-weight: 700 !important;
}
h2, h3 {
    color: #9d174d !important;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #f472b6, #ec4899) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    transition: 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ec4899, #db2777) !important;
    box-shadow: 0 4px 14px rgba(236,72,153,0.4);
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #f9a8d4 !important;
}

/* Slider */
[data-baseweb="slider"] {
    color: #ec4899 !important;
}

/* Canvas card */
.canvas-card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #fbcfe8;
    box-shadow: 0 6px 18px rgba(236,72,153,0.15);
    margin-bottom: 20px;
}

/* Texto */
p, label {
    color: #6b7280 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# FUNCIONES
# ─────────────────────────────
Expert=" "
profile_imgenh=" "

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        return None

# ─────────────────────────────
# UI
# ─────────────────────────────
st.title('🎀 Tablero Inteligente')
st.subheader('Dibuja tu idea y deja que la IA la interprete ✨')

with st.sidebar:
    st.subheader("💖 Acerca de")
    st.markdown("""
    Esta app permite:
    
    🎨 Dibujar bocetos  
    🤖 Analizarlos con IA  
    ✨ Obtener descripciones automáticas  
    
    ¡Explora tu creatividad!
    """)

# Canvas settings
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Grosor del trazo ✍️', 1, 30, 5)

stroke_color = "#000000"
bg_color = '#FFFFFF'

st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

canvas_result = st_canvas(
    fill_color="rgba(255, 192, 203, 0.3)",  # rosita 💕
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

st.markdown('</div>', unsafe_allow_html=True)

# API KEY
ke = st.text_input('🔑 Ingresa tu API Key')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=api_key)

# Botón
analyze_button = st.button("✨ Analizar dibujo")

# ─────────────────────────────
# LÓGICA
# ─────────────────────────────
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("💭 Analizando tu dibujo..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")

        prompt_text = "Describe en español brevemente la imagen"

        try:
            full_response = ""
            message_placeholder = st.empty()

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )

            if response.choices[0].message.content:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(f"💖 {full_response}")

            if Expert == profile_imgenh:
                st.session_state.mi_respuesta = response.choices[0].message.content

        except Exception as e:
            st.error(f"Error: {e}")

else:
    if not api_key:
        st.warning("⚠️ Ingresa tu API key para continuar 💖")
