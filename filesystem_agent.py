import asyncio
import os
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MultiMCPTools
from dotenv import load_dotenv
from agno.models.deepseek import DeepSeek

load_dotenv()


async def run_agent(message: str) -> None:
    """Run the filesystem agent with the given message."""

    model = DeepSeek(
        id="deepseek-ai/DeepSeek-V3",
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        base_url=os.environ.get("DEEPSEEK_API_BASE_URL", "")
    )

    # model = OpenAIChat(id="gpt-4o")

    file_path = str(Path(__file__).parent.parent)

    async with MultiMCPTools(
        [
            f"npx -y @modelcontextprotocol/server-filesystem {file_path}",
            "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
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
    asyncio.run(run_agent("Can you help me find the file with the file name filesystem_agent"))
    # asyncio.run(run_agent("What rental information is available on Airbnb for babies under $1000 in Shanghai"))
