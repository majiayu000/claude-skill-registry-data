---
name: bmc-dependencies-service-mapper
description: >
  Connects all dependencies and maps all BMC Dashboard services so they work
  perfectly: dependency graph, service inventory, contracts, entry points,
  health checks. Use when connecting dependencies, mapping services, validating
  integration points, or ensuring end-to-end alignment across modules.
---

# BMC Dependencies & Service Mapper

The agent connects **all dependencies** and **maps all services** for the BMC Dashboard so the system works end-to-end. Outputs: dependency graph, service map, integration checklist.

## When to Use

- User asks to **connect all dependencies** or validate that modules are wired correctly.
- User asks to **map all services** so they work perfectly.
- Preparing or validating integration points between Cotizaciones, Operaciones, Finanzas, Ventas, Invoque Panelin, Shell/Infra.
- After Phase 2 or Phase 3 of the Full Improvement Plan: produce dependency/service artifacts from context briefs and the plan.

## Scope

- **Dependencies:** Per module (and globally): APIs consumed, env vars, Sheets, other modules. Document and align so nothing is missing or inconsistent.
- **Services:** Express routes (bmcDashboard, legacyQuote, calc), Vite app (5173), dashboard (3001/finanzas, 3849), Sheets API, ngrok, external (ML/Shopify if present). For each: contract (inputs/outputs), entry point (URL/port), health check, failure mode.

## Workflow

1. **Before working:** Read `docs/team/knowledge/Dependencies.md` if it exists. Read `docs/team/PROJECT-STATE.md` (cambios recientes, pendientes).
2. **Gather** — From context briefs (`context-briefs/`), `server/`, `src/`, env docs: list every module, its dependencies, and every service (route, app, integration).
3. **Dependency graph** — Produce a short dependency doc or table: Module → depends on (env, APIs, Sheets, other modules). Flag missing or conflicting deps.
4. **Service map** — Produce a service inventory table: Service name, Type (API route / app / integration), Entry point, Contract (key in/out), Health check, Owner (universe). Ensure entry points and ports (5173, 3001, 3849) are consistent.
5. **Integration checklist** — List integration points (e.g. Shell → Cotizaciones link, bmcDashboard → Sheets, Operaciones ↔ Finanzas). Mark status: OK, gap, or needs config.

## Outputs

- **Dependency doc:** `docs/bmc-dashboard-modernization/dependencies.md` (or appended to 02-investigation) — module → deps, gaps.
- **Service map:** `docs/bmc-dashboard-modernization/service-map.md` — services table, entry points, health checks.
- Optionally: update context briefs or improvement plan with dependency/service findings.

## Reference

- Dependency graph, service map, and integration checklist templates: [reference.md](reference.md).
- Modules and artifacts: PROMPT-AGENT-TEAM-FULL-IMPROVEMENT-PLAN.md § Reference.
- Backend routes: `server/routes/bmcDashboard.js`, `server/index.js`; ports and health: `/health`, 3001, 5173, 3849.
