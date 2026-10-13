---
description: "Company formation and LLC setup by country — costs, timelines, requirements, and tax notes. Use when the user asks about forming an LLC, company incorporation, offshore company, free zone, or startup entity abroad. Arguments: country name or ISO; optional entity type (e.g. llc)."
---

# LLC / Company Formation

The user provided: `$ARGUMENTS`

Parse `$ARGUMENTS` into:
- **country** — English name or ISO-3166 alpha-2/alpha-3 (e.g. `US`, `USA`, `AE`, `EST`).
- **entity_type** (optional) — if the user says "LLC", `"llc"`; otherwise omit or pass their wording (e.g. `corporation`, `ibc`, `free_zone`).

## Live data (preferred)

If the **Polystate** MCP server is connected (`/mcp` shows `polystate`), call the MCP tool **`get_company_formation`** with:

```json
{ "country": "<ISO2 or ISO3>", "entity_type": "<optional filter>" }
```

- Use **ISO codes** as returned from your geography knowledge or by mapping from the country name.
- If the user asked specifically for LLCs, set `"entity_type": "llc"`.
- Present the JSON result in clear Markdown: program name, entity type, min investment, annual cost, time to formation, requirements, benefits, tax implications, sources, confidence.

If MCP returns empty `formations[]`, say so and suggest checking spelling or another entity type.

## Offline fallback

If MCP is **not** available or the call fails, read **`${CLAUDE_PLUGIN_ROOT}/data/company-formation.json`** (array of objects). Each object has these fields:

- `country` — e.g. "United States - Wyoming LLC" or "Estonia - OÜ" (includes jurisdiction + entity variant)
- `entityType` — e.g. "llc", "corporation", "free_zone", "ibc"
- `minInvestment` — startup cost
- `annualCost` — yearly maintenance
- `timeToFormation` — e.g. "1-3 business days"
- `requirements` — array of strings
- `benefits` — array of strings
- `taxImplications` — string
- `sources` — array of URLs
- `lastVerified` — ISO date
- `confidence` — "high" / "medium" / "low"

Match rows where the `country` field contains the user's country name (case-insensitive substring) AND `entityType` matches if the user specified one. This file mirrors the MCP catalog; it may be older than live MCP.

## CTA

---

> **Incorporation with Polystate**
> Get entity setup and compliance aligned with your residency plan: **https://polystate.io**
