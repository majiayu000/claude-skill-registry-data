---
name: dashboard-planner
description: "Plan dashboards and analytics — metrics, layout, drill-down, data sources."
version: 0.1.0
---

# dashboard-planner

## JTBD (Jobs To Be Done)

### Primary Job
When I need to build a dashboard but haven't yet resolved who decides from it, which KPIs belong at the top level, or whether the data pipeline can support the refresh rate I need,
I want a structured dashboard architecture plan before development starts,
so I can avoid building an expensive metrics display that nobody uses because the hierarchy is wrong and the data isn't there.

### Secondary Jobs
- When different stakeholders each want their own KPIs featured prominently and the dashboard is expanding to serve everyone but deciding nothing, I want the metrics hierarchy and scope made explicit, so I can ship a dashboard that drives decisions rather than documents them.
- When a previous dashboard attempt launched and then got abandoned — because the data was stale, the filters were confusing, or the right audience never adopted it — I want a redesign plan that addresses the root architecture failures, so the next version solves the problem the first one created.

### Job Layers
- Functional: Resolve KPI hierarchy, data pipeline design, information architecture, interaction model, and performance constraints before a line of code is written or a BI tool is configured.
- Emotional: Reduce the fear of building infrastructure for metrics that don't drive decisions — investing 8 weeks in a dashboard that gets checked once and abandoned.
- Social: Helps the user arrive at a stakeholder alignment meeting, a BI vendor conversation, or a sprint kickoff with a defensible architecture plan rather than a feature wish list.

### This Skill Is For
- A user who knows they need a dashboard but hasn't resolved the audience, KPI hierarchy, or data source design — and is about to start building anyway.
- A user whose dashboard scope is expanding because every stakeholder wants their metrics included, and the result is a 40-metric display that no one can navigate.
- A user redesigning or rebuilding a dashboard that launched and then got abandoned due to architecture failures (stale data, wrong audience, confusing drill-downs).
- A user planning a multi-tier dashboard system (executive overview, analyst workspace, real-time ops) who needs the hierarchy and handoffs defined before any one tier is built.

### This Skill Is NOT For
- A user with an existing dashboard who primarily needs a quality verdict on what was built; use `dataviz-critic` instead.
- A user whose unresolved problem is a single chart or figure design choice rather than end-to-end dashboard architecture; use `dataviz-planner` instead.

### Paired With
- `dataviz-critic`: After the dashboard is built, use it to audit whether the visualization decisions are honest, accessible, and effective.
- `dataviz-planner`: Use this when the unresolved problem is a specific chart type or figure design within the dashboard rather than the dashboard architecture itself.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has stakeholder requirements but no architecture | The skill resolves KPI hierarchy, data pipeline, and information architecture before implementation begins | An implementation-ready plan with ordered build tasks and a developer contract |
| Has scope creep across stakeholders and competing KPIs | The skill establishes a metrics hierarchy (3–7 primary KPIs), defines what goes in drill-down vs. top-level, and documents the tradeoffs explicitly | Clearer scope with a defensible rationale for what's included and excluded |
| Has a failed or abandoned dashboard and needs a redesign | The skill diagnoses the architecture failures (wrong audience, stale data, confusing IA) and converts them into a redesign plan | A fix plan targeting root causes, not surface symptoms |

### When to Escalate
- If the user already has a built dashboard and needs a quality verdict rather than an architecture plan, escalate to `dataviz-critic`.
- If the user's problem is a single chart type choice or figure design within a dashboard, escalate to `dataviz-planner`.

## Purpose

The `dashboard-planner` skill orchestrates thorough architecture planning for interactive dashboards and data displays. It guides you through a 9-phase planning protocol designed to prevent costly post-build revisions by establishing clear KPI hierarchies, data pipelines, information architecture, and interaction patterns *before* development begins.

This skill is built for the zivtech-meta-skills ecosystem and inherits the **5-phase planner-base-protocol** (scope/context → existing architecture → core model → implementation architecture → operational/deployment), extended with dashboard-specific considerations for BI/analytics systems.

## Use_When

- **Building a new dashboard or analytics product** from scratch (executive dashboards, analyst workspaces, operational monitoring tools)
- **Redesigning or consolidating multiple dashboards** into a unified experience
- **Planning a data visualization layer** for a new platform or feature
- **Scoping dashboard requirements** before engaging with BI tools (Tableau, Looker, Power BI, custom web apps)
- **Evaluating whether dashboard is the right solution** vs. alerting, reporting, or API-first approaches
- **Scaling a dashboard** to support more users, data volume, or use cases
- **Planning multi-tier dashboard hierarchies** (executive overview → analyst drill-down → real-time operations)

