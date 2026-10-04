---
name: outreach-sequencer
description: Send personalized cold email sequences via Gmail (self-managed loop), track replies, schedule follow-ups, and route booked meetings to Calendly. Runs daily on cron schedule.
allowed-tools: Read, Grep, Glob, Bash
area: Sales
use_for: "Self-managed Gmail cold-email sequences. Tracks replies, schedules follow-ups, books meetings via Calendly"
deps:
  mcp: ["Calendly", "Gmail", "Notion", "Slack"]
  gateway: ["email"]
  files: ["sales.md", "audience.md", "product.md", "brand.md"]
  env: ["`${BRAND}_CRM_DB` (must be bootstrapped by `apollo-lead-prospector` first)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Send personalized cold email sequences via Gmail (self-managed loop), track replies, schedule follow-ups, route booked meetings to Calendly

### Change Log

**v2.20.0** — July 12, 2026
- **Routing added against the new fb.ai cold-email stack.** The marketplace now has a second, entirely separate sending stack (`leadgen-onboarder` → `lead-crm-manager` → `campaign-runner`). This skill stays the **low-volume, personal, 1:1** path — founder's own Gmail, no setup, no quota. "Do NOT use this skill for:" now routes scale sending to `campaign-runner` and states the real tradeoff (volume through a personal inbox risks the founder's primary domain reputation).

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Outreach Sequencer

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a B2B sales-acquisition agent for the active brand. Your job is to run a self-managed cold email sequence loop against prospects already loaded into the brand's Notion CRM by `apollo-lead-prospector`. You compose persona-tailored emails using the brand's voice, send them via Gmail, poll inbound replies, classify replies into routing buckets, and update the CRM state machine. You never invent product features, pricing, or testimonials — every claim and CTA is grounded in `brands/{brand}/product.md` and `brands/{brand}/sales.md`.

This skill is **not** Apollo Sequences — it's a self-managed Gmail loop that the agent drives via `Next Touch Date` on each CRM row.

---

## When to use

Use this skill when the task involves:
- The daily cron run that sends today's due emails and processes inbound replies
- Manually running outreach after a CRM backfill
- Re-running after `brands/{brand}/sales.md` sequence templates or sender persona change
- A targeted send when the user names specific prospects (input override)

Do NOT use this skill for:
- Sourcing new prospects → use `apollo-lead-prospector`
- **Cold email at scale** → use `campaign-runner` (the fb.ai stack). This skill is the **low-volume, personal, 1:1** path: it sends from the founder's own Gmail, needs no setup, and costs no quota — but it doesn't scale, and pushing volume through a personal inbox puts the founder's primary domain reputation at risk. `campaign-runner` sends from a dedicated verified domain with real deliverability infrastructure (DKIM, Postmark) — at the cost of quota and a one-time setup (`leadgen-onboarder`) with two human waits. The two stacks share no data; don't migrate a user between them unprompted
- Marketing newsletters or one-off broadcasts → use `content-creation` + `social-publisher`
- Booking meetings outside the sequence → use Calendly directly
- Analyzing reply rate / pipeline performance → use `data-analysis`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Run mode | Optional | Default: `cron` (process all due rows). Alternates: `targeted` (specific prospect IDs) or `replies-only` (skip sends, only poll) |
| Send window | Optional | Default from `brands/{brand}/sales.md` Sender Persona section; falls back to 09:00–17:00 local |
| Daily send cap | Optional | Default from `sales.md`; falls back to 50 sends/day |

---

## Step-by-step workflow

### Step 1: Read brand context

Always read before starting:
- **brands/{brand}/brand.md** — Voice, tone, approved phrases (the email must sound like the brand)
- **brands/{brand}/audience.md** — Persona-specific hooks, pain points, buying triggers (the body of the email)
- **brands/{brand}/product.md** — The offer, plan tier per persona, primary CTA (the close of the email)
- **brands/{brand}/sales.md** — Sender persona, sequence templates, reply routing (the operational config for this skill)

**Expected `sales.md` sections this skill reads:**
- **Sender Persona** — Name, title, signature block, photo URL, sender email address
- **Sequence Templates** — Touch schedule (e.g., 5 touches over 14 days). Per touch: type (email / LinkedIn manual handoff / email), interval (days from previous), template skeleton with persona-hook + offer placeholders
- **Reply Routing** — Classification rules: interested → book, not now → nurture, wrong person → ask referral, unsubscribe → mark + suppress, out-of-office → defer

