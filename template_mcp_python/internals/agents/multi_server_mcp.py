import json

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from template_mcp_python.internals.llms.azure_openai import AzureOpenAiWrapper


def get_vscode_config():
    with open(".vscode/mcp.json") as f:
        config = json.load(f)
        return config["servers"]


async def make_graph():
    configs = get_vscode_config()
    client = MultiServerMCPClient(configs)
    tools = await client.get_tools()
    agent = create_agent(
        model=AzureOpenAiWrapper().llm,
        tools=tools,
    )
    return agent
