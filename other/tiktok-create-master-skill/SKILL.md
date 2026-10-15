---
name: tiktok-create-master-skill
description: "Use for any TikTok Ads launch: a new campaign, ad group or ads, catalog and Smart+ campaigns. Creative-first, placement-aware, one-call launch via tiktok_propose_create_campaign_structure with approval before anything goes live."
metadata:
  source: "prompts/skills/tiktok/create/master-skill"
---

# TikTok Ad Launch Workflow

A creative-first workflow for launching TikTok ads. The sequence is fixed:
**creative → placement → account scan → propose**. Placement is decided *second*,
immediately after the creative, because on TikTok the creative format dictates
the placement and **placement can never be changed after the ad group exists**.

> **Tool behavior:** the entire launch — campaign, ad group and ads — is proposed
> in **ONE call** to `tiktok_propose_create_campaign_structure`. Each entity gets
> its own `operation_id`. Through AI app connections TikTok changes can only be
> validated as a dry run: show the user the validated launch, then give them the
> steps to apply it in TikTok Ads Manager (see `tiktok-ads`). Where a live call is
> possible, it executes in dependency order (campaign → ad group → ads). Never thread IDs between slots — the server wires
> each new parent's ID into its children.

---

## HARD RULE — Creation Failure Limit (strictly enforced)

**If a launch call fails 2 or more times within the same workflow, STOP.** Do not
propose again, do not retry, do not attempt a workaround.

> "I've attempted this step twice and it wasn't successful both times. This looks
> like it needs a change in TikTok Ads Manager or an account permission I can't
> resolve from here. I'd suggest reviewing the error above before trying again in
> a new conversation. Is there anything else I can help you with?"

A "failure" is a validation error (601), a platform error (403), or a thrown
exception. A user rejecting a card is NOT a failure. Partial success is NOT a
failure — re-propose only the failed children with `adgroup_id`.

**Never keep varying one parameter to escape an error.** If a create fails on
targeting or placement, the fix is almost always a *different* field than the one
you just changed. Guessing countries one at a time is the classic wrong loop.

---

## Sub-Skill Index

| Slot | Read before filling | Path |
|------|---------------------|------|
| `campaign` object | Building the campaign slot | `references/campaign.md` |
| `adgroup` object | Building the ad group slot | `references/ad-group.md` |
| `ads` array | Building the ads | `references/ad.md` |
| Upgraded Smart+ (any smart_plus work) | Before touching `tiktok_propose_manage_smart_plus` | `references/smart-plus.md` |

**Slot combinations** (each parent is a config to create XOR an existing ID):
- `campaign` + `adgroup` + `ads` → full launch
- `campaign_id` + `adgroup` + `ads` → new ad group + ads under an existing campaign
- `adgroup_id` + `ads` → add ads to an existing ad group
- **ONE ad group per call.** More ad groups → one call each, passing `campaign_id`.

---

## Phase 1 — Get the Creative

The creative comes first, always.

- Image, video or carousel attached → go to Phase 2.
- Referenced an existing ad → pull it and go to Phase 2.
- Nothing attached → ask exactly one question: *"Share the creative, or point me
  to an existing ad to clone."* No objective, budget or audience questions.

