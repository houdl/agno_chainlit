import os

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv

from mcp_client import get_mcp_tools

load_dotenv()


def create_agno_agent(session_id: str):
    model = DeepSeek(
        id="deepseek-ai/DeepSeek-V2.5",
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        base_url=os.environ.get("DEEPSEEK_API_BASE_URL", ""),
    )

    # model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    # model = AwsBedrock(
    #     id=model_id,
    #     aws_region=os.environ.get("AWS_REGION_NAME", ""),
    #     aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
    #     aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    # )

    mcp_tools = get_mcp_tools()
    print(mcp_tools)
    agent = Agent(
        instructions=["You are a assiant for help me."],
        model=model,
        # tools=[DuckDuckGoTools(), YFinanceTools(stock_price=True)],
        tools=[mcp_tools],
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
