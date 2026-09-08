import os

from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = FoundryChatClient(
    project_endpoint=PROJECT_ENDPOINT,
    model=MODEL,
    credential=AzureCliCredential(),
)

agent = Agent(
    client=client,
    name="HelloAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
)

if __name__ == "__main__":
    import asyncio

    result = asyncio.run(
        agent.run("How do I create an Azure storage account using the Azure CLI?")
    )

    print(result)
