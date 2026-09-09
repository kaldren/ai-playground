# .NET implementation guidance

Read this reference only for C# or .NET Microsoft Agent Framework work.

## Inspect before editing

- Locate the target `.csproj`, solution, and any `Directory.Packages.props`, `Directory.Build.props`, or central package management.
- Preserve the target framework, nullable settings, implicit usings, analyzers, and the repository's dependency-injection and configuration conventions.
- Search for existing `Microsoft.Agents.AI`, `Microsoft.Extensions.AI`, provider, Azure Identity, logging, and resilience packages before adding dependencies.

## Resolve current packages and APIs

Use Microsoft Learn MCP to verify the packages needed for the selected provider and feature. `Microsoft.Agents.AI` is the core package family, but provider, workflow, hosting, and evaluation features can require separate packages. Let current docs and existing central package management determine exact package IDs and versions.

Do not add `--prerelease` automatically. Use it only when current docs require a preview package for the requested feature or the project already follows preview versions.

## Implementation conventions

- Keep agent construction near the application's composition root when it depends on clients, credentials, options, logging, or middleware.
- Reuse an existing `IChatClient` or provider registration when present rather than constructing a parallel client stack.
- Expose business operations as small, typed tools and keep authorization checks in the underlying service boundary.
- Use `async` APIs end to end and pass `CancellationToken` through agent runs, tools, workflows, and hosting boundaries.
- Prefer `IOptions`-based configuration and structured `ILogger` messages. Do not log secrets, raw credentials, or sensitive conversation content.
- Dispose or scope clients according to the provider documentation and existing dependency-injection lifetime.
- Keep session or checkpoint persistence behind an application-owned abstraction when durable state is required.

## Verification

Run the narrowest commands that cover the change, expanding only when failures or repository conventions justify it:

```text
dotnet restore <solution-or-project>
dotnet build <solution-or-project> --no-restore
dotnet test <test-project-or-solution> --no-build
```

Use the repository's formatter or analyzer command when configured. Unit-test tool argument validation, service behavior, workflow branching, and state serialization without requiring a live model. Mark live provider tests clearly and do not run them without the required credentials and user-authorized external access.
