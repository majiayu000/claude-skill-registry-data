---
name: "surface"
description: "Show ranked attack surface for a target. Invokes recon-ranker agent. Usage: /surface target.com"
---

# Surface

*Sourced from h-mmer-pentest-agents*

Rank attack surface for: $ARGUMENTS

1. Verify recon data exists in recon/ directory. If not, suggest /recon first.
2. Read brain data for this target.
3. Launch `recon-ranker` agent: "Rank the attack surface for $ARGUMENTS. Read recon/ for discovery data and brain for tested endpoints. Output P1/P2/Kill ranking."
4. Show the ranking to the user.
5. Suggest: `/hunt $ARGUMENTS` to start testing P1 targets.

## Top-Tier Surface Ranking

Rank by exploit economics.

P1 requires at least two of:
- crown-jewel function: auth, billing, admin, tenant data, integrations, uploads, exports, webhooks, AI/tool execution
- weak boundary: cross-tenant IDs, mixed roles, public/private transition, OAuth callback, parser boundary, file ingestion
- novelty: new asset, changed JS, low hacktivity coverage, unusual vendor or beta endpoint
- proof path: two-account test, clear callback, readable response, browser-verifiable sink, local PoC

Kill or P3 assets that are static marketing pages, hardened vendor panels with no program-owned data, or endpoints already exhausted with strong evidence. Every P1 must include the best first vuln class and first request to try.

