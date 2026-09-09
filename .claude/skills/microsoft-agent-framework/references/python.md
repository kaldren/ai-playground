# Python implementation guidance

Read this reference only for Python Microsoft Agent Framework work.

## Inspect before editing

- Locate the relevant `pyproject.toml`, lockfile, virtual environment instructions, Python version, package layout, and test configuration.
- Preserve the repository's package manager and commands, whether they use `uv`, Poetry, PDM, pip-tools, or pip.
- Search for existing `agent_framework`, provider, Azure Identity, telemetry, and async application setup before adding dependencies.

## Resolve current packages and APIs

Use Microsoft Learn MCP to verify the packages and extras needed for the selected provider and feature. `agent-framework` is the core distribution, but providers, protocols, and hosting features can use additional distributions. Let current docs and the active lockfile determine exact names and versions.

Do not add pre-release options automatically. Use them only when current docs require a preview release for the requested feature or the project already follows that release channel.

## Implementation conventions

- Follow the application's existing async entrypoint and lifecycle. Do not hide `asyncio.run()` inside reusable library code.
- Reuse established model clients, credentials, configuration objects, and dependency wiring instead of constructing a second provider stack.
- Expose business operations as small typed functions or callables. Validate tool inputs at the boundary and keep authorization in the underlying service.
- Use type hints for public functions and tool schemas. Keep results concise and serializable.
- Use async context managers or explicit cleanup where current provider documentation requires them.
- Keep secrets in environment-backed or managed configuration. Do not log credentials or sensitive conversation content.
- Keep session or checkpoint persistence behind an application-owned interface when durable state is required.

## Verification

Use the repository's configured commands. Typical focused checks are:

```text
python -m pytest <focused-test-path>
python -m ruff check <changed-paths>
python -m mypy <changed-package>
```

Run only tools the project already configures unless adding one is part of the request. Unit-test tools, business logic, workflow branching, and serialization with fakes or stubs. Mark live-model tests clearly and do not run them without the required credentials and user-authorized external access.