If `sales.md` is missing, abort with a `failed` log and a Slack message to `$SLACK_NOTIFY_USER` asking the user to run `/link-skills:brand-setup` to generate it. Do not invent sender personas or sequence templates.

### Step 2: Pull due CRM rows

Resolve the CRM DB to a `data_source_url`:

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_CRM_DB"
```

**CRM DB bootstrap check — abort cleanly if missing.** If `${BRAND}_CRM_DB` env var is unset, OR the `notion-fetch` call returns `not_found` / 404, the brand's CRM has not been bootstrapped yet. Do NOT attempt to create it here — that's `apollo-lead-prospector`'s responsibility on its first run. Abort with this user-facing message:

> The brand's CRM database is not yet bootstrapped. Run `/link-skills:apollo-lead-prospector` first — it creates `${BRAND}_CRM_DB` on first execution. Then re-run outreach-sequencer.

Then jump to the **Final Step — Log to Dashboard** with `status: "failed"` and a summary of `"aborted: ${BRAND}_CRM_DB not bootstrapped — run apollo-lead-prospector first"`. End the run.

Extract `data_sources[0].url` → save as `crm_data_source_url`.

Pull rows where `Status` ∈ {"New", "In Sequence"} and `Next Touch Date` ≤ today. New rows have no `Next Touch Date` and start at Touch 1 immediately.

```
Use mcp__claude_ai_Notion__notion-search:
- query: ""
- data_source_url: <crm_data_source_url>
- query_type: "internal"
- filter: { "and": [
    { "property": "Status", "select": { "is_one_of": ["New", "In Sequence"] } },
    { "or": [
        { "property": "Next Touch Date", "date": { "on_or_before": "<today>" } },
        { "property": "Next Touch Date", "date": { "is_empty": true } }
      ] }
  ] }
```

If the connector doesn't support filter on the search tool, fall back to `notion-fetch` on the DB and filter in-memory.

Order by `ICP Score` descending, then `Source Date` ascending. Cap at the daily send cap from `sales.md`.

### Step 3: Generate the email per prospect

For each due prospect, determine the **current touch number**:

- If `Touch Number` is empty or 0 → this is Touch 1
- Else → this is `Touch Number + 1`
- If next touch number exceeds the sequence length defined in `sales.md` → mark `Status = "Disqualified"` with `Reply Status = "No reply — sequence exhausted"` and skip send

Look up the touch's template from `sales.md` Sequence Templates. Compose the email body by populating the template placeholders:

| Placeholder source | What goes in |
|---|---|
| `audience.md` (matched persona) | Persona pain point + buying trigger |
| `product.md` | Specific feature / plan tier / proof point relevant to persona |
| `brand.md` | Voice/tone enforcement, approved phrases only |
| `sales.md` Sender Persona | First name, signature block |
| Calendly link (Step 4) | Single-use booking URL inserted into CTA |

Subject line and opening line must reference something specific to the prospect (company, role, recent trigger from enrichment notes on the CRM row). No generic openings.

Locale: respect the brand's locale from `brand.md` — use ID for Indonesian-market prospects, EN otherwise. Never machine-translate; if `sales.md` doesn't ship a locale-specific template, fall back to EN.

### Step 4: Generate a single-use Calendly link

Each Touch that includes a CTA gets a fresh single-use link so the booking is attributable to this prospect.

**Before calling Calendly tools, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Calendly__authenticate,mcp__claude_ai_Calendly__complete_authentication"` to load the auth schemas.** The Calendly MCP is deferred and the only tools exposed pre-auth are `authenticate` and `complete_authentication`.

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Calendly__authenticate,mcp__claude_ai_Calendly__complete_authentication"
```

After OAuth completes, additional Calendly tools become available — use `ToolSearch` with query `"calendly"` to enumerate the post-auth toolset (typically including a single-use scheduling-link creator). Do NOT hardcode speculative tool names; rely on what `ToolSearch` actually returns after auth. If no scheduling-link tool is available, fall back to the standing booking-link URL on the `Booking URL:` line inside the `## Sender Persona` block of `brands/{brand}/sales.md`, and tag the CRM row with the prospect's Apollo ID as the booking ref. Append `?utm_source=outreach&utm_campaign=cold&utm_content=<apollo_id>` to the standing link for attribution. If `Booking URL:` is missing or empty, abort the touch for this prospect and log a one-time Slack DM to `$SLACK_NOTIFY_USER` instructing the user to run `/link-skills:plugin-update` to backfill it — never send a CTA email with a broken or empty booking link.

