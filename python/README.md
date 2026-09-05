# Python examples

## Local telemetry with Aspire Dashboard

The standalone Aspire Dashboard receives OpenTelemetry traces, metrics, and logs
from any example in this folder.

1. Create your local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Start the dashboard:

   ```powershell
   docker compose up -d
   ```

3. In each instrumented example, configure the Agent Framework telemetry
   providers after loading `.env` and before creating a client or agent:

   ```python
   from dotenv import load_dotenv
   from agent_framework.observability import configure_otel_providers

   load_dotenv()
   configure_otel_providers()
   ```

4. Run an example from this directory, then open
   [http://localhost:18888](http://localhost:18888).

   ```powershell
   uv run python src/examples/agent_evals_monitoring.py
   ```

Use a distinct `OTEL_SERVICE_NAME` when you want examples to appear as separate
services. Prompt text, responses, and tool arguments are not exported by default;
set `ENABLE_SENSITIVE_DATA=true` only for local data you are comfortable viewing
in the dashboard.

Stop and remove the dashboard container with:

```powershell
docker compose down
```

## Microsoft Learn MCP

`agent_evals_monitoring.py` connects the agent to the remote Microsoft Learn MCP
server using `MCPStreamableHTTPTool`. Its name and endpoint are configurable with
`MCP_NAME` and `MCP_URL` in `.env`; the defaults already point to Microsoft Learn.

The MCP connection uses an async context manager so it is opened before the agent
runs and closed cleanly afterward. Calls to the MCP server are included in the
OpenTelemetry trace sent to Aspire.
