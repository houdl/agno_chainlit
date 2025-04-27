from typing import Dict, Optional

import chainlit as cl
from dotenv import load_dotenv

from agno_agent import create_agno_agent, create_agno_team_agent

load_dotenv()

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="TextNow <> Jampp 4.10号的 direct spend",
            message="获取feedmob 中 client = TextNow, vendor = Jampp  4月10 号的 direct spend 数据.",
        ),
        cl.Starter(
            label="appsamurai 昨天的 spend 数据",
            message="appsamurai 昨天的 spend 数据",
        ),
        cl.Starter(
            label="特斯拉股价",
            message="请查询一下昨天和今天的特斯拉股价.",
        )
    ]


commands = [
    {"id": "Team", "icon": "globe", "description": "Find on the Team"},
]

@cl.on_chat_start
async def on_chat_start():
    await cl.context.emitter.set_commands(commands)
    current_user = __current_user()

    agent = create_agno_agent(session_id=cl.context.session.id)
    team_agent = create_agno_team_agent(session_id=cl.context.session.id)
    cl.user_session.set("agent", agent)
    cl.user_session.set("team_agent", team_agent)


@cl.on_message
async def on_message(message: cl.Message):
    if message.command == "Team":
       agent = cl.user_session.get("team_agent")
    else:
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
