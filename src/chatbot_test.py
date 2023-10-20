import os
from unittest import mock

import pytest
from hamcrest import assert_that, equal_to
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from chatbot import get_chat_response

MODEL_NAME = "chat-bison@001"


@pytest.fixture(autouse=True)
def patch_env():
    with mock.patch.dict(os.environ, {"MODEL_NAME": MODEL_NAME}):
        yield


@mock.patch("chatbot.ChatVertexAI")
def test_get_chat_response_init_chat_model_with_correct_params(chat_model):
    get_chat_response([])
    chat_model.assert_called_with(model_name=MODEL_NAME)


@mock.patch("chatbot.ChatVertexAI")
def test_get_chat_response_return_correctly(chat_model):
    text_response = "response 1"
    chat_model.return_value.return_value = AIMessage(content=text_response)
    chat_history = [{"role": "user", "content": "message 1"}]
    chat_response = get_chat_response(chat_history)
    assert_that(chat_response, equal_to(text_response))


@mock.patch("chatbot.ChatVertexAI")
def test_get_chat_response_call_langchain_with_correct_history(chat_model):
    user_message = "message 1"
    chat_history = [
        {"role": "user", "content": "message 1"},
        {"role": "assistant", "content": "response 1"},
        {"role": "user", "content": "message 2"},
    ]
    get_chat_response(chat_history)
    with open(f"{os.path.dirname(__file__)}/prompt.txt") as f:
        prompt = f.read()
    chat_model.return_value.assert_called_with(
        [
            SystemMessage(content=prompt),
            HumanMessage(content="message 1"),
            AIMessage(content="response 1"),
            HumanMessage(content="message 2"),
        ]
    )
