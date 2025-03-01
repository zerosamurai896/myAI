
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemini-1.0-pro"

# Function to authenticate user
def authenticate():
    password_input = st.session_state.password
    if password_input == "password":  # Hardcoded password
        st.session_state.authenticated = True
    else:
        st.error("Incorrect password. Please try again.")

# Function to configure the API
def setup_gemini_api():
    try:
        genai.configure(api_key=st.session_state.api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        return False

# Function to generate response
def generate_response(prompt):
    try:
        model = genai.GenerativeModel(st.session_state.selected_model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to reset chat
def reset_chat():
    st.session_state.messages = []
    st.success("Chat has been reset!")

# Login page
if not st.session_state.authenticated:
    st.title("🔒 Gemini Chatbot Login")
    
    with st.form("login_form"):
        st.text_input("Password", type="password", key="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            authenticate()
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This is a password-protected chatbot powered by Google Gemini. Enter the password to access.")

# Main chat interface
else:
    st.title("🤖 Gemini AI Chatbot")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        # API Key input
        api_key = st.text_input("Enter your Google Gemini API Key", type="password", key="api_key")
        
        # Model selection
        st.subheader("Select Model")
        model_options = {
            "gemini-1.0-pro": "Gemini 1.0 Pro",
            "gemini-1.0-pro-vision": "Gemini 1.0 Pro Vision",
            "gemini-1.5-pro": "Gemini 1.5 Pro",
            "gemini-1.5-flash": "Gemini 1.5 Flash"
        }
        selected_model = st.selectbox(
            "Choose a model",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            key="selected_model"
        )
        
        # Reset button
        st.button("Reset Chat", on_click=reset_chat, type="primary")
        
        # Logout button
        if st.button("Logout", type="secondary"):
            st.session_state.authenticated = False
            st.experimental_rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not api_key:
            st.error("Please enter your Google Gemini API key in the sidebar.")
        else:
            # Configure API
            if setup_gemini_api():
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Display user message
                with st.chat_message("user"):
                    st.write(prompt)
                
                # Generate and display assistant response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = generate_response(prompt)
                        st.write(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
