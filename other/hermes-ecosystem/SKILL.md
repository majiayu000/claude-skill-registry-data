---
name: hermes-ecosystem
description: Reference research on the Hermes Agent ecosystem — deployment templates, ecosystem maps, brain/memory layers, expert role packs, and community projects. Use whenever the user asks what else exists around Hermes Agent, how to extend it, or which community project to adopt.
---

# Hermes Ecosystem Projects

Use the curated selection heuristic below when the user wants a recommendation.

## Deployment Templates

| Repo | Stars | Forks | Updated | Value |
|------|-------|-------|---------|-------|
| `praveen-ks-2001/hermes-agent-template` | 200 | 172 | 2026-06-12 | Railway one-click deploy + admin dashboard. Manage config, gateway, user pairing from browser. Key envs: `ADMIN_PASSWORD`, `HERMES_REF`. Supports OpenRouter/DeepSeek/DashScope/GLM/Kimi/MiniMax/HF. Channels: TG/Discord/Slack/WhatsApp/Email/Mattermost/Matrix. |
| *(404)* `jinwon-int/wiki-agent` | — | — | — | Multi-node knowledge graph + agent collaboration. README unavailable. Cannot verify after 2026-06-13 check. |

## Ecosystem Maps & Indexes

| Repo | Stars | Forks | Value |
|------|-------|-------|-------|
| `ksimback/hermes-ecosystem` | 1,001 | 81 | "Hermes Atlas" — community map at hermesatlas.com. 80+ quality-filtered repos across 12 categories, live star sparklines, RAG chatbot (OpenRouter + Redis). |
| *(unverified)* Hermes Skill Registry | — | — | Supposed skill marketplace. Mentioned in @GitTrend0x tweet but no canonical repo identified. |

## Brain / Memory / Knowledge Graph

| Repo | Stars | Forks | License | Value |
|------|-------|-------|---------|-------|
| `garrytan/gbrain` | 22,464 | 3,227 | MIT | "Opinionated brain layer." Synthesis + self-wiring knowledge graph + dream cycle. P@5 49.1%, R@5 97.9% on BrainBench (+31.4 P@5 over graph-disabled). 15 page types. MCP clients: Claude Code / Codex / Cursor / ChatGPT / Perplexity / Claude Desktop. Quick-start: `gbrain init --pglite`. |
| *(mentioned)* Graphiti / Mnemosyne / YantrikDB | — | — | — | Knowledge graph plugin, memory observability dashboard, enterprise vector memory backend. Mentioned in tweet, no repos verified as of 2026-06-13. |

## Expert Role Packs

| Repo | Stars | Forks | License | Value |
|------|-------|-------|---------|-------|
| `jnMetaCode/agency-agents-zh` | 14,729 | 2,579 | MIT | 215 plug-and-play AI expert roles. 165 translated + 50 China-market original. 18 departments. 17 tools including Hermes Agent. Install: `./scripts/install.sh --tool hermes`. Works with `agency-orchestrator` for DAG multi-agent execution. |

## Pitfalls

- Twitter/X social posts frequently truncate project names and omit the actual repo link. Always resolve claims back to the canonical repo via `gh repo view`.
- `jinwon-int/wiki-agent` returned 404 in 2026-06-13 check; a link/tweet mentioning it is stale until a real repo exists.
- "Official" sounding tooling like Hermes Skill Registry may not yet have a public repository — treat tweets as leads, not sources of truth.
- GBrain claims strong metrics; only adopt after validating it against actual Hermes tool integration, not brand endorsements alone.
- GBrain's CLI requires `bun` runtime. If `bun` is unavailable, the GBrain CLI path is blocked; fall back to cloning the repo for study only. The full-install path needs `gbrain init --pglite` or Docker.
- `agency-agents-zh/scripts/convert.sh` writes Hermes-formatted skills into `integrations/hermes/` but does not copy them to `~/.hermes/skills/`. You still need `install.sh --tool hermes` to make them active.

## Curated Selection Heuristic

For direct Hermes carryover value:
1. **GBrain** — production-grade brain layer with published metrics, fastest path to durable Hermes memory.
2. **Agency Agents ZH** — immediate expert roster expansion, especially valuable for China-focused workflows.
- **Hermes Atlas** — ecosystem discovery surface when choosing future integrations. Prefer direct browsing of the cloned repo's `data/repos.json` over the live site when offline or API-constrained.
4. **hermes-agent-template** — only if Railway one-click deploy is the actual deployment target; otherwise a side project.

See also `references/ecosystem-projects.md` for raw README summaries and links.