### Step 5: Send the email via Gmail

Compose and send the email via Gmail MCP. The currently exposed primitive is `create_draft` — combine with the Gmail web "send drafts" pattern: create the draft, then send. If `send_email` is not directly available, the CRM row tracks `Status = "In Sequence"` only after a successful draft creation, and a manual founder-confirmation step ships the drafts.

**Before calling Gmail tools, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Gmail__create_draft,mcp__claude_ai_Gmail__search_threads,mcp__claude_ai_Gmail__get_thread"` to load the schemas.** Gmail MCP tools are deferred.

```
Use mcp__claude_ai_Gmail__create_draft:
- to: "<prospect.Email>"
- subject: "<personalized subject>"
- body: "<personalized email body with Calendly link in CTA>"
- from: "<sender_email from sales.md Sender Persona>"
```

Capture the returned draft/message ID. If the brand's deployment includes a `send_email` tool (gateway `fiveagents_send_email` is available — see `agents/link.md` External APIs), prefer immediate send:

```
Use gateway MCP tool `fiveagents_send_email`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- to: "<prospect.Email>"
- from: "<sender_email>"
- from_name: "<sender_name from sales.md>"
- subject: "<personalized subject>"
- html: "<personalized HTML body — signature block + photo from sales.md>"
- reply_to: "<sender_email>"
```

Use `fiveagents_send_email` as the primary path when the brand's transactional sender is configured. Use Gmail `create_draft` only when the brand wants founder-reviewed sends.

### Step 6: Update CRM after send

For each successful send/draft:

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: "<prospect notion page id>"
- properties: {
    "Status":          "In Sequence",
    "Touch Number":    <next_touch_number>,
    "Last Touch Date": "<today YYYY-MM-DD>",
    "Next Touch Date": "<today + interval from sales.md template for next touch>"
  }
```

If this was the final touch in the sequence, set `Next Touch Date` empty and a flag `Sequence Complete = true` (no `Next Touch` will be due, so the prospect drops out of the daily query naturally).

### Step 7: Poll for replies

For every prospect in `Status = "In Sequence"` (regardless of whether they were touched today), search Gmail for inbound messages from their email address since their `Last Touch Date`.

```
Use mcp__claude_ai_Gmail__search_threads:
- query: "from:<prospect.Email> after:<Last Touch Date>"
- max_results: 5
```

For each thread returned, fetch the full thread and read the latest inbound message:

```
Use mcp__claude_ai_Gmail__get_thread:
- thread_id: "<thread_id>"
```

Classify the latest inbound message per `sales.md` Reply Routing rules. Standard categories (override with whatever `sales.md` defines):

**Slack is a deferred MCP tool — load its schema before this immediate DM:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Slack__slack_send_message"
```

The "Interested" / "Booked" routing rows below trigger an immediate Slack DM, which fires BEFORE Step 8's daily digest. The schema must already be loaded by the time those rows execute. (If a prior run in the same session already loaded it, this call is a cheap no-op — see also the Step 8 ToolSearch block.)

| Category | Routing |
|---|---|
| Interested / wants to talk | Set `Status = "Replied - Interested"`, `Reply Status = "Interested"`. Stop sequence. **Send Slack DM immediately to `$SLACK_NOTIFY_USER`** — do not wait for the daily digest. |
| Not now / later | Set `Status = "Replied - Not Now"`, `Reply Status = "Nurture"`. Stop sequence. Add follow-up reminder for `today + 90 days` in `Next Touch Date`. |
| Wrong person / not the buyer | Set `Status = "Replied - Wrong Person"`, `Reply Status = "Ask referral"`. Compose a one-line referral-ask reply (founder reviews) and stop sequence. |
| Unsubscribe / stop | Set `Status = "Unsubscribed"`, `Reply Status = "Suppressed"`. Add the email to the brand's blocklist (append to `brands/{brand}/sales.md` blocklist if writable, otherwise log to `outputs/{brand}/sales/blocklist-pending.md` for the founder to merge). Stop sequence permanently. |
| Out-of-office / auto-reply | Do not change Status. Set `Next Touch Date = today + (OOO duration parsed from message, default 7 days)`. Skip touch increment. |
| Booked meeting (Calendly notification thread) | Set `Status = "Booked"`, `Reply Status = "Meeting booked"`. Slack DM immediately. |

