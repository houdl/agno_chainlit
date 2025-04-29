import os
from pathlib import Path
from typing import Optional

from agno.tools.mcp import MultiMCPTools
from fastapi import FastAPI
from mcp.client.stdio import get_default_environment

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
    env = {
        **os.environ,
        "APPSAMURAI_API_KEY": os.getenv("APPSAMURAI_API_KEY"),
        "POSTGRES_DATABASE": os.getenv("POSTGRES_DATABASE"),
        "JAMPP_API_CLIENT_SECRET": os.getenv("JAMPP_API_CLIENT_SECRET"),
        "FEEDMOB_KEY": os.getenv("FEEDMOB_KEY"),
        "FEEDMOB_SECRET": os.getenv("FEEDMOB_SECRET"),
        "FEEDMOB_API_BASE": os.getenv("FEEDMOB_API_BASE"),
        "INMOBI_CLIENT_ID": os.getenv("INMOBI_CLIENT_ID"),
        "INMOBI_CLIENT_SECRET": os.getenv("INMOBI_CLIENT_SECRET"),
    }

    return MultiMCPTools(
        [
            "npx -y @modelcontextprotocol/server-sequential-thinking",
            "npx -y @feedmob/appsamurai-reporting",
            f"node {os.path.join(current_dir, "mcp_servers", "servers", "feedmob-spend", "dist", "index.js")}",
            f"uv run {os.path.join(current_dir, "mcp_servers", "math_server.py")}",
            # f"uv --directory {os.path.join(current_dir, "mcp_servers", "servers", "feedmob")} run feedmob",
            f"uv --directory {os.path.join(current_dir, "mcp_servers", "servers", "inmobi")} run inmobi",
            f"uv --directory {os.path.join(current_dir, "mcp_servers", "servers", "jampp")} run jampp",
        ],
        env=env,
    )