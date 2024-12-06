import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数をロードする
load_dotenv()

# OpenAIクライアントを作成
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY is missing. Please set it in the .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("コンタクトレンズ相談所")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display the fox illustration with a smaller size
st.image("kon.png", caption="コンタクトの専門家", width=200)

# Accept user input
if prompt := st.chat_input("ここに入力してください?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Add instruction for conversation
                messages = st.session_state.messages + [
                    {"role": "system", "content": "あなたは、コンタクトレンズの専門家です。のんびりと優しい関西弁で、答えてください。"}
                ]

                # Generate response using OpenAI API
                response = client.chat.completions.create(
                    messages=messages,
                    model=st.session_state["openai_model"]
                )
                # Extract the assistant's reply
                response_text = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error generating response: {e}")
                response_text = "An error occurred."

            st.markdown(response_text)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
