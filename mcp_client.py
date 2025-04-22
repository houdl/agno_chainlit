import os
from typing import Optional

from fastapi import FastAPI
from mcp.client.stdio import get_default_environment
from agno.tools.mcp import MultiMCPTools
from pathlib import Path

_app: Optional[FastAPI] = None


def initialize_app_reference(app: FastAPI):
    """
    Initialize the FastAPI app reference for MCP tools.
    """
    global _app
    _app = app


def get_mcp_tools():
    """
    Get MCP tools for the application.
    """
    if _app is None:
        raise ValueError("FastAPI App reference not initialized")
    return _app.state.mcp_tools


def create_mcp_client():
    """
    Create an MCP client for the application.
    """

    default_env = get_default_environment()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = str(Path(__file__).parent)

    return MultiMCPTools(
        [
            f"npx -y @modelcontextprotocol/server-filesystem {file_path}",
        ]
    )