import os

from agent_framework import Agent
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

    agent = Agent(
        client=client,
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    result = await agent.run("What is the capital of France?")
    print(f"Agent: {result}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
