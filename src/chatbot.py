import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def _make_langchain_message(message):
    if message["role"] == "user":
        return HumanMessage(content=message["content"])
    if message["role"] == "assistant":
        return AIMessage(content=message["content"])


def get_chat_response(chat_history):
    chat = ChatOpenAI(model=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"))
    with open(f"{os.path.dirname(__file__)}/prompt.txt") as f:
        prompt = f.read()
    system_message = SystemMessage(content=prompt)
    response = chat(
        [system_message] + [_make_langchain_message(m) for m in chat_history]
    )
    return response.content
