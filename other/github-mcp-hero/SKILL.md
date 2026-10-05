---
name: github-mcp-hero
description: Governed GitHub over MCP; read is admitted, out-of-scope mutation is sealed as a denial.
---
# GitHub MCP Hero

This example drives a deterministic GitHub-shaped MCP fixture through the native
`mcp` source front. The read runner grants `repo.read` and seals a read-only issue
snapshot. The refusal runner grants the same read scope, then attempts a mutating
comment step that requires `repo.write`; the provider-permission effect blocks it
before the MCP mutation tool runs and seals a blocked graph receipt.
