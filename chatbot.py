import streamlit as st
import google.generativeai as genai
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)

# --- CONFIGURATION ---
# Replace with your actual API Key
# This grabs the key securely from the Streamlit Cloud safe


# We are switching to 'gemini-pro' because it is the most stable model 
# and avoids the "404 not found" error you were seeing.
model = genai.GenerativeModel('gemini-2.5-flash')

# --- PAGE SETUP ---
st.title("🤖 My First AI Chatbot")

# --- MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- CHAT LOGIC (Fixed the NameError here!) ---
# Notice the ':=' symbol. This assigns the value AND checks if it exists.
if user_input := st.chat_input("Type your message here..."):
    
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 2. Generate AI Response
    with st.chat_message("assistant"):
        try:
            # Create a chat session with history
            history_for_model = [
                {"role": "user" if m["role"] == "user" else "model", "parts": m["content"]}
                for m in st.session_state.messages[:-1] # Exclude the very last message we just added
            ]
            
            chat = model.start_chat(history=history_for_model)
            response = chat.send_message(user_input)
            
            st.write(response.text)
            
            # Save AI response to memory
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:

            st.error(f"An error occurred: {e}")


