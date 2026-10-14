---
name: clickmax-temperature-score
description: Use when the user wants to understand, tune, or audit contact Temperature (behavioural 0-100 engagement) and contact Score (criteria-based fit points) in Clickmax, including why one contact has a given number and the Temperature × Score health of the base.
---

## When this applies

Use for the two per-contact indicators of the CRM: **Temperature** (what the contact DID, 0-100, decays) and **Score** (who the contact IS, points from rules, does not decay). Covers reading/changing their configuration, explaining one contact's number, and measuring the base.

Not this skill:

- filtering/listing contacts by number → `clickmax-leads`, `clickmax-list-segments` (fields `temperatureScore`, `leadScore`)
- the hot/warm/cold/frozen label typed by hand on an opportunity card → `clickmax-pipelines`
- automations that react to or nudge Temperature → `clickmax-flows`

## Key assumptions

|Topic|Fact|
|-|-|
|Temperature input|behaviour only: messages, e-mail opens/clicks, pages/checkout, payments, members area, meetings, pipeline events; registration fields never count|
|Temperature model|4 sub-scores 0-100: Recency, Frequency, Depth, Declaration (intent to buy); blended by the active model; R and F decay (`halflifeR/F` days), P and D do not decay inside `windowDays`|
|Bands|cold < `thresholdMorno` ≤ warm < `thresholdQuente` ≤ hot; default preset `lancamento` = 30 / 60|
|Model vs numbers|`activeModelId` only picks the R/F/P/D blend. Thresholds, channel multipliers, window and half-lives are the numbers saved in settings: switching model does NOT copy that model's numbers|
|Per-event weights|`eventWeights` holds only overrides (−100..100); absent event = product default; channel multiplier 0 silences the whole channel; the field replaces the stored map when sent|
|Score formula|sum of `points` of ENABLED rules the contact satisfies now, floor 0, cap `maxScore`; tier low/medium/high by `thresholdMedium`/`thresholdHigh`|
|Score default|OFF. Rules can exist but nobody gets a number until `enabled: true`; turning it off clears every stored Score|
|Rule criteria|same filter tree as a segment; describes the contact (data, tags, origin, purchases), never behaviour; empty criteria scores nobody|
|Blast radius|any settings/rule save re-scores the whole base asynchronously (seconds to minutes); the write returns the saved config, not the new numbers|
|Automations|a Temperature settings save can make contacts change band and fire temperature-triggered automations in bulk; a Score settings/rule re-score fires nothing|
|Permissions|reads = any role; writes = workspace admin/editor or coordinator attendant|
|Previews|model switch → `temperature_model_impact` (bands now vs after, ≤400 active contacts re-scored then projected, inactive exact, no hysteresis, uses the TARGET model's own numbers); Score rule → `lead_score_rules_preview` with `points` (+ `ruleId` when editing) = net tier delta from the stored, already clamped Score — approximations, the re-score after saving is the truth|
|Not exposed|the six preset models are read-only; no tool enumerates the event catalog (names come from `temperature_lead_explain`); the per-slider live preview of the settings screen is browser-side only|

## Thought process

1. Classify the ask: understand one contact | audit the base | change configuration.
2. Understand/audit first, change second. A change never precedes reading current settings, because writes are full replaces.
3. Temperature question ("is engaged?") vs Score question ("is a good fit?") → never answer one with the other's tool.
4. Config changes are workspace-wide and slow to show: state that, then verify with a read after a short wait.

## Execute guide

- **Why this contact?** Resolve the contact id (`clickmax-leads`), then call `mcp__plugin_clickmax_clickmax__temperature_lead_explain` for Temperature and `mcp__plugin_clickmax_clickmax__lead_score_lead_explain` for Score. Temperature: compare `stored` vs `live` (they differ because R/F decay and the nightly pass only saves 3+ point drifts), name the top events by `weightedPoints`, and offer `missingSignals` as what would raise it. Score: list rules by `status`; `disabled` shows what would have matched, `clampedBy` says if the floor/ceiling hid part of the sum.
- **State of the base.** `mcp__plugin_clickmax_clickmax__lead_indicators_metrics` with `filters = []` (or a segment-style audience) gives bands, tiers, the matrix and `priority` (hot AND high Score) in one call. `mcp__plugin_clickmax_clickmax__lead_score_distribution` is the Score-only cut. `score.enabled = false` explains an all-`none` Score column.
- **Switch model ("what if").** `mcp__plugin_clickmax_clickmax__temperature_model_impact` with the candidate `modelId` → compare `current` vs `next` per band (say "estimated" when `estimated: true`). The preview assumes the target model's own thresholds/channels/window/half-lives; the switch only matches it if `temperature_settings_update` sends those same numbers with the new `activeModelId`.
- **Tune Temperature.** `mcp__plugin_clickmax_clickmax__temperature_settings_get` → change only what was asked → `mcp__plugin_clickmax_clickmax__temperature_settings_update` with EVERY scalar field resent. To adopt a preset wholesale, copy its numbers from `builtInModels` into the same call together with `activeModelId`. To change one event weight, resend the whole stored `eventWeights` with that entry edited (`{}` clears all overrides; omitting the field keeps them).
- **Saved calibration ("my model").** `mcp__plugin_clickmax_clickmax__temperature_custom_models_create` stores a snapshot only; it takes effect after `temperature_settings_update` with its id + its numbers. Update/delete affect just the snapshot; deleting the ACTIVE model is refused, and max 20 per workspace.
- **Set up Score.** `mcp__plugin_clickmax_clickmax__lead_score_settings_get` → for each rule: `mcp__plugin_clickmax_clickmax__lead_score_rules_preview` with `points` (size + tier shift + 3 examples) → `mcp__plugin_clickmax_clickmax__lead_score_rules_create` → finally `mcp__plugin_clickmax_clickmax__lead_score_settings_update` with `enabled: true` if it is still off (confirm `thresholdHigh` > `thresholdMedium` and ≤ `maxScore`).
- **Pause/resume a rule.** `mcp__plugin_clickmax_clickmax__lead_score_rules_set_enabled` flips only `enabled` (re-scores the base). Before switching ON, preview with the rule's `filters` + `points`. Prefer it over `mcp__plugin_clickmax_clickmax__lead_score_rules_delete`, which is permanent.
- **Edit a rule.** Preview the change with `mcp__plugin_clickmax_clickmax__lead_score_rules_preview` passing new `filters`, `points` AND the `ruleId` (so today's contribution is subtracted). `mcp__plugin_clickmax_clickmax__lead_score_rules_update` is a full replace: omitted `enabled` becomes true, `description` null, `sortOrder` 0, criteria replaced. Read the rule first and resend everything that should stay.
- Nudging one contact's Temperature from an automation is the flow action "Warm up or cool down contact" (signal: light warm, warm, cool, strong cool) → `clickmax-flows`; it records a signal that fades like any activity, it does not write a number.

## Report

- Lead with the indicator (Temperature or Score) and the job: explanation, base audit, or configuration change.
- Explanation: the number and band first, then at most 5 contributing events/rules ordered by impact (`+N more`), then what would move it. Say "not calculated yet" for null, never 0.
- Base audit: totals per band/tier, the `priority` count, then the matrix cells with the largest counts.
- Preview: bands/tiers before → after (or the net delta per tier) plus the examples; label it an estimate.
- Configuration change: the before → after of each changed field, then the blast-radius note (whole base re-scored, may take minutes; automations may fire for Temperature). Never quote new contact counts before a re-read confirms them.
- Follow-up mutations are opt-in only.

## Warnings

- Temperature settings save can trigger automations in bulk; confirm with the user before saving and prefer small steps.
- Score rules and settings writes are silent no-ops for contacts while the Score is off.
- A stale `live` vs `stored` gap is normal decay, not a bug.
- Do not put behaviour ("opened e-mail", "visited page") in a Score rule; it belongs to Temperature.
- Do not use the card hot/warm/cold label as if it were the contact Temperature number.

## Anti-patterns

- Sending a partial settings body or a partial rule update (both are full replaces).
- Assuming a preset switch loaded that preset's thresholds and channel weights.
- Deleting a rule, or resending it whole through update, just to pause it.
- Switching model without sending the target model's numbers, then expecting the previewed bands.
- Creating rules and reporting success while the Score is still disabled.
- Reporting a re-scored count right after the write, before the background job finished.

---

Clickmax skill revision: `b8294822a4d6`
