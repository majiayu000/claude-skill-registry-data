---
name: article-publisher
description: Turn fb.ai article briefs into published articles — check the destination is connected, price the batch (1.0 quota per article), generate, optionally route through human approval, then publish to the connected CMS/social platform. Also owns the publishing calendar and fb.ai's daily autopilot automations. Run on demand, after seo-researcher.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Generate articles from fb.ai content briefs, publish them to a connected CMS or social platform, manage the publishing calendar, and configure daily autopilot"
deps:
  mcp: []
  gateway: ["fivebucks (**scopes: content, publishing, integrations**)", "FiveAgents (logging)"]
  files: ["brand.md", "tone-of-voice.md (opt)"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.1 | July 13, 2026 |

**Description:** Turn fb.ai article briefs into published articles — verify the destination is connected, price the batch, generate, optionally route through human approval, then publish.

### Change Log

**v2.20.1** — July 13, 2026
- **Corrected the `whoami` quota field (v2.20.0 referenced a `quota.remaining` field that doesn't exist)** — quota now read from `quota.quotas.content_generation.{current, max}`. Added a use-existing-first check (Step 3) so the skill checks `fivebucks_list_content` for an already-generated article before spending 1.0 quota to regenerate one. Corrected the contentId field name — `fivebucks_list_content` returns `id`, not `contentId`.

**v2.20.0** — July 12, 2026
- Initial release. Drives fb.ai's `content` + `publishing` + `integrations` scopes (gateway v1.8.0).
- **Gained the publishing calendar and the daily autopilot automations** (Steps 9–10). These were originally slated to go into the four *social* skills, but fb.ai's `publish_content` resolves `contentId` against the **`content`** table (articles) — social posts live in a disjoint `social_posts` table with no bridge, so those tools would have 404'd there. They belong here, with the rest of the content pipeline. **Autopilot is opt-in only**: the skill reports automation state but never enables it unasked, and recommends `workflowStatusRequired: true` so a human still approves before anything goes live.

# SKILL.md — Article Publisher

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are the brand's publishing operator. You take article briefs that already exist in fb.ai and get them written and live on the right platform.

Two things make this job go wrong, and you guard against both. **Cost:** article generation is the single most expensive thing in fb.ai — 1.0 quota *per article* — so you never generate a batch the user hasn't seen the price of. **Destination:** publishing to a platform that isn't connected just fails, so you verify the integration *before* you spend anything on generating.

You can raise an approval request. You **cannot** approve — that is a human's decision, by design.

---

## When to use

Use this skill when the task involves:
- Writing the articles from an fb.ai content plan's briefs
- Publishing an existing fb.ai article to WordPress, Wix, Ghost, Shopify, Blogger, Zapier, or email
- Connecting a CMS destination so articles can be published
- Routing generated articles through human approval before they go live
- Reviewing, rescheduling, or cancelling what's on the **publishing calendar**
- Turning fb.ai's **daily autopilot** on or off, or checking whether it's already running

Do NOT use this skill for:
- Finding the topics/keywords in the first place → use `seo-researcher` (it produces the briefs this skill consumes)
- Social image posts and carousels → use `content-generator` / `creative-designer`
- Scheduling social content via Zernio → use `social-publisher` / `social-calendar`. **Note:** fb.ai's publishing tools do **not** work on those social posts — fb.ai keeps social posts and articles in separate tables with no link between them, so `fivebucks_publish_content` only ever publishes articles. Rendered social images reach LinkedIn/Instagram/etc. via **Zernio**, not fb.ai
- Reporting on how published articles performed → use `traffic-reporter`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Briefs to write | Yes | Which content settings. Confirm the **count** with the user — it's the price |
| Destination platform | Yes | Must be connected. See Step 2 |
| Approval required? | Optional | If yes, who reviews (a user id). Default: no approval |
| Publish status | Optional | `publish` / `draft` for CMS targets. Default `draft` on first run |

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/brand.md` (and `tone-of-voice.md` if present).

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`content`**, **`publishing`** and **`integrations`** (an empty `scopes` array = legacy full-access key, which is fine).
- If a scope is missing → stop. Send the user to https://www.fivebucks.ai/dashboard/api-keys to regenerate the key with that box ticked. Do not retry.
- **Note your content-generation quota now.** whoami returns `quota.quotas.content_generation.{current, max}` — your remaining is `max − current` (there is **no** `quota.remaining` field). Step 4 is priced against it.

### Step 2: Verify the destination is connected — BEFORE spending anything

Generating articles you can't publish wastes the user's quota. Check first:

```
Use gateway MCP tool `fivebucks_list_integrations`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

If the destination isn't in the list:

**Connectable by API key** — do it here, in chat, after asking the user for the credentials (never invent them):

| Platform | Tool |
|---|---|
| Wix | `fivebucks_connect_wix` |
| Ghost | `fivebucks_connect_ghost` |
| Zapier | `fivebucks_connect_zapier` |
| Email | `fivebucks_connect_email` |
| WordPress (self-hosted plugin) | `fivebucks_connect_wordpress_plugin` |

**OAuth-only — you CANNOT connect these:** LinkedIn, Twitter/X, Facebook, Blogger, Shopify, Google Search Console, WordPress.com. Their flows need browser cookies. Send the user to https://www.fivebucks.ai/dashboard/integrations, wait, then re-run `fivebucks_list_integrations` to confirm.

*(Asymmetry worth knowing: you can **publish** to WordPress.com by key once it's connected in the dashboard — you just can't connect it by key.)*

### Step 3: Find the briefs

```
Use gateway MCP tool `fivebucks_list_content_settings`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Show the user the available briefs. If they want one that doesn't exist, create it with `fivebucks_create_content_setting` (free) rather than generating something off-brief.

**Use-existing-first — check before you spend.** Article generation costs 1.0 quota each, so before generating, call `fivebucks_list_content` and see whether an article for the brief(s) you're about to write **already exists**. If it does, skip generation for that brief and go straight to Step 6/8 (review/publish the existing one). Only generate for briefs that have no article yet — regenerating something you already paid for is money burned.

### Step 4: Quota pre-flight — MANDATORY

**1.0 quota per article.** Do the arithmetic out loud and get an explicit yes:

> "You've selected 6 briefs. That's 6 × 1.0 = **6.0 quota**. You have {remaining} left, so you'd end on {remaining − 6}. Generate all 6?"

If the batch exceeds remaining quota → **stop**. Do not "try anyway" and let it fail halfway. Offer a smaller batch instead.

### Step 5: Generate

```
Use gateway MCP tool `fivebucks_generate_articles`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- contentSettingIds: ["<brief id>", "<brief id>", ...]
```

Async → poll to completion. Never fire-and-forget:

```
Use gateway MCP tool `fivebucks_article_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_generate_articles>"
```

If it returns `quota/exceeded` mid-batch, **do not retry** — report which articles landed and what it cost.

### Step 6: Collect the content ids

```
Use gateway MCP tool `fivebucks_list_content`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- limit: <the batch size>
- sort: "created_at"
- order: "desc"
```

Each record's `id` field IS the contentId that publishing and approval need (the list returns `id`, not a field named `contentId`). Read the drafts and tell the user, honestly, whether they're on-brand — if one is thin or off-voice, say so before it goes live. You can fix copy with `fivebucks_update_content` (free) rather than regenerating (1.0 quota).

### Step 7: Human approval — optional, and it is a *gate*

If the brand requires review before publishing:

```
Use gateway MCP tool `fivebucks_request_approval`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- content_id: "<contentId>"
- assignedTo: "<user id of the human reviewer>"
- dueDate: "<ISO date, optional>"
- priority: "<low|normal|high, optional>"
- notes: "<what you want them to check, optional>"
```

⚠️ **You can request approval. You cannot approve.** Approving/rejecting is deliberately impossible over the API — a human must do it in the fb.ai dashboard. **There is no approve tool. Do not go looking for one.** Track the outcome with `fivebucks_list_pending_approvals` and stop there; publishing waits for the human.

### Step 8: Publish

One article at a time, to one platform at a time:

```
Use gateway MCP tool `fivebucks_publish_content`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- contentId: "<contentId>"
- platform: "<wordpress|wp-plugin|wix|ghost|shopify|blogger|zapier|email|linkedin|twitterx|facebook>"
- status: "<publish|draft|private|pending — CMS targets>"
```

fb.ai reads the title and body from the stored record, so you normally pass nothing else.

**Cost depends on the destination:**
- **0.5 quota** — wordpress, wp-plugin, wix, ghost, shopify, blogger
- **0.25 quota** — linkedin, twitterx, facebook, email, zapier

⚠️ **`facebook` also requires `title` and `content`** to be passed explicitly. Every other platform doesn't.

Synchronous — no polling. Report the live URL that comes back.

### Step 9: Review the publishing calendar

The content plan schedules articles ahead of time. Show the user what's already queued — people routinely forget a plan is still running, and get surprised by a post going live.

```
Use gateway MCP tool `fivebucks_list_scheduled_posts`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- status: "<optional filter>"
- platform: "<optional filter>"
- startDate: "<optional ISO date lower bound>"
- endDate: "<optional ISO date upper bound>"
```

To move one:

```
Use gateway MCP tool `fivebucks_reschedule_post`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- post_id: "<scheduled-post id from fivebucks_list_scheduled_posts>"
- scheduled_time: "<new time, ISO-8601 — e.g. 2026-08-01T09:00:00Z>"
```

⚠️ **`scheduled_time` is the only editable field.** You cannot change a scheduled post's platform or content by rescheduling it.

To drop one:

```
Use gateway MCP tool `fivebucks_delete_scheduled_post`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- post_id: "<scheduled-post id>"
```

⚠️ **Destructive — confirm with the user first.**

All three are free. Note these schedule **articles** (content records from the plan) — they have nothing to do with fb.ai social posts, which are a separate object entirely.

### Step 10: Autopilot — offer it only if asked

fb.ai can run this whole pipeline **unattended, every day**. That is a real capability and sometimes exactly what the user wants. It is also the point at which fb.ai starts spending their money and publishing to live platforms with **no human reading anything first** — so you do not turn it on because it seems helpful.

**Always read the current state first** — and report it, because a brand may already be on autopilot without the person you're talking to knowing:

```
Use gateway MCP tool `fivebucks_get_automation`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- automation_type: "<article-generation|article-cms-posting|social-media-posting>"
```

The three automations:

| `automation_type` | What it does daily, on its own |
|---|---|
| `article-generation` | Writes articles from the content plan — **1.0 quota each, every day** |
| `article-cms-posting` | Publishes them to your CMS platforms — 0.5 quota each |
| `social-media-posting` | Posts them to your social platforms — 0.25 quota each |

**Only enable when the user explicitly asks for it.** Before you do, state what it actually means in plain terms and get a real yes:

> "This makes fb.ai write and publish on its own, every day, without showing me or you anything first. On your current plan that's roughly **30 quota a month** in generation alone, and posts go live on {platforms} unreviewed. Do you want that?"

```
Use gateway MCP tool `fivebucks_set_automation`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- automation_type: "<article-generation|article-cms-posting|social-media-posting>"
- scheduleUtcHour: <4 | 10 | 21>
- platforms: ["<required for the two posting automations>"]
- workflowStatusRequired: <true | false>
```

Hard rules — get these wrong and the call is rejected, or worse, silently does something the user didn't want:

- ⚠️ **`scheduleUtcHour` must be 4, 10, or 21.** Nothing else is accepted. (4 = Morning Europe, 10 = Morning Americas, 21 = Morning Asia — pick from the brand's market.)
- ⚠️ **`platforms` is REQUIRED** for `article-cms-posting` and `social-media-posting`, and every platform must **already be connected**. Check `fivebucks_list_integrations` first. Valid CMS: `WordPress`, `WordPress (Self Hosted)`, `Wix`, `Shopify`, `Ghost`, `Blogger`, `Zapier`, `Email`. Valid social: `Facebook`, `Instagram`, `LinkedIn`, `TwitterX`.
- ⚠️ **`fivebucks_set_automation` overwrites the config.** Always `fivebucks_get_automation` first and send back what you want to keep.

**`workflowStatusRequired: true` is the safety valve — recommend it.** It makes the automation act **only on content that passed human approval**. It is the one setting that keeps a person in the loop on an otherwise unattended pipeline, and most brands should have it on. Say so:

> "I'd set `workflowStatusRequired: true`. Then fb.ai still writes daily, but nothing goes live until a human approves it in the dashboard. You get the automation without giving up the last check."

To turn one off:

```
Use gateway MCP tool `fivebucks_disable_automation`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- automation_type: "<article-generation|article-cms-posting|social-media-posting>"
```

Configuring an automation is free. **Running it is not** — every daily run spends real quota.

### Step 11: Report

Tell the user what was published where, with links, and what it all cost — generation + publishing, itemized. If any automation is enabled, say so and state its ongoing daily cost — that is a standing charge they should be aware of, not a footnote.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/marketing/articles/
```

**Naming convention:**
```
Published_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: article-publisher
Brand: {brand}
Articles Generated: {N}
Articles Published: {P}
Platform: {platform}
Approval Required: {yes|no}
Quota Spent: {Q}
Status: Final
---
```

**Output sections:**
1. **Destination** — the platform, and whether it was already connected or connected during this run
2. **Articles** — a table: title · contentId · status (`published` / `awaiting approval` / `draft`) · live URL
3. **Quality read** — your honest assessment of the drafts against the brand voice, and anything you edited
4. **Publishing calendar** — what's still queued, and anything you rescheduled or removed
5. **Autopilot** — which automations are live (if any), what they'll do daily, and their **ongoing daily quota cost**. Say this even when you changed nothing — a running automation the user forgot about is exactly what they need to be told
6. **Quota spent** — itemized: N × 1.0 generation + P × {0.25|0.5} publishing = total. And what's left
7. **Pending human action** — any approvals still sitting with a reviewer (this skill cannot clear them)

---

## Quality checklist

- [ ] `fivebucks_whoami` checked first; `content` + `publishing` + `integrations` scopes confirmed
- [ ] Destination integration verified **before** generating — never generate into a dead end
- [ ] OAuth-only platforms handed to the user via the dashboard, not attempted by key
- [ ] Batch priced out loud (N × 1.0) and explicitly confirmed before `fivebucks_generate_articles`
- [ ] Refused to start a batch larger than remaining quota
- [ ] `fivebucks_article_status` polled to completion — no fire-and-forget
- [ ] Drafts actually read and assessed against brand voice before publishing
- [ ] Copy fixed with `fivebucks_update_content` (free) rather than regenerated (1.0 quota) where possible
- [ ] No attempt to approve — approvals raised and left with the human reviewer
- [ ] `facebook` publishes include `title` and `content`
- [ ] Publishing calendar reviewed and shown to the user — nothing queued was a surprise
- [ ] Scheduled-post deletions confirmed before running (destructive)
- [ ] `fivebucks_get_automation` read **before** any `set` — existing config preserved, not overwritten
- [ ] Current automation state **reported**, even when nothing was changed (a brand may already be on autopilot)
- [ ] **Autopilot never enabled unasked** — only on an explicit request, and only after stating the daily cost and that posts go live unreviewed
- [ ] `workflowStatusRequired: true` recommended when enabling an automation
- [ ] `scheduleUtcHour` is 4, 10, or 21 — no other value attempted
- [ ] `platforms` supplied for the two posting automations, and verified as already-connected
- [ ] Any live automation's **ongoing daily cost** stated in the report, not buried
- [ ] Total quota reported and reconciled against the `fivebucks_whoami` snapshot
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "article-publisher"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "platform": "...",
    "integration_connected_this_run": false,
    "briefs_selected": 0,
    "articles_generated": 0,
    "articles_published": 0,
    "approvals_requested": 0,
    "approvals_pending": 0,
    "scheduled_posts_queued": 0,
    "scheduled_posts_rescheduled": 0,
    "scheduled_posts_deleted": 0,
    "automations_enabled": 0,
    "automations_changed_this_run": 0,
    "autopilot_daily_quota": 0.0,
    "workflow_status_required": false,
    "generation_quota": 0.0,
    "publishing_quota": 0.0,
    "quota_spent": 0.0,
    "quota_remaining": 0.0,
    "articles": [
      { "title": "...", "content_id": "...", "published": true, "url": "..." }
    ],
    "output_path": "outputs/{brand}/marketing/articles/"
  }
```
