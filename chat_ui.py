  # This is the NEW "Pro UI" code for chat_ui.py (with REAL History)

import streamlit as st
import requests
from datetime import datetime

# 1. Set up the page (full-width)
st.set_page_config(
    page_title="Chat with Zebo",
    page_icon="🤖",
    layout="wide"
)

# 2. --- NEW: Function to load CSS from a file ---
def load_css_from_file(file_path):
    try:
        with open(file_path) as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found. Please create a file named '{file_path}' in the same folder.")

# We run the function to load our new style.css file
load_css_from_file("style.css")
# --- END OF CSS ---


# 3. --- NEW: Chat History Logic ---

# Initialize the full conversation history (a dictionary)
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

# Initialize the ID of the currently active chat
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

# If there are no conversations, create the first one
if not st.session_state.conversations:
    first_chat_id = "chat_" + str(datetime.now().timestamp())
    st.session_state.conversations = {
        first_chat_id: [
            {"role": "assistant", "content": "Hi there! I'm Zebo. Ask me about a GenAI topic."}
        ]
    }
    st.session_state.current_conversation_id = first_chat_id

# --- END OF HISTORY LOGIC ---


# 4. --- NEW: Sidebar (Now Functional) ---
with st.sidebar:
    st.title("Chat History")
    
    # "New Chat" button
    if st.button("New Chat ➕"):
        new_chat_id = "chat_" + str(datetime.now().timestamp())
        st.session_state.conversations[new_chat_id] = [
            {"role": "assistant", "content": "Hi, I'm Zebo! How can I help you today?"}
        ]
        st.session_state.current_conversation_id = new_chat_id
        st.rerun() # Refresh the page to show the new chat

    st.divider()

    # Display buttons for all existing conversations
    # We loop in reverse to show the newest chats first
    for chat_id in reversed(list(st.session_state.conversations.keys())):
        
        # Get the first user message as a title, or use a default
        chat_title = st.session_state.conversations[chat_id][0]['content'][:30] + "..." # Default title
        for msg in st.session_state.conversations[chat_id]:
            if msg["role"] == "user":
                chat_title = msg["content"][:30] + "..." # Truncate for display
                break
        
        # Create a button for each chat
        if st.button(chat_title, key=chat_id):
            st.session_state.current_conversation_id = chat_id
            st.rerun() # Refresh to load the selected chat

    st.divider()
    
    if st.button("Clear All History"):
        st.session_state.conversations = {} # Empty the dictionary
        st.session_state.current_conversation_id = None
        st.rerun()
# --- END OF SIDEBAR ---


# 5. --- Main Page Header ---
st.title("Chat with Zebo")
st.caption("Your personal Generative AI Analyst")
st.divider()
# --- END OF HEADER ---


# 6. --- CHAT INTERFACE ---
# Get the currently active message list
current_messages = st.session_state.conversations.get(st.session_state.current_conversation_id, [])

# We use a container to hold the chat history
chat_container = st.container()
with chat_container:
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. --- BACKEND LOGIC ---
BACKEND_URL = "http://127.0.0.1:8000"

def submit_prompt(prompt_text):
    """A function to handle submitting the prompt to the backend."""
    
    # Get the ID of the *current* chat
    chat_id = st.session_state.current_conversation_id
    
    # Add user message to the *current* chat's history
    st.session_state.conversations[chat_id].append({"role": "user", "content": prompt_text})
    
    # Display user message in the container
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt_text)
    
    # --- "THINKING" SPINNER ---
    with chat_container:
        with st.chat_message("assistant"):
            # This command shows the spinner AND the text
            with st.spinner("Zebo is thinking..."):
                try:
                    # Call the backend
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        # Send ONLY the current chat's history
                        json={"history": st.session_state.conversations[chat_id]} 
                    )
                    response.raise_for_status()
                    bot_response = response.json().get("response", "Sorry, I had trouble thinking of a reply.")
                    
                except requests.exceptions.RequestException as e:
                    bot_response = f"Error: Could not get response from backend. {e}"

            # Once the "with" block is done, the spinner disappears
            # and we write the final answer.
            st.markdown(bot_response)
    # --- END SPINNER ---

    # Add the *final* bot response to the *current* chat's history
    st.session_state.conversations[chat_id].append({"role": "assistant", "content": bot_response})

# --- Handle input from the text bar ---
if prompt_from_bar := st.chat_input("Ask me anything..."):
    submit_prompt(prompt_from_bar)