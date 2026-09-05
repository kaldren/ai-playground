import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.observability import (
    configure_otel_providers,
    enable_sensitive_telemetry,
)
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

load_dotenv()


def configure_telemetry() -> None:
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    configured_exporter = os.getenv("TELEMETRY_EXPORTER")
    exporter = (
        configured_exporter
        or ("applicationinsights" if connection_string else "aspire")
    ).strip().lower()

    if exporter == "aspire":
        configure_otel_providers()
    elif exporter == "applicationinsights":
        if not connection_string:
            raise RuntimeError(
                "APPLICATIONINSIGHTS_CONNECTION_STRING must be set when "
                "TELEMETRY_EXPORTER=applicationinsights."
            )

        # An explicit exporter choice is the documented local-test path. Avoid
        # probing Azure Instance Metadata locally; automatic deployed selection
        # retains Azure resource detection. A caller-set value always wins.
        if configured_exporter:
            os.environ.setdefault("OTEL_EXPERIMENTAL_RESOURCE_DETECTORS", "otel")

        configure_azure_monitor(
            connection_string=connection_string,
            logger_name="examples",
        )
        if os.getenv("ENABLE_SENSITIVE_DATA", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            enable_sensitive_telemetry()
    else:
        raise ValueError(
            f"Unsupported TELEMETRY_EXPORTER value '{exporter}'. "
            "Use 'aspire' or 'applicationinsights'."
        )


configure_telemetry()


async def main():

    PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

    client = FoundryChatClient(
        project_endpoint=PROJECT_ENDPOINT,
        model="gpt-4o",
        credential=AzureCliCredential(),
    )

    async with MCPStreamableHTTPTool(
        name=os.getenv("MCP_NAME"),
        url=os.getenv("MCP_URL"),
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
