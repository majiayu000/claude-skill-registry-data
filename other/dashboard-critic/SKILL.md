---
name: dashboard-critic
type: critic
description: "Review dashboards for metric clarity, layout effectiveness, drill-down paths, and data integrity."
version: 0.1.0
---

# Dashboard Critic Skill

## When to Use

**Primary triggers:**
- "review this dashboard", "critique this dashboard", "is this dashboard well-designed?"
- "check the KPI hierarchy", "review the filter architecture"
- User has a dashboard implementation and wants architecture-level review
- Dashboard-executor just generated output and needs review

---

## Do Not Use When

- You need to **design** a dashboard — use `dashboard-planner`
- You need to **generate** a dashboard — use `dashboard-executor`
- You need to review a **single chart** — use `dataviz-critic`
- You need to review **code quality** — use a code reviewer
- The dashboard doesn't exist yet — plan first, review after

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a dashboard, need architecture review | This skill |
| Have a dashboard, need individual chart review | Use `dataviz-critic` |
| Need to design a dashboard | Use `dashboard-planner` |
| Need to generate a dashboard | Use `dashboard-executor` |
| Dashboard critic returns REVISE/REJECT | Route fixes to `dashboard-planner` for re-planning |

---

## What You Get

- **14-phase investigation** covering KPI hierarchy, information architecture, filters, drill-down, consistency, responsive, performance, accessibility
- **Multi-perspective review** from executive (3-second test), analyst (exploration), ops manager (monitoring), accessibility auditor
- **Severity-rated findings** (CRITICAL / MAJOR / MINOR / ENHANCEMENT) with evidence and fixes
- **Verdict** (REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT)
- **Gap analysis** identifying what's missing, not just what's wrong

---

## Key Review Areas

| Area | What's Evaluated |
|------|-----------------|
| KPI Hierarchy | Do primary → supporting → diagnostic metrics decompose logically? |
| Information Architecture | Does spatial layout support decision-making flow? |
| Filter Architecture | Do global filters cascade? Cross-filtering work? Sensible defaults? |
| Drill-Down Paths | Can users navigate deeper without losing context? |
| Cross-Chart Consistency | Same category = same color everywhere? Aligned time axes? |
| Responsive Layout | Does column collapse preserve comparison context? |
| Performance | Chart count, data volume, lazy loading, debounced filters? |
| Accessibility | ARIA landmarks, keyboard nav, screen reader, alt text, contrast? |

---

## Companion Skills

- **dashboard-planner** (upstream planner): Designs the dashboard architecture
- **dashboard-executor** (upstream executor): Generates the dashboard this critic reviews
- **dataviz-critic** (sibling): Reviews individual charts — use for chart-level encoding issues

---

## meta-router Registry Note

Listed under the **Critics** table.
Trigger signals: `review dashboard, critique dashboard, dashboard review, evaluate dashboard, dashboard architecture review, check dashboard KPIs`