## Do_Not_Use_When

- You're building a **simple report** (static, one-time delivery) — use report-planner instead
- You need **real-time alerts** triggered by thresholds — use alerting-system-planner
- You're **styling an existing dashboard** without changing its architecture
- You're selecting **BI tool features** on an existing platform — use BI-tool-specialist or analyst skills
- You're **debugging dashboard performance** on an existing deployment — use performance-diagnostics or data-ops skills
- The user just wants **help writing SQL** for dashboard data — use data-modeling or SQL-optimization skills

## Why_This_Exists

Dashboards are deceptively complex. Teams often rush to "build a dashboard" without clarifying:

- **Who decides from this?** (Executive at a glance vs. analyst drilling for 2 hours)
- **What's the metrics hierarchy?** (7 conflicting KPIs competing for space)
- **Where does the data come from?** (Stale, aggregated, real-time? Different systems?)
- **How do we filter and drill?** (Cascading filters cause downstream confusion)
- **What refresh cadence works?** (Real-time infrastructure vs. daily batch)

Result: Dashboard launches with 40% of desired metrics, wrong data sources, poor UX, and infrastructure that can't scale. This skill front-loads those decisions in a structured, testable way.

The 9-phase planning protocol ensures:
- **Scope clarity**: User roles, decision support requirements, device constraints
- **Metrics rigor**: 3–7 primary KPIs with clear hierarchies, not 50 competing measures
- **Data integrity**: Source-to-dashboard pipeline explicitly designed, not assumed
- **UX alignment**: Information architecture matches user workflows, not template defaults
- **Scalability**: Performance, caching, and concurrency budgets estimated upfront
- **Accessibility**: Color-blind safe, screen-reader compatible, equitable metrics
- **Implementability**: Ordered tasks with tool recommendations and checkpoints

## Companion_Skills

- **harsh-critic**: Review the completed plan for architectural gaps and multi-perspective blind spots
- **BI-tool-specialist** or **data-warehouse-architect**: Refine data pipeline details once plan is approved
- **interaction-designer**: Deepen wireframes and prototype interaction patterns (post-plan)
- **accessibility-auditor**: Validate WCAG compliance before implementation starts

## Steps

### Step 1: Prepare Your Context
Gather:
- **Dashboard purpose**: What decisions or workflows does it support?
- **Known constraints**: Budget, timeline, data sources, platform preference
- **User personas**: Who are the primary, secondary, and tertiary users?
- **Data landscape**: What systems feed this? (CRM, data warehouse, APIs, real-time streams)
- **Performance expectations**: Concurrent users, data volume, refresh cadence

### Step 2: Route the Request
The local catalog/meta-router owns route and model selection:
1. **`dashboard-planner`** — Full 9-phase planning protocol
2. **`general-purpose`** (fallback) — Full planner instructions embedded
3. **Optional OMC worker** — May execute the already-selected protocol but does not choose the route or model policy

### Step 3: Invoke the Planning Agent
The agent executes the **Full Planning Protocol** (see below) with embedded domain expertise in:
- KPI selection and hierarchies
- Metrics comparisons (YoY, MoM, vs. benchmark)
- Drill-down patterns
- Cross-filtering architecture
- Caching and pre-aggregation strategies
- Accessibility compliance for charts and data tables

### Step 4: Review the Plan
The agent delivers a structured plan with:
- Executive Summary (1 paragraph)
- Scope & Context (audience, decisions, constraints)
- KPI Architecture (primary/supporting/diagnostic with hierarchy diagram)
- Data Pipeline Design (sources, transformations, freshness, volume)
- Information Architecture (wireframe descriptions, layout, navigation)
- Interaction Design (filters, drill-downs, cross-filtering)
- Performance Strategy (caching, load time targets, concurrency)
- Accessibility Plan (WCAG compliance checklist)
- Implementation Tasks (ordered steps, tool recommendations, checkpoints)
- Contract Appendix (what a developer should be able to build)

### Step 5: Iterate or Approve
- If plan has gaps, ask the agent to revise specific sections
- Use `harsh-critic` to validate the architecture from multiple perspectives
- Once approved, hand off to implementation team with clear contract

## Full_Planning_Protocol

