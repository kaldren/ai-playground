// --- Configuration ---
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;

string projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException(
        "Neither FOUNDRY_PROJECT_ENDPOINT (platform-injected in hosted runtime) " +
        "nor AZURE_AI_PROJECT_ENDPOINT (local-dev convention) is set.");
string deploymentName = Environment.GetEnvironmentVariable("FOUNDRY_MODEL")
    ?? Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-4.1-mini";

// Name of the toolbox to load; the consumer MCP endpoint is built from
// projectEndpoint + toolboxName by AddFoundryToolboxes.
string toolboxName = Environment.GetEnvironmentVariable("TOOLBOX_NAME") ?? "demo-toolbox";

AzureCliCredential credential = new();

AIAgent agent = new AIProjectClient(new Uri(projectEndpoint), credential)
    .AsAIAgent(
        model: deploymentName,
        instructions: """
            You are a helpful assistant with access to tools provided by the Foundry Toolbox.
            Use the available tools to answer user questions.
            If a tool is not available for a request, let the user know clearly.
            """,
        name: Environment.GetEnvironmentVariable("AGENT_NAME") ?? "foundry-toolbox-agent",
        description: "Hosted agent backed by Foundry Toolbox MCP tools");

var builder = WebApplication.CreateBuilder(args);

// Register the agent and response handler.
builder.Services.AddFoundryResponses(agent);

// Register the Foundry Toolbox: discovers tools via tools/list at startup and
// invokes them via tools/call as the agent uses them.
builder.Services.AddFoundryToolboxes(credential, toolboxName);

var app = builder.Build();
app.MapFoundryResponses();
app.Run();
