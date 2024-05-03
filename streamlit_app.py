from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Customization options
language = st.selectbox("Language", ["Cebuano", "English", "Tagalog", "Korean", "Japanese", "Chinese", "German", "French", "Spanish"])
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.slider("Age", min_value=18, max_value=100, value=22)
personality = st.selectbox("Personality", ["Serious", "Joker", "Romantic", "Sad", "Jolly", "Flirty"])
avatar = st.selectbox("Avatar", [
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "😉", "😌", "😍", "🥰", "😘", "😋",
    "🤨", "😎", "🥳", "😏", "🙄", "😒", "😔", "😞", "😢", "😠", "🤯", "😳", "🥶", "😨", "🤐", "🤕", "🤢",
    "👹", "💩", "👻", "💀", "🤖", "👽", "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾"
])

# Function to map personalities to responses
def get_personality_response(prompt, personality):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Personality: " + personality}
        ],
        max_tokens=50,
        temperature=0.7,
        stop=["\n"]
    )
    response = stream.choices[0].message
    return response

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.text_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fetching the dynamic response based on the user's prompt and chosen personality
    response = get_personality_response(prompt, personality)

    with st.chat_message("assistant"):
        st.markdown(response["content"])
    st.session_state.messages.append({"role": "assistant", "content": response["content"]})
