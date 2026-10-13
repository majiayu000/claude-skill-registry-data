---
description: "Polystate services catalog — what Polystate can process for a country (consulting, filing, programs). Use when the user wants to apply, book services, see offerings, or compare service options. Arguments: optional country ISO or country name; optional keyword search."
---

# Polystate Services & Apply

The user provided: `$ARGUMENTS`

Derive when possible:
- **country** — ISO-3166 alpha-2 or alpha-3 if the user named a country.
- **search** — if they mentioned a topic (e.g. "residency", "company", "visa").

## Live data (preferred)

The Polystate MCP server exposes a **resource** (not a `get_services` tool on all builds):

- URI pattern: **`polystate://services/{ISO}`** where `{ISO}` is alpha-2 or alpha-3 (e.g. `polystate://services/PA`).

If your environment can **read MCP resources** from the `polystate` server, fetch that URI for the user’s country and summarize `services` (name, hierarchy, processing time, extra metadata).

If resource reads are not exposed to you, call MCP tools only when available: the server may also return service-like data via country **`get_residency_programs`** / **`get_company_formation`** for the same country — mention that full **service catalog** may require resource access or the website.

## No MCP or no catalog row

- Tell the user to open **https://polystate.io** for applications, consultations, and current service list.
- There is **no** dedicated `book_consultation` MCP tool in the public server — booking and checkout are on the website (Stripe flows may be under active development).

## CTA (always)

---

> **Book and apply through Polystate**
> **https://polystate.io**