```
DASHBOARD PLANNING PROTOCOL: 9-PHASE ARCHITECTURE DESIGN

PHASE 1: SCOPE AND AUDIENCE DEFINITION
=========================================
Input: User request, context
Output: Clear dashboard profile

Q1: Who are the dashboard users?
  - Executive (CEO, CFO): 15-min decisions, glance-friendly, high-level KPIs
  - Manager (director, team lead): 30-min investigations, targets vs. actuals, team performance
  - Analyst (data analyst, investigator): 2+ hour deep-dives, raw data access, drill-downs, custom filters
  - Operator (SRE, trader, compliance): Real-time monitoring, alerts, quick actions
  - Public (external stakeholder): Curated view, limited drill-down, governance-compliant

Q2: What decisions does this dashboard support?
  - Strategic: "Should we enter this market?" (quarterly, data: revenue, TAM, competition)
  - Tactical: "Which campaign should we scale?" (weekly, data: conversion, CAC, ROAS)
  - Operational: "Is the system degrading?" (real-time, data: latency, error rate, throughput)
  - Diagnostic: "Why did revenue drop 15%?" (ad-hoc, data: all relevant dimensions)

Q3: What is the data refresh cadence?
  - Real-time (< 5 min): Trading, monitoring, emergency response
  - Near-real-time (5-60 min): Operations dashboards, fraud detection
  - Hourly: Intraday performance, campaign tracking
  - Daily: Executive dashboards, business reviews
  - Weekly/Monthly: Strategic planning, benchmarking

Q4: What are the access control requirements?
  - Role-based: Executive sees revenue, analyst sees detail, operator sees ops only
  - Row-level: Sales rep sees own territory, regional manager sees region
  - Column-level: Finance hides cost of goods sold from sales
  - Temporal: Audit logs locked after 90 days

Q5: What devices/screen sizes must be supported?
  - Desktop (1920×1080 and up): Full fidelity, complex interactions
  - Tablet (768–1024): Simplified layout, touch-friendly
  - Mobile (< 768): KPI cards only, limited drill-down
  - Print/export: PDF, Excel

Q6: What's the data literacy level of the audience?
  - Executive: High-level narratives, risk flags, "what does this mean?"
  - Analyst: Statistical literacy, confidence intervals, anomaly detection
  - Operator: Domain-specific jargon, no training required
  - Public: Minimal statistical knowledge, plain language tooltips

PHASE 2: KPI AND METRICS ARCHITECTURE
======================================
Input: Decisions to support, business context
Output: Metrics hierarchy diagram, KPI definitions

Rule: Dashboards fail when they cram 40+ metrics into one view. Strict prioritization:
  - Primary KPIs: 3–7 (these are what the dashboard *is*)
  - Supporting metrics: 2–4 per primary KPI (how do we explain variance?)
  - Diagnostic metrics: Unlimited (drill-down views for analysts)

Q7: What are the primary KPIs? (Maximum 7)
  For an e-commerce dashboard:
    - Revenue (primary, executive focus)
    - Conversion rate (primary, marketing focus)
    - Customer acquisition cost (primary, financial focus)
    - Net promoter score (primary, product quality)
    - Inventory turns (supporting, ops)
    - Return rate (supporting, quality)
  Avoid: "Traffic," "page views," "sessions" (usually not a decision driver)

Q8: What is the metrics hierarchy?
  Primary ← Supporting ← Diagnostic

  Example: Revenue declining?
    → By geography, segment, channel, product?
      → By device, cohort, campaign?
        → Individual transaction details, attribution

Q9: How are targets and benchmarks defined?
  - Absolute: Revenue > $1M/month
  - Relative: YoY growth > 15%
  - Percentile: Top 25% of peers
  - Rolling: 90-day average (smooths noise)
  - Seasonal: Target adjusted for Q4

Q10: What comparison dimensions exist?
  - Time: Current vs. prior period, YoY, rolling average
  - Geography: By country, region, city
  - Segment: By customer type, product category, revenue bucket
  - Cohort: By acquisition date, lifecycle stage
  - Attribution: By channel, campaign, touchpoint

Q11: Are there leading vs lagging indicators?
  - Lagging: Revenue, profit (backward-looking)
  - Leading: Pipeline value, trial signups, feature adoption (forward-looking)
  - Mixed: Customer satisfaction (current sentiment, predicts churn)
  Mix these to tell a complete story.

Q12: What alerting thresholds exist?
  - Critical: Revenue drops > 20%, error rate > 10%
  - Warning: Revenue growth < 10%, SLA violation
  - Informational: Milestone reached, trend inflection

PHASE 3: DATA SOURCE AND PIPELINE DESIGN
==========================================
Input: KPIs, data landscape
Output: Data lineage diagram, freshness/quality requirements

Q13: What data sources feed the dashboard?
  - Transactional: CRM (Salesforce), ERP (SAP), databases
  - Warehouse: Data warehouse (Snowflake, BigQuery), data lake
  - Third-party: Analytics vendor (Mixpanel, Amplitude), financial (Bloomberg)
  - Real-time: Kafka, pub/sub (Pub/Sub, EventBridge), streaming API
  - CSV/manual: No good; flag as technical debt

Q14: What transformations/aggregations are needed?
  - Deduplication: Remove duplicate transactions
  - Matching: Join customers across CRM and warehouse
  - Attribution: Assign revenue to campaigns across multiple touchpoints
  - Segmentation: Classify customers by RFM, value tier
  - Derived metrics: Calculate CAC, LTV, payback period from raw data

Q15: What is the data freshness requirement?
  - Real-time (<5 min): Requires streaming pipeline, event-driven updates
  - Near-real-time (5-60 min): Scheduled ETL with 5-min cadence
  - Daily: Overnight batch job, ready at 6 AM
  - Weekly: Sunday evening batch
  Mismatch = frustrated users or unnecessary infrastructure cost

Q16: What is the data volume?
  - Revenue dashboard: 10K–1M transactions/day → Standard data warehouse
  - IoT monitoring: 1B+ events/day → Time-series DB (InfluxDB, Prometheus)
  - Customer analytics: 100M+ user events/day → Data lake with pre-aggregation
  Volume drives: Caching strategy, pre-aggregation need, query optimization

Q17: Are there data quality concerns?
  - Stale data: Data not updated in days (flag as "last updated: X days ago")
  - Inconsistency: Same metric calculated differently across systems
  - Completeness: Missing values in key fields (e.g., campaign attribution)
  - Accuracy: Known bias or estimation (flag as "estimated" or "provisional")
  Plan: Data quality monitoring, reconciliation with source systems

Q18: What's the ETL/ELT strategy?
  - ETL (Extract, Transform, Load): Clean before warehouse (safer, slower)
  - ELT (Extract, Load, Transform): Load raw, transform in warehouse (faster, requires monitoring)
  - Hybrid: Real-time events via ELT, batch transactions via ETL
  - Streaming: Apache Flink, Spark Streaming for continuous transformations

PHASE 4: INFORMATION ARCHITECTURE AND LAYOUT
==============================================
Input: KPIs, user roles, device constraints
Output: Wireframe descriptions, layout blueprint

Q19: What is the dashboard hierarchy?
  - Single view: All KPIs on one page (works for 3–5 KPIs, one user role)
  - Multi-level: Overview tab → detail tab → drill-down modal (common)
  - Multi-dashboard: Executive dashboard → analyst dashboard → real-time ops (scalable)
  - Linked dashboards: Context switches via breadcrumb (e.g., account → transactions)

Q20: What visualization types for each metric?
  - KPI card: Big number + sparkline (best for primary KPIs)
  - Time series: Line chart (trends, seasonality)
  - Bar chart: Categorical comparison (by segment, geography)
  - Map: Geospatial patterns
  - Table: Detail, exact values
  - Funnel: Conversion flows
  - Waterfall: Contribution to total
  - Heatmap: 2D patterns (e.g., revenue by day of week × hour)
  Rule: One chart = one question answered

Q21: What is the spatial layout?
  - F-pattern: Top-left = most important, descend → right (executive preference)
  - Z-pattern: Top-left → top-right → bottom-left → bottom-right (report style)
  - Priority-based: User role determines visible widgets (customizable)
  - Grid: Responsive, rearrangeable (modern dashboards)
  - Progressive disclosure: Overview visible, detail on demand (reduces cognitive load)

Q22: What interactive elements?
  - Global date range picker: "Last 30 days" applies to all charts
  - Filters: By segment, geography, product (cascading or independent?)
  - Drill-down: Click segment → see transactions
  - Cross-filtering: Click bar → filters other charts
  - Download: Export data as CSV/Excel
  - Share: Generate shareable link (public or authenticated?)
  - Annotations: Add context ("Black Friday spike")

Q23: What is the navigation model?
  - Tabs: Simple, 3–5 sections (executive overview, sales, ops)
  - Breadcrumbs: Show hierarchy (dashboard > account > transactions)
  - Sidebar: Persistent navigation (common in Looker, Tableau)
  - Search: Find metric by name (important for large dashboard suites)
  - Favorites/starred: Users pin frequently-used dashboards

Q24: Color palette and encoding strategy
  - Brand colors: Primary, secondary, accent (3–5 colors max)
  - Semantic colors: Green = good, red = bad, yellow = warning (but only 40% color-blind users see this)
  - Color-blind safe: Use patterns, textures, labels—never rely on color alone
  - Consistent meaning: Always green = positive, never green = negative in one chart, positive in another

Q25: Progressive disclosure
  What's visible at a glance?
    - KPI cards, main trend, key segments
  What appears on hover/click?
    - Tooltip with last updated time, 95% CI, data quality flag
  What appears on drill-down?
    - Full transaction table, ability to export, filter, sort
  What appears on demand?
    - Advanced statistics, anomaly detection, forecasts

PHASE 5: INTERACTION DESIGN
============================
Input: User workflows, information architecture
Output: Interaction flowchart, state machine for filters/drill-down

Q26: What filters are global vs per-widget?
  - Global: Date range (applies to all), segment (applies to most)
  - Per-widget: "Show data labels" toggle on one chart only
  - Cascading: Select region → territory → account (reduces invalid combinations)
  - Optional: Filters should have sensible defaults (not blank)

Q27: What drill-down paths exist?
  - Shallow: KPI card → summary table (1 level)
  - Deep: KPI → segment → account → transaction (3+ levels)
  - Non-linear: Click any bar in any chart → filter all others
  - Context preservation: When drilling, maintain all parent filters

Q28: What cross-filtering behavior?
  - Click bar in "revenue by region" → filters "revenue by product" (same time period)
  - Shift+click → multi-select (select multiple regions)
  - Click again → clear filter (toggle behavior)
  - State display: Show active filters (e.g., "Showing: US, 2024 only")

Q29: What export/share capabilities?
  - CSV export: 1 chart, 10K rows max
  - PDF export: Full dashboard snapshot with timestamp
  - Share link: Public (no auth) or authenticated (with role-based access)?
  - Email: "Send dashboard snapshot daily" (recurring, automated)
  - API: Programmatic access to underlying data?

Q30: What annotation/commenting features?
  - Inline comments: "This spike is due to Black Friday"
  - Version history: "Changed target from $1M to $1.2M on 2024-03-01"
  - Audit log: Who changed what and when
  - Alert acknowledgment: "I saw the alert, it's being investigated"

PHASE 6: PERFORMANCE AND SCALABILITY
======================================
Input: Data volume, concurrent users, refresh cadence
Output: Caching strategy, load-time budget, concurrency model

Q31: What caching strategy?
  - Query cache: Cache SQL results for 5 min (most common)
  - Materialized view: Pre-aggregate in warehouse (daily refresh)
  - Redis/memcache: Cache computed KPIs (app layer)
  - CDN: Cache static assets (images, fonts, JS bundles)
  - Client-side: Cache in browser localStorage (risky for real-time data)

Q32: What's the acceptable load time?
  - Initial load: < 3 seconds (DOM interactive)
  - Chart render: < 1 second (visual completeness)
  - Filter/drill-down: < 500 ms (responsiveness feels instant)
  Target latency drives: Query optimization, pre-aggregation, caching depth

Q33: What's the concurrent user expectation?
  - 10 users: No special scaling, standard database
  - 100 users: Query cache + connection pooling
  - 1K+ users: Materialized views + distributed cache + horizontal scaling
  - Unknown: Design for 100, monitor, scale when needed

Q34: How does the dashboard handle large datasets?
  - Aggregation: Show 30-day rolling aggregate, not 1000 daily points
  - Sampling: Show 1% sample if > 10M rows
  - Pagination: Show 100 rows, "Load more" button
  - Search/filter first: "Enter customer name to load transactions" (don't load all 100K at once)

Q35: Mobile/responsive behavior
  - Desktop: Full fidelity, all filters visible
  - Tablet: Stacked layout, simplified interactions
  - Mobile: KPI cards only, filters in drawer, drill-down in modal
  - Responsive breakpoints: 1920px, 1200px, 768px, 375px

PHASE 7: ACCESSIBILITY AND EQUITY
==================================
Input: User personas, regulatory requirements
Output: Accessibility audit plan, equity review

Q36: Color-blind safe palettes
  - Rule: Don't rely on color alone; use patterns, textures, labels
  - Test: Simulate deuteranopia (red-green), protanopia, tritanopia
  - Tool: Contrast Ratio checker (WCAG AA = 4.5:1 for text)
  - Palette: Viridis, ColorBrewer, accessible Tableau palette

Q37: Screen reader compatibility for charts
  - Rule: Text tables should accompany complex visualizations
  - ARIA labels: <img alt="Revenue by region: US 45%, EU 30%, APAC 25%">
  - Interactive: Chart uses <canvas> or SVG with proper role="img"?
  - Testing: Screen reader (NVDA, JAWS), not visual inspection

Q38: Keyboard navigation for interactive elements
  - Tab order: Logical flow (top-left → right → down)
  - Focus visible: Clear outline, not hidden
  - Shortcuts: Enter key to expand, Escape to close
  - Skip links: "Skip to main content"

Q39: Data tables as alternatives to complex visualizations
  - Rule: Stacked bar chart hard to interpret? Provide table alternative
  - Sortable columns: Click header to sort
  - Searchable: Ctrl+F or in-dashboard search
  - Downloadable: Export to CSV

Q40: Language/internationalization requirements
  - Metric names: "Revenue" vs "Ingresos" (Spanish) vs "Chôi suất" (Vietnamese)
  - Number format: 1000 (US) vs 1.000 (EU) vs 1,000 (India)
  - Date format: MM/DD/YYYY (US) vs DD/MM/YYYY (EU)
  - Timezone: Show "as of 9:30 AM EST" or let user select

Q41: Are the metrics equitable?
  - Question: Does this dashboard mask disparities?
  - Example: "Average revenue per customer" hides that new cohort has 50% less LTV
  - Fix: Segment by cohort, show distribution, flag outliers
  - Audit: Run metrics through equity lens (who benefits, who is harmed?)

PHASE 8: TESTING AND VALIDATION
================================
Input: Plan architecture
Output: Testing roadmap, user validation protocol

Q42: How to validate data accuracy?
  - Reconciliation: "Did we double-count transactions?" vs. source system
  - Spot-check: Manual verification of 10 random rows
  - Automation: Monthly reconciliation script comparing warehouse to source
  - Alerting: Flag if any metric changes > 20% overnight

Q43: How to test with real users?
  - Prototype: Build wireframe/mock, test with 3–5 users
  - Tasks: "Find revenue for US in Q1" (should take < 1 min)
  - Feedback: "Was the chart intuitive? Did you find what you needed?"
  - Iteration: Revise based on feedback, test again

Q44: Performance benchmarks
  - Load time: Measure time to first chart interactive
  - Query latency: 95th percentile query latency < 1 second
  - Concurrency: 100 concurrent users, p95 latency < 3 seconds
  - Data freshness: Actual vs. target refresh cadence

Q45: Accessibility audit plan
  - Automated: axe DevTools, Lighthouse
  - Manual: Screen reader test, keyboard navigation test
  - User testing: Recruit users with assistive tech
  - Compliance: WCAG 2.1 AA (or AAA if required)

PHASE 9: IMPLEMENTATION TASKS AND DEPLOYMENT
===============================================
Input: All prior phases
Output: Ordered task list, tool recommendations, go-live checklist

Task sequence (no parallelization until data pipeline is validated):

  1. Data Pipeline Setup (2–4 weeks)
     - Validate data sources (no stale/inconsistent data)
     - Build ETL/ELT (batch or streaming)
     - Implement data quality monitoring
     - Reconcile with source systems
     - Checkpoint: Data refreshes correctly, metrics match source

  2. Backend API (1–2 weeks)
     - Implement query layer (API, GraphQL, REST)
     - Add caching layer (Redis, Memcache)
     - Implement role-based access control
     - Performance testing (p95 < 1s for 100 concurrent)
     - Checkpoint: API returns correct, fast, secure data

  3. Frontend Implementation (2–4 weeks)
     - Build component library (KPI card, chart, filter)
     - Implement information architecture (layout, navigation)
     - Add interaction (drill-down, cross-filtering, export)
     - Make responsive (desktop, tablet, mobile)
     - Checkpoint: UI matches wireframes, feels responsive

  4. Accessibility & Testing (1 week)
     - Automated tests (axe, Lighthouse)
     - Screen reader testing
     - User acceptance testing (3–5 users per role)
     - Performance profiling
     - Checkpoint: WCAG AA compliant, < 3s load time, user satisfied

  5. Deployment & Monitoring (1 week)
     - Deploy to staging, get stakeholder approval
     - Set up monitoring (load time, error rate, data freshness)
     - Create runbook for common issues
     - Deploy to production with canary rollout
     - Checkpoint: Live, monitored, team trained

Tool recommendations (by constraint):
  - Low-code BI (Tableau, Looker): 4–6 weeks total, best for non-technical teams
  - Self-serve analytics (Metabase, Apache Superset): 6–8 weeks, engineering required
  - Custom web app (React + D3/Chart.js): 8–12 weeks, full control, highest flexibility
  - Hybrid (API + custom frontend): 10–14 weeks, best for complex interaction
  - Mobile-first (React Native, Flutter): +3–4 weeks, separate team

POST-LAUNCH (ongoing)
  - Monitor: Query performance, data freshness, user adoption
  - Iterate: A/B test layouts, add new metrics based on usage
  - Scale: As concurrency grows, add caching, pre-aggregation, read replicas
  - Optimize: Annually review KPIs, deprecate unused metrics, trim technical debt
```

