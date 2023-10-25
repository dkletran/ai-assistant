import os

import streamlit as st

from chatbot import get_chat_response

app_icon = open(f"{os.path.dirname(__file__)}/icon.svg").read()
user_icon = "🧑‍💻"
st.set_page_config(
    page_title="Duc's AI virtual Assistant",
    page_icon=app_icon,
)

st.title("Chat with my AI Assistant")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar=app_icon if (message["role"] == "assistant") else user_icon,
    ):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    with st.chat_message("user", avatar=user_icon):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
if prompt:
    with st.chat_message("assistant", avatar=app_icon), st.spinner(""):
        response = get_chat_response(st.session_state.messages)
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
