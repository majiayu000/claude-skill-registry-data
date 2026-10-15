---
name: google-ads-create-master-skill
description: "MUST load FIRST for any Google Ads create, update, or mutation task. Master workflow for create campaigns, ad groups, ads, assets, sitelinks, experiments, negative keyword lists, bid modifiers, pause/rename/update. Triggers: any Google Ads write intent."
metadata:
  source: "prompts/skills/google_ads/create/master-skill"
---

# Google Ads Mutation Workflow

Master workflow for any Google Ads create or update operation — campaigns, ad groups, ads, assets, experiments, shared negative lists, bid modifiers. Sequence is fixed: confirm intent → pull context → propose as a dry run → show the exact changes → explicit user yes → apply with `mode: "live"` → confirm.

> **Tool behavior:** Every `google_ads_propose_*` tool both validates and applies: call it with `mode: "dryrun"`, show the user every proposed change (entity, current value, new value), and only after an explicit yes call it again with `mode: "live"` and the approved `operation_ids`. There is NO separate execute tool of any kind. Campaign + ad group + ad creation happens in **ONE call** to `google_ads_propose_create_campaign_structure` (the legacy `google_ads_propose_create_campaign` / `_create_adgroup` / `_create_ad` tools no longer exist — never call them). Execution is a single atomic mutate: the whole structure lands or nothing does. Capture the returned IDs and resource names from the tool response.

---

## Sub-Skill Index

Each step has a dedicated sub-skill. **Read the sub-skill at its step — not all upfront.**

| Step | Read before | Path |
|------|------------|------|
| Campaign — create slot / update | Filling the `campaign` slot of `google_ads_propose_create_campaign_structure`, or calling `google_ads_propose_update_campaigns` | `references/campaign.md` |
| Ad group — create slot / update | Filling the `adgroup` slot of `google_ads_propose_create_campaign_structure`, or calling `google_ads_propose_update_adgroups` | `references/ad-group.md` |
| Ads (RSA) — create slot / update | Filling the `ads` array of `google_ads_propose_create_campaign_structure`, or calling `google_ads_propose_update_ads` | `references/ad.md` |
| Create / update asset, update PMax asset group | Calling `google_ads_propose_create_asset`, `google_ads_propose_update_asset`, or `google_ads_propose_update_pmax_asset_group` | `references/asset.md` |
| Create / update experiment | Calling `google_ads_propose_create_experiment` or `google_ads_propose_update_experiment` | `references/experiment.md` |
| Create / update shared negative keyword list | Calling `google_ads_propose_create_negative_keyword_list` or `google_ads_propose_update_negative_keyword_list` | `references/negative-keyword-list.md` |
| Adjust bid modifiers / ad schedule | Calling `google_ads_propose_update_bid_modifiers` | `references/bid-modifiers.md` |

Always honor `google-ads-guardrails` before proposing any change.

---

## Phase 1 — Confirm the Mutation Intent

Read the user's request and identify:
- **Action** — create or update?
- **Entity type** — campaign / ad group / ad / asset / experiment / negative list / bid modifier
- **Customer ID** — must be 10 digits, no dashes. Confirm with the user only if multiple accounts are accessible or the request is ambiguous.
- **Manager ID** — required only when operating cross-account through an MCC.

If the entity type is ambiguous (e.g. user says "boost mobile by 20%" — could be DEVICE bid modifier or campaign-level mobile bid), ask exactly one clarifying question. Otherwise proceed.

---

## Phase 2 — Pull Just-Enough Context

Run targeted GAQL queries to fill in what's needed for a clean propose. Don't dump raw rows at the user — synthesize into 1–3 lines.

