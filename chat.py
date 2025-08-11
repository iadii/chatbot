import streamlit as st
from groq import Groq
import time


client = Groq(api_key=st.secrets["GROQ_API_KEY"])


st.set_page_config(page_title="Adii's LLM Chat", page_icon="🤖", layout="wide")


st.sidebar.title("⚙️ Settings")
model = st.sidebar.selectbox(
    "Choose Model",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "qwen/qwen3-32b"
    ],
)



temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.7)


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]


st.title("Adii ai Chatbot")
st.caption(f"Model: {model}")


for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


if prompt := st.chat_input("Type your message..."):

    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True
            )

            for chunk in response:
                chunk_text = chunk.choices[0].delta.content or ""
                full_response += chunk_text
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.02)

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
