---
name: meta-agent-operations
description: "Use when proposing or executing Meta Ads changes: propose/execute workflow, campaign/adset/ad update rules, currency in cents."
metadata:
  source: "prompts/skills/meta/agent-operations"
---

# Meta Ads - Agent Operations

Rules for proposing and executing changes on Meta Ads via propose tools: dry run first, then apply with `mode: "live"` after the user approves.

## General Workflow
1. Describe the intended change in plain language to the user
2. Call the appropriate propose tool with `mode: "dryrun"`. It validates the change and returns `operation_ids`; nothing changes yet.
3. Show the user every proposed change (entity, current value, new value) and wait for an explicit yes.
4. Call the same propose tool with `mode: "live"` and only the approved `operation_ids` — there is NO separate execute tool (`facebook_execute_approved_operation` no longer exists; never call it). That response includes the execution result and any new/updated IDs.
5. Confirm outcome to the user

## Currency Rules
- ALL Meta propose tools — the create launch AND every update tool — take budgets/bids in **account currency, human-readable** (50 means $50, 300 means ₹300). The SERVER converts to cents. Never pass cents (5000 for $50 would set a 100× budget).
- Values returned by `facebook_get_campaign_details` / adset details are already in account currency; only Meta's raw insights/`account_structure` budget fields are in cents (divide by 100 for display).
- Always retrieve ad account details to confirm currency before proposing budget changes
- Display amounts with correct currency symbol — never assume USD
- Show before/after: "Current: $100.00/day → Proposed: $120.00/day (+20%)"

## Campaign Updates (`facebook_propose_update_campaigns`)
**Supported fields**: name, status (ACTIVE/PAUSED), objective, daily_budget, lifetime_budget, bid_strategy, spend_cap, pacing_type — all money fields in ACCOUNT CURRENCY (server converts to cents)
- `buying_type` is read-only after creation — will fail if changed
- `daily_budget` and `lifetime_budget` cannot coexist
- Pass `spend_cap: 0` (or `null`) to REMOVE the cap — the server substitutes Meta's max-int sentinel itself. Never pass the sentinel directly (it would be currency-converted and overflow)
- One array entry per field change for independent user approval

## Ad Set Updates (`facebook_propose_update_adsets`)
**Supported fields**: name, status, daily_budget, lifetime_budget, targeting, bid_strategy, bid_amount, optimization_goal, billing_event, destination_type, start_time, end_time, frequency_control_specs, attribution_spec — money fields in ACCOUNT CURRENCY (server converts)

**CRITICAL — Targeting is full-replacement**: When changing targeting, `new_state` must contain the COMPLETE targeting object (geo_locations, age_min, age_max, genders, flexible_spec, custom_audiences, etc.) — not just changed parts. Omitted fields get removed.

**CBO budget gating**: If the parent campaign uses Campaign Budget Optimization (CBO), ad set-level budget changes are controlled by the campaign. NEVER propose ad set budgets on a CBO campaign.

**Do NOT include `publisher_platforms`** in targeting — switching between manual and Advantage+ placements is not supported via this tool.

**Product set**: `promoted_object` (including `product_set_id`) is immutable on ad sets, and NO update tool can change a catalog ad's product set (the ad-level update schema has no product_set_id either). Direct the user to Ads Manager, or propose a fresh ad with the new product set.

## Ad Updates (`facebook_propose_update_ads`)
**Supported fields**: name, status, creative (URL + CTA only), url_tags (UTM parameters), tracking_specs

**CRITICAL — Creative requires complete object**: When updating creative fields (CTA, destination URL), provide the COMPLETE `object_story_spec` including `page_id` and ALL `link_data` fields. Omitted fields get cleared.

**NOT supported** (do not propose):
- Swap image/video (requires binary upload)
- Change primary text, headline, or description (creates new ad instead — suggest this to user)
- Update product set for catalog ads (not supported at ad level)

**Creative structure for URL/CTA changes**:
```json
{
  "object_story_spec": {
    "page_id": "<PAGE_ID>",
    "link_data": {
      "link": "https://destination-url.com",
      "call_to_action": { "type": "SHOP_NOW", "value": { "link": "https://..." } }
    }
  }
}
```

**Self-discovery**: Before proposing any ad/creative update, use `facebook_get_ad_creative_details` to fetch IDs and current state. Never ask the user for creative IDs.

## Ad Creative Updates (`facebook_propose_update_ad_creatives`)
Only `name` and `status` (ACTIVE, IN_PROCESS, WITH_ISSUES, DELETED) are updatable on existing creatives. No other fields can be updated — Meta API creates a new creative instead. If user requests text/image/video changes, explain this limitation and suggest creating a new creative.

## Budget Change Guardrails
- Budget increase > 100%: warn user this is a major increase, confirm intent
- Budget decrease > 50%: warn user this significantly reduces reach and performance
- Always distinguish daily vs lifetime budget
- Max recommended scaling: 20% at once (from guardrails)

## Status Change Warnings
- **Pausing**: Traffic and spending stop immediately
- **DELETED**: Permanent, cannot be undone — require explicit confirmation
- **ARCHIVED**: Reversible — can be unarchived (set back to PAUSED)

## Bidding Changes
- Changing bid strategy resets the learning phase — always warn user
- Display bids in human-readable format: "Cost Cap: $15.00" not "bid_amount: 1500"
- Target CPA / Target ROAS require sufficient conversion history

## Common CTA Types
SHOP_NOW, LEARN_MORE, SIGN_UP, BOOK_NOW, CONTACT_US, DOWNLOAD, GET_OFFER, BUY_NOW, SUBSCRIBE, ORDER_NOW, APPLY_NOW, GET_QUOTE, WHATSAPP_MESSAGE, CALL_NOW, NO_BUTTON

## Dynamic URL Macros
`{{campaign.id}}`, `{{campaign.name}}`, `{{adset.id}}`, `{{adset.name}}`, `{{ad.id}}`, `{{ad.name}}`, `{{placement}}`, `{{site_source_name}}`
