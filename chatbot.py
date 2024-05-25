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

role_options = ["AI Tutor", "AI Girlfriend", "AI Joker", "AI Boyfriend", "AI Narcissist Bisaya"]
role = st.selectbox(
    "Select a role",
    role_options
)

avatars = {
    "AI Tutor": [
        {"name": "Mark", "image": "avatars/tutor.png"}, 
        {"name": "R0bot Teacher", "image": "avatars/tutor2.png"},
        {"name": "AI Simpson", "image": "avatars/tutor3.png"}, 
        {"name": "ST3vE", "image": "avatars/tutor4.png"}, 
        {"name": "Lucy 5", "image": "avatars/tutor5.png"}
    ],
    "AI Girlfriend": [
        {"name": "Makima", "image": "avatars/girlfriend.png"}, 
        {"name": "Asa Mikata", "image": "avatars/girlfriend2.png"},
        {"name": "Power", "image": "avatars/girlfriend3.png"}, 
        {"name": "Himeno", "image": "avatars/girlfriend4.png"}, 
        {"name": "Dahyun", "image": "avatars/girlfriend5.png"}
    ],
    # Add entries for other roles similarly
    "AI Joker": [
        {"name": "Laugh Meme", "image": "avatars/joker.gif"}, 
        {"name": "Pepe Joker", "image": "avatars/joker2.png"},
        {"name": "Joker", "image": "avatars/joker3.png"}, 
        {"name": "Luffy", "image": "avatars/joker4.png"}, 
        {"name": "Clown Drake", "image": "avatars/joker5.png"}
    ],
    "AI Boyfriend": [
        {"name": "Yuji", "image": "avatars/boyfriend.png"}, 
        {"name": "Denji", "image": "avatars/boyfriend2.png"},
        {"name": "Korean Oppa", "image": "avatars/boyfriend3.png"}, 
        {"name": "Daddy", "image": "avatars/boyfriend4.png"}, 
        {"name": "Sung Jinwoo", "image": "avatars/boyfriend6.png"}
    ],
    "AI Narcissist Bisaya": [
        {"name": "Kyle Gwapo", "image": "avatars/bisaya1.jpg"}, 
        {"name": "Jay Gwapo", "image": "avatars/bisaya2.jpg"},
        {"name": "Fern Gwapo", "image": "avatars/bisaya3.png"},
        {"name": "Pinaka Gwapo", "image": "avatars/bisaya4.png"}
    ],
}


# Display avatar selection based on the selected role
avatars_for_role = avatars.get(role, [])
avatar_names = [avatar["name"] for avatar in avatars_for_role]
selected_avatar_index = st.radio(
    f"Select an avatar for {role}",
    list(range(len(avatars_for_role))),
    format_func=lambda i: avatar_names[i],  # Display avatar names in radio button
    index=0  # Set default index to 0
)

# Convert selected_avatar_index to integer
selected_avatar_index = int(selected_avatar_index)

# Display avatar selection based on the selected role
selected_avatar = avatars.get(role, [])[selected_avatar_index]
st.image(selected_avatar["image"], width=100, caption=selected_avatar["name"])

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
