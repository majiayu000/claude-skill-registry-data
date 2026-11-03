---
name: marketing-revops
description: Design revenue operations — funnel stages from lead to customer, lead scoring, routing, sales SLAs, revenue attribution and leadership dashboards. Use when marketing and sales disagree on lead quality, handoffs drop leads, or leadership wants pipeline reporting. Not for product event tracking; see /marketing-analytics-tracking.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# RevOps

Design revenue operations processes for "$ARGUMENTS". Plan pipeline management, attribution, reporting, and marketing-sales alignment.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"marketing-revops","workflow":"marketing","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

## Prerequisites

None — this is a utility skill. Works best with strategy and analytics context.

## Process

1. **Read context** (if available):
   - Read `.singularskills/marketing/<project>/00-strategy.md` for business context
   - Read `.singularskills/marketing/<project>/analytics-tracking.md` if it exists

2. **Define the revenue funnel:**
   - Map stages: visitor → lead → MQL → SQL → opportunity → customer
   - Define stage criteria: what qualifies a lead for each stage?
   - Conversion rate benchmarks per stage
   - Handoff process between marketing and sales

3. **Lead scoring model:**
   - Demographic scoring: how well does the lead match ICP?
   - Behavioral scoring: what actions indicate intent?
   - Score thresholds for MQL and SQL
   - Score decay: how scores change over time with inactivity

4. **Attribution and reporting:**
   - Revenue attribution model: how is marketing credit assigned?
   - Key reports: pipeline, velocity, conversion rates, CAC, LTV
   - Dashboard design: what does leadership need to see?
   - Reporting cadence: daily, weekly, monthly, quarterly

5. **Process design:**
   - Lead routing: how are leads assigned to sales?
   - SLA: marketing response time, sales follow-up time
   - Feedback loops: how does sales inform marketing on lead quality?
   - Tech stack recommendations: CRM, marketing automation, BI tools

6. **Write the artifact** — write to `.singularskills/marketing/<project>/revops.md`:
   - **Revenue Funnel** — stages, criteria, benchmarks
   - **Lead Scoring Model** — scoring framework
   - **Attribution & Reporting** — model, dashboards, cadence
   - **Processes** — routing, SLAs, feedback loops
   - **Tech Stack** — recommended tools

## Output

RevOps plan written to `.singularskills/marketing/<project>/revops.md`. Present a summary highlighting:
- Funnel stages with conversion benchmarks
- Lead scoring model overview
- Key reports to build