**Exception — catalog / shop ads.** If the user asks to promote a *product feed
or store* rather than a specific creative ("run catalog ads", "promote my
products", "GMV Max"), there is no creative to collect. Skip to the inventory
check in Phase 3 instead, and pick the path from what actually exists:

| Inventory found | Path |
|---|---|
| A catalog (`resource: CATALOG`) | `PRODUCT_SALES` + `campaign_product_source: CATALOG` → catalog ad group + ads |
| Only a TikTok Shop store (`resource: STORE`) | `GMV_MAX` — campaign-only, no ad group or ads |
| Neither | **Stop and say so.** No tool here creates a catalog; it must be set up in TikTok Ads Manager / Business Center first. |

Having a store does **not** imply having a catalog — most Shop accounts have a
store and zero catalogs. Check before promising either path.

---

## Phase 2 — Decide the Placement (TikTok-specific, do this early)

**The creative format decides the placement, and the placement decides
everything downstream.** Get this wrong and the ad group must be rebuilt — it
cannot be edited.

| Creative | Placement | Identity type |
|---|---|---|
| Video | `PLACEMENT_TIKTOK` or automatic | `BC_AUTH_TT` / `TT_USER` |
| Carousel | `PLACEMENT_TIKTOK` | `BC_AUTH_TT` / `TT_USER` |
| **Single image** | **`PLACEMENT_PANGLE` or `PLACEMENT_GLOBAL_APP_BUNDLE` only** | **`CUSTOMIZED_USER`** |

Three rules that cause most launch failures:

1. **A single image ad cannot run on TikTok feed.** Doc 1777633230937090 — image
   ads exist only on Pangle and Global App Bundle. On TikTok placement the create
   fails with `Incorrect source field (40002)`, which names nothing.
2. **The identity type must match the placement.** Spark identities
   (`BC_AUTH_TT`, `TT_USER`) exist only on TikTok. Pangle and Global App Bundle
   take the advertiser's own `CUSTOMIZED_USER` identity. Mixing them gives the
   same `Incorrect source field`.
3. **Pangle and Global App Bundle serve far fewer countries than TikTok**, and
   the list depends on the ad account's registration market. Verify before
   proposing — see Phase 3.

If the user supplied a still image and wants US or UK delivery, say so plainly
before proposing: image ads cannot serve there on most accounts, and the options
are a Pangle-eligible country or a video creative.

---

## Phase 3 — Scan the Account

Pull what you need to propose without asking. Synthesise into 1–2 lines; never
dump raw data.

- Existing campaigns/ad groups — objective, optimization goal, budgets, geos
- `tiktok_get_identities` — **note which types exist.** You need a
  `CUSTOMIZED_USER` identity for image ads and a `BC_AUTH_TT`/`TT_USER` one for
  video. If the required type is missing, that's a blocker worth stating early.
- Pixel(s) via `tiktok_list_pixels` when optimizing for CONVERT/VALUE
- **Catalog / store inventory** via `tiktok_list_catalogs` — only for the catalog
  or GMV Max paths. `resource: CATALOG` → `PRODUCT_SET` → `PRODUCT` (individual
  SKUs), or `resource: STORE` for TikTok Shop. This is a read-only listing; it
  cannot create a catalog, a product set, or a store.
- **Available locations for the chosen placement.** Call `/tool/region/` with
  `placements` + `objective_type` (`tiktok_search_targeting` surfaces this).
  Never assume a country is eligible, and never copy a country list from
  documentation — the live list differs per account and changes.

**Synthesis output:** "Ref: `<campaign>` — Website conversions / CONVERT+SHOPPING
/ US 18-55 / $25/day. Pixel `<n>`, identity `<name>` (BC_AUTH_TT)."

---

## Phase 4 — Propose or Ask

Default to proposing. Ask only when a choice genuinely changes the outcome:
multiple ad accounts, an ambiguous funnel stage, or no reference data and unknown
budget. Batch into one turn, max 2 questions, tappable options.

---

## Phase 5 — Show the Configuration

| Field | Proposed value | Source |
|---|---|---|
| Objective | Website conversions | Mirrors top campaign |
| Placement | Pangle (image creative) | Creative format |
| Locations | Canada | Pangle-eligible, from /tool/region/ |
| Optimization | CONVERT / SHOPPING | Account default |
| Daily budget | $25 | Median of existing ad groups |
| Identity | EvanAlexanderGrooming (CUSTOMIZED_USER) | Required for Pangle |
| Status | Paused | Always |

Then send the proposal as a dry run and show the user exactly what it would create.

---

## Phase 6 — Launch (ONE call)

```json
tiktok_propose_create_campaign_structure({
  "advertiser_id": "...",
  "currency_code": "USD",
  "campaign": { ...per references/campaign.md... },
  "adgroup":  { ...per references/ad-group.md... },
  "ads":      [ ...per references/ad.md... ]
})
```

- Never split into one call per entity. Never pass IDs between slots.
- **Everything is created PAUSED** (`operation_status: DISABLE`). TikTok's own
  default is ENABLE — i.e. live spend on approval — so the server forces DISABLE
  unless the user explicitly asks otherwise. Enable after review.
- The dry run persists operations; the live call takes only `operation_ids` +
  `account_id`. Do not resend the full payload on the live call.

---

## Other campaign families — dedicated tools, not this launch flow

- **Upgraded Smart+**: reads `tiktok_get_smart_plus`, writes
  `tiktok_propose_manage_smart_plus` — load
  `references/smart-plus.md` first; the payload rules differ
  from everything in this skill.
- **Reach & Frequency** (reservation buying): estimate with
  `tiktok_get_reach_frequency`, then `tiktok_propose_manage_reach_frequency`.
  CREATE_ADGROUP RESERVES REAL BUDGET on approval and cannot be paused; the
  account must be R&F-allowlisted AND hold a Commercial Contract for Branding.
- **Split tests**: `tiktok_get_split_test` / `tiktok_propose_manage_split_test`
  — CREATE overwrites both ad groups' budgets and requires them ENABLED.
- **Appeals & offline events**: `tiktok_get_offline_event_sets` /
  `tiktok_propose_manage_review_and_events` — an appeal is one-shot per
  rejection.

## Reading TikTok's errors

TikTok returns `40002` for almost everything and rarely names the field. The
server rewrites the two worst offenders — trust its added explanation.

| Message | What it actually means |
|---|---|
| `Incorrect source field` | The identity type doesn't match the placement (or an image ad is on TikTok placement). Not a creative problem. |
| `Unable to access image…` | You passed `material_id` where `image_ids` wants the `image_id` (`ad-site-i18n-sg/...`). |
| `You must upload an image` | A video ad has no cover — pass `image_ids` with the cover. |
| `audience … must increase to over 1000` | The targeted countries have no eligible inventory on the chosen placement. Change the placement or the countries — not the audience size. |
| `Custom identities are no longer supported` | `CUSTOMIZED_USER` on TikTok placement. Use `BC_AUTH_TT`/`TT_USER` there. |
| `shopping_ads_type` rejected as an invalid enum | You used the campaign-level values (`PRODUCT`/`LIVE`) on the ad group, or the ad-group values (`VIDEO`/`LIVE`/`PRODUCT_SHOPPING_ADS`) on a GMV_MAX campaign. Same field name, different enum per slot. |
| `Copy API is an allowlist-only feature` | Campaign copy (regular AND Smart+) is not granted to this advertiser. Stop — a TikTok representative must enable it. Retrying cannot help. |
| CTA `not supported` repeated across different values | Account-enablement wall (Smart+ ads), not a payload problem. Stop instead of iterating CTA values. |
| `Split tests can only be created for active ad groups` | The split-test endpoint requires ENABLED ad groups at creation time, even with a future start_time. |
| `description: Missing data for required field` (offline event sets) | `/offline/create/` requires `description` even though the doc table doesn't mark it. |
| `Your budget setting must not be less than $50` (or similar) | Some accounts enforce a HIGHER floor than the documented $20 baseline per objective. Re-propose at the number TikTok names. |

**Never re-upload a creative in response to any of these.** The asset is fine;
the configuration is not.