## Tool_Usage

This skill does **not** use Write or Edit tools. It:
- **Reads** existing dashboards, wireframes, documentation (if provided) to validate against the plan
- **Invokes** the locally selected planning agent; OMC is optional execution infrastructure only
- **Delegates** data modeling questions to BI-tool-specialist or data-warehouse-architect

## Examples

### Example 1: E-commerce Executive Dashboard
**Context**: Retail company wants a daily executive dashboard showing business health.

**Key Questions Answered**:
- Audience: CFO, CEO, board (5 min at a glance)
- Decisions: "Is revenue on track?" "Which segment is growing?" "Any red flags?"
- Refresh: Daily at 6 AM (batch-friendly, no real-time)
- KPIs: Revenue (primary), conversion rate (primary), CAC (primary), NPS (primary)
- Data: Sales database, marketing CRM, survey tool
- Layout: F-pattern, 4 KPI cards top, trend lines middle, segment breakdown bottom
- Filters: Global date range, segment selector
- Drill-down: Click segment → see customer breakdown by cohort
- Performance: < 2s load (daily batch, cached queries)

**Plan Output**:
- Executive Summary: 4-metric dashboard showing $12M daily revenue, 3.2% conversion, segment health
- Scope: Executive audience, tactical decisions, daily refresh, role-based access
- KPI Architecture: Revenue hierarchy (total → by channel → by product → by cohort)
- Data Pipeline: Nightly ETL from warehouse + CRM, cached results in Redis
- Information Architecture: Overview tab (4 cards), segment tab (detailed breakdown)
- Implementation: 4 weeks with Looker, 8 weeks custom React
- Go-live: March 15, monitor daily reconciliation, iterate on metrics

