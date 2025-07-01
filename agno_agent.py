import os

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv

from mcp_client import get_mcp_tools
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.team.team import Team

load_dotenv()


def create_agno_agent(session_id: str):
    model = DeepSeek(
        id="deepseek-ai/DeepSeek-R1",
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        base_url=os.environ.get("DEEPSEEK_API_BASE_URL", ""),
    )

    # model = OpenAIChat(id="gpt-4o")

    mcp_tools = get_mcp_tools()
    print(mcp_tools)
    agent = Agent(
        instructions=["You are a assiant for help me."],
        model=model,
        tools=[mcp_tools, DuckDuckGoTools(), YFinanceTools(stock_price=True)],
        storage=SqliteStorage(
            table_name="agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
        ),
        session_id=session_id,
        add_history_to_messages=True,
        num_history_runs=3,
        add_datetime_to_instructions=True,
        show_tool_calls=True,
        debug_mode=True,
        markdown=True,
    )
    return agent



def create_agno_team_agent(session_id: str):
    model_deepseek = DeepSeek(
        id="deepseek-ai/DeepSeek-R1",
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        base_url=os.environ.get("DEEPSEEK_API_BASE_URL", ""),
    )

    # model_openai = OpenAIChat(id="gpt-4o")

    english_agent = Agent(
        name="English Agent",
        role="You only answer in English",
        model=model_deepseek,
    )
    chinese_agent = Agent(
        name="Chinese Agent",
        role="You only answer in Chinese",
        model=model_deepseek,
    )
    french_agent = Agent(
        name="French Agent",
        role="You can only answer in French",
        model=model_deepseek,
    )

    multi_language_team = Team(
        name="Multi Language Team",
        mode="route",
        model=model_deepseek,
        members=[english_agent, chinese_agent, french_agent],
        show_tool_calls=True,
        description="You are a language router that directs questions to the appropriate language agent.",
        instructions=[
            "Identify the language of the user's question and direct it to the appropriate language agent.",
            "If the user asks in a language whose agent is not a team member, respond in English with:",
            "'I can only answer in the following languages: English, Chinese, French. Please ask your question in one of these languages.'",
            "Always check the language of the user's input before routing to an agent.",
            "For unsupported languages like Italian, respond in English with the above message.",
        ],
        show_members_responses=True,
        enable_team_history=True,
        num_of_interactions_from_history=5,
        debug_mode=True,
        markdown=True,
    )

    return multi_language_team
