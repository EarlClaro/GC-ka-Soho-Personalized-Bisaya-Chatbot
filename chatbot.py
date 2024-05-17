import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv

load_dotenv()
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

# Define theme colors for each role
theme_colors = {
    "AI Tutor": {"background": "#ADD8E6", "text": "black"},
    "AI Girlfriend": {"background": "#FFC0CB", "text": "black"},
    "AI Joker": {"background": "#FFD700", "text": "black"},
    "AI Boyfriend": {"background": "#87CEEB", "text": "black"}
}

st.title("PersonalAI")

role_options = ["AI Tutor", "AI Girlfriend", "AI Joker", "AI Boyfriend"]
role = st.selectbox(
    "Select a role",
    role_options
)

# Define avatar options for each role
avatars = {
    "AI Tutor": [
        "avatars/tutor.png", "avatars/tutor2.png",
        "avatars/tutor3.png", 
    ],
    "AI Girlfriend": [
        "avatars/girlfriend.png", "avatars/girlfriend2.png",
        "avatars/girlfriend3.png", "avatars/girlfriend4.png"
    ],
    "AI Joker": [
        "avatars/joker.gif", "avatars/joker2.gif",
        "https://example.com/avatar5.jpg", "https://example.com/avatar6.jpg"
    ],
    "AI Boyfriend": [
        "avatars/boyfriend.png", "avatars/boyfriend2.png",
        "avatars/boyfriend3.png","avatars/boyfriend4.png"
    ]
}

# Display avatar selection based on the selected role
selected_avatar_index = st.radio(
    f"Select an avatar for {role}",
    range(len(avatars.get(role, []))),
    index=0  # Set default index to 0
)

# Display avatar images from the gallery
selected_avatar = avatars.get(role, [])[selected_avatar_index]
st.image(selected_avatar, width=100, caption="Selected Avatar")


st.subheader(f"{role}:")  # Update subheader dynamically based on the selected role

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input")

if 'messages' not in st.session_state or st.session_state.get('role') != role:
    st.session_state['messages'] = get_initial_message(role)
    st.session_state['role'] = role

# Set theme colors based on selected role
role_theme = theme_colors.get(role, {"background": "white", "text": "black"})
st.markdown(
    f"""
    <style>
        body {{
            background-color: {role_theme["background"]};
        }}
        .stApp {{
            background-color: {role_theme["background"]};
        }}
        .st-df div {{
            background-color: {role_theme["background"]};
            color: {role_theme["text"]};
            font-weight: bold;
        }}
        .st-dg div {{
            background-color: {role_theme["background"]};
            color: {role_theme["text"]};
            font-weight: bold;
        }}
        .st-e0 div {{
            background-color: {role_theme["background"]};
            color: {role_theme["text"]};
            font-weight: bold;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

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
