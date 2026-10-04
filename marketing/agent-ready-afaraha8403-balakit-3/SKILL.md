---
name: agent-ready
description: >-
  Make a public origin discoverable to AI agents: well-known discovery
  documents, crawl signals, auth metadata, agent protocol cards, and
  optional agentic commerce. Use when the user asks about agent-ready,
  well-known discovery, Auth.md, api-catalog, A2A, MCP server cards,
  WebMCP, DNS-AID, ACP, UCP, or x402. Stack- and host-agnostic: publish
  the HTTP contract from whatever already serves the site. For page SEO,
  crawl audits, and GEO strategy use seo-audit and everything-seo.
user-invocable: true
disable-model-invocation: false
version: "1.0.0"
author: "Ali Farahat"
tags: ["agent-ready", "agent-discovery", "well-known", "mcp", "a2a", "geo"]
when_to_use: |
  USE WHEN:
  - User asks to make a site or API agent-ready / agent-discoverable.
  - User mentions well-known agent documents, Auth.md, api-catalog,
    A2A agent cards, MCP server cards, WebMCP, DNS-AID, ACP, UCP, or x402.
  - A scanner or audit reports missing agent discovery endpoints.

  DO NOT USE WHEN:
  - User needs page SEO, titles, schema, or a crawl audit of public HTML
    (use seo-audit).
  - User needs ranking / GEO / digital PR strategy (use everything-seo).
  - User needs paid search (PPC).
---

# Agent-ready discovery

> **Leading words:** skip unless, well-known discovery, policy match,
> HTTP contract, stack-agnostic, host-agnostic.

Publish the **HTTP contract** (URL, status, Content-Type, required fields).
Serve it from origin, the static/public dir, or the edge in front of origin —
whatever already ships the site. Do not prescribe a host product or a
single framework.

Copy this file's phases into the todo list verbatim. Skipped steps stay
with `skip:` / `n/a:`.

## Phase 1 — Classify

```
- [ ] Name the origin (scheme + host). No hard-coded example domains.
- [ ] Public content? (HTML pages, blog, marketing)
- [ ] API? (programmatic surface agents might call)
- [ ] Agent product? (this origin hosts A2A, MCP, WebMCP, or outbound bot requests)
- [ ] Commerce? (agents can buy, pay, or check out)
```

🛑 **Checkpoint:** Write the four yes/no flags. Do not publish discovery
documents the classification did not select.

## Phase 2 — Crawl surface

Delegate robots.txt + sitemap **existence** to `seo-audit` if a page audit
is already in flight. This skill still owns **policy match** and optional
markdown negotiation.

```
- [ ] GET /robots.txt is text/plain 200 (RFC 9309). Sitemap: line if a sitemap exists.
- [ ] Content-Signal on robots.txt matches User-agent policy (search / ai-train / ai-input).
- [ ] GET /sitemap.xml is XML 200 listing canonical public URLs, or n/a: no public HTML.
- [ ] Optional: Accept: text/markdown on key pages returns markdown; HTML stays the default.
```

Pull [references/well-known-discovery.md](references/well-known-discovery.md)
only for Link headers / catalogs. Content-Signal detail lives with
`everything-seo` technical SEO.

🛑 **Checkpoint:** Policy is named (what search, train, and input are set to)
and User-agent lines match it. `skip:` if the origin has no public crawl surface.

## Phase 3 — Discovery documents that apply

```
- [ ] API catalog + Link headers — skip unless API
- [ ] Auth.md + OAuth/OIDC / protected-resource metadata — skip unless API with auth
- [ ] A2A card, agent-skills index, MCP server card, WebMCP — skip unless agent product
- [ ] Web Bot Auth JWKS — skip unless this origin sends bot/agent requests
- [ ] DNS-AID under _agents — skip unless agent product needs DNS discovery
- [ ] ACP / AP2 / MPP / UCP / x402 — skip unless commerce
```

Pull depth only for selected rows:

| File | When |
|---|---|
| [references/well-known-discovery.md](references/well-known-discovery.md) | api-catalog, Link, Auth.md, OAuth |
| [references/agent-protocols.md](references/agent-protocols.md) | A2A, skills index, MCP, WebMCP, Web Bot Auth, DNS-AID |
| [references/agentic-commerce.md](references/agentic-commerce.md) | ACP, AP2, MPP, UCP, x402 |

## Phase 4 — Verify

```
- [ ] For each published URL: GET it. Record status, Content-Type, required fields.
- [ ] Do not POST registration or payment endpoints during a passive check.
- [ ] List every skip: / n/a: with the classification reason.
```

Any miss on a selected document → back to Phase 3.

## Reply contract

1. Classification flags (content / API / agent product / commerce).
2. Published URLs that passed, with status + Content-Type.
3. Failures (URL + missing field).
4. Every `skip:` / `n/a:` line.

## What NOT to do

- **No host lock-in.** Do not tell the agent to use a specific CDN, DNS
  dashboard, or edge worker product.
- **No framework lock-in.** Do not require Next, Workers, or a named
  middleware package when the project's stack already has an equivalent.
- **No scanner lock-in.** A third-party agent-ready scanner is optional.
  The proof is the fetched document.
- **Do not invent endpoints** for a site that is not an API, agent
  product, or store.
- **Do not POST** `/agent/auth`, checkout, or payment during discovery.