Common probes (run only what's relevant):
- `customer.currency_code` — needed for any budget input.
- Existing `campaign_budget.id` — when reusing a budget instead of creating one.
- `campaign.advertising_channel_type` + `campaign.bidding_strategy_type` — when switching strategies on update.
- `ad_group.id`/`name` + parent `campaign.id` — when adding ads or keywords to an existing group.
- `customer.conversion_tracking_status` — required gate for smart bidding (TARGET_CPA / MAXIMIZE_CONVERSIONS / TARGET_ROAS / MAXIMIZE_CONVERSION_VALUE).

If the account has no conversion tracking and the user asked for smart bidding, the validator will reject — instead, propose `MAXIMIZE_CLICKS` (TARGET_SPEND) and tell the user why.

---

## Phase 3 — Propose

Read the relevant sub-skill from the index above. Build the propose call with all auto-detected values filled in. Each entry in a batched call returns its own `operation_id`, so the user can approve or decline each item.

Output a tight summary table to the user *before* the propose tool returns its preview — keep it short:

| Field | Proposed value | Source |
|---|---|---|
| ... | ... | ... |

After the dry-run call returns, show the user each proposed change (entity, current value, new value) and ask for an explicit yes. Then call the same tool with `mode: "live"` and only the approved `operation_ids`; that response includes the execution result and any returned IDs/resource names.

---

## Phase 4 — Read the Result

The propose tool returns one merged response covering propose **and** execute. Inspect it:

- `success: true` and `execution_results[]` populated → mutation landed. Capture each entry's `entity_id`, `resource_names`, and surface the relevant IDs to the user.
- `success: false` and `execution_results[i].success === false` → mutation failed at the platform. Read `error_code`, `error`, `platform_errors[]` from that entry.
- `validation_errors[]` populated → propose-side validation rejected before any approval prompt. Fix the inputs and re-propose.
- `rejected_operation_ids[]` populated → user declined. Do nothing further unless they ask.
- `timeout_operation_ids[]` populated → user didn't act in the active window. They can still approve via the panel for 24 hours — let them know, then stop.

If a step fails:
1. Read `validation_errors[]` and `platform_errors[]` carefully. If the root cause is fixable from the agent side (e.g. validation, bad ID), correct it and retry once.
2. If the same step fails again or the error needs a manual fix in Google Ads UI (policy violation, account suspension, missing permission), stop and surface it cleanly. Don't loop on the same broken payload — explain what failed and what the user needs to do.

---

## Phase 5 — Confirm

After execution succeeds, post one short confirmation line per entity. Format:

> Done. Created campaign `<name>` (id `<id>`) ENABLED and ad group `<name>` (id `<id>`) ENABLED. Ads are PAUSED — enable when ready.

**Default status convention** (mirrors Meta):
- **Campaigns** — created `ENABLED` (active)
- **Ad groups** — created `ENABLED` (active)
- **Ads** — created `PAUSED`. Ads are the user's final gate before spend begins.

Even when the user says "launch it" or "go live", new ads stay `PAUSED` until the user explicitly approves an enable step. To enable: separate explicit propose call — `google_ads_propose_update_ads` setting `status: ENABLED`. (Dry run first; apply with `mode: "live"` only after an explicit yes.)

We only flip between `ENABLED` and `PAUSED`. There is no removal — the API supports it, but our skill set deliberately does not. If the user asks to "delete" or "remove" an entity, propose pausing it instead and explain.

---

## Edge Cases

- **Empty account, no reference campaigns:** Use cold-start defaults — `MAXIMIZE_CLICKS` bidding, single GEO from the user's market, English language, ~$30–$50/day budget. Flag the cold start once: "No active campaigns to mirror — using defaults; happy to adjust before approval."
- **Smart bidding requested but no conversion tracking:** Propose `MAXIMIZE_CLICKS` instead. Tell the user the account needs conversion tracking before TARGET_CPA / TARGET_ROAS / MAXIMIZE_CONVERSIONS / MAXIMIZE_CONVERSION_VALUE will work.
- **Multiple items in one batch (UPDATE tools):** Use a single propose call with N items in the array — never split into N calls.
- **Any create request — campaign, ad group, ads, or all three** ("create a campaign with an ad group and ads"): ONE call to `google_ads_propose_create_campaign_structure` with `campaign` + `adgroup` + `ads` slots. Each level is a config to create XOR an existing id (`campaign`/`campaign_id`, `adgroup`/`adgroup_id`). The server links levels via temp IDs inside one atomic mutate — you NEVER capture and thread IDs between create steps. **ONE ad group per call**; more ad groups → additional calls passing `campaign_id`. All ads in a call land in that call's single ad group.
- **Rejection semantics:** the execution is all-or-nothing. If the user rejects every ad of a launch that proposed ads — or rejects a parent whose children were approved — the server creates NOTHING (no orphan campaign/ad group shells).
- **Re-using a budget (`budget_id`):** Always GAQL-confirm the budget exists and is not removed before referencing.
- **Cross-account (MCC):** `manager_id` must be set on the propose call. Verify the manager has linkage to the customer before proposing.

---

## Output Rules

- **Phase 1 / Phase 2 synthesis:** 1–3 lines. Account, currency, reference campaign or "cold start". Done.
- **Phase 3 summary table:** Compact. Only fields the user could reasonably want to override.
- **Approval:** Show the dry-run changes once, clearly, and ask for an explicit yes before calling with `mode: "live"`.
- **Phase 4 errors:** Short error line + suggested fix. No raw API dumps.
- **Phase 5 confirmation:** One line per executed entity. Then stop.

Never mention "skill", "protocol", "propose tool", or internal tool names in user-facing output — describe what's happening in business terms.
