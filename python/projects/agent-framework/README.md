# Basic Microsoft Agent Framework agent

This example uses `FoundryChatClient` with Azure CLI authentication. It loads the
existing configuration from `../agent-observability/.env`; it does not copy or
commit credentials.

The shared `.env` (or your shell environment) must provide:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=https://<project>.services.ai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

`AZURE_OPENAI_DEPLOYMENT` is optional and defaults to `gpt-4o` to match the
existing observability examples.

Sign in and run the agent from this directory:

```powershell
az login
uv sync
uv run python basic_agent.py "Explain Microsoft Agent Framework in one sentence."
```
