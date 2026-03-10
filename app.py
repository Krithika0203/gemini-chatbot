import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
st.set_page_config(
    page_title="Gemini Pro Nexus",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR BEAUTIFICATION ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    h1 {
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    # Change this line in the Sidebar section:
    model_name = st.selectbox("Model Engine", ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"])
    temp = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)
    
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- INITIALIZE GEMINI ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# --- CHAT LOGIC ---
st.title("Gemini Pro Nexus")
st.caption("Advanced Generative AI Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & Response
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Simple streaming simulation or direct call
            response = model.generate_content(
                prompt, 
                generation_config={"temperature": temp}
            )
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})