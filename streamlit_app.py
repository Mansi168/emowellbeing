from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import json
from streamlit_lottie import st_lottie
import google.generativeai as genai

# Configure the Google API Key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Page title and configuration
st.set_page_config(page_title='Emotional Well Being ChatBot', page_icon='😁')
st.title('Emotional Well Being ChatBot')

# Load and display animation
with open('src/customer-service.json', encoding='utf-8') as anim_source:
    animation_data = json.load(anim_source)
    st_lottie(animation_data, speed=1, loop=True, quality='high', height=350, key="high")

# Styling
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }

    .stButton button:hover {
        background-color: white; 
        color: black; 
        border: 2px solid #4CAF50;
    }

    .response-container {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .header-title {
        font-family: 'Arial Black', sans-serif;
        color: #333;
    }

    .instruction-text {
        font-style: italic;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True
)

# Instruction
st.markdown("<p class='instruction-text'>Ask any question related to your emotional well-being and get an intelligent response.</p>", unsafe_allow_html=True)

# Input and button
input = st.text_input("How are you feeling today?", key="input")

submit = st.button("Ask the question")

# If ask button is clicked
if submit:
    with st.spinner("Thinking..."):
        response = get_gemini_response(input)
        if response:
            st.subheader("The Response is")
            st.markdown("<div class='response-container'>", unsafe_allow_html=True)
            for chunk in response:
                if hasattr(chunk, 'text'):
                    st.write(chunk.text)
                    st.markdown("<hr>", unsafe_allow_html=True)
                else:
                    st.error("The response does not contain valid text.")
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='instruction-text'>Thank you for using our Emotional Well Being ChatBot. Stay happy and healthy!</p>", unsafe_allow_html=True)
