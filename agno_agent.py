import os

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv

from mcp_client import get_mcp_tools
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

load_dotenv()


def create_agno_agent(session_id: str):
    # model = DeepSeek(
    #     id="deepseek-ai/DeepSeek-V3",
    #     api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    #     base_url=os.environ.get("DEEPSEEK_API_BASE_URL", ""),
    # )

    model = OpenAIChat(id="gpt-4o")

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
