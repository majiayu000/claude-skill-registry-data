---
name: mcp-builder
description: Build production-grade MCP (Model Context Protocol) servers that connect AI agents to external APIs, databases, and services. Use when the user wants to build an MCP server, integrate an external API with Claude or any AI agent, create custom tools for an AI agent, expose a service via MCP, or asks how to connect their app to an AI model using the MCP standard.
---

# MCP Server Development

MCP (Model Context Protocol) is the standard for connecting AI agents to external tools and services. An MCP server exposes tools, resources, and prompts that any compatible AI agent can call — Claude, GPT-4, Gemini, or any other model that speaks the protocol.

Build MCP servers like you build APIs: with clear contracts, proper error handling, and the caller (the AI agent) as your user. A badly designed MCP tool confuses the model. A well-designed one makes the model dramatically more capable.

---

## MCP Builder Principles

- **The AI agent is the caller — design for it.** Tool names, descriptions, and schemas must be clear enough that an LLM picks the right tool without being told. If a tool name is ambiguous, the agent will misuse it.
- **Tool descriptions are prompt engineering.** The `description` field in your tool schema is what the model reads to decide when and how to call it. Write it like a senior engineer explaining an API to a junior — concrete, precise, with examples.
- **Comprehensive beats clever.** Cover the API's core operations completely before adding workflow shortcuts. Agents can compose basic tools; they cannot invent missing operations.
- **Actionable errors are non-negotiable.** When a tool fails, the error message must tell the agent exactly what went wrong and exactly what to try next. "An error occurred" is useless. "Authentication failed: API key missing. Set the X-API-KEY header with your key from https://example.com/settings/api" is useful.
- **Stateless by default.** Design tools to be stateless and idempotent where possible. Stateful MCP servers are harder to debug, scale, and reason about.
- **Security is not optional.** MCP servers run with the credentials of the human user. Never log secrets. Validate every input. Scope permissions to the minimum required.

---

## Step 0: Plan Before You Build

Answer these before writing a line of code:

1. **What service are you wrapping?** Name it. What does it do?
2. **What are the 5 most common operations a user needs?** Start here — not with full API coverage.
3. **What is the authentication mechanism?** API key, OAuth, bearer token, mTLS?
4. **What transport?** `stdio` for local tools (runs on user's machine), `streamable HTTP` for remote servers (deployed, shareable).
5. **What language?** TypeScript recommended (best SDK support, type safety, broad compatibility). Python (FastMCP) for data/ML workflows.
6. **What are the failure modes?** API rate limits, network timeouts, auth expiry — plan the error messages now.

---

## Architecture

### Transport Selection

| Transport | When to use | How it works |
|---|---|---|
| **stdio** | Local tools, developer utilities, file system access | Agent spawns the server as a subprocess; communicates via stdin/stdout |
| **Streamable HTTP** | Remote services, shared team servers, deployed APIs | Server runs independently; agent connects via HTTP; stateless JSON preferred |

**Rule:** stdio for anything touching the local machine (files, databases, local dev tools). HTTP for anything deployed or shared.

### Tool Design Patterns

#### Pattern 1: Direct API Mapping (recommended first)
One tool per major API endpoint. Simple, predictable, composable.

```typescript
server.registerTool("github_list_repos", {
  description: "List repositories for a GitHub user or organization. Returns name, description, stars, and clone URL for each repo.",
  inputSchema: {
    owner: z.string().describe("GitHub username or organization name"),
    type: z.enum(["all", "public", "private"]).default("public").describe("Filter by repository type"),
    per_page: z.number().min(1).max(100).default(30).describe("Number of repos to return (max 100)")
  }
}, async ({ owner, type, per_page }) => {
  // implementation
})
```

#### Pattern 2: Workflow Tool (after core coverage)
Higher-level tools that combine multiple operations for common use cases.

```typescript
server.registerTool("github_create_pr_from_branch", {
  description: "Create a pull request from a feature branch to main. Automatically sets title from branch name if not provided.",
  inputSchema: {
    repo: z.string().describe("Repository in format 'owner/repo'"),
    branch: z.string().describe("Source branch name"),
    title: z.string().optional().describe("PR title (defaults to branch name with hyphens replaced by spaces)"),
    body: z.string().optional().describe("PR description in Markdown")
  }
}, async ({ repo, branch, title, body }) => {
  // implementation combining list-branches, create-pr operations
})
```

---

## TypeScript Implementation (Recommended)

### Project Structure
```
my-mcp-server/
├── src/
│   ├── index.ts          # Server entry point
│   ├── tools/            # One file per tool group
│   │   ├── repos.ts
│   │   └── issues.ts
│   ├── client.ts         # API client with auth + retry
│   └── errors.ts         # Error types and formatters
├── package.json
├── tsconfig.json
└── README.md
```

### package.json
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "dev": "tsx watch src/index.ts",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "tsx": "^4.11.0"
  }
}
```

### Server Entry Point (stdio)
```typescript
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerRepoTools } from "./tools/repos.js";
import { registerIssueTools } from "./tools/issues.js";

