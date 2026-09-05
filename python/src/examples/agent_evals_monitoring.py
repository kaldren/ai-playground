import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.observability import configure_otel_providers
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()
configure_otel_providers()


async def main():

    PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

    client = FoundryChatClient(
        project_endpoint=PROJECT_ENDPOINT,
        model="gpt-4o",
        credential=AzureCliCredential(),
    )

    async with MCPStreamableHTTPTool(
        name=os.getenv("MCP_NAME", "Microsoft Learn MCP"),
        url=os.getenv("MCP_URL", "https://learn.microsoft.com/api/mcp"),
    ) as learn_mcp:
        agent = Agent(
            client=client,
            name="DocsAgent",
            instructions=(
                "You are a friendly assistant. Use Microsoft Learn when answering "
                "questions about Microsoft products, and keep your answers brief."
            ),
            tools=[learn_mcp],
        )

        result = await agent.run(
            "How do I create an Azure storage account using the Azure CLI?"
        )
        print(f"Agent: {result}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
