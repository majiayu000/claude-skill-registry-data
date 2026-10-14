---
name: clickmax-tags
description: Use when the user wants to inspect, X-ray usage of, create, update, delete, clone, or apply CRM tags to leads in Clickmax.
---

## When this applies

Use this skill when the user wants to manage CRM tags or use tags as cohort labels: inspect manual/system tags and where each is used, create/update/delete/clone manual tags, or apply/remove tags from many leads.

Not this skill:

- raw event timelines -> `clickmax-leads-activity-analysis`
- manual lists or dynamic segments -> `clickmax-list-segments`

## Key assumptions

- system tags are event-derived and cannot be updated or deleted
- manual tag create always yields a non-system tag
- deleting a manual tag also removes its lead/opportunity assignments and related kanban links, but NOT its references: automations, segments (and forms/boards) that cite it keep a dangling id, so the automation silently stops matching/applying it and the segment changes its contacts. Usage = `references` in `mcp__plugin_clickmax_clickmax__tags_insights` or the `flowsCount`/`segmentsCount`/`formsCount`/`boardsCount` columns of `mcp__plugin_clickmax_clickmax__tags_manual_list`
- `leadsCount` = contacts with the tag; `opportunitiesCount` = opportunity cards with it — different populations
- a system tag is a lead-timeline event name (`eventName`), not a stored tag: `count` = unique contacts, `occurrences` = total fires; tag apply/remove, lead created/captured and opportunity move/status/tag events are not system tags
- `mcp__plugin_clickmax_clickmax__tags_insights` `trend` is CUMULATIVE (contacts that had the tag at month end; a removal shows as a drop); `mcp__plugin_clickmax_clickmax__tags_system_insights` `monthly`/`daily` count OCCURRENCES (an event is a dated fact) and its `weekdays`/`hours` are in America/Sao_Paulo time
- lead apply/remove tools mutate assignments, not the tag definition itself

## Thought process

1. Determine whether the need is taxonomy management or lead assignment.
2. Distinguish manual vs system tags early.
3. Use batch apply/remove only when the user really wants bulk cohort mutation.
4. "Is this tag used / can I delete it / what does it do?" is a usage question, not a list question: X-ray it (`tags_insights`, or `tags_system_insights` for events) before proposing a delete.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__tags_list` when the user starts broad and wants the full tag catalog.
- Use `mcp__plugin_clickmax_clickmax__tags_manual_list` for editable CRM labels with usage columns (`leadsCount`, `opportunitiesCount`, `flowsCount`, `segmentsCount`, `formsCount`, `boardsCount`), name filtering (`name`), and sorting (`orderBy` + `order`; default A-Z, count columns default desc). It has no growth series any more — growth = `tags_insights`. "Most used" = `orderBy = leadsCount`; "unused" = all consumer counts 0 AND low `leadsCount`.
- Use `mcp__plugin_clickmax_clickmax__tags_system_list` for event-derived labels (`search` by event name, `orderBy` count/occurrences/occurrencesLast7Days/lastSeenAt...); use `mcp__plugin_clickmax_clickmax__tags_system_activities` when the user needs the contacts/events behind one system tag.
- Use `mcp__plugin_clickmax_clickmax__tags_insights` (by `tagId`) for one manual tag: coverage of the base, last 30 days applied, 6-month trend, 14-day daily series, and the NAMED consumers (`references`, capped at 100 per kind; `referencesTotal` is the real total). Not valid for system tags.
- Use `mcp__plugin_clickmax_clickmax__tags_system_insights` (by `eventName` taken from `tags_system_list`) for one system tag: reach, 7/30-day pace, first-time firers, weekday/hour pattern, top contacts, events that tend to come with it (`coOccurring` is measured over a sample of the 500 most recent contacts — say "in a recent sample"), and the automations listening to it. Unknown `eventName` = not found.
- Use `mcp__plugin_clickmax_clickmax__tags_get` before changing a specific tag so manual vs system status is explicit.
- Use `mcp__plugin_clickmax_clickmax__tags_create` for new manual tags. If the user also wants the new tag applied immediately, create first, then use `mcp__plugin_clickmax_clickmax__crm_tags_apply_to_leads` with the returned tag id.
- Use `mcp__plugin_clickmax_clickmax__tags_update`, `mcp__plugin_clickmax_clickmax__tags_clone`, and `mcp__plugin_clickmax_clickmax__tags_delete` only for manual tags. Before `tags_delete`, read `mcp__plugin_clickmax_clickmax__tags_insights`: if `references` is not empty, name the automations/segments/forms/boards that will lose the tag and get an explicit go-ahead.
- Cloned tags are named from the original with a numeric suffix, such as `<original name> (1)`; rename after cloning if the user needs a business-friendly label.
- Use `mcp__plugin_clickmax_clickmax__crm_tags_remove_from_leads` when the tag definition should stay but specific leads should lose the assignment.
- Use `mcp__plugin_clickmax_clickmax__crm_tags_batch_apply_to_leads` only for intentional bulk cohort changes across many leads. When the result needs validation, inspect membership changes with `mcp__plugin_clickmax_clickmax__tags_manual_leads_timeline`.
- Preferred order: inspect tag type -> inspect current definition, usage or membership when relevant -> mutate the tag or assignments -> verify updated state for high-impact changes.

## Report

- Start with the tag job type: taxonomy change, assignment change, or inspection.
- For taxonomy changes: report tag name, tag id, and the exact change.
- For lead assignment changes: report affected lead count first, then skips/errors, then the tags involved.
- For inspections: show manual vs system status first because it determines what can be changed.
- For usage/X-ray answers: lead with reach (`leadsCount` and `coverage` as a % of the base), then recent pace, then who depends on it (consumers by kind, named), and end with the safe/unsafe-to-delete read.
- If listing multiple tags, order the most relevant matches first and cap the list with `+N more`.
- Follow-up mutations are opt-in only.

## Warnings

- Do not offer update/delete for system tags.
- Do not present consumer counts of 0 as "nothing happens on delete": the contacts and cards carrying the tag still lose it.
- Do not treat manual-tag timelines as raw activity streams.
- Batch apply/remove is high-impact cohort mutation.

## Anti-patterns

- Editing system tags.
- Deleting a tag from a list view alone, without reading its consumers.
- Confusing tag assignment with segment/list membership.
- Applying tags to a broad unresolved cohort without confirming intent.

---

Clickmax skill revision: `b8294822a4d6`
