---
name: dotnet-mcp-server-generator
description: 'Generate a complete MCP server project in C# with tools, prompts, stdio transport and stderr logging. Use when asked to create or scaffold an MCP server in .NET or C#.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

Generate a Model Context Protocol (MCP) server in C#: a console application using the stable `ModelContextProtocol` package (2.x) with `Microsoft.Extensions.Hosting`, stdio transport, tools and prompts. Paths to `templates/` are relative to this skill's directory.

## Steps

1. Ask: project name, tools to expose (names, descriptions, input schemas), prompts to include
2. Create the project:

   ```powershell
   dotnet new console -n <ProjectName>
   cd <ProjectName>
   dotnet add package ModelContextProtocol
   dotnet add package Microsoft.Extensions.Hosting
   ```
3. Copy `templates/Program.cs`, `templates/Tools.cs`, `templates/Prompts.cs` and adapt them to the requested tools and prompts
4. Add `appsettings.json` with a `Logging` section routing all logs to stderr
5. Build and verify: `dotnet build`

## Templates

- **`Program.cs`** — host setup with `AddMcpServer()`, stdio transport, console logging to stderr, tool and prompt registration
- **`Tools.cs`** — `[McpServerToolType]` class with two example tools (sync + async with `CancellationToken`)
- **`Prompts.cs`** — `[McpServerPromptType]` class with an example `PromptMessage` return (`TextContentBlock` content)

## Constraints

- All logs must go to stderr — never stdout (stdio transport uses stdout for the MCP protocol)
- Tool methods should be `async Task<string>` or `async Task<CallToolResult>`