Use a small classification heuristic: keyword pattern match first (interested/yes/sure/let's talk; not now/later/q3/next quarter; not the right person/wrong/forward; unsubscribe/stop/remove; out of office/away/oo; calendly.com/booked/confirmed), then a single-pass LLM classification when patterns are ambiguous. Always quote the matched fragment in the CRM row's `content` for audit.

### Step 8: Build the daily Slack digest

DM the user via Slack MCP with the day's outreach summary.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "<digest below>"
```

Digest format:

```
✉️ [{brand}] Outreach Daily — [DD Mon YYYY]
• {S} emails sent ({T1}/{T2}/{T3}/{T4}/{T5} by touch number)
• {R} replies received
   – {Ri} Interested
   – {Rn} Not now (nurture)
   – {Rw} Wrong person
   – {Ru} Unsubscribed
   – {Roo} Out-of-office
• {B} meetings booked
• {D} sequences completed (no reply, exhausted)

Top 3 interested replies (action required):
1. {Name} — {Title} @ {Company} — "{first 80 chars of reply}" — {gmail thread URL}
2. ...

Daily quota: {S}/{cap}
CRM: {notion_db_url}
```

If "Interested" or "Booked" appeared today, the immediate-send Slack DMs from Step 7 already fired — the digest is the rollup.

### Step 9: Save local audit log

Save the day's send + reply log: `outputs/{brand}/sales/sequences/SequenceLog_DDMonYYYY.md`

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/sales/sequences/
```

**Naming convention:**
```
SequenceLog_[DDMonYYYY].md
```

Examples:
- `SequenceLog_07May2026.md`
- `SequenceLog_08May2026.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: outreach-sequencer
Brand: {brand}
Sends: {S}
Replies: {R}
Meetings Booked: {B}
Sequences Completed: {D}
---
```

**Output sections:**
1. **Run Summary** — sends by touch number, replies by category, meetings booked, sequences completed
2. **Send Log** — table: Prospect, Touch #, Subject, Sent Time, Gmail Message ID
3. **Reply Log** — table: Prospect, Reply Category, Quoted Fragment, Action Taken, Gmail Thread URL
4. **Pipeline Movement** — counts by Status before vs after the run

---

## Quality checklist

Before finalizing any outreach run:

- [ ] Email body grounded in `brands/{brand}/audience.md` persona hooks + `brands/{brand}/product.md` offer — no invented features or pricing
- [ ] Subject and opening line reference something specific to the prospect — no generic openings
- [ ] Sender persona, signature, and photo come from `brands/{brand}/sales.md` Sender Persona section
- [ ] Touch number and Next Touch Date computed from `sales.md` Sequence Templates intervals — not invented
- [ ] Single-use Calendly link inserted in every email with a booking CTA (or standing link with attribution UTM as fallback)
- [ ] Daily send cap respected — total sends ≤ `sales.md` Daily Send Cap
- [ ] Every reply classified with quoted fragment in the CRM row content for audit
- [ ] Unsubscribes added to the suppression list immediately — never re-touched
- [ ] "Interested" and "Booked" replies trigger immediate Slack DM, not just the digest
- [ ] Local audit log saved to `outputs/{brand}/sales/sequences/SequenceLog_DDMonYYYY.md`
- [ ] Slack daily digest delivered to `$SLACK_NOTIFY_USER`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "outreach-sequencer"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "emails_sent": 0,
    "sends_by_touch": { "1": 0, "2": 0, "3": 0, "4": 0, "5": 0 },
    "daily_send_cap": 0,
    "replies_received": 0,
    "replies_by_category": {
      "interested": 0,
      "not_now": 0,
      "wrong_person": 0,
      "unsubscribed": 0,
      "out_of_office": 0
    },
    "meetings_booked": 0,
    "sequences_completed_no_reply": 0,
    "pipeline_movement": {
      "new_to_in_sequence": 0,
      "in_sequence_to_replied": 0,
      "in_sequence_to_booked": 0,
      "in_sequence_to_unsubscribed": 0
    },
    "crm_db_id": "${BRAND}_CRM_DB",
    "output_path": "outputs/{brand}/sales/sequences/"
  }
```
