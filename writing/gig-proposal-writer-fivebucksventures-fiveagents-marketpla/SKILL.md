---
name: gig-proposal-writer
description: Write a freelance-marketplace bid for a chosen gig — detects the client's required "secret word", maps the job to a service the brand sells, and drafts a tailored cover letter plus a 60-second VSL (video sales letter) script, written back onto the gig's Notion row. On-demand per gig. The Write phase of the Inbound Gig Engine.
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__read_page
area: Sales
use_for: "Draft a freelance bid (cover letter + 60s VSL script) for a chosen gig from the opportunities DB, with secret-word detection, written back onto the gig's Notion row"
deps:
  mcp: ["Notion", "Slack", "Claude in Chrome (opt — re-reads the live job post when the gig row's description is truncated)"]
  gateway: ["FiveAgents (logging)"]
  files: ["sales.md", "product.md", "brand.md", "audience.md", "competitors.md"]
  env: ["`${BRAND}_GIGS_DB` (created by `gig-prospector`)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.17.0 | June 21, 2026 |

**Description:** Write a freelance-marketplace bid (cover letter + 60-second VSL script) for a chosen gig from the opportunities DB — with secret-word detection and service mapping — written back onto the gig's Notion row.

### Change Log

**v2.17.0** — June 21, 2026
- New skill (Sales). The **Write** phase of the **Inbound Gig Engine** (`gig-prospector → gig-proposal-writer → n8n-workflow-builder → vsl-demo-producer`). Takes a single reviewed gig from `${BRAND}_GIGS_DB`, maps it to a service the brand actually sells (from `product.md`), detects any client-required **secret word** ("start your proposal with X") and makes it the literal first line, then drafts a tailored **cover letter** + **60-second VSL script** in the brand voice. Writes both back onto the gig row (long-form copy as page-body blocks; queryable fields as properties it ensures exist), advances `Status` to `Drafted`, and Slacks the founder. The cover letter ends with a tool-agnostic `[DEMO VIDEO LINK]` placeholder that `vsl-demo-producer` fills. Distinct from `proposal-generator`, which builds a Gamma deck + Stripe link from a CRM **deal** (`${BRAND}_CRM_DB`) — this skill bids on **inbound freelance gigs**.

---

# SKILL.md — Gig Proposal Writer

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a freelance proposal writer for the active brand. Your job is to turn **one** open gig — already discovered, deduped, and scored by `gig-prospector` and chosen for pursuit by the founder — into a bid that wins the client's attention: a short, specific **cover letter** and a **60-second VSL script** (the spoken pitch the founder will record over a screen demo). Every claim, capability, and number you write comes from the brand context files — you never invent experience, results, tools, or pricing. You write in the brand's voice and lead with the client's own pain in their own words.

This is the bid-writing counterpart to `proposal-generator`: that skill closes a **CRM deal** with a branded deck + payment link; this one writes a **freelance-marketplace bid** for an inbound gig.

---

## When to use

Use this skill when:
- The founder picks a gig from `${BRAND}_GIGS_DB` (typically `Status="Reviewing"`) and wants the bid drafted
- Re-drafting a bid after the founder edits the angle, tier, or service emphasis
- Backfilling cover letters for a batch of reviewed gigs (run once per gig)

Do NOT use this skill for:
- Discovering / scoring gigs → use `gig-prospector` (this skill consumes its output)
- Building the proof-of-concept automation that backs the bid → use `n8n-workflow-builder` (the next phase)
- Capturing the workflow screenshot + recording instructions → use `vsl-demo-producer`
- A CRM deal proposal (Gamma deck + Stripe link) → use `proposal-generator`
- Cold outreach email copy → use `outreach-sequencer`

---

## Inputs required

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Gig | Yes | A Notion page URL/ID in `${BRAND}_GIGS_DB`, **or** a Fit-Score-ranked pick ("draft the top `Reviewing` gig"). Must live in `${BRAND}_GIGS_DB` |
| Service emphasis | Optional | Which brand service to lead with; defaults to the gig row's `Service Match` / the best `product.md` fit |
| Tone override | Optional | Defaults to `brand.md` voice |

---

## Step-by-step workflow

### Step 1 — Read brand context (the source of truth for every claim)

Read before writing a single line:
- **brands/{brand}/product.md** — the services the brand sells, differentiators, and concrete proof (what to promise and what *not* to)
- **brands/{brand}/sales.md** — **Sender Persona** (name, signature, the "experience paragraph" / proof stats used in bids) and any **Proposal Defaults** (rates, turnaround, guarantees). This replaces the hardcoded `YOUR_NAME` / `EXPERIENCE_PARAGRAPH` from the legacy script — never hardcode them
- **brands/{brand}/audience.md** — pain points and buying triggers, to restate the client's problem in resonant language
- **brands/{brand}/brand.md** — voice, tone, locale, approved phrases
- **brands/{brand}/competitors.md** — for honest differentiation when the job names alternatives

If `product.md`, `sales.md`, or `brand.md` is missing, abort with a `failed` log and a Slack note telling the founder which file to populate (point them at `/link-skills:brand-setup`). Never invent a Sender Persona or proof stats.

### Step 2 — Fetch the chosen gig from `${BRAND}_GIGS_DB`

Resolve the gig page. It **must** live inside `${BRAND}_GIGS_DB` (read the ID from `.claude/settings.local.json`) — never accept a row from another brand's DB.

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: <gig page URL or page ID>
```

If the input was a ranked pick rather than a specific page, query the DB for the highest `Fit Score` with `Status="Reviewing"` (fall back to `"New"` if the founder hasn't triaged yet) and confirm the choice in your summary.

Extract: `title`, `url`, `platform`, `market`, `budget`, `budget_type`, `client` block, `fit_score`, `service_match`, and the **full job description** from the page body. If the stored description looks truncated (gig-prospector caps excerpts) **and** Claude in Chrome is available, re-open `url` and read the full post with `mcp__Claude_in_Chrome__get_page_text` so secret-word and requirement detection are accurate. If Chrome MCP is absent, work from the stored excerpt and note the limitation.

### Step 3 — Detect the secret word (client filter)

Clients often plant a compliance test: "to show you read this, start your proposal with **{word}**" (or "begin with", "include the word", "use the phrase"). Scan the description, most-reliable signal first:

1. Explicit instruction patterns — `start (your proposal|with) ["']?(\w+)`, `begin with ["']?(\w+)`, `(include|use) the (word|phrase) ["']?([\w \-]+)`.
2. An ALL-CAPS or quoted token presented as a password near such an instruction.
3. None found → no secret word (most gigs).

If found, the secret word (or phrase) **must be the literal first line** of the cover letter, on its own, before anything else. Surface the detected word in your final summary so the founder can eyeball it — a missed secret word means instant rejection.

### Step 4 — Map the gig to a brand service + the pain point

Match the job to the service(s) the brand sells (from `product.md` / the row's `Service Match`). Pick the single strongest mapping to lead with. Extract the **client's pain point** as a short human phrase from the job text (what they're trying to fix), to open the cover letter and the VSL. If the job is a weak/tangential fit (`Service Match=Weak`), say so in your summary and recommend skipping rather than writing a forced bid.

Note the **solution shape** this gig implies (e.g. lead-gen pipeline, email automation, AI receptionist, CRM sync, social scheduler) — `n8n-workflow-builder` reads this from the row to build the matching proof workflow, so record it explicitly.

### Step 5 — Draft the cover letter

Short, specific, skimmable — in `brand.md` voice. Structure:

1. **Secret word** (Step 3) as the first line, verbatim — only if one was detected.
2. **Hook** — restate the client's pain point (Step 4) in their language. No "Dear Hiring Manager", no "I am writing to apply".
3. **Proof of fit** — one or two sentences mapping their need to the brand's service, grounded in the Sender Persona's experience paragraph / proof stats from `sales.md`. Real numbers only.
4. **The plan** — 2–4 plain-language steps describing the automation you'd build (this is the same shape `n8n-workflow-builder` will render). Use the client's vocabulary, not node names.
5. **Demo offer + CTA** — offer the 60-second walkthrough video and a quick call. End with the literal placeholder `[DEMO VIDEO LINK]` (tool-agnostic — the founder records it in Loom, Tella, Vidyard, ScreenStudio, or any recorder; `vsl-demo-producer` fills it). Do **not** hardcode a specific recording tool.
6. **Signature** — exact Sender Persona block from `sales.md`.

Keep it tight (≈120–200 words). Match the locale/currency from `brand.md` if rates are mentioned.

### Step 6 — Write the 60-second VSL script

A spoken script (~150 words) the founder will record over a screen capture of the n8n workflow. Mark the on-screen action with `[SHOW WORKFLOW]` where the demo should appear. Structure:

1. **Hook** (~10s) — name the pain ("You're still copying leads into your CRM by hand…").
2. **Promise** (~10s) — the outcome the automation delivers.
3. **Demo** (~30s) — `[SHOW WORKFLOW]` walk the trigger → steps → visible result in the client's language.
4. **CTA** (~10s) — "If you want this running in your account, let's hop on a quick call."

Write it to be read aloud — short sentences, second person, brand voice.

### Step 7 — Write the bid back onto the gig row

Persist to the same Notion page so the whole pipeline shares one record.

**Ensure the queryable properties exist** on `${BRAND}_GIGS_DB` (idempotent — add only if missing, preserving all existing properties):

```
Use mcp__claude_ai_Notion__notion-update-data-source (only for properties not already present):
- Category      : select   (the solution shape from Step 4)
- Secret Word   : rich_text
- Proposal Path : rich_text   (local backup path from Step 8)
```

Then update the page:

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <gig page id>
- properties: {
    "Status":      "Drafted",          // adds the select option if new
    "Category":    "<solution shape>",
    "Secret Word": "<word or empty>"
  }
```

**Append the long-form copy as page-body blocks** (rich_text properties cap at ~2000 chars; cover letters + scripts can exceed that). Add two headed sections to the page body: `## Cover Letter` (with the secret word visible on line 1) and `## VSL Script (60s)`. This keeps the bid auditable in Notion next to the job description.

### Step 8 — Save local backup

Save the full bid to `outputs/{brand}/sales/gigs/proposals/Proposal_{gig-slug}_{DDMonYYYY}.md` (cover letter + VSL script + metadata). Record this path in the `Proposal Path` property (Step 7).

### Step 9 — Slack the founder

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the deferred tool schema** — otherwise the task hangs.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "<digest below>"
```

Digest:

```
✍️ [{brand}] Bid drafted — {gig title}
• {Platform}/{Market} · {Budget} · Fit {score}/100 · Service: {service match}
• Secret word: {word or "none detected"}
• Solution shape: {category}  → next: /link-skills:n8n-workflow-builder
Cover letter + VSL script written to the gig row: {notion_url}
```

Match the tone to `brand.md`.

---

## Output format

**Save location:** `outputs/{brand}/sales/gigs/proposals/`
**Naming:** `Proposal_{gig-slug}_{DDMonYYYY}.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: gig-proposal-writer
Brand: {brand}
Gig: {gig title}
Gig URL: {url}
Platform: {platform}
Market: {market}
Service Match: {Strong|Partial|Weak}
Category: {solution shape}
Secret Word: {word or none}
Notion Gig Row: {url}
Status: Drafted
---
```

**Output sections:**
1. **Cover Letter** — final copy (secret word on line 1 if any; `[DEMO VIDEO LINK]` placeholder near the CTA)
2. **VSL Script (60s)** — spoken script with `[SHOW WORKFLOW]` marker
3. **Bid notes** — service mapped, pain point used, why this angle; any truncation/Chrome-absent caveat

---

## Quality checklist

- [ ] Active brand resolved; `agents/link.md` + brand context read first
- [ ] Gig page confirmed to live in `${BRAND}_GIGS_DB` — no cross-brand contamination
- [ ] Full job description used (re-read live via Chrome when the stored excerpt was truncated, or caveat logged)
- [ ] Secret word detected and placed as the literal first line — or confirmed none exists; surfaced in the summary
- [ ] Cover letter leads with the client's pain in their words; no "Dear Hiring Manager" filler
- [ ] Every capability/number traces to `product.md` / `sales.md` — no invented experience, results, or pricing
- [ ] Sender Persona signature is the exact block from `sales.md`
- [ ] Cover letter ends with the tool-agnostic `[DEMO VIDEO LINK]` placeholder — no hardcoded recorder
- [ ] VSL script is ~60s, second person, brand voice, with a `[SHOW WORKFLOW]` marker
- [ ] Solution shape recorded as `Category` so `n8n-workflow-builder` can build the matching workflow
- [ ] Cover letter + VSL written to the gig row as page-body blocks; `Status="Drafted"`
- [ ] Weak-fit gigs flagged with a skip recommendation rather than a forced bid
- [ ] Local backup saved; `Proposal Path` set
- [ ] Slack digest sent to `$SLACK_NOTIFY_USER`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "gig-proposal-writer"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "gig_title": "<title>",
    "gig_url": "<url>",
    "platform": "<platform>",
    "market": "<market>",
    "fit_score": 0,
    "service_match": "<Strong|Partial|Weak>",
    "category": "<solution shape>",
    "secret_word_detected": false,
    "secret_word": "<word or empty>",
    "cover_letter_words": 0,
    "vsl_script_words": 0,
    "status_after": "Drafted",
    "notion_gig_url": "<url>",
    "output_path": "outputs/{brand}/sales/gigs/proposals/",
    "deliverable": "Proposal_{gig-slug}_{DDMonYYYY}.md"
  }
```

---

## Part of the pipeline

The **Write** phase of the **Inbound Gig Engine**:

```
gig-prospector (Discover → ${BRAND}_GIGS_DB, Status="New")
  → founder review (Status="Reviewing")
  → gig-proposal-writer (this skill — cover letter + VSL, Status="Drafted")
  → n8n-workflow-builder (Prove — real n8n workflow + URL, Status="Workflow Built")
  → vsl-demo-producer (Demo — screenshot + recording instructions, Status="Demo Ready")
  → founder records the video, pastes [DEMO VIDEO LINK], submits the bid
```

On-demand, one gig at a time.
