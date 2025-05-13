from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os
import shelve
import time
import pandas as pd
import json
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="🌠 CosmicQuery",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# CosmicQuery - Asking questions to the universe\nEnhanced chatbot interface powered by Groq API"
    }
)

# Custom CSS
st.markdown("""
<style>
    /* Main app styling - Dark theme */
    .stApp {
        background-color: #1a1a1a;
        color: #f0f0f0;
    }
    
    /* Header styling */
    .main-header {
        background-color: #2d2d2d;
        color: #f0f0f0;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat message styling */
    .user-message {
        background-color: #2d3748;
        border-left: 5px solid #63b3ed;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        color: #f0f0f0;
    }
    
    .assistant-message {
        background-color: #2d3748;
        border-left: 5px solid #68d391;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        color: #f0f0f0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #262626;
    }
    
    /* All text in the app */
    body, p, span, label, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3d5a80;
        color: #f0f0f0;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #4d6a90;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }
    
    /* Dropdown styling */
    .stSelectbox label {
        color: #f0f0f0;
        font-weight: bold;
    }
    
    .stSelectbox > div[data-baseweb="select"] > div {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-color: #4d4d4d;
    }
    
    /* Radio button styling */
    .stRadio label {
        color: #f0f0f0;
        font-weight: bold;
    }
    
    /* Chat input styling */
    .stTextArea textarea, div[data-baseweb="input"] > div > input {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-radius: 10px;
        border: 1px solid #4d4d4d;
    }
    
    /* Status indicator */
    .status-indicator {
        height: 12px;
        width: 12px;
        background-color: #68d391;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #262626;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #262626;
        border-radius: 10px;
        padding: 10px;
        color: #f0f0f0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3d5a80;
        color: #f0f0f0;
    }
    
    /* Chat message containers */
    .stChatMessage {
        background-color: #2d2d2d !important;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .stChatMessage.user {
        border-left: 5px solid #63b3ed;
    }
    
    .stChatMessage.assistant {
        border-left: 5px solid #68d391;
    }
    
    /* Widget labels */
    div.stSlider label, div.stNumberInput label {
        color: #f0f0f0 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2d2d2d;
        color: #f0f0f0 !important;
        border-radius: 5px;
    }
    
    .streamlit-expanderContent {
        background-color: #262626;
        color: #f0f0f0;
        border-radius: 0 0 5px 5px;
    }
    
    /* Slider handle */
    .stSlider div[role="slider"] {
        background-color: #3d5a80;
    }
    
    /* Code blocks */
    code {
        background-color: #2d2d2d;
        color: #f0f0f0;
    }
    
    pre {
        background-color: #2d2d2d;
        border-radius: 5px;
        padding: 10px;
    }
    
    /* Input fields */
    input, textarea {
        background-color: #2d2d2d !important;
        color: #f0f0f0 !important;
        border-color: #4d4d4d !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = {}
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = f"Conversation-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
if "groq_model" not in st.session_state:
    st.session_state.groq_model = "llama-3.3-70b-versatile"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1024
if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9
if "thinking_emoji" not in st.session_state:
    st.session_state.thinking_emoji = "🤔"
if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = ""

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Available models
MODELS = {
    "Llama-3.3-70B": "llama-3.3-70b-versatile",
    "Llama-3.1-70B": "llama-3.1-70b-versatile",
    "Llama-3.1-8B": "llama-3.1-8b-versatile",
    "Mixtral-8x7B": "mixtral-8x7b-32768",
    "Claude-3.5 Sonnet": "claude-3-5-sonnet",
    "Gemma-7B": "gemma-7b"
}

# Custom emoji avatars
AVATARS = {
    "user": ["👤", "👩‍💻", "👨‍💻", "🧑‍💻", "🙋‍♀️", "🙋‍♂️"],
    "assistant": ["🤖", "🧠", "🦾", "🔮", "🧩", "💫"]
}

# Function to load chat history from shelve
def load_chat_history():
    with shelve.open("chat_history_db") as db:
        st.session_state.messages = db.get("messages", [])
        st.session_state.conversation_history = db.get("conversation_history", {})
        st.session_state.current_conversation = db.get("current_conversation", 
                                                      f"Conversation-{datetime.now().strftime('%Y%m%d-%H%M%S')}")

# Function to save chat history to shelve
def save_chat_history():
    with shelve.open("chat_history_db") as db:
        db["messages"] = st.session_state.messages
        db["conversation_history"] = st.session_state.conversation_history
        db["current_conversation"] = st.session_state.current_conversation

# Function to create a new conversation
def new_conversation():
    st.session_state.current_conversation = f"Conversation-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    st.session_state.messages = []
    st.session_state.chat_summary = ""
    save_chat_history()

# Function to switch conversation
def switch_conversation(conversation_id):
    st.session_state.current_conversation = conversation_id
    st.session_state.messages = st.session_state.conversation_history.get(conversation_id, [])
    save_chat_history()

# Function to delete conversation
def delete_conversation(conversation_id):
    if conversation_id in st.session_state.conversation_history:
        del st.session_state.conversation_history[conversation_id]
    if conversation_id == st.session_state.current_conversation:
        new_conversation()
    save_chat_history()

# Function to summarize chat
def summarize_chat():
    if not st.session_state.messages:
        return "No conversation to summarize"
    
    # Create a prompt for summarization
    summarize_prompt = "Please provide a brief summary of the following conversation in 2-3 sentences:\n\n"
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        summarize_prompt += f"{role}: {msg['content']}\n"
    
    try:
        summary_response = client.chat.completions.create(
            model=st.session_state.groq_model,
            messages=[{"role": "user", "content": summarize_prompt}],
            temperature=0.5,
            max_tokens=100,
        )
        summary = summary_response.choices[0].message.content
        st.session_state.chat_summary = summary
        return summary
    except Exception as e:
        return f"Failed to generate summary: {str(e)}"

# Function to handle file export
def export_chat_to_file(file_format):
    if not st.session_state.messages:
        st.warning("No conversation to export")
        return
    
    try:
        if file_format == "JSON":
            # Convert to JSON
            chat_data = {
                "conversation_id": st.session_state.current_conversation,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "messages": st.session_state.messages
            }
            
            # Create a download link
            json_data = json.dumps(chat_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"{st.session_state.current_conversation}.json",
                mime="application/json"
            )
            
        elif file_format == "CSV":
            # Convert to CSV
            rows = []
            for msg in st.session_state.messages:
                rows.append({
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            df = pd.DataFrame(rows)
            csv_data = df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{st.session_state.current_conversation}.csv",
                mime="text/csv"
            )
            
        elif file_format == "Text":
            # Convert to plain text
            text_data = f"Conversation: {st.session_state.current_conversation}\n"
            text_data += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                text_data += f"{role}: {msg['content']}\n\n"
            
            st.download_button(
                label="Download Text",
                data=text_data,
                file_name=f"{st.session_state.current_conversation}.txt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"Error exporting conversation: {str(e)}")

# Function to save user preferences
def save_preferences():
    try:
        with shelve.open("user_preferences") as db:
            db["groq_model"] = st.session_state.groq_model
            db["temperature"] = st.session_state.temperature
            db["max_tokens"] = st.session_state.max_tokens
            db["top_p"] = st.session_state.top_p
            db["user_avatar"] = st.session_state.get("user_avatar", "👤")
            db["assistant_avatar"] = st.session_state.get("assistant_avatar", "🤖")
        st.success("Preferences saved successfully!")
    except Exception as e:
        st.error(f"Error saving preferences: {str(e)}")

# Function to load user preferences
def load_preferences():
    try:
        with shelve.open("user_preferences") as db:
            st.session_state.groq_model = db.get("groq_model", "llama-3.3-70b-versatile")
            st.session_state.temperature = db.get("temperature", 0.7)
            st.session_state.max_tokens = db.get("max_tokens", 1024)
            st.session_state.top_p = db.get("top_p", 0.9)
            st.session_state.user_avatar = db.get("user_avatar", "👤")
            st.session_state.assistant_avatar = db.get("assistant_avatar", "🤖")
    except:
        # Use defaults if preferences can't be loaded
        pass

# Load preferences on startup
if "preferences_loaded" not in st.session_state:
    load_preferences()
    load_chat_history()
    st.session_state.preferences_loaded = True

# Define UI Components
st.markdown("""
<div class="main-header">
    <h1>🌠 CosmicQuery - Dark Mode</h1>
    <p>An enhanced chatbot interface powered by Groq's cutting-edge LLM technology</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌌 CosmicQuery Settings")
    st.markdown("### Conversation Controls")
    
    # Model selection
    selected_model_name = st.selectbox(
        "Select Model",
        options=list(MODELS.keys()),
        index=list(MODELS.values()).index(st.session_state.groq_model) if st.session_state.groq_model in MODELS.values() else 0
    )
    st.session_state.groq_model = MODELS[selected_model_name]
    
    # Conversation management
    st.markdown("### 📝 Conversations")
    
    # List of conversations
    if st.session_state.conversation_history:
        for conv_id in list(st.session_state.conversation_history.keys()):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                if st.button(conv_id, key=f"btn_{conv_id}"):
                    switch_conversation(conv_id)
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}"):
                    delete_conversation(conv_id)
    
    if st.button("➕ New Conversation"):
        new_conversation()
    
    st.markdown("---")
    
    # Advanced settings tab
    with st.expander("⚙️ Advanced Settings"):
        st.markdown("### Model Parameters")
        st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.05)
        st.session_state.max_tokens = st.slider("Max Tokens", min_value=256, max_value=4096, value=st.session_state.max_tokens, step=128)
        st.session_state.top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=st.session_state.top_p, step=0.05)
        
        st.markdown("### Personalization")
        user_avatar = st.selectbox("User Avatar", options=AVATARS["user"], index=AVATARS["user"].index(st.session_state.get("user_avatar", "👤")))
        st.session_state.user_avatar = user_avatar
        
        assistant_avatar = st.selectbox("Assistant Avatar", options=AVATARS["assistant"], index=AVATARS["assistant"].index(st.session_state.get("assistant_avatar", "🤖")))
        st.session_state.assistant_avatar = assistant_avatar
        
        if st.button("Save Preferences"):
            save_preferences()
    
    # Export options
    with st.expander("📤 Export Conversation"):
        file_format = st.radio("Select Format", ["JSON", "CSV", "Text"])
        st.button("Export", on_click=export_chat_to_file, args=(file_format,))
    
    # Delete all conversations
    if st.button("🗑️ Delete All Conversations"):
        st.session_state.conversation_history = {}
        new_conversation()
        save_chat_history()
        st.success("All conversations deleted")

