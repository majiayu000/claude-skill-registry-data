---
name: bmc-holistic-project-health
description: >
  Evidence-based holistic snapshot of Calculadora BMC: project status from
  PROJECT-STATE, architecture areas (Vite SPA, Express API, Sheets/MATRIZ,
  ML/Shopify, Drive, Postgres, hub UI, GPT/MCP, CI), health commands
  (smoke:prod, gate:local, contracts, ml:verify), readiness % per area with
  explicit legend, recent developments, risks, and next steps. Use when the
  user asks for project health, architecture map, readiness report, full status
  snapshot, or interpret smoke/gate results across modules.
---

# BMC Holistic Project Health — Calculadora BMC

Single runbook for a **cross-cutting status report**: what the repo says, what checks proved this run, and what to do next—without duplicating deploy or full-team orchestration.

## Hard rules

1. **Evidence only:** Prefer [`docs/team/PROJECT-STATE.md`](../../../docs/team/PROJECT-STATE.md) (header **Última actualización**, **Cambios recientes**, **Pendientes** if present), then root [`AGENTS.md`](../../../AGENTS.md), [`CLAUDE.md`](../../../CLAUDE.md), [`README.md`](../../../README.md), [`docs/google-sheets-module/README.md`](../../../docs/google-sheets-module/README.md), [`docs/bmc-dashboard-modernization/DASHBOARD-INTERFACE-MAP.md`](../../../docs/bmc-dashboard-modernization/DASHBOARD-INTERFACE-MAP.md). For capabilities vs code: [`docs/api/AGENT-CAPABILITIES.json`](../../../docs/api/AGENT-CAPABILITIES.json) (regenerate with `npm run capabilities:snapshot` when needed; manifest in `server/agentCapabilitiesManifest.js`).
2. **No secrets:** Never paste `.env` values, tokens, or private URLs. Reference variable **names** only (see `.env.example`).
3. **No fabrication:** Do not assert prod OAuth, Sheets row counts, or CRM state without doc quote or command output from **this** run. If a check was not run, write **unknown — verify with: `<command>`**.
4. **503 semantics:** Per `AGENTS.md`, many upstream gaps surface as `503` (Sheets/IA unavailable)—do not relabel as generic “500” for Sheets.

## When to use

- User asks: project health, holistic status, architecture map, readiness %, “where are we”, executive snapshot, interpret last `smoke:prod` / gate, or **documented** next steps per area.
- After a large merge or before a stakeholder update (read-only narrative + optional checks).

## Delegate — do not duplicate

| Need | Follow |
|------|--------|
| Deploy, Cloud Run/Vercel rollback, env sync | [`bmc-calculadora-deploy-from-cursor`](../bmc-calculadora-deploy-from-cursor/SKILL.md) |
| Local vs prod verification pipeline, §4 propagation | [`bmc-cross-sync-propagation`](../bmc-cross-sync-propagation/SKILL.md) |
| Update `PROJECT-STATE` / full team / §4 protocol | [`bmc-project-team-sync`](../bmc-project-team-sync/SKILL.md), [`PROJECT-TEAM-FULL-COVERAGE.md`](../../../docs/team/PROJECT-TEAM-FULL-COVERAGE.md) |
| npm command reference | Root [`AGENTS.md`](../../../AGENTS.md) |

## Architecture areas (inventory checklist)

Use this list as **rows** in the output table; adjust labels if the repo grew—cite `CLAUDE.md` / `server/index.js` for new routes.