const server = new McpServer({
  name: "github-mcp",
  version: "1.0.0",
});

// Register all tool groups
registerRepoTools(server);
registerIssueTools(server);

// Start with stdio transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Server Entry Point (HTTP)
```typescript
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";

const app = express();
app.use(express.json());

app.post("/mcp", async (req, res) => {
  const server = new McpServer({ name: "my-mcp", version: "1.0.0" });
  // register tools...
  const transport = new StreamableHTTPServerTransport({ sessionType: "stateless" });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(3000);
```

### Tool Implementation with Full Error Handling
```typescript
// src/tools/repos.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export function registerRepoTools(server: McpServer) {
  server.registerTool(
    "github_get_repo",
    {
      description: "Get details about a GitHub repository including description, stars, forks, language, and open issue count.",
      inputSchema: {
        repo: z.string().describe("Repository in 'owner/repo' format, e.g. 'microsoft/vscode'"),
      },
      // Annotations help agents understand tool behavior
      annotations: {
        readOnlyHint: true,      // Does not modify data
        destructiveHint: false,
        idempotentHint: true,    // Same input = same output
      }
    },
    async ({ repo }) => {
      // Input validation (beyond schema)
      if (!repo.includes("/")) {
        return {
          isError: true,
          content: [{
            type: "text",
            text: `Invalid repo format: "${repo}". Expected "owner/repo", e.g. "microsoft/vscode".`
          }]
        };
      }

      try {
        const response = await fetch(`https://api.github.com/repos/${repo}`, {
          headers: {
            Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
            Accept: "application/vnd.github.v3+json",
          },
        });

        if (response.status === 404) {
          return {
            isError: true,
            content: [{ type: "text", text: `Repository "${repo}" not found. Check the name and ensure it is public or your token has access.` }]
          };
        }

        if (response.status === 401) {
          return {
            isError: true,
            content: [{ type: "text", text: "GitHub authentication failed. Set the GITHUB_TOKEN environment variable with a valid personal access token." }]
          };
        }

        if (!response.ok) {
          return {
            isError: true,
            content: [{ type: "text", text: `GitHub API error ${response.status}: ${await response.text()}` }]
          };
        }

        const data = await response.json();

        // Return both structured data and human-readable text
        return {
          content: [
            {
              type: "text",
              text: `**${data.full_name}**\n${data.description ?? "No description"}\n\n⭐ ${data.stargazers_count} stars · 🍴 ${data.forks_count} forks · 🐛 ${data.open_issues_count} open issues\nLanguage: ${data.language ?? "Unknown"}\nURL: ${data.html_url}`
            }
          ],
          structuredContent: data  // Full JSON for programmatic use
        };

      } catch (error) {
        return {
          isError: true,
          content: [{ type: "text", text: `Network error connecting to GitHub API: ${error instanceof Error ? error.message : String(error)}. Check your internet connection.` }]
        };
      }
    }
  );
}
```

---

## Python Implementation (FastMCP)

```python
# server.py
from fastmcp import FastMCP
import httpx
import os

