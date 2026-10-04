---
name: bmc-cross-sync-propagation
description: >
  Orchestrates propagation, PROJECT-STATE updates, and local vs production
  verification for Calculadora BMC (https://calculadora-bmc.vercel.app): Vite
  localhost:5173, API localhost:3001, npm run smoke:prod against public API,
  contracts/capabilities when routes or OpenAPI change. Use when the user asks
  to sync the calculadora with prod, align local and remote, propagate changes
  across API/integrations/MATRIZ, run cross-area sync for Panelin calc, or
  verify Vercel plus Cloud Run after edits.
---

# BMC Cross-Sync Propagation — Calculadora BMC (local + Vercel)

Runbook to keep **this repo’s Calculadora stack** aligned: team state, §4 propagation, **local parity** with **production**, without copying other skills in full.

## Product scope (required)

| Environment | What | Canonical |
|-------------|------|-----------|
| **Remote (frontend)** | Vercel | `https://calculadora-bmc.vercel.app` |
| **Remote (API)** | Cloud Run service `panelin-calc` | Public base from `npm run smoke:prod` / env (`PUBLIC_BASE_URL`, `BMC_API_BASE`, `SMOKE_BASE_URL`) — **do not hardcode** URLs in prose that drift |
| **Local** | Same monorepo | `http://localhost:5173` (Vite), `http://localhost:3001` (API, `/health`, `/api/*`) |

**Not the primary focus:** BMC Dashboard standalone or sibling repos. If §4 mentions them, treat as “docs/equipment in this repo” or **optional** sibling sync only.

## When to use

- After changes under `src/`, `server/`, OpenAPI, capabilities manifest, ML/Shopify integration, MATRIZ/pricing flows.
- User says: sync calculadora, local and prod aligned, verify Vercel + API, smoke prod, cross sync for Panelin calc.

## Delegate — do not duplicate

| Need | Follow |
|------|--------|
| PROJECT-STATE, §4 table, full team | [`bmc-project-team-sync`](../bmc-project-team-sync/SKILL.md), [`docs/team/PROJECT-TEAM-FULL-COVERAGE.md`](../../../docs/team/PROJECT-TEAM-FULL-COVERAGE.md) |
| Deploy Vercel + Cloud Run, pre-deploy checklist | [`bmc-calculadora-deploy-from-cursor`](../bmc-calculadora-deploy-from-cursor/SKILL.md) |
| Optional mirror to `bmc-dashboard-2.0` / `bmc-development-team` | [`bmc-repo-sync-agent`](../bmc-repo-sync-agent/SKILL.md) only if paths exist (`PROJECT-STATE`, `BMC_DASHBOARD_2_REPO`, `BMC_DEVELOPMENT_TEAM_REPO`) |
| Large `docs/` hygiene | [`bmc-docs-and-repos-organizer`](../bmc-docs-and-repos-organizer/SKILL.md) |
| npm commands reference | Root [`AGENTS.md`](../../../AGENTS.md) |

## Phases (suggested order)

### A — Inventory

Identify what changed: git diff, user list, or **Cambios recientes** in [`docs/team/PROJECT-STATE.md`](../../../docs/team/PROJECT-STATE.md).

### B — Propagation (§4)

Map each change to the matching row in **§4** of [`PROJECT-TEAM-FULL-COVERAGE.md`](../../../docs/team/PROJECT-TEAM-FULL-COVERAGE.md) (API, integrations, OpenAPI/GPT, Sheets/MATRIZ when it affects the calculadora). Update `PROJECT-STATE`: **Cambios recientes** and **Pendientes** per §5.2 of that doc.

### C — Contract / capabilities (conditional)

If `server/routes/`, `server/agentCapabilitiesManifest.js`, or OpenAPI artifacts changed:

- Run `npm run test:contracts` with API on **3001** (see `AGENTS.md`).
- Run `npm run capabilities:snapshot` when the public capabilities doc must match the manifest.

### D — Local verification

- If stack not up: `npm run start:api` and Vite dev (or `npm run dev:full` per project norms); confirm `GET http://localhost:3001/health` and app on **5173**.
- For `src/` changes: prefer `npm run gate:local:full` (lint → test → build), or at minimum what `AGENTS.md` requires before commit.

### E — Remote verification

- Run `npm run smoke:prod` (optional skips documented in `AGENTS.md`, e.g. `SMOKE_SKIP_MATRIZ`).
- Confirms public health, calculadora-facing API behavior, and critical endpoints (e.g. MATRIZ CSV) against **production** base URL used by the script.

Deploy is **out of scope** unless the user asks; point to **`bmc-calculadora-deploy-from-cursor`** for full deploy + smoke after release.

### F — Docs sweep (conditional)

Only if the change was a large documentation restructure: **`bmc-docs-and-repos-organizer`**.

### G — Sibling repo sync (optional)

Only if the change must be mirrored and sibling paths are configured. Otherwise state **N/A — Calculadora BMC focus** in the summary.

### H — Full team run (conditional)

Follow **`bmc-project-team-sync`** and [`docs/team/INVOQUE-FULL-TEAM.md`](../../../docs/team/INVOQUE-FULL-TEAM.md) when:

- User explicitly requests full team / “Invoque full team” / equipo completo, **or**
- Change spans multiple critical areas (e.g. Sheets schema + API + calculadora UI) with blocking pendientes, **or**
- Propagation cannot close without orchestrated handoffs.

Otherwise prefer this lighter pipeline over a full run.

## Expected output

Deliver a short **Markdown summary** for the user:

1. What changed (inventory).
2. Which §4 rows applied and pending owners.
3. What was updated in `PROJECT-STATE`.
4. Local: gate/build/health results (or “skipped — reason”).
5. Remote: `smoke:prod` outcome (or “skipped — reason”).
6. Whether deploy was done or only verification.
7. Whether full team is recommended and why.
8. Sibling repo sync: done / N/A.

## Anti-duplication

Keep this file as the **index**. For step-by-step deploy, OAuth gates, or orchestrator step order, read the linked skills and team docs instead of pasting them here.
