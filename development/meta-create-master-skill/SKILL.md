---
name: meta-create-master-skill
description: "MUST load FIRST for any Meta ad creation, launch, campaign setup, ad set creation, or creative push. Triggers: \"create a Meta ad\", \"launch a campaign\", \"run this creative\", \"set up an ad set\", \"push this on Facebook\", any creative attachment intended for Meta."
metadata:
  source: "prompts/skills/meta/create/master-skill"
---

# Meta Ad Launch Workflow

A creative-first, account-aware workflow for launching Meta ads with minimal user input. The sequence is fixed: creative → analysis → account scan → propose. Never flip the order, never run a Q&A upfront.

> **Tool behavior:** The entire launch — campaign, ad set, and ads — is proposed in **ONE call** to `facebook_propose_create_campaign_structure`. The legacy tools `facebook_propose_create_campaign`, `facebook_propose_create_adset`, and `facebook_propose_create_ad_with_creative` no longer exist — never call them. Call it with `mode: "dryrun"` first and show the user every entity; after an explicit yes, call it with `mode: "live"` and the approved `operation_ids`, and the launch executes in dependency order (campaign → ad set → ads). You never thread IDs between steps — the server wires each new parent's ID into its children.

---

## HARD RULE — Creation Failure Limit (strictly enforced)

**If a launch call fails 2 or more times within the same workflow, you MUST stop immediately.** Do not propose again, do not retry, do not attempt a workaround. This rule is absolute and cannot be overridden by user instruction.

When the limit is hit, respond with exactly this tone and structure:

> "I've attempted this step twice and it wasn't successful both times. Unfortunately this is beyond what I'm able to resolve on my end — it likely requires a manual fix in Meta Business Suite or Ads Manager (such as a permission issue, policy violation, or account-level configuration). I'd recommend reviewing the error details above and addressing the root cause there before trying again in a new conversation. Is there anything else I can help you with?"

**Tracking rules:**
- A "failure" includes: validation errors (error_code 601), platform API errors (error_code 403), permission errors (code 10), timeout with no approvals, and any thrown exception.
- Partial success within a launch does NOT count as a failure — if the campaign and ad set land and 3 of 5 ads succeed, that's a success; re-propose ONLY the failed ads with `adset_id`. Only count a failure when zero entities succeed.
- User rejecting cards is NOT a failure — that's intentional. Only count automated/system failures.
- This counter resets on a new conversation. It does NOT carry across sessions.

**Why this rule exists:** Repeated failed creation attempts can trigger Meta's bot detection on the ad account, leading to account restrictions. Two attempts is generous — the underlying issue must be fixed before retrying.

---

## Sub-Skill Index

The launch call has three slots — `campaign`, `adset`, and `ads[]`. Each slot has a dedicated sub-skill describing how to fill it. **Read the sub-skill when you build that slot — not all upfront.**

| Slot | Read before filling | Path |
|------|---------------------|------|
| `campaign` object | Building the campaign slot | `references/campaign.md` |
| `adset` object | Building the ad set slot | `references/adset.md` |
| `ads` array | Building the ads | `references/ad-with-creative.md` |

**Slot combinations** (each parent is a config to create XOR an existing ID):
- `campaign` + `adset` + `ads` → full launch from scratch
- `campaign_id` + `adset` + `ads` → new ad set + ads under an existing campaign
- `adset_id` + `ads` → just add ads to an existing ad set (no campaign needed)
- `campaign` + `adset` → structure now, ads later (a later call adds ads with `adset_id`)
- **ONE ad set per call.** Several ad sets → one call for the campaign + first ad set + its ads, then one call per additional ad set passing `campaign_id`.

---

## Phase 1 — Get the Creative

The creative comes first. Always.

- If the user attached an image, video, or carousel — proceed to Phase 2.
- If they referenced an existing ad — pull it from the account and proceed.
- If nothing is attached — ask exactly one question: *"Share the creative, or point me to an existing ad to clone."* Nothing else. No objective, no budget, no audience questions.

