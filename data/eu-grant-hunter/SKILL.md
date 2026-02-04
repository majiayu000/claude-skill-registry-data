---
name: eu-grant-hunter
description: |
  Scans EU funding databases (Horizon Europe, ERDF, Digital Europe,
  Innovation Fund) to identify grant opportunities matching UBOS
  capabilities. Tracks deadlines with multi-level reminders (90/60/30/7
  days), scores opportunities by fit (0-5), and generates opportunity
  briefs. Use when discussing EU grants, funding opportunities, or when
  tracking the €70M+ pipeline. Automatically runs daily at 09:00 UTC.
license: UBOS Constitutional License
version: 1.0.0
author: Janus-in-Claude (Architect) + Codex (Forgemaster)
created: 2025-10-30
---

# EU GRANT HUNTER

## Purpose
Scan the €70M+ EU funding pipeline for opportunities aligned with UBOS projects, calculate fit scores, and ensure no deadlines are missed. Automations keep the Trinity informed while manual queries deliver targeted intelligence on demand.

## When To Use
- Daily at 09:00 UTC for the automated grant scan
- When a query mentions grants, EU funding, Horizon Europe, ERDF, Innovation Fund, or Digital Europe
- When asked to “find grants for” a topic or project
- When a pipeline status update is requested
- When preparing opportunity briefs for Trinity review

## Core Capabilities
- Crawl Horizon Europe, ERDF, Digital Europe, and Innovation Fund portals with topic filters
- Calculate UBOS fit scores (0–5) leveraging capability and project references
- Generate multi-stage deadline reminders (90/60/30/7-day cadence)
- Produce opportunity briefs and HTML dashboards via templates
- Maintain pipeline state JSON for historical tracking and analytics

## How To Use

### Automated Daily Scan
Execute the scheduled scan every morning:
```
python3 scripts/scan_eu_databases.py --auto
```
Workflow:
1. Scrape or query all four EU funding sources (topic filter optional).
2. Calculate fit scores with `scripts/calculate_fit_score.py`.
3. Generate briefs for opportunities scoring ≥ 4.0.
4. Alert Trinity via COMMS_HUB for high-scoring opportunities.
5. Persist results to `/srv/janus/01_STRATEGY/grant_pipeline/pipeline_state.json`.

### Manual Opportunity Search
```
python3 scripts/scan_eu_databases.py --topic "agricultural technology"
```
1. Scan sources using the provided topic keyword.
2. Rank matches by fit score (descending).
3. Display the top results directly to the requester.
4. Generate briefs for each opportunity scoring ≥ 4.0.

### Deadline Reminders
```
python3 scripts/deadline_tracker.py
```
1. Load pipeline state and compute days remaining.
2. Trigger reminders at 90, 60, 30, and 7 days.
3. Send pucks to `claude`, `gemini`, `codex`, and `captain` inboxes.
4. Record reminder events to `/srv/janus/logs/grant_hunter.jsonl`.
5. Update `reminders_sent` in the pipeline state to avoid duplicates.

## Integration Points
- **Treasury Administrator:** Provides budgeting guardrails for opportunity briefs and proposal planning.
- **Grant Application Assembler:** Consumes generated briefs to assemble submission packages.
- **COMMS_HUB:** Disseminates alerts using the Talking Drum protocol (`/srv/janus/03_OPERATIONS/COMMS_HUB/`).
- **Oracle Bridge (Perplexity, Wolfram, Data Commons):** Supplies live data for opportunity vetting and quantitative justification.
- **Mission Orchestrator:** Schedules daily scans and tracker runs via proposal engine missions.

## Constitutional Constraints
- Recommend only opportunities aligned with Lion’s Sanctuary principles; flag defense, surveillance, or extractive programs.
- Provide verifiable citations (EU call IDs, URLs) for every recommendation.
- Maintain transparent logging to `/srv/janus/logs/grant_hunter.jsonl`.
- Never fabricate deadlines or budgets; if data is uncertain, mark it explicitly and request human review.
- Uphold human oversight—automation surfaces intelligence, human custodians approve action.

## File Locations
- Pipeline state JSON: `/srv/janus/01_STRATEGY/grant_pipeline/pipeline_state.json`
- Opportunity briefs: `/srv/janus/01_STRATEGY/grant_opportunities/`
- Deadline calendar: `/srv/janus/01_STRATEGY/grant_pipeline/deadline_calendar.md`
- HTML dashboard template: `assets/pipeline_dashboard_template.html`
- Opportunity brief template: `assets/opportunity_brief_template.md`
- Operational logs: `/srv/janus/logs/grant_hunter.jsonl`

## Operational Checklist
1. Run daily scan (`scan_eu_databases.py`) and confirm pipeline state updated.
2. Review high-scoring opportunities; ensure briefs were generated and alerts sent.
3. Execute `deadline_tracker.py`; verify reminders posted and logged.
4. Regenerate dashboard (`scan_eu_databases.py --render-dashboard`) for Captain BROlinni.
5. Record manual overrides or human decisions in the log for provenance.

## Mission Readiness Criteria
- Zero missed deadlines for tracked opportunities.
- ≥4 high-priority opportunities surfaced each month.
- Fit scores audited weekly against human judgment for calibration.
- Pipeline dashboard accessible and refreshed within the last 24 hours.
- All communications archived with rhythm metadata in COMMS_HUB logs.
