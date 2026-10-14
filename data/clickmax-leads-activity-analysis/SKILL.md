---
name: clickmax-leads-activity-analysis
description: Use when the user wants to inspect CRM activity streams, event timelines, or activity-derived metrics for leads and opportunities.
---

## When this applies

Use this skill when the user needs the raw or grouped activity stream behind CRM behavior: per-lead timelines, system activity groups, owner-level activity counts/timeseries, or opportunity-card activity.

Not this skill:

- tag lifecycle views -> `clickmax-tags`
- the Activities queue (follow-up tasks + booked appointments: what is late, the team's agenda, closing a batch) -> `clickmax-activities`. Same word, different data: this skill reads the event log of what HAPPENED, that one reads work someone owes or booked
- high-level KPI dashboard reading with no need for raw event streams -> use the direct analytics tools
- kanban/pipeline card mutation -> `clickmax-pipelines`

## Key assumptions

- per-lead lookups are cheaper and safer when the lead is already known
- system-list/system-by-lead are derived grouped views, not manual tags
- owner stats/timeseries/count are aggregate activity tools, not row-level cohort discovery
- opportunity activity requires `cardId`
- timeline rows carry who did it (`actorId`/`actorType`: `user` = a person of the workspace, `system` = nobody did it by hand, e.g. public booking link, calendar sync, automatic no-show); older rows may have neither, which means "not recorded", not "system"

## Thought process

1. Decide whether the user needs a raw timeline, a grouped system view, or owner-level aggregates.
2. Prefer per-lead/per-card calls when the entity is known.
3. Use aggregate activity tools only when the question is about counts or trends.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__lead_activities_list` for filtered activity cohorts, passing pagination plus the relevant date window and any needed pipeline, actor, or event-name filters.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_list_by_lead` for one lead's raw timeline, passing the lead id as `leadId` (not `id`) plus pagination.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_metrics_by_lead` when the question is about one lead's activity totals or derived metrics inside a specific date window.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_system_by_lead` when the user wants the grouped system view for one lead rather than the raw event stream.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_opportunity_list` for opportunity-card activity, passing the `cardId` and pagination.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_owner_stats` for owner-level concentration or summary questions across a date window.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_owner_timeseries` for owner-level change-over-time questions across a date window.
- Use `mcp__plugin_clickmax_clickmax__lead_activities_owner_count` when the user only needs owner activity counts, not a trend series.
- For `did X` cohorts, build a system activity/tag list for X, inspect a small page to confirm event/category fields, then paginate as needed.
- For `did X but not Y` cohorts, get both cohorts with the same time assumptions, dedupe by lead, subtract Y from X, and report the remaining leads.
- When comparing several streams, keep the same date window and filters so the results stay comparable.

## Report

- Open with the scope assumed: lead timeline, opportunity activity, grouped system view, or owner aggregate.
- Present timelines chronologically and group them by meaningful phases when possible.
- For aggregates, lead with what changed, where activity is concentrated, and the strongest visible trend.
- Keep raw event payloads out unless the user explicitly asks.
- If the result set is long, show the most relevant items first and summarize the remainder as `+N more`.

## Warnings

- Do not confuse grouped system activity with manual tag assignment.
- Do not use owner-level aggregates as if they were a lead timeline.
- Do not guess opportunity activity from lead activity; use the card-specific tool.

## Anti-patterns

- Dumping every event row without synthesis.
- Guessing a card id from lead context.
- Answering a timeline question with only aggregates.

---

Clickmax skill revision: `b8294822a4d6`
