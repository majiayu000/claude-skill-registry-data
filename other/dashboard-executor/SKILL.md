---
name: dashboard-executor
type: executor
description: "Execute dashboard implementations from dashboard-planner specs."
version: 0.1.0
---

# Dashboard Executor Skill

## When to Use

**Primary triggers:**
- "generate a dashboard", "build this dashboard", "create an interactive dashboard"
- "execute this dashboard plan", "generate from this dashboard spec"
- "make a KPI dashboard from this data"
- User has a dashboard-planner spec and wants an HTML dashboard generated
- User has a CSV/JSON file and wants a multi-chart dashboard

---

## Do Not Use When

- You need to **design** a dashboard — use `dashboard-planner` first
- You need to **review** an existing dashboard — use `dashboard-critic`
- You need a **single chart** — use `dataviz-executor`
- You need **statistical analysis** — analyze first, then visualize
- You need a **BI platform integration** (Tableau, Power BI) — this produces standalone HTML

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a dashboard-planner spec, need dashboard | This skill |
| Need to design the dashboard first | Use `dashboard-planner`, then come back |
| Have a dashboard, need architecture review | Use `dashboard-critic` |
| Have a dashboard, need individual chart review | Use `dataviz-critic` |
| Need a single chart, not a dashboard | Use `dataviz-executor` |
| Have raw data, need quick KPI dashboard | This skill — direct request mode (simple cases) |

---

## What You Get

- **Self-contained HTML file** with Plotly.js charts, CSS Grid layout, vanilla JS interactions
- **KPI cards** with big numbers, trend indicators, sparklines, and target comparison
- **Global filters** with debounced cascading and cross-filtering between charts
- **Responsive layout** at desktop (1280+), tablet (768-1279), mobile (<768)
- **Accessibility features**: ARIA landmarks, skip link, keyboard nav, alt text, screen reader support
- **Deviation log** documenting any departures from the planner spec
- **Critic handoff commands** for both dashboard-critic and dataviz-critic

---

## Input Modes

### Mode 1: Planner Spec (Preferred)
Provide the output from `dashboard-planner`. The executor parses the structured plan (Executive Summary, KPI Architecture, Information Architecture, Interaction Design, Accessibility Plan) and generates an HTML dashboard matching the spec.

### Mode 2: Direct Request (Simple Cases)
Provide a data file and describe the dashboard: "Create a KPI dashboard showing revenue, orders, and customer satisfaction from quarterly.csv." For simple dashboards (≤4 charts, clear KPIs), the executor generates with sensible defaults. For complex multi-level dashboards, redirects to `dashboard-planner`.

---

## Companion Skills

- **dashboard-planner** (upstream): Designs the dashboard architecture this executor implements
- **dashboard-critic** (downstream): Reviews the dashboard for KPI hierarchy, filter logic, responsive layout
- **dataviz-critic** (downstream): Reviews individual charts within the dashboard

---

## meta-router Registry Note

Listed under the **Executors** table.
Trigger signals: `generate dashboard, create dashboard, build dashboard, generate KPI dashboard, create interactive dashboard, execute dashboard plan`