# Main chat area
chat_container = st.container()

# Display chat summary
if st.session_state.messages and not st.session_state.chat_summary:
    with st.expander("📝 Conversation Summary"):
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = summarize_chat()
                st.write(summary)
elif st.session_state.chat_summary:
    with st.expander("📝 Conversation Summary"):
        st.write(st.session_state.chat_summary)
        if st.button("Refresh Summary"):
            with st.spinner("Updating summary..."):
                summary = summarize_chat()
                st.write(summary)

# Chat messages display
with chat_container:
    for i, message in enumerate(st.session_state.messages):
        avatar = st.session_state.user_avatar if message["role"] == "user" else st.session_state.assistant_avatar
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Chat input area
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(user_input)
    
    # Get response from Groq
    with st.chat_message("assistant", avatar=st.session_state.assistant_avatar):
        thinking_emoji_placeholder = st.empty()
        message_placeholder = st.empty()
        
        # Show thinking animation - more subtle for dark mode
        for _ in range(2):
            for emoji in ["💭", "🧠"]:
                thinking_emoji_placeholder.markdown(f"<h3 style='color: #a0aec0;'>{emoji} Processing...</h3>", unsafe_allow_html=True)
                time.sleep(0.3)
        
        # Start generating response
        full_response = ""
        
        # No progress bar in this version as requested
        try:
            for chunk in client.chat.completions.create(
                model=st.session_state.groq_model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=st.session_state.temperature,
                max_tokens=st.session_state.max_tokens,
                top_p=st.session_state.top_p,
                stream=True,
            ):
                content = chunk.choices[0].delta.content or ""
                full_response += content
                
                # Just update the message as we receive chunks
                message_placeholder.markdown(full_response + "▌")
                
            # Clear thinking animation when done
            thinking_emoji_placeholder.empty()
            
            # Display final response
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            message_placeholder.error(f"Error: {str(e)}")
            st.session_state.messages.pop()  # Remove the user message if there was an error
            st.stop()
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Save this conversation to history
    st.session_state.conversation_history[st.session_state.current_conversation] = st.session_state.messages
    
    # Clear summary when new messages are added
    st.session_state.chat_summary = ""
    
    # Save chat history
    save_chat_history()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #a0aec0;">
    <p>Powered by Groq API | Made with ❤️ by Tushar Gautam in Streamlit</p>
    <p>Version 1.0</p>
</div>
""", unsafe_allow_html=True)
