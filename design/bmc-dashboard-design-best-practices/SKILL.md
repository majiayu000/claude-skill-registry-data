---
name: bmc-dashboard-design-best-practices
description: >
  Researches best practices on similar dashboards, reviews them against BMC
  needs, and implements the most suitable aesthetic and functional design with
  time-saving as the main goal. Use when improving dashboard UX/UI, designing
  views for Finanzas/Operaciones/Cotizaciones/Ventas, or optimizing workflows
  for speed and clarity.
---

# BMC Dashboard Design — Best Practices & Time-Saving UX

Acts as a skilled designer of **visual design and functionality**. Research similar dashboards, align with BMC needs, then implement the most suitable aesthetic and functional solution. **Main task: saving time** (fewer clicks, clear actions, fast scanning, guided flows).

## When to Use

- Improving dashboard look and feel (aesthetic) or interaction (functionality).
- Designing or refining views for Finanzas, Operaciones, Cotizaciones, Ventas, or shell/nav.
- User asks for best practices, similar dashboards, or time-saving UX.
- Aligning new UI with DASHBOARD-FRONT-VISION (sheets as DB, actions, edit-from-dashboard).

## Workflow

1. **Before working:** Read `docs/team/knowledge/Design.md` if it exists. Read `docs/team/PROJECT-STATE.md` (changes, pendientes).
2. **Research** — Best practices on dashboards similar to BMC (operational/finance/quote/sales): layout, density, actions, filters, tables vs cards, loading states, mobile. Prefer concise bullets or a short reference; link to [reference.md](reference.md) for patterns.
3. **Review against our needs** — Map findings to BMC: sections (IA.md), data (planillas via API), actions (marcar entregado, costeo, administrar venta), and primary users (ops, finanzas, ventas). Call out what fits and what to adapt.
4. **Propose** — One or a few concrete options: layout, components, interaction (e.g. table + row actions, filters, modals for edit). State how each option **saves time** (fewer steps, less scrolling, one-click actions).
5. **Implement** — Apply the chosen approach in the repo: dashboard HTML/CSS/JS or React components, aligned with existing entry (3001/finanzas, 5173, 3849) and with DASHBOARD-FRONT-VISION (data from API, edit from dashboard, buttons for actions).
6. **After changes:** Update `docs/team/PROJECT-STATE.md` and write Log for [Agent] if the change affects Mapping or Networks.

## Principles (time-saving first)

- **Scan fast:** Key info above the fold; tables/cards with clear headers and stable column order.
- **Act in one place:** Primary actions (marcar entregado, costeo, administrar) as buttons per row or in a clear CTA; avoid “open sheet → find cell → edit.”
- **Fewer steps:** Filters and grouping instead of scrolling; modals or side panels for edit instead of new pages when possible.
- **Feedback:** Loading states, success/error messages, so the user knows the action ran.
- **Consistent:** Reuse patterns (e.g. table + actions) across Operaciones, Finanzas, Ventas so behavior is predictable.

## Sources

- **Our needs:** [DASHBOARD-FRONT-VISION.md](../../docs/bmc-dashboard-modernization/DASHBOARD-FRONT-VISION.md), [IA.md](../../docs/bmc-dashboard-modernization/IA.md), PLAN-PROPOSAL-PLANILLA-DASHBOARD-MAPPING (first task: functionality and localhost usage).
- **Existing UI:** `docs/bmc-dashboard-modernization/dashboard/`, `server/` (routes serving dashboard).
- **Patterns and references:** [reference.md](reference.md) (similar dashboards, layout patterns, time-saving checklist).

## Output

- Short **research summary** (best practices + fit with BMC).
- **Proposal** (option A/B with rationale and time-saving impact).
- **Implementation** in code (HTML/CSS/JS or components) plus any updates to docs (e.g. DASHBOARD-INTERFACE-MAP or IA) so the team knows what changed.