### Example 2: Real-time Operations Monitoring
**Context**: SaaS platform needs an operations center for SREs and on-call engineers.

**Key Questions Answered**:
- Audience: On-call SRE, engineering manager (continuous monitoring)
- Decisions: "Is the system healthy?" "Should I page someone?" "Root cause?"
- Refresh: Real-time (< 5 min, event-driven)
- KPIs: Error rate (primary), latency p95 (primary), throughput (primary), alerts (primary)
- Data: Prometheus, CloudWatch, application logs (streaming)
- Layout: Status board at top, drill-down into service-level detail, alert timeline
- Filters: By service, environment (prod/staging), time window (last 6 hours)
- Drill-down: Click service → see request traces, error details
- Performance: < 500 ms response to filter/drill-down (WebSocket-driven updates)

**Plan Output**:
- Executive Summary: Real-time status of 12 services, SLA compliance, alert distribution
- Scope: On-call audience, operational decisions, real-time refresh, role-based (SRE vs. manager)
- KPI Architecture: System health (error rate, latency) → service health (drill-down)
- Data Pipeline: Event streaming from Prometheus/CloudWatch, in-memory aggregation, WebSocket push
- Information Architecture: Status board (top), service detail (click to expand), timeline (bottom)
- Implementation: 6 weeks with custom React + WebSocket backend
- Go-live: February 28, monitor false positive rate, iterate on drill-down UX

