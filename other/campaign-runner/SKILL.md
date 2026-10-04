---
name: campaign-runner
description: Build an fb.ai cold-email workflow and send it — checks the four send gates, prices the send out loud (0.01/email), sends, then polls the job because some failures only surface as a failed job. This skill emails real people. Run on demand.
allowed-tools: Read, Grep, Glob, Bash
area: Sales
use_for: "Build an fb.ai cold-email workflow, verify the send gates, send the campaign, and report results"
deps:
  mcp: []
  gateway: ["fivebucks (**scopes: leadgen_campaigns, leadgen_crm**)", "FiveAgents (logging)"]
  files: ["sales.md", "product.md", "audience.md", "brand.md"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.1 | July 13, 2026 |

**Description:** Build an fb.ai cold-email workflow, verify the four send gates, send the campaign, and report results.

### Change Log

**v2.20.1** — July 13, 2026
- **Corrected the `whoami` quota field (v2.20.0 referenced a `quota.remaining` field that doesn't exist)** — quota now read from `quota.quotas.automatic_posting.{current, max}`.

**v2.20.0** — July 12, 2026
- Initial release. Drives fb.ai's `leadgen_campaigns` scope, plus `leadgen_crm` for the recipient-count pre-flight (gateway v1.8.0).

# SKILL.md — Campaign Runner

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You build and send the brand's cold-email campaign.

**This skill emails real people, from the brand's real domain.** Every other fb.ai skill spends quota; this one spends the brand's sending reputation, and that doesn't come back. A campaign sent to a bad list, or with a broken sequence, or to more people than the user expected, is not an error you can retract.

So you are deliberately slow at exactly one moment: **before the send.** You state the recipient count, you state the cost, you confirm the four gates, and you get an explicit yes. Everything else you can do briskly.

Two things about fb.ai's send that make silence dangerous, and that you must never let pass:
- **Masked (unenriched) leads are silently dropped.** No error. The campaign just emails fewer people than the user thinks.
- **An empty email sequence does not return an error.** The send call returns 200 and then comes back as a **failed job**. If you don't poll, a total failure looks like a success.

---

## When to use

Use this skill when the task involves:
- Creating or editing an fb.ai cold-email workflow and its sequence
- Sending a campaign to an fb.ai lead list or segment
- Reporting on how a campaign performed
- Retrying failed sends

Do NOT use this skill for:
- Setting up the sending domain / signature → use `leadgen-onboarder` (do that **first** — a workflow can't be created without a verified domain)
- Finding, importing, or enriching the leads → use `lead-crm-manager`
- **Low-volume, personal, 1:1 outreach from the founder's own Gmail** → use `outreach-sequencer`. That's the right tool when you're emailing a handful of people individually and want replies landing in your own inbox. It needs no domain, no DNS, no Postmark, and costs no quota. **This** skill is the right tool when you're sending at scale from a dedicated verified domain with real deliverability infrastructure behind it

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Verified domain | Yes | Must already be verified. If not → `leadgen-onboarder` |
| Confirmed signature | Yes | The sender. If not confirmed → `leadgen-onboarder` |
| Target | Yes | A lead list, a segment, or an explicit set of lead ids |
| Email sequence | Yes | Subject + body per step. Drafted from `product.md` / `audience.md` — never invented |
| Send schedule | Optional | `schedule_utc_hour` must be **4, 10, 21, or null**. No other value is accepted |

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/sales.md` (sender persona, sequence templates), `product.md` (features and pricing — the **only** source), `audience.md` (personas and pain points).

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`leadgen_campaigns`** and **`leadgen_crm`** (the latter is needed to count recipients for the pre-flight). An empty `scopes` array = legacy full-access key, which is fine.
- If either is missing → stop. Send the user to https://www.fivebucks.ai/dashboard/api-keys. Do not retry.
- **Note your sending quota.** whoami returns `quota.quotas.automatic_posting.{current, max}` — remaining is `max − current` (there is **no** `quota.remaining` field). The send is priced against it in Step 5.

### Step 2: Reuse an existing workflow before building a new one

```
Use gateway MCP tool `fivebucks_list_workflows`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

If a suitable workflow exists, read it with `fivebucks_get_workflow(workflow_id)` and edit it rather than duplicating. Duplicated workflows are how brands end up emailing the same person twice.

### Step 3: Draft the email sequence

Write it from `product.md`, `audience.md`, and the brand voice in `brand.md`. **Never invent a feature, a price, a customer, or a result.** Show the user the full sequence — every subject line and every body — and get their edits before you create anything. This is the cheapest possible moment to fix bad copy.

A sequence is a list of templates, each with a `sequence_number` starting at **1**:

```
templates: [
  { "subject": "...", "body_html": "...", "body_text": "...", "sequence_number": 1 },
  { "subject": "...", "body_html": "...", "body_text": "...", "sequence_number": 2, "send_delay_days": 3 }
]
```

⚠️ **The sequence must be non-empty.** An empty sequence is the failure mode that returns 200 and then fails as a job — see Step 6.

### Step 4: Create the workflow

```
Use gateway MCP tool `fivebucks_create_workflow`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- name: "<campaign name>"
- domainId: "<VERIFIED domain id>"
- emailSequence: { "templates": [ ... ], "max_follow_ups": <int>, "send_interval_days": <int> }
- signatureId: "<confirmed signature id>"
- from_name: "<sender name>"
- reply_to: "<reply-to address>"
- offeringType: "<service|saas|product>"
- target_type: "<all|lists|segment|custom>"
- target_list_ids: ["<list id>"]
- target_segment_id: "<segment id>"
- schedule_utc_hour: <4 | 10 | 21 | null>
```

⚠️ **The parameter casing here is genuinely inconsistent and it is load-bearing.** Create takes **camelCase** `domainId` / `emailSequence` / `signatureId` / `offeringType`, but **snake_case** `from_name` / `reply_to` / `target_*` / `schedule_utc_hour`. And `fivebucks_update_workflow` takes the **snake_case** forms — `domain_id` / `email_sequence` / `signature_id` — for those same three fields. Copy them exactly; a wrong-cased key is dropped silently.

⚠️ **`domainId` must be an ALREADY-VERIFIED domain.** An unverified domain is rejected with `domain/not-verified`. **This is the only place verification is ever checked** — the send route does not re-check it. If you hit this error, do not retry: send the user to `leadgen-onboarder`.

Creating a workflow is **free**. Sending is what costs.

To edit later: `fivebucks_update_workflow(workflow_id, ...)` — send only what changed. Note that `email_sequence` **replaces the whole sequence**, it does not merge. Pause a running campaign with `status: 'paused'`.

### Step 5: The pre-flight — do not skip any of this

**First, resolve the real recipient count.** Not an estimate:

```
Use gateway MCP tool `fivebucks_segment_count`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- segment_id: "<segment id>"
```

*(For a static list, use its size from `fivebucks_list_lead_lists`. For explicit `leadIds`, it's the length of the array.)*

**Then check all four send gates.** Each fails differently, and three of the four fail *quietly*:

| # | Gate | What happens if it fails |
|---|---|---|
| 1 | Domain **verified** | Rejected back at **workflow-create** (`domain/not-verified`) — not at send |
| 2 | ≥1 **confirmed** signature on that domain | `domain/no-confirmed-signatures` |
| 3 | **Every targeted lead enriched** (no `***` emails) | ⚠️ Masked leads are **silently dropped**. If all drop → `validation/no-valid-leads` |
| 4 | **Non-empty email sequence** | ⚠️ **No error at all.** Returns 200, then comes back as a **FAILED JOB** |

Gate 3 is the one that quietly ruins a campaign. Verify it: pull the target's leads with `fivebucks_list_leads` and count how many still have `***` in `email`. If any do, say so and route to `lead-crm-manager` — do not send a campaign that will silently email fewer people than the user was told.

**Then state the whole thing and get an explicit yes:**

> "This will email **312 real people** from `hello@mail.example.com`. Cost: 312 × 0.01 = **3.12 quota** (you have {remaining}).
> All four gates pass: domain verified ✅, signature confirmed ✅, all 312 leads enriched ✅, 3-step sequence ✅.
> This cannot be undone once it starts. Send?"

If any gate fails, **do not send.** Say which one, and which skill fixes it.

*(Trial accounts are capped around 50 emails — a bigger send fails with `quota/trial-limit-reached`.)*

### Step 6: Send — then poll, because the send can lie

```
Use gateway MCP tool `fivebucks_send_campaign`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- workflow_id: "<workflow id>"
- targeting: { "target_type": "<all|lists|segment|custom>", "target_list_ids": ["..."], "target_segment_id": "..." }
```

⚠️ **Supply exactly ONE of `leadIds` or `targeting`** — not both, not neither.

**You MUST poll.** This is not optional here, and the poller is the odd one out:

```
Use gateway MCP tool `fivebucks_send_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- workflow_id: "<workflow id>"
- jobId: "<jobId from fivebucks_send_campaign>"
```

⚠️ **`fivebucks_send_status` takes BOTH `workflow_id` and `jobId`** — the only poller in fb.ai that needs a second parameter. Every other status tool takes just a job id.

A send can return 200 and then come back as a **failed job** — an empty email sequence does exactly this. Reporting "sent!" off the 200 without polling is reporting a success that never happened. Poll until the job resolves, and read the sent / failed / scheduled counts off it.

*(Re-sending the same request within ~30 minutes returns the **existing** job rather than sending twice. If you get the same job id back, poll it — do not retry.)*

### Step 7: Report and repair

Pull the send log:

```
Use gateway MCP tool `fivebucks_export_sends`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- workflow_id: "<workflow id>"
- status: "<optional filter, e.g. failed>"
- engagement: "<optional>"
- sent_after: "<optional ISO date>"
- sent_before: "<optional ISO date>"
- sequence_number: <optional int>
```

⚠️ **This returns raw CSV text, not JSON.** Parse it as CSV.

To retry a single failed email, filter the export to `status=failed`, take its `send_id`, and:

```
Use gateway MCP tool `fivebucks_retry_send`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- send_id: "<the lead_workflow_sends record id from the CSV export>"
```

⚠️ **`send_id`, not a `jobId`** — it's the id of the individual send record, from the export. Retrying does **not** re-charge quota.

Report honestly: how many were sent, how many failed and why, how many were dropped. If the sent count is lower than the recipient count you quoted in Step 5, **say so and explain the gap** — that's almost always silently-dropped masked leads.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/sales/campaigns/
```

**Naming convention:**
```
Campaign_[CampaignName]_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: campaign-runner
Brand: {brand}
Campaign: {name}
Sender: {from_email}
Recipients Quoted: {Q}
Emails Sent: {S}
Quota Spent: {C}
Status: Final
---
```

**Output sections:**
1. **What was sent** — campaign name, sender, target, and the real sent count
2. **The sequence** — every subject and body, as sent (this is the record of what real people received)
3. **Gate check** — all four gates and their status at send time
4. **Results** — sent / failed / scheduled, from the polled job. Failures with their reasons
5. **The gap** — if fewer emails went out than were quoted, why. Do not bury this
6. **Quota spent** — N × 0.01, and what's left
7. **Next** — retries needed, or when to expect replies

---

## Quality checklist

- [ ] `fivebucks_whoami` checked first; `leadgen_campaigns` + `leadgen_crm` scopes confirmed
- [ ] `fivebucks_list_workflows` checked first — existing workflow reused, not duplicated
- [ ] Email sequence drafted from `product.md` / `audience.md` — **no invented features, prices, customers, or results**
- [ ] Full sequence shown to the user and approved **before** the workflow was created
- [ ] Workflow param casing copied exactly (`domainId`/`emailSequence` on create; `domain_id`/`email_sequence` on update)
- [ ] `domain/not-verified` routed to `leadgen-onboarder` — never retried
- [ ] **Real recipient count resolved** (`fivebucks_segment_count` / list size), not estimated
- [ ] **All four send gates explicitly checked**, including counting masked (`***`) leads in the target
- [ ] Recipient count **and** quota cost (N × 0.01) stated out loud, with an explicit confirmation before sending
- [ ] Exactly one of `leadIds` / `targeting` supplied
- [ ] **`fivebucks_send_status` polled** with BOTH `workflow_id` and `jobId` — a 200 was never reported as success
- [ ] A repeat send within ~30 min recognized as the existing job and polled, not retried
- [ ] `fivebucks_export_sends` parsed as **CSV**, not JSON
- [ ] `fivebucks_retry_send` given a `send_id` from the export, not a `jobId`
- [ ] Any gap between quoted recipients and actual sends surfaced and explained
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "campaign-runner"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "campaign": "...",
    "workflow_created_this_run": false,
    "sequence_steps": 0,
    "target_type": "all|lists|segment|custom",
    "recipients_quoted": 0,
    "emails_sent": 0,
    "emails_failed": 0,
    "emails_scheduled": 0,
    "leads_dropped_masked": 0,
    "gates_all_passed": true,
    "retries_run": 0,
    "quota_spent": 0.0,
    "quota_remaining": 0.0,
    "output_path": "outputs/{brand}/sales/campaigns/"
  }
```
