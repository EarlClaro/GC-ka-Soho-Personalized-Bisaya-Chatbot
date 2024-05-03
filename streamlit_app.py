from openai import OpenAI
import streamlit as st

st.title("Bisaya Buddy")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Default values for personality customization
default_language = "Bisaya"
default_gender = "Male"
default_age = ""
default_avatar = ":smiley:"
default_personality = "Serious"

# User input for personality customization
language = st.selectbox("Language", ["Bisaya", "English", "Other"], index=0)
gender = st.radio("Gender", ["Male", "Female"], index=0)
age = st.text_input("Age")
avatar = st.selectbox("Avatar", [":smiley:", ":girl:", ":boy:", ":man:", ":woman:"], index=0)
personality = st.selectbox("Personality", ["Serious", "Joker", "Romantic", "Sad", "Jolly", "Flirty"], index=0)

# Maintain user-selected personality settings in session state
st.session_state.personality = {
    "language": language,
    "gender": gender,
    "age": age,
    "avatar": avatar,
    "personality": personality
}

# Initialize messages list in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input and generate chatbot response
if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construct persona based on user-selected personality attributes
    persona = f"Language: {language}\nGender: {gender}\nAge: {age}\nAvatar: {avatar}\nPersonality: {personality}"
    
    # Generate chatbot response using OpenAI API
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            persona=persona,  # Pass persona to the OpenAI API
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