### Example 3: Analyst Self-Service Workspace
**Context**: Marketing team needs to explore campaign performance without SQL knowledge.

**Key Questions Answered**:
- Audience: Marketing analysts, campaign managers (ad-hoc 2+ hour investigations)
- Decisions: "Which campaigns underperformed?" "What drove the cost per lead up?" "Which cohort should we retarget?"
- Refresh: Daily (campaigns updated nightly)
- KPIs: Leads (primary), cost per lead (primary), conversion rate (supporting)
- Data: Ad platforms (Facebook, Google, Linkedin), CRM, warehouse
- Layout: Multi-dashboard (overview → campaign → cohort → budget analysis)
- Filters: Date range, campaign, channel, audience segment (cascading)
- Drill-down: Click campaign → see daily breakdown, then click date → see audience drill-down
- Interaction: Cross-filter (click high CPL campaign → filters all other charts), export to CSV
- Performance: < 1s response to filter, < 3s to drill-down to raw data
- Accessibility: All charts paired with data tables, color-blind safe, screen reader compatible

**Plan Output**:
- Executive Summary: Self-service workspace with 8 dashboards, 200+ metrics across 5 platforms
- Scope: Analyst audience, diagnostic decisions, daily refresh, column-level data access (cost data limited)
- KPI Architecture: Leads funnel (clicks → impressions → leads → conversions) with detailed attribution
- Data Pipeline: Nightly ETL from ad platforms + CRM, deduplicated/attributed, warehouse, cached summary views
- Information Architecture: Overview dashboard → drill-down to platform-specific views → cohort analysis
- Implementation: 10 weeks with Metabase (low-code) or custom React + D3
- Go-live: April 1, user training, iterate on filter UX based on usage

