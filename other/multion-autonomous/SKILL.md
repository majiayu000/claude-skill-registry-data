---
name: multion-autonomous
description: MultiOn autonomous web agents — natural-language browse, cloud sessions, local Chrome extension, parallel agents. Pair with Open-Connect MCP/Grok for motor-cortex style browser control.
---

# MultiOn Autonomous Browser (Open-Connect)

[MultiOn docs](https://docs.multion.ai/welcome) — **Motor Cortex layer for AI**: autonomous web actions with natural language.

## Why with Open-Connect

| Capability | How |
|------------|-----|
| **Cloud browser** | MultiOn remote sessions (`local: false`) |
| **Local browser** | Chrome extension + `local: true` |
| **Cloudflare headless** | `cloudflare-browser` skill (CDP on Workers) |
| **CLI agent browser** | `agent-browser` skill (snapshot/click/fill) |
| **Models / Grok** | Open-Connect `/v1` + `oc_live_` key |
| **MCP tools** | Open-Connect `/mcp` for agents that orchestrate MultiOn |

## Quick start

```bash
npm install multion
export MULTION_API_KEY=your_key
```

```ts
import { MultiOnClient } from "multion";

const multion = new MultiOnClient({ apiKey: process.env.MULTION_API_KEY });

const res = await multion.browse({
  cmd: "Find the top comment of the top post on Hacker News.",
  url: "https://news.ycombinator.com/",
  // local: true  // requires Chrome extension + API Enabled
});
```

HTTP:

```bash
curl -X POST https://api.multion.ai/v1/web/browse \
  -H "X_MULTION_API_KEY: $MULTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"cmd":"Summarize the homepage","url":"https://open-connect.site/"}'
```

## Open-Connect + Grok pattern

1. Mint `oc_live_` key in Open-Connect (scopes: models + tools).
2. Store MultiOn key in **Secrets** (`service_name=multion_api_key`).
3. Agent (Grok / Claude / Open WebUI) uses Open-Connect MCP + MultiOn browse.
4. Edge/headless without MultiOn: **cloudflare-browser** CDP skill.
5. Local CLI: **agent-browser** skill.

## Session modes

- **Remote (default):** isolated cloud headless browser, proxy support.
- **Local:** MultiOn Chrome extension; agent drives your browser.
- **Parallel:** concurrent agents (MultiOn docs).

## Security

- Never commit MultiOn keys; use Open-Connect Secrets / agent_vault.
- Prefer remote sessions for untrusted sites.
- Role scopes: developer+ for browser tools.

## Related packages

- `cloudflare-browser` — Cloudflare Browser Rendering CDP
- `agent-browser` — Agent browser CLI
- Integrations → MultiOn · Grok · Open WebUI

## Links

- https://docs.multion.ai/welcome
- https://docs.multion.ai/quick-start
- https://docs.multion.ai/api-reference/autonomous-api-reference/browse
- https://open-connect.site/integrations
