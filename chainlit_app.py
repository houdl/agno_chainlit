import pdb
import chainlit as cl
import os
from dotenv import load_dotenv
from typing import Dict, Optional
from agno_agent import create_agno_agent

load_dotenv()


@cl.on_chat_start
async def on_chat_start():
    current_user = __current_user()

    agent = create_agno_agent(session_id=cl.context.session.id)
    cl.user_session.set("agent", agent)

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")

    try:
        response = agent.run(message.content)
        await cl.Message(response.content).send()

    except Exception as e:
        error_msg = f"处理过程中出现错误：{str(e)}"
        await cl.Message(content=error_msg).send()


# google 授权登陆
@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
  return default_user


def __current_user() -> Optional[cl.PersistedUser]:
    return cl.user_session.get("user")