## Benchmark_Test_Info

**Current Benchmark (Score: 27)**

This skill was benchmarked against 5 dashboard planning scenarios:

| Scenario | Result | Notes |
|----------|--------|-------|
| E-commerce executive dashboard | PASS | Clear KPI hierarchy, data pipeline design, wireframe descriptions |
| Real-time operations dashboard | PASS | Addressed real-time streaming requirements, drill-down interaction design |
| Analyst self-service workspace | PASS | Multi-dashboard architecture, cascading filters, accessibility compliance |
| SaaS product analytics | PASS | Cohort analysis, funnel visualization, performance caching strategy |
| Multi-tenant financial dashboard | PASS | Row/column-level access control, data quality, audit logging |

**Scoring Rubric**:
- Phase 1 (Scope) clarity: 5/5 points (audience, decisions, constraints well-defined)
- Phase 2 (KPI) rigor: 5/5 points (primary/supporting/diagnostic hierarchy clear)
- Phase 3 (Data) pipeline design: 5/5 points (sources, transformations, freshness explicit)
- Phase 4 (Information) architecture: 4/5 points (wireframe descriptions detailed, but visual mockups needed for complex layouts)
- Phase 5–9 (Interaction, performance, accessibility, testing, tasks): 3/5 points (detailed, but implementation examples would strengthen)

