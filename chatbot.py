import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv()
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("PersonalAI")

role_options = ["AI Tutor", "AI Girlfriend", "AI Joker", "AI Boyfriend"]
role = st.selectbox(
    "Select a role",
    role_options
)

avatars = {
    "AI Tutor": "avatars/tutor.png",
    "AI Girlfriend": "avatars/girlfriend.png",
    "AI Joker": "avatars/joker.gif",
    "AI Boyfriend": "avatars/boyfriend.png"
}

st.subheader(f"{role}:")  # Update subheader dynamically based on the selected role

# Display avatar
if role in avatars:
    st.image(avatars[role], width=100)  # Adjust width as needed

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input")

if 'messages' not in st.session_state or st.session_state['role'] != role:
    st.session_state['messages'] = get_initial_message(role)
    st.session_state['role'] = role

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        for msg in st.session_state['messages']:
            st.write(msg)
