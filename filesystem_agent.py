import asyncio
import os
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MultiMCPTools
from dotenv import load_dotenv
from agno.models.deepseek import DeepSeek
from agno.models.aws import AwsBedrock

load_dotenv()


async def run_agent(message: str) -> None:
    """Run the filesystem agent with the given message."""

    model = DeepSeek(
        id="deepseek-ai/DeepSeek-V2.5",
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        base_url=os.environ.get("DEEPSEEK_API_BASE_URL", "")
    )

    # model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    # model = AwsBedrock(
    #     id=model_id,
    #     aws_region=os.environ.get("AWS_REGION_NAME", ""),
    #     aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
    #     aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    # )

    file_path = str(Path(__file__).parent.parent)

    async with MultiMCPTools(
        [
            f"npx -y @modelcontextprotocol/server-filesystem {file_path}",
        ]
    ) as mcp_tools:
        agent = Agent(
            model=model,
            tools=[mcp_tools],
            instructions=dedent("""\
                You are a filesystem assistant. Help users explore files and directories.

                - Use search_files tool with appropriate patterns to find files
                - For Python files, use pattern="*.py"
                - List files in a clear, organized way using markdown
                - Include only the information requested by the user
                - Be concise and focus on relevant information\
            """),
            markdown=True,
            show_tool_calls=True,
            debug_mode=True,
        )

        # Run the agent
        await agent.aprint_response(message)


# Example usage
if __name__ == "__main__":
    # List all Python files in the project
    asyncio.run(run_agent("帮我找到 文件名是 filesystem_agent 的文件"))
