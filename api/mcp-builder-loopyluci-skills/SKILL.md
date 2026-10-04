---
name: mcp-builder
description: Use when building MCP servers for AI agent tools.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [mcp, model-context-protocol, api, typescript, python]
---

# MCP Server Development Guide

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

## Process

### Phase 1: Deep Research and Planning

**Design Principles:**
- Balance comprehensive API endpoint coverage with specialized workflow tools
- Use clear, descriptive tool names with consistent prefixes
- Design tools that return focused, relevant data
- Error messages should guide agents toward solutions

**Recommended Stack:**
- **Language**: TypeScript (preferred) or Python
- **Transport**: Streamable HTTP for remote, stdio for local

### Phase 2: Implementation

**Project Structure:**
```
mcp-server/
├── src/
│   ├── index.ts (or .py)
│   ├── tools/
│   └── utils/
├── package.json (or pyproject.toml)
└── tsconfig.json
```

**TypeScript Implementation:**
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

server.tool(
  "my_tool",
  { param: z.string().describe("Description of param") },
  async ({ param }) => {
    return { content: [{ type: "text", text: `Result: ${param}` }] };
  }
);
```

**Python Implementation:**
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Description of my tool."""
    return f"Result: {param}"
```

### Phase 3: Review and Test

```bash
# TypeScript
npm run build
npx @modelcontextprotocol/inspector

# Python
python -m py_compile your_server.py
```

### Phase 4: Create Evaluations

Create 10 complex, realistic questions that require multiple tool calls to answer, saved as XML.

## Common Pitfalls

- ❌ **Vague tool descriptions** — Agents need clear, action-oriented descriptions
- ❌ **Poor error messages** — Always guide toward solutions
- ❌ **Missing pagination** — Large results overwhelm context
- ❌ **Ignoring authentication** — Secure credential handling is essential
- ❌ **No output schemas** — Structured data helps agents process results

## Verification Checklist

- [ ] Server compiles and runs without errors
- [ ] Tools have clear names and descriptions
- [ ] Error messages are actionable (guide toward solutions)
- [ ] Authentication is properly handled
- [ ] Pagination supported for list operations
- [ ] MCP Inspector test passes for all tools
- [ ] Evaluations created with 10+ realistic questions