| Area | Primary paths / docs |
|------|----------------------|
| Frontend Vite SPA | `src/`, `PanelinCalculadoraV3_backup.jsx`, `src/data/constants.js`, `src/utils/calculations.js` |
| Express API | `server/index.js`, `server/config.js`, `server/routes/*` |
| Sheets / MATRIZ / CRM | `server/routes/bmcDashboard.js`, Sheets hub docs, `GET /api/actualizar-precios-calculadora` |
| ML / Shopify / webhooks | `server/routes/` + `.env.example` entries |
| Drive / GCS / PDF | `.env.example`, `server/routes/pdf.js` (and related) |
| Postgres / Transportista / Omni | `DATABASE_URL`, migrations per `AGENTS.md` |
| Hub / Wolfboard / dashboard UI | `DASHBOARD-INTERFACE-MAP.md`, hub modules under `src/` |
| GPT / MCP / OpenAPI | `docs/openapi*.yaml`, `docs/api/AGENT-CAPABILITIES.json`, `npm run mcp:panelin` |
| CI / quality | `.github/workflows/ci.yml`, `npm run gate:local*` |
| Docs / team process | `PROJECT-STATE.md`, `PROJECT-TEAM-FULL-COVERAGE.md` |

## Procedure (each run)

1. **Scope:** Note branch/commit (`git status -sb`, `git log -1 --oneline`) if available.
2. **Read** `docs/team/PROJECT-STATE.md` — capture **Última actualización** and the most relevant **Cambios recientes** bullets (last few).
3. **Health checks** (execute or explicitly mark skipped with reason):

| Command | Pass criteria |
|---------|----------------|
| `npm run smoke:prod` | Exit 0; script reports `/health`, `/capabilities`, `public_base_url` alignment, and MATRIZ CSV unless skipped per `AGENTS.md` (`SMOKE_SKIP_MATRIZ`, `-- --skip-matriz`) |
| `npm run gate:local` | ESLint clean on `src/`; `npm test` exit 0 |
| `npm run gate:local:full` | Gate local + `npm run build` exit 0 |
| `curl -sS http://localhost:3001/health` | After `npm run start:api`: HTTP 200, JSON `ok: true` |
| `npm run test:contracts` | With API on 3001: validator exit 0 |
| `npm run ml:verify` | When ML env configured: script exit 0 |

4. **Readiness %:** Apply the legend below to **each** architecture row. Lower the score for any unknown critical check.
5. **Risks:** Only items evidenced by PROJECT-STATE, failing commands, or linked human gates ([`docs/team/HUMAN-GATES-ONE-BY-ONE.md`](../../../docs/team/HUMAN-GATES-ONE-BY-ONE.md)).
6. **Deliverable:** Fill the **Output template** (next section). Optionally write `docs/team/reports/PROJECT-HEALTH-SNAPSHOT-YYYY-MM-DD.md` when the user wants a tracked snapshot.

## Readiness legend (required for every %)

- **100%:** Smoke + gate:local:full green this run, docs explicitly aligned, no evidenced blockers for that area.
- **85–99%:** Core checks green; minor gaps (optional E2E not run, non-critical doc lag).
- **70–84%:** Partial verification or some checks skipped; dependencies on secrets/human gates documented.
- **50–69%:** Known partial failures or unverified critical path for that area.
- **Below 50%:** Broken critical path for that area or **no** safe evidence—list verification commands.

## Output template

### Executive summary

5–8 sentences: posture, what changed recently (cite PROJECT-STATE dates), whether smoke/gate ran and passed **this run**, top 1–3 risks with evidence.

### Architecture map table

| Area | Responsibility | Evidence | Status | Readiness % | Objective | Impact | Next steps |
|------|----------------|----------|--------|-------------|-----------|--------|------------|
| … | … | path or doc § | one line | use legend | one line | one line | bullet(s) |

### Health checks table

| Command | Result this run | Notes |
|---------|-----------------|-------|
| … | pass / fail / skipped | excerpt or “not executed” |

### Recent developments

Bullets citing **dated** `PROJECT-STATE` **Cambios recientes** (optional `git log -5 --oneline`—flag if it diverges from PROJECT-STATE).

### Risks / blockers

Evidence-only list.

## Anti-duplication

Keep this file as the **index**. For deploy steps, OAuth gates, or orchestrator order, follow the delegated skills above.
