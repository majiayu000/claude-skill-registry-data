---
name: meta-ads-remote
description: Access Meta Ads through Meta's official remote MCP server at https://mcp.facebook.com/ads.
  Use when Codex needs to inspect Meta Ads accounts, campaigns, ad sets, ads, creatives,
  delivery, spend, pacing, or insights for paid media analysis, especially Afinz reporting
  and paid media diagnostics.
metadata:
  version: 1.0.0
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Mídia paga
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Meta Ads Remote

Use the Meta Ads MCP tools exposed by the remote server. Prefer read-only inspection and analysis unless the user explicitly asks for a write action and the exposed tool clearly supports it.

When analyzing Afinz paid media:

- Start by listing available ad accounts and confirm the relevant account before querying campaigns.
- Use closed-day date ranges for reporting unless the user explicitly asks for same-day data.
- Keep Meta platform metrics separate from business CAC/card metrics unless an attribution source reconciles them.
- Report campaign, ad set, ad, and creative granularity when the MCP tools expose those levels.
- Treat MCP authentication failures as an OAuth/session issue, not as missing data.

Do not ask the user to paste Meta tokens in chat. The official remote MCP should authenticate through the Codex/Meta OAuth flow.