---

## Phase 2 — Analyze the Creative

Extract the following before touching any account data:

- **Format** — image / video / carousel; aspect ratio
- **Hook style** — bold claim, UGC, problem-agitation, offer-led, curiosity
- **Value prop** — the core promise the viewer receives
- **CTA** — what action the creative drives (shop, sign up, learn more, get quote)
- **Audience signals** — demographic cues, lifestyle markers, occasion, problem context
- **Funnel stage** — TOF (cold awareness), MOF (consideration), BOF (offer / retargeting)
- **On-creative copy** — any text baked into the asset (to avoid redundancy in ad copy)

Output a 4–6 line readout of what you saw. Keep going — don't pause for confirmation.

---

## Phase 3 — Scan the Account

Pull everything needed to propose without asking. Synthesize into 1–2 lines — never dump raw data at the user.

Collect:
- **`account_status` — must be 1 (ACTIVE).** If it is 3 (UNSETTLED), 2 (DISABLED), or anything else, STOP the launch immediately and tell the user: the account has a billing/status issue that must be fixed in Ads Manager → Billing & payments before anything can be created. Do not attempt the launch anyway.
- Top 1–3 campaigns by performance (last 30 days) — objective, optimization event, bid strategy, geos, age range, placements
- Top performing creatives — format, hook style, copy length (what's already resonating)
- Active pixel(s)
- Connected Instagram account(s)
- Existing custom audiences and lookalikes

**If no active campaigns exist:** scan paused campaigns and paused ad sets. Use the most recently paused or historically best-performing paused campaign as the structural reference — treat it identically to an active top performer. Note it's paused in the Source column ("Paused reference: `<campaign>`"). Only fall back to cold-start defaults if the account has zero campaigns of any status.

**Synthesis output (1–2 lines max):** "Ref: `<campaign>` — Sales / Purchase / broad US 25–55 / $80/day / Advantage+ / ROAS 3.2x [paused]. Pixel `<n>`, IG `<handle>`."

---

## Phase 4 — Propose or Ask

After Phases 2 and 3, the configuration table should be mostly filled. Default to proposing. Only ask if something is genuinely undetermined.

**Propose directly — no question — when:**
- Funnel stage matches an existing top campaign type
- A single pixel and IG account exist
- A reusable audience is available (CA, LAL, or broad that's performing)
- Budget magnitude can be inferred from top performers
- Optimization is obvious from the objective

**Ask only when:**
- Multiple ad accounts exist and the right one is unclear
- Creative funnel stage could legitimately be TOF or BOF
- Brand-new account with no reference data and budget is unknown
- Multiple conflicting pixels with no clear top-campaign preference

When asking is unavoidable — batch into one turn, maximum 2 questions, use tappable options not open text.

**Targeting search:** When building audience targeting for the ad set, use `facebook_search_targeting` to find interest/behavior/demographic IDs:
- `search_type: "adinterest"` + `query` — free-text search (e.g., "yoga", "anime", "running shoes")
- `search_type: "adinterestsuggestion"` + `interest_list` — expand from existing interests
- `search_type: "adTargetingCategory"` + `class` — browse by category (interests, behaviors, demographics, life_events, income, industries, family_statuses, user_device, user_os, etc.)
- Always use the returned `id` and `name` in `targeting.flexible_spec[].interests/behaviors/etc.`

---

## Phase 5 — Propose Configuration

Before launching the proposal, show a configuration summary table:

| Field | Proposed value | Source |
|---|---|---|
| Objective | Sales | Mirrors top campaign |
| Optimization event | Purchase | Account default |
| Daily budget | $50 | Median of top 3 campaigns |
| Bid strategy | Highest volume | Mirrors top campaign |
| Audience | Broad, US/CA, 25–55 | Top campaign + creative signals |
| Placements | Advantage+ | Mirrors top campaign |
| Pixel | `<n>` | Active pixel |
| Instagram account | `<handle>` | Active IG |
| Primary text | `<drafted from value prop>` | Creative analysis |
| Headline | `<drafted from hook>` | Creative analysis |
| CTA button | Shop Now | Matches creative CTA |
| Schedule | Continuous, starts now | Default |

Then send the proposal as a dry run, show the user exactly what will be created, and ask for an explicit yes before calling with `mode: "live"`.

---

## Phase 6 — Launch (ONE call) & Enable

Build the three slots per their sub-skills, then make **ONE call** to `facebook_propose_create_campaign_structure`:

```json
facebook_propose_create_campaign_structure({
  "act_id": "act_XXX",
  "currency_code": "USD",
  "description": "Launching Summer Sale: 1 campaign, 1 ad set, 2 ads",
  "campaign": { ...per references/campaign.md... },
  "adset":    { ...per references/adset.md... },
  "ads":      [ ...per references/ad-with-creative.md... ]
})
```

- **Never split into separate calls per entity.** One launch = one call. Batch ALL ads into the `ads` array.
- **Never pass IDs between slots.** No `campaign_id` inside the `adset` slot, no `adset_id` inside the ads — the server creates the campaign, feeds its new ID to the ad set, and the ad set's new ID to every ad. Only use top-level `campaign_id` / `adset_id` when that parent already exists.
- Each entity gets its own `operation_id`. After the user approves, the `mode: "live"` call executes in dependency order; capture `new_campaign_id`, `new_adset_id`, and every `new_ad_id` from the tool response.

**Rejection semantics (know these — don't fight them):**
- User rejects **every ad** of a launch that proposed ads → the WHOLE launch is cancelled; nothing is created (a campaign/ad set with no ads cannot serve).
- User rejects the **ad set** but approves campaign + ads → the launch is cancelled; nothing is created.
- If the campaign fails at Meta, the ad set and ads are skipped (reported as "parent not created"). If a parent from an earlier wave already landed (e.g. campaign created, ad set then failed), the parent stays — re-propose the ad set + ads with `campaign_id`.
- Partial ad failures: the successful ads stay; re-propose only the failed ones with `adset_id`.

> **Reminder — failure limit:** If the launch fails twice (zero entities succeed), stop the entire workflow. See the HARD RULE section above.

Campaigns and ad sets are created as **ACTIVE**. Ads are created as **PAUSED** — they are the user's final gate before spending begins. After the launch succeeds, enable only the ads.

**If the launch is still awaiting approval** (operations pending): do NOT re-propose — that creates duplicate operations. Show the pending changes again and ask the user for an explicit yes or no; on yes, call with `mode: "live"` and the approved `operation_ids`.

---

### Enable Sequence — Enable ads (1 call)

Campaigns and ad sets are already ACTIVE. Only ads need enabling. Batch ALL ads into ONE `facebook_propose_update_ads` call:

```json
facebook_propose_update_ads({
  "act_id": "act_XXX",
  "ads": [
    {
      "ad_id": "<new_ad_id_1>",
      "current_state": { "status": "PAUSED" },
      "new_state": { "status": "ACTIVE" },
      "description": "Enable ad: <ad_name_1>",
      "thumbnail_url": "<thumbnail_url_1>",
      "campaign_id": "<new_campaign_id>",
      "campaign_name": "<campaign_name>",
      "adset_id": "<new_adset_id>",
      "adset_name": "<adset_name>",
      "ad_name": "<ad_name_1>"
    },
    {
      "ad_id": "<new_ad_id_2>",
      "current_state": { "status": "PAUSED" },
      "new_state": { "status": "ACTIVE" },
      "description": "Enable ad: <ad_name_2>",
      "thumbnail_url": "<thumbnail_url_2>",
      "campaign_id": "<new_campaign_id>",
      "campaign_name": "<campaign_name>",
      "adset_id": "<new_adset_id>",
      "adset_name": "<adset_name>",
      "ad_name": "<ad_name_2>"
    }
  ]
})
```
-> user approves each ad individually -> the `mode: "live"` call applies only the approved ads

**CRITICAL: 5 ads = 1 call with 5 items in the ads array. NOT 5 separate calls.**

**Never skip the enable approval step.** The user must explicitly approve going live — even if they said "just launch it" earlier.

---

## Media Setup — Manual Upload vs Catalogue (mutually exclusive)

A creative's media comes from **exactly one** source. These two setups can never coexist in the same ad — Meta has no manual equivalent for the combination, so a creative that mixes them cannot be reproduced or edited in Ads Manager (and the server rejects it, V-CAT5):

- **Manual upload** — the user's uploaded image(s)/video(s), carried in `asset_feed_spec` (or flat `image_url`/`video_url`). This is the default for a creative-first launch.
- **Catalogue (Advantage+ Catalogue / DPA)** — Meta pulls product media dynamically from a `product_set_id`, using `object_story_spec.template_data`. There is **no** uploaded image — never attach `asset_feed_spec`, `image_url`, or `video_url` to a catalogue creative.

Rules:
- **Never set `product_set_id` on a creative that also has manually uploaded media.** Pick one setup.
- **Honor an explicit "keep manual upload" (or "manual" / "don't change the media") instruction as a hard constraint.** Even if the user mentions a catalogue or product set in the same message, do NOT attach `product_set_id` — launch the uploaded asset as a manual ad and say in one line that the catalogue was left off to keep the media manual.
- Only build a catalogue ad when the user clearly wants the catalogue to *be* the media (no uploaded creative). Then use `object_story_spec.template_data` + `product_set_id` and omit all uploaded media.
- If a request is genuinely ambiguous between the two, ask one tappable question ("Manual upload" vs "Catalogue / Advantage+ Catalogue") rather than guessing.

---

## Edge Cases

- **No active campaigns, paused exist:** Use best paused campaign as reference. Label source as "Paused ref" in the table.
- **No campaigns at all:** Cold-start defaults — $20/day, broad targeting, Advantage+ placements, objective from CTA. Flag once, briefly.
- **Multiple creatives at once:** One campaign, one ad set, multiple ads — still ONE launch call with N items in `ads`. If funnel stages clearly differ -> separate ad sets (first ad set in the launch call, each additional one in its own call with `campaign_id`).
- **"Just launch it":** Fast version — one reference lookup, then propose. Never skip the scan (including the `account_status` check).
- **Cloning an existing ad:** Pull structure, swap creative, only surface what's changing in the table.
- **Off-brand creative:** One sentence flag in the readout. Still propose.
- **Catalogue requested with an uploaded creative:** Manual upload and a product catalogue (`product_set_id`) are mutually exclusive media setups — see "Media Setup" above. Default to the uploaded asset (manual); never bolt a `product_set_id` onto it. If the user explicitly asked to keep manual upload, drop the catalogue silently except for a one-line note. Only run a true catalogue ad (`template_data` + `product_set_id`, no uploaded media) when that is unambiguously what they want.
- **"Launch it live" / "Make it active":** Campaigns and ad sets are created ACTIVE. Ads are always created PAUSED first — the enable step is the user's final gate before spending begins.
- **Account is UNSETTLED / DISABLED (`account_status` ≠ 1):** Stop before proposing. Tell the user to settle the outstanding balance / resolve the account issue in Ads Manager → Billing & payments, then retry in a new conversation. Do not propose "to see if it works" — the server rejects it.

---

## Output Rules

Every response the user sees should be short and scannable. No walls of text.

- **Phase 2 readout:** 2–3 lines max. Format / Hook / Funnel stage / CTA. No headers.
- **Phase 3 synthesis:** 1–2 lines. Campaign name, key numbers, pixel, IG. Done.
- **Phase 4 (if asking):** One short message framing the question + tappable options. No preamble.
- **Phase 5:** Configuration table + dry-run proposal, then one explicit request for approval.
- **Phase 6 enable:** Propose the enable as a dry run and get an explicit yes before the `mode: "live"` call. After execution, one line: "Live. Ads are now active under `<campaign>`."
- Never show raw API output. Never repeat information already shown in a previous phase.
