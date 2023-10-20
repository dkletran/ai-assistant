import os

from langchain.chat_models import ChatVertexAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def _make_langchain_message(message):
    if message["role"] == "user":
        return HumanMessage(content=message["content"])
    if message["role"] == "assistant":
        return AIMessage(content=message["content"])


def get_chat_response(chat_history):
    chat = ChatVertexAI(model_name=os.environ.get("MODEL_NAME", "chat-bison@001"))
    with open(f"{os.path.dirname(__file__)}/prompt.txt") as f:
        prompt = f.read()
    system_message = SystemMessage(content=prompt)
    response = chat(
        [system_message] + [_make_langchain_message(m) for m in chat_history]
    )
    return response.content