mcp = FastMCP("my-mcp-server")

@mcp.tool()
async def get_repo(repo: str) -> str:
    """Get details about a GitHub repository.
    
    Args:
        repo: Repository in 'owner/repo' format, e.g. 'microsoft/vscode'
    
    Returns:
        Repository details including description, stars, and language.
    """
    if "/" not in repo:
        raise ValueError(f'Invalid repo format: "{repo}". Expected "owner/repo".')
    
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError(
            "GITHUB_TOKEN not set. Create a token at https://github.com/settings/tokens"
        )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
    
    return (
        f"**{data['full_name']}**\n"
        f"{data.get('description', 'No description')}\n"
        f"⭐ {data['stargazers_count']} stars · Language: {data.get('language', 'Unknown')}"
    )

if __name__ == "__main__":
    mcp.run()
```

---

## Tool Description Writing Guide

The description field is what the model reads. Write it like documentation for a developer:

**Bad description:**
```
"Gets stuff from GitHub"
```

**Good description:**
```
"Get details about a GitHub repository including name, description, star count, 
fork count, open issue count, primary language, and clone URL. Use when you need 
to look up information about a specific repo before performing operations on it."
```

**Template for every tool description:**
```
[Verb] [what it does] including [key data returned]. 
Use when [specific trigger condition].
[Auth note if non-obvious.]
[Format note if output is structured.]
```

---

## Testing Your MCP Server

### MCP Inspector (interactive)
```bash
# TypeScript server
npx @modelcontextprotocol/inspector node dist/index.js

# Python server
npx @modelcontextprotocol/inspector python server.py
```

Opens a web UI where you can call every tool manually and inspect request/response.

### Automated Tests
```typescript
// Test each tool in isolation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";

const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
const server = new McpServer({ name: "test", version: "1.0.0" });
registerRepoTools(server);
await server.connect(serverTransport);

// Call tool and assert response
const result = await client.callTool("github_get_repo", { repo: "microsoft/vscode" });
assert(result.content[0].text.includes("microsoft/vscode"));
```

---

## Claude Desktop Integration (stdio)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/my-mcp-server/dist/index.js"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

For Python:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": { "GITHUB_TOKEN": "ghp_xxx" }
    }
  }
}
```

---

## Security Checklist

- [ ] No secrets in source code — all via environment variables
- [ ] No secrets in logs or error messages — strip before returning
- [ ] All user inputs validated — schema + semantic validation
- [ ] API calls have explicit timeouts (default: 10s)
- [ ] Rate limit errors handled gracefully with retry guidance
- [ ] Tool annotations set (`readOnlyHint`, `destructiveHint`) — helps agents and UIs warn before destructive calls
- [ ] Permissions scoped to minimum required — don't request admin if read is enough

---

## Bundled Reference

Read [tool-design.md](./references/tool-design.md) when defining a tool inventory, descriptions, schemas, and destructive-operation safeguards. It is a review aid; the project API contract remains the source of truth. For a JSON tool inventory, run `python scripts/validate_tool_contract.py tools.json` before implementation.

## Definition of Done — MCP Server

- [ ] All planned tools implemented with complete input schemas
- [ ] Every parameter has a `describe()` string
- [ ] Every error path returns an actionable error message (not a raw exception)
- [ ] Auth errors specifically explain how to fix the auth issue
- [ ] Tool annotations set on every tool
- [ ] Tested via MCP Inspector — all tools callable
- [ ] At least one automated test per tool
- [ ] README includes: what the server does, prerequisites, install steps, env vars, Claude Desktop config snippet
- [ ] No secrets in source, logs, or error responses
- [ ] Works with `npx @modelcontextprotocol/inspector` — passes manual smoke test
