---
name: clickmax-custom-fields
description: Use when the user wants to audit, clean up, or manage the workspace custom fields (campos customizados) of contacts or opportunities — fill rate, usage, health, who filled them, groups, bulk changes, or creating/editing one.
---

## When this applies

Use for the DEFINITIONS of custom fields and how much they are used: health of the field base, which fields are dead weight, where a field is consumed, who filled it, grouping, bulk flag changes, creating or editing one field.

Not this skill:

- reading the VALUES of one contact's custom fields -> `clickmax-leads` (`mcp__plugin_clickmax_clickmax__leads_get`, `customValues`)
- writing a custom-field value on many opportunities -> `clickmax-pipelines`
- form/quiz questions that fill fields -> `clickmax-forms-quizzes`
- segmenting contacts by a custom field -> `clickmax-list-segments`
- fields of a CUSTOM OBJECT (Imóveis, Contratos…; `entityType = objects` + `objectId`) and their records -> `clickmax-custom-objects`

## Key assumptions

- two kinds, always say which: `entityType = leads` (contact fields) vs `opportunities` (deal-card fields). Same `fieldName` can exist in both. The management tools (`managed_list`, `overview`) REQUIRE `entityType`; ask or run both when the user did not say
- `fillRate` = filled records / ALL contacts (or ALL opportunity cards) of the workspace, 0..1 — a field meant for a niche is legitimately low, so judge fill together with usage
- health verdict (fixed rules): `unused` = no consumer AND under 5% filled | `critical` = has consumers AND under 25% filled | `attention` = under 60% filled | `healthy` otherwise
- consumers (`usageByKind`) = segments, automations (flow), forms, dashboards, reports, schedules, stage rules that reference the field. Usage of 0 is what makes a field a safe cleanup candidate
- "excluir" in the product = INACTIVATE (`isActive = false`): definition and stored values stay, the field disappears from lists/forms/cards/filters and is reversible, but consumers are NOT cleaned up or blocked — they keep pointing at a hidden field
- `mcp__plugin_clickmax_clickmax__custom_fields_list` returns ONLY active fields, unpaginated, full definition (options, defaults, visibility flags), no numbers. `mcp__plugin_clickmax_clickmax__custom_fields_managed_list` is the paginated view WITH fill/usage/health but without options/defaults; inactive rows come back with zeros, not real numbers
- numbers come from a short-lived snapshot (fill ~15s, consumers ~30s): a value written seconds ago may not show yet
- creating a field whose `fieldName` matches an INACTIVE one revives and overwrites the old field (same id, values kept) instead of failing
- select / multi_select / radio fields need at least one non-empty option; the value of an option always equals its label

## Thought process

1. Audit question ("how healthy are my fields?") -> `overview` first, then drill with `managed_list` filters; do not page the whole base.
2. One field question ("is this field worth keeping / who uses it / who filled it?") -> `insights` for the aggregate + consumers, `records` for the rows.
3. Any deactivation is a consequence question: read consumers first, tell the user what will keep pointing at a hidden field, then act.
4. Same change on many fields -> `bulk_update`; per-field identity edits (label, key, type, options) -> `update` one at a time.

## Execute guide

- Overview: `mcp__plugin_clickmax_clickmax__custom_fields_overview` with `entityType` -> totals, active vs inactive, average fill, health distribution, fields per type, and per-group averages (`name` null = ungrouped). Computed over the whole active scope, never over a filter.
- Find candidates: `mcp__plugin_clickmax_clickmax__custom_fields_managed_list` with `entityType` plus any of `health`, `fieldType`, `groupName` (empty string = ungrouped only), `required`, `search` (label, key or description), `isActive = false` (the inactivated bin, where reactivation candidates live). Sorted group A-Z then configured order. `perPage` (max 2000) is only an optimization: when `meta` says there are more pages, consume every page before validating or picking candidates.
- One field: `mcp__plugin_clickmax_clickmax__custom_fields_insights` with the field id -> fill / empty / distinct values, new fills in the last 30 days (live vs inherited), 6-month cumulative trend, top values (share is over FILLED records), numeric summary for numeric types, and the NAMED consumers (`references`). `mcp__plugin_clickmax_clickmax__custom_fields_records` with the field id (and `limit`, max 200) -> latest fillers with the value as text and where it came from (`source`: manual, import, form, booking, webchat, flow, api, system, unknown = stored before origins were tracked).
- Groups: `mcp__plugin_clickmax_clickmax__custom_fields_group_names` before creating or moving fields, to reuse an existing group spelling.
- Bulk: `mcp__plugin_clickmax_clickmax__custom_fields_bulk_update` with 1-500 unique ids and a `patch` of ONLY `isActive`, `groupName` (null/blank = no group), `filterable`, `pinned`, `required`. All-or-nothing and synchronous: one id outside the workspace, or reactivating a choice field with no options, fails the whole batch and nothing changes. Returns only the updated count — verify with `managed_list`. Treat it as confirmation-worthy: it can hide many fields at once, and clients that enforce confirmations will ask the user first.
- Create/edit one: `mcp__plugin_clickmax_clickmax__custom_fields_create` / `mcp__plugin_clickmax_clickmax__custom_fields_update` (unique `fieldName` per entity type; a blank `groupName` clears the group). Check `custom_fields_group_names` and an inactive-list search for name reuse first.
- Preferred order for cleanup: `overview` -> `managed_list` with `health = unused` (then `critical`) -> `insights` on the ones the user doubts -> confirm -> `bulk_update` with `isActive = false` -> re-read `managed_list` with `isActive = false` to confirm.

## Report

- Open with the entity type and the headline: total active fields, average fill, health split.
- Order candidates worst first (`critical` before `unused`, then lowest `fillRate`); cap at 10 rows with `+N more`.
- For a field: reach (fill %), pace (new fills last 30 days), top values, then consumers by kind, named; end with the keep / fix / deactivate read.
- Before any deactivation state, per field, what references it and that those consumers will keep pointing at a hidden field. Deactivating is opt-in only.
- Say fill rates are % of all contacts/cards, and that numbers may lag a few seconds.

## Warnings

- `unused` does not mean empty of data: it means no consumer and under 5% filled. Inactivating keeps values, but they stop being editable/visible where the field was shown.
- Consumer names are collected by scanning configurations; treat an empty list as "none found", and re-check after a recent change.
- `records` shows contact names and typed values: personal data, summarize instead of dumping rows unless asked.
- Deactivation and creation revive rules are per `entityType`; never assume a leads field and an opportunities field with the same key are linked.

## Anti-patterns

- Paging `custom_fields_list` (unpaginated, heavy) to answer a fill-rate question.
- Calling `insights` in a loop over hundreds of fields; use `managed_list` for the ranking and `insights` only on the few that matter.
- Bulk-inactivating everything `unused` without reading consumers or getting a go-ahead.
- Trying to bulk-edit labels, keys, types or options — not accepted by the bulk call.
- Asking the user for the workspace id or a field id you can find with `managed_list` `search`.

---

Clickmax skill revision: `b8294822a4d6`
