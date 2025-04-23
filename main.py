from contextlib import asynccontextmanager

from chainlit.utils import mount_chainlit
from fastapi import FastAPI

import mcp_client as mcp_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: setup code here
    # start mcp servers
    mcp_tools = mcp_client.create_mcp_client()
    await mcp_tools.__aenter__()
    app.state.mcp_tools = mcp_tools
    yield
    # Shutdown: cleanup code here (if any)
    await app.state.mcp_tools.__aexit__(None, None, None)


app = FastAPI(title="DEMO API", lifespan=lifespan)

# Initialize MCP client reference
mcp_client.initialize_app_reference(app)


@app.get("/")
def read_main():
    return {"message": "Hello World from main app"}


mount_chainlit(app=app, target="chainlit_app.py", path="/chainlit")
