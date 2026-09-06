import os

from agent_framework import Agent, MCPStreamableHTTPTool, evaluate_agent
from agent_framework_foundry import FoundryChatClient, FoundryEvals
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

MODEL = "gpt-4o"
AGENT_INSTRUCTIONS = (
    "You are a friendly assistant. Use Microsoft Learn when answering "
    "questions about Microsoft products, and keep your answers brief."
)
EVALUATION_QUERY = "How do I create an Azure storage account using the Azure CLI?"


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set.")
    return value


async def main() -> None:
    project_endpoint = required_env("AZURE_AI_PROJECT_ENDPOINT")
    credential = AzureCliCredential()

    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=MODEL,
        credential=credential,
    )

    async with MCPStreamableHTTPTool(
        name=required_env("MCP_NAME"),
        url=required_env("MCP_URL"),
    ) as learn_mcp:
        agent = Agent(
            client=client,
            name="DocsAgent",
            instructions=AGENT_INSTRUCTIONS,
            tools=[learn_mcp],
        )

        # FoundryEvals submits the run to the managed evaluation service through
        # this FoundryChatClient's project-scoped endpoint.
        results = await evaluate_agent(
            agent=agent,
            queries=[EVALUATION_QUERY],
            evaluators=FoundryEvals(
                client=client,
                evaluators=[
                    FoundryEvals.INTENT_RESOLUTION,
                    FoundryEvals.TASK_ADHERENCE,
                    FoundryEvals.TOOL_CALL_ACCURACY,
                ],
            ),
            eval_name="DocsAgent basic evaluation",
        )

    for result in results:
        print(f"Status: {result.status}")
        print(f"Results: {result.passed}/{result.total} passed")
        if result.report_url:
            print(f"Foundry report: {result.report_url}")
        result.raise_for_status()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
