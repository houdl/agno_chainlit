from typing import Dict, Optional

import chainlit as cl
from dotenv import load_dotenv

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
        # Use arun instead of run for async operation
        response = await agent.arun(message.content)
        print(f"DEBUG - Response type: {type(response)}")
        
        if hasattr(response, 'content'):
            print(f"DEBUG - Content type: {type(response.content)}")
            await cl.Message(content=response.content).send()
        else:
            # If response is not in expected format, convert to string
            print(f"DEBUG - Converting response to string")
            await cl.Message(content=str(response)).send()

    except Exception as e:
        print(f"DEBUG - Exception occurred: {type(e)}: {str(e)}")
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
