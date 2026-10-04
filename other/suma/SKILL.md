---
name: suma
description: Use when operating or improving a Sumanos/Hermes agent from Codex through the Suma plugin and the `sumanos` MCP server.
---

# Suma for Codex

Suma connects Codex to the Sumanos authoring MCP.

```txt
MCP server id: sumanos (prod) | sumanos-dev (develop)
Endpoint prod: https://app.sumanos.com/mcp/authoring/agents/${SUMANOS_AGENT_ID}
Endpoint dev:  https://development.sumanos.com/mcp/authoring/agents/${SUMANOS_AGENT_ID}
Auth:          OAuth or admin API key in SUMANOS_KEY
```

## Operating flow

1. Check auth and available tools before changing anything.
2. Use `list_agents` first when the user names an agent.
3. Use `read_soul` before `edit_soul`; `edit_soul` replaces the full SOUL.
4. Preview meaningful changes before applying them.
5. Treat `install_plugin` and `set_credential` as high risk; they should be staged for human approval.
6. If operator workspace tools are available, verify changes with logs or direct reads.
7. End with a short report: changed, verified, staged, next step.
