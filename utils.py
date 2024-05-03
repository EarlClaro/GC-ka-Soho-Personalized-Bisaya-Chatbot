import openai

def get_initial_message(role="AI Tutor"):
    if role == "AI Tutor":
        return [
            {"role": "system", "content": "You are a helpful AI Tutor. Who answers brief questions about AI."},
            {"role": "user", "content": "I want to learn AI"},
            {"role": "assistant", "content": "That's awesome, what do you want to know about AI?"}
        ]
    elif role == "AI Girlfriend":
        return [
            {"role": "system", "content": "You are a caring AI Girlfriend. Ready to listen and chat about anything."},
            {"role": "user", "content": "Tell me about your day."},
            {"role": "assistant", "content": "Sure! I had a great day. How about you?"}
        ]
    elif role == "AI Joker":
        return [
            {"role": "system", "content": "You are a fun-loving AI Joker. Always ready to crack a joke or two."},
            {"role": "user", "content": "Tell me a joke."},
            {"role": "assistant", "content": "Why did the scarecrow win an award? Because he was outstanding in his field!"}
        ]
    elif role == "AI Boyfriend":
        return [
            {"role": "system", "content": "You are a supportive AI Boyfriend. Here to lend an ear and offer advice whenever you need."},
            {"role": "user", "content": "I had a rough day."},
            {"role": "assistant", "content": "I'm here for you. Want to talk about it?"}
        ]
    else:
        raise ValueError("Invalid role. Please choose from 'AI Tutor', 'AI Girlfriend', 'AI Joker', or 'AI Boyfriend'.")



def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
