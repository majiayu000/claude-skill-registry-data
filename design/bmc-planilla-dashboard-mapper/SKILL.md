---
name: bmc-planilla-dashboard-mapper
description: >
  Maps both planillas (Google Sheets/templates) and the dashboard interface so
  the agent knows where each element lives. Produces a plan and proposal before
  implementation. Use when mapping planillas and dashboard UI together, defining
  where templates vs interface components live, or generating the mapping plan
  and proposal for sheet + dashboard.
---

# BMC Planilla & Dashboard Mapper

Maps **planillas** (sheets/templates) and **dashboard interface** in one pass so we understand where each piece lives. **Always produce a plan and proposal first**; implement mapping only after the plan is agreed.

## When to Use

- Mapping both planillas (sheets/templates) and dashboard interface.
- Defining where each element lives (which sheet/tab, which UI section/component).
- Generating the **plan and proposal** for how mapping will be done before implementation.
- User provides information about each planilla or dashboard section; agent applies it against the plan.

## Rule: Plan and Proposal Before Implementation

1. **First:** Generate or update the **plan-and-proposal** document (see [references/plan-proposal.md](references/plan-proposal.md) and `docs/bmc-dashboard-modernization/PLAN-PROPOSAL-PLANILLA-DASHBOARD-MAPPING.md`). It must state:
   - What we are mapping (planillas/templates vs dashboard UI).
   - How we will map each (sources, structure, outputs).
   - Where each mapping artifact will live.
   - Order and dependencies (e.g. sheet map before UI map if UI consumes sheet data).
2. **Then:** When the user provides information about each planilla or dashboard section, execute the mapping according to the plan and write to the agreed artifacts.

Do not implement mapping without a written plan and proposal (or explicit user approval of the existing one).

## Scope

- **Planillas (sheets/templates):** All relevant tabs, columns, data types, validation, and which API or UI consumes them. Reuse structure from [google-sheets-mapping-agent](.cursor/skills/google-sheets-mapping-agent/): sheet inventory, GET/PUSH, relationships.
- **Dashboard interface:** Sections (Inicio, Cotizaciones, Operaciones, Finanzas, Ventas, Invoque Panelin), UI blocks (tables, cards, forms), entry points (URLs, ports), and which planilla/API feeds each block. Use DASHBOARD-VISUAL-MAP.md and IA.md as sources.

## Outputs (from plan)

- **Planilla map:** Sheet(s) inventory, per-sheet column/type/validation, GET/PUSH, and which dashboard section or API uses it. Location: e.g. `docs/google-sheets-module/` or mapping-agent output.
- **Dashboard interface map:** Section → UI blocks → data source (API route, sheet). Location: e.g. `docs/bmc-dashboard-modernization/` or extend DASHBOARD-VISUAL-MAP.
- **Cross-reference:** Table or matrix: Planilla/template ↔ Dashboard section/component ↔ API route. So we know "where each one is."

**Canonical files (do not fork):** update the existing hub at `docs/google-sheets-module/README.md` and keep `MAPPER-PRECISO-PLANILLAS-CODIGO.md` (code truth), `SYNC-FULL-TEAM-SHEETS-ACCESS-MAP.md` (product access), and `VARIABLES-Y-MAPEO-UNO-A-UNO.md` in sync when the mapping changes — do not add parallel “mapper v2” docs without deprecating the old ones.

## Workflow

1. **Before working:** Read `docs/team/knowledge/Mapping.md` if it exists (convenciones, handoffs). Read `docs/team/PROJECT-STATE.md` if it exists (changes, pendientes).
2. Read or create `docs/bmc-dashboard-modernization/PLAN-PROPOSAL-PLANILLA-DASHBOARD-MAPPING.md`.
2. If the user provides new information (planilla names, UI sections, etc.), update the plan/proposal to include it and state where it will be documented.
3. Only after the plan is in place (and agreed if needed): produce the planilla map and dashboard interface map per the plan.
4. Produce or update the cross-reference (planilla ↔ dashboard ↔ API).
5. **After changes:** Update `docs/PROJECT-STATE.md` (Cambios recientes, Pendientes) and write Log for [Agent] if the change affects Design or Networks.

## Reference

- Plan and proposal template: [references/plan-proposal.md](references/plan-proposal.md). Live plan: `docs/bmc-dashboard-modernization/PLAN-PROPOSAL-PLANILLA-DASHBOARD-MAPPING.md`.
- Existing sheet mapping: google-sheets-mapping-agent; existing visual map: `docs/bmc-dashboard-modernization/DASHBOARD-VISUAL-MAP.md`, IA.md.
