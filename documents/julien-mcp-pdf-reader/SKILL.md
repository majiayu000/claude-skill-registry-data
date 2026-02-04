---
name: julien-mcp-pdf-reader
description: Install PDF Reader MCP for document extraction. Use when user needs to read PDF content.
category: mcp
triggers:
  - install pdf reader mcp
  - pdf mcp
  - read pdf mcp
---

# MCP PDF Reader Installer

This skill installs the PDF Reader MCP server into the current project.

## Installation Procedure

When the user asks to install PDF Reader MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "pdf-reader": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@sylphlab/pdf-reader-mcp"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "pdf-reader": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@sylphlab/pdf-reader-mcp"]
    }
  }
}
```

## Prerequisites

- Node.js and npm installed

## Usage After Installation

Restart Claude Code to activate the MCP server. Provides PDF text extraction capabilities.

## Skill Chaining

- **Input**: User request to install PDF Reader MCP
- **Output**: Configured `.mcp.json` with pdf-reader server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Any document processing workflow

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npx` not found | Install Node.js and ensure npm is in PATH |
| PDF parsing error | Check PDF is not encrypted/password protected |
| Memory error | Large PDFs may need chunked processing |
| File not found | Use absolute paths for PDF files |