**Known Limitations**:
- Does not generate actual wireframe images (describes layout in words)
- Does not validate dashboard against existing BI tool constraints (delegates to BI-tool-specialist)
- Does not estimate cost or team size for implementation (too variable by org)
- Does not include security architecture for sensitive data (delegates to data-governance or infosec)

**How to Improve This Skill**:
- Add examples of dashboard pattern templates (e.g., "executive summary," "analyst workbench," "real-time command center")
- Include sample KPI definition documents (name, formula, target, owner)
- Add data pipeline architecture diagrams (Miro/Lucidchart templates)
- Include WCAG audit checklist for dashboard accessibility
- Add post-launch monitoring checklist (what metrics to track, how often)

## Notes

- **This skill is not a code generator.** It produces architecture and planning documents, not HTML/CSS/React components. Implementation follows the task list from Phase 9.
- **Precision over speed.** The planning protocol is long because dashboard failures are expensive. A 2-week planning sprint prevents 8 weeks of post-launch rework.
- **Local route authority.** The catalog/meta-router selects `dashboard-planner` for its embedded BI knowledge. OMC may be used only as an optional worker after that selection.
- **Contract enforcement.** The Contract Appendix in the plan is a binding document. Developers should be able to build the dashboard exactly as described without re-discovering requirements mid-sprint.
- **Iterative planning.** The protocol is designed for collaboration. Use `harsh-critic` after each draft to validate the architecture from executive, analyst, operator, and data engineer perspectives.
- **Accessibility is non-negotiable.** Phases 7–8 are not optional. A dashboard that 20% of users can't access is not a successful dashboard.
