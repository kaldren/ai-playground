import asyncio
import os
import sys
from pathlib import Path

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv


def required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the environment.")
    return value


async def main() -> None:
    load_dotenv()

    client = FoundryChatClient(
        project_endpoint=required_setting("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        credential=AzureCliCredential(),
    )
    agent = Agent(
        client=client,
        name="BasicAgent",
        instructions="You are a helpful assistant. Keep your answers concise.",
    )

    prompt = " ".join(sys.argv[1:]) or "What can you help me with?"
    response = await agent.run(prompt)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
