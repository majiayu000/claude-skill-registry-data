---
name: panelin-calculadora-knowledge-planner
description: Turns Panelin Signal / Knowledge Antenna outputs into evaluated improvement quests and concrete implementation plans for Calculadora BMC (https://calculadora-bmc.vercel.app). Reads magazine HTML and underlying JSON reports, maps news to repo areas, and produces scoped plans (full stack or single area). Use when the user asks for improvements from knowledge news, Panelin Signal, antenna magazine, knowledge run output, or implementation plans driven by external AI/platform updates.
---

# Panelin Calculadora — Knowledge News → Implementation Plans

## Role

Act as a **Calculadora BMC / Panelin** product+engineering lead: connect **fresh ecosystem signals** (Knowledge Antenna) to **this repo** and **production** ([Calculadora BMC on Vercel](https://calculadora-bmc.vercel.app)), then deliver **evaluated improvements** and **implementation plans**.

## Scope gate (first step)

1. Confirm **quest scope**:
   - **Full sweep** — all major areas (frontend, API, deploy, integrations, docs/ops), or
   - **Single area** — user names one (e.g. “solo calculadora”, “solo API Cloud Run”, “solo CRM/GPT”).
2. If unclear, default to **full sweep** with a short table of contents and mark P0 items.

## Inputs to read (in order)

Use **machine-readable sources first**; HTML magazine for narrative context.

| Purpose | Path |
|--------|------|
| Human magazine (latest) | `docs/team/knowledge/reports/KNOWLEDGE-MAGAZINE-latest.html` |
| Dated snapshot | `docs/team/knowledge/reports/KNOWLEDGE-MAGAZINE-YYYY-MM-DD.html` |
| References catalog | `docs/team/knowledge/references-catalog.json` |
| Impact map | `docs/team/knowledge/impact-map.json` |
| Source registry / ranks | `docs/team/knowledge/sources-registry.json` |
| Latest run log | `docs/team/knowledge/reports/KNOWLEDGE-REPORT-*.md` (newest by date in filename) |
| Consolidated DB + eval | `docs/team/knowledge/knowledge-db.json`, `docs/team/knowledge/reports/KNOWLEDGE-IMPROVEMENT-EVAL-*.md` |
| Direction tracker | `docs/team/knowledge/DEVELOPMENT-DIRECTION-TRACKER.md`, `development-direction-tracker.json` |
| Magazine generator (schema only) | `scripts/knowledge-antenna-magazine.mjs` — use to understand how sections map to JSON; do not treat HTML as the only source of truth |

**Stale data:** If inputs are old or empty, tell the user to run `npm run knowledge:run` or at least `npm run knowledge:magazine` after updating JSON.

## Project ground truth

- **Deployed SPA (reference UX):** [https://calculadora-bmc.vercel.app](https://calculadora-bmc.vercel.app)
- **Repo map:** `AGENTS.md`, `src/` (Vite/React), `server/` (Express API), `scripts/` (antenna, deploy, smoke), `docs/team/` (state, knowledge)
- **Do not** hardcode sheet IDs or secrets; follow existing env and AGENTS conventions.

## Evaluation method

For each **news item / reference / impact row** relevant to the quest:

1. **Signal** — one line: what changed externally.
2. **Relevance to Panelin** — tie to calculadora, API, CRM, ML, Shopify, deploy, or docs.
3. **Risk if ignored** — security, breakage, cost, UX, compliance (short).
4. **Effort** — S / M / L (rough).
5. **Evidence** — link from `references-catalog` or file targets from `impact-map`.

Prioritize **`priority: high`** mappings in `impact-map.json` when they overlap references.

## Implementation plan output (required format)

Produce a single markdown document (or sections in chat) with:

```markdown
# Quest: [short title from user or from top news theme]

## 0. Scope
- Areas: [list]
- Out of scope: [list]

## 1. Executive summary
[3–6 bullets]

## 2. Findings from Knowledge Antenna
| Source / ref | Insight | Repo touchpoints | Priority |

## 3. Recommended work packages
### P0 — [name]
- Goal:
- Files / modules:
- Verification: [e.g. npm run lint, npm test, smoke:prod, test:contracts]
- Rollout / flags:

### P1 — …

## 4. Open questions
- …

## 5. Propagation
- Update `docs/team/PROJECT-STATE.md` if work ships or gates change (per repo rules).
```

## Collaboration with other skills

- Deep calculator BOM/pricing: `.cursor/skills/bmc-calculadora-specialist/SKILL.md`
- Deploy / smoke: `.cursor/skills/bmc-calculadora-deploy-from-cursor/SKILL.md`
- Formal handoff doc shape: `.cursor/skills/bmc-implementation-plan-reporter/SKILL.md`

## Anti-patterns

- Do not invent vendor release facts not supported by the JSON/report links.
- Do not propose `rm -rf` or mass deletes without user approval (repo disk-space rules).
- Do not paste secrets or production tokens.

## Additional reference

- Area → folder mapping and artifact index: [reference.md](reference.md)
