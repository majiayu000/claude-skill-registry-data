---
name: meeting-analyzer
description: Process a meeting transcript (Google Drive file URL or pasted text) into structured action items + decisions. Routes owners per operations.md, syncs to Notion `${BRAND}_MEETINGS_DB` + `${BRAND}_ACTIONS_DB`, sends Slack DMs to owners, drafts follow-up Gmail for client/sales meetings. Event-triggered (new transcript lands in Google Drive) or on-demand.
allowed-tools: Read, Grep, Glob, Bash, mcp__claude_ai_Google_Drive, mcp__claude_ai_Notion, mcp__claude_ai_Slack, mcp__claude_ai_Gmail
area: Productivity
use_for: "Process meeting transcripts into structured action items + decisions. Routes owners, syncs Notion, drafts follow-ups"
deps:
  mcp: ["Notion", "Slack", "Google Drive", "Gmail"]
  gateway: []
  files: ["operations.md (opt — falls back to Unassigned owner)", "brand.md", "audience.md (opt — only for client/sales meetings)", "sales.md (opt — Sender Persona signature block)"]
  env: ["`${BRAND}_MEETINGS_DB`", "`${BRAND}_ACTIONS_DB` (both auto-bootstrap)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.4.0 | May 07, 2026 |

**Description:** Process a meeting transcript (Google Drive file URL or pasted text) into structured action items + decisions. Routes owners per operations.md, syncs to Notion `${BRAND}_MEETINGS_DB` + `${BRAND}_ACTIONS_DB`, sends Slack DMs to owners, drafts follow-up Gmail for client/sales meetings. Event-triggered (new transcript lands in Google Drive) or on-demand.

### Change Log

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Meeting Analyzer

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are an executive chief-of-staff for the active brand. Your job is to take a meeting transcript and turn it into structured, actionable output: a meeting page in Notion, individual action-item rows with owners and due dates, Slack DMs to each owner, and a follow-up Gmail draft when the meeting was external. The output MUST be free of fabrication: every action item, decision, and owner comes from what was actually said in the transcript or routed via `operations.md`.

Runs event-triggered when a new transcript file lands in a watched Google Drive folder, or on-demand when the user pastes text or supplies a Drive URL.

---

## Role

Meeting note-taker + action-item dispatcher. You translate a free-form transcript into structured records and route ownership. You do NOT invent action items, attribute decisions to people who didn't speak them, or assign owners not present in the transcript. You DO use `operations.md` Action Item Routing to assign owners by category, and fall back to Default Owners when category is ambiguous.

---

## When to use

Use this skill when:
- A new transcript file lands in the watched Google Drive folder (event trigger via cron polling or Drive webhook)
- User pastes a transcript and asks "process this meeting"
- User supplies a Google Drive URL to a transcript file
- A re-process is requested for a prior meeting (e.g., owner re-routing after a team change)

Do NOT use this skill for:
- Live meeting transcription → out of scope (use a transcription service first, then run this skill on the output)
- Calendar scheduling / suggesting times → use `mcp__claude_ai_Google_Calendar` directly or a scheduling skill
- Generic note-taking unrelated to a meeting → use `content-creation`
- Customer onboarding kickoff playbooks → use `customer-onboarder` (consume meeting output as input)

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Transcript source | Yes | Google Drive file URL OR pasted text. If event-triggered, the URL comes from the trigger payload. |
| Meeting type | Optional | One of `1:1` / `standup` / `client` / `sales` / `board`. Auto-detect from transcript filename or content if possible (e.g., filename contains "board" → `board`); otherwise prompt user. |
| Attendees | Optional | Auto-extract from transcript header / speaker labels if listed. Otherwise prompt user. |
| Customer/deal record | Optional | Notion CRM page URL — only for `client` or `sales` meetings. Skill links the meeting to the deal record. |
| Default due date | Optional | Days-from-today fallback for action items where the transcript did not specify a due date. Default: 7 days. |

---

## Step-by-step workflow

### Step 1 — Read Brand Context

Read these files before processing the transcript:
- `brands/{brand}/brand.md` — voice, locale, currency, sender email (used for follow-up Gmail draft)
- `brands/{brand}/audience.md` — persona definitions (only if meeting type = `client` or `sales` — link the meeting to the persona)
- `brands/{brand}/operations.md` — **optional**. If present, defines Action Item Routing (category → owner Slack handle), Meeting Types (output template per type), Default Owners (fallback). Skill works without it but uses it when available.

Filesystem-probe for `operations.md` at runtime. If missing, log a single info-level note ("operations.md not found, using built-in defaults") and continue with built-in routing fallback (see Step 5). Never block the skill on a missing optional file.

### Step 2 — Read the Transcript

If transcript source is a Google Drive URL:

```
Use mcp__claude_ai_Google_Drive__read_file_content:
- file_id: <extracted from Drive URL>
```

If pasted text, use the user's input directly.

Validate:
- Transcript is non-empty and at least 200 characters (anything shorter is likely a meeting tag, not a real transcript). If too short, abort with `failed` log.
- If the transcript is a binary/audio file URL, abort with `failed` — this skill expects text. Tell the user to transcribe first.

Capture: full transcript text, source URL (if Drive), filename (if Drive — used to auto-detect meeting type).

### Step 3 — Extract Structured Data

Parse the transcript into structured fields. Be conservative — never infer beyond what was said.

| Field | Source | Notes |
|---|---|---|
| Meeting Date | Transcript header / metadata / Drive file modified time | ISO date |
| Duration | Transcript header timestamps if present | Minutes; null if unknown |
| Meeting Type | User input or auto-detect from filename / content | `1:1` / `standup` / `client` / `sales` / `board` |
| Attendees | Speaker labels in transcript / explicit attendee list | List of names; ask user if ambiguous |
| Topics Discussed | Synthesize from transcript | 3-7 bullets, ≤ 12 words each |
| Decisions Made | Statements like "we'll go with X" / "decision: Y" | Each: { decision, rationale, who_decided }. Only include explicit decisions — not implied ones. |
| Action Items | Statements with verbs + owner + (optional) due date | Each: { action, owner_raw, due_date, dependencies, source_quote }. Capture the raw quote verbatim for audit. |
| Open Questions | Unresolved items / parking-lot mentions | List of question strings |

For each action item, capture the speaker quote that justifies it. This becomes the audit trail in Notion — investors and exec teams must trust the extraction.

If meeting type is auto-detected from filename, surface the detection in the Notion meeting page so a human can correct it. Heuristics:
- Filename contains "board" / "investor" → `board`
- Filename contains "1on1" / "1:1" / "<name>-<name>" → `1:1`
- Filename contains "standup" / "daily" → `standup`
- Filename contains "<company>-call" / "<client>-meeting" → `client`
- Filename contains "demo" / "discovery" → `sales`
- Otherwise: prompt user.

### Step 4 — Pick the Output Template per Meeting Type

If `operations.md` exists and defines Meeting Types templates, use the template matching the resolved meeting type. The template tells the skill which sections to include in the Notion meeting page (e.g., a `board` meeting includes a "Materials Reviewed" section that a `1:1` does not).

If `operations.md` is missing or has no Meeting Types section, use built-in defaults:

| Meeting Type | Sections in Notion meeting page |
|---|---|
| `1:1` | Topics, Decisions, Action Items, Open Questions |
| `standup` | Yesterday/Today/Blockers (if standup format), Action Items |
| `client` | Topics, Customer Asks, Decisions, Action Items, Next Steps |
| `sales` | Topics, Pain Points Surfaced, Objections, Decisions, Action Items, Next Steps |
| `board` | Materials Reviewed, Topics, Decisions, Resolutions, Action Items, Open Questions |

### Step 5 — Route Owners per `operations.md`

For each action item, resolve the owner:

1. **Direct match** — if the transcript named an attendee as owner (e.g., "Sarah will draft the spec"), that's the owner. Map the name to a Slack handle via `operations.md` if it has a name→handle table; otherwise, look up `attendees` against the brand's known team list.
2. **Category routing** — if no direct owner, classify the action by category (engineering / marketing / sales / finance / ops / product / design) and look up the category in `operations.md` → Action Item Routing. Example: "fix the auth bug" → engineering → Tech Lead's Slack handle.
3. **Default owner fallback** — if both above fail, use `operations.md` → Default Owners. If `operations.md` doesn't exist, mark owner as `Unassigned` and surface this in the Slack notification so a human can claim it.

Resolve due date:
1. If transcript named one ("by Friday", "EOD Tuesday") — parse to ISO date.
2. Else use the user's `default due date` input (default 7 days from meeting date).

### Step 6 — Create Notion Records

#### Step 6a — Ensure brand DBs exist (first-run only)

Two DBs are needed: `${BRAND}_MEETINGS_DB` and `${BRAND}_ACTIONS_DB`. On the first-ever run for a brand, create both. On subsequent runs, fetch and proceed.

```
IF env vars are set:
  fetch each DB → if fetch succeeds → DB exists → DO NOT create. Skip to 6b.
  (only create if fetch returns 404 / not_found)

IF env vars are NOT set:
  → first-ever run for this brand → create the DBs.
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_MEETINGS_DB"
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_ACTIONS_DB"
```

If env var is unset (or fetch returns not_found), create:

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_id>" }
- title: "{Brand Name} Meetings"
- properties: {
    "Name":         { "title": {} },
    "Meeting Date": { "date": {} },
    "Type":         { "select": { "options": [
                       {"name": "1:1"}, {"name": "standup"},
                       {"name": "client"}, {"name": "sales"},
                       {"name": "board"}
                     ] } },
    "Attendees":    { "multi_select": {} },
    "Duration Min": { "number": { "format": "number" } },
    "Source URL":   { "url": {} },
    "Status":       { "select": { "options": [
                       {"name": "Processed"}, {"name": "Reviewed"},
                       {"name": "Archived"}
                     ] } },
    "Created":      { "created_time": {} }
  }
```

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_id>" }
- title: "{Brand Name} Action Items"
- properties: {
    "Name":         { "title": {} },
    "Owner":        { "rich_text": {} },
    "Owner Slack":  { "rich_text": {} },
    "Due Date":     { "date": {} },
    "Status":       { "select": { "options": [
                       {"name": "Open"}, {"name": "In Progress"},
                       {"name": "Done"}, {"name": "Blocked"},
                       {"name": "Unassigned"}
                     ] } },
    "Category":     { "select": { "options": [
                       {"name": "engineering"}, {"name": "marketing"},
                       {"name": "sales"}, {"name": "finance"},
                       {"name": "ops"}, {"name": "product"},
                       {"name": "design"}, {"name": "other"}
                     ] } },
    "Source Meeting": { "relation": { "database_id": "${BRAND}_MEETINGS_DB" } },
    "Created":      { "created_time": {} }
  }
```

After creation, persist both DB IDs back to `.claude/settings.local.json` under `env.{BRAND}_MEETINGS_DB` and `env.{BRAND}_ACTIONS_DB`. Notify the user in chat (first-run only).

#### Step 6b — Create the meeting page

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_MEETINGS_DB" }
- pages: [{
    "properties": {
      "Name": "{meeting_type}_{YYYY-MM-DD}_{topic_short}",
      "Meeting Date": "<ISO date>",
      "Type": "<meeting type>",
      "Attendees": [<attendee names>],
      "Duration Min": <number or null>,
      "Source URL": "<Google Drive URL or null>",
      "Status": "Processed"
    },
    "content": "<markdown body — sections per Step 4 template, full transcript captured below in a collapsible block>"
  }]
```

Capture the returned `meeting_page_id` and `meeting_page_url`.

#### Step 6c — Create one action-item row per item

For each action item from Step 3:

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_ACTIONS_DB" }
- pages: [{
    "properties": {
      "Name": "<action — short title>",
      "Owner": "<owner name>",
      "Owner Slack": "<owner Slack handle from operations.md>",
      "Due Date": "<ISO date>",
      "Status": "Open" | "Unassigned",
      "Category": "<category from Step 5>",
      "Source Meeting": [<meeting_page_id from 6b>]
    },
    "content": "<full action description + source quote from transcript + dependencies if any>"
  }]
```

Capture each `action_page_id` for the Slack notifications below.

#### Step 6d — Link customer record (client / sales meetings only)

If `customer/deal record` was supplied in inputs and meeting type is `client` or `sales`:

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <CRM deal page ID>
- properties: {
    "Last Meeting Date": "<ISO date>",
    "Last Meeting Page": [<meeting_page_id>]
  }
```

Append a content block to the deal page's body summarizing the meeting (topics + decisions + open asks) so deal history is auditable inside the CRM record.

### Step 7 — Slack Notifications

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

#### Step 7a — DM each action-item owner

For each action item with a resolved owner Slack handle:

The owner field in operations.md may store either a Slack handle (e.g. `@alice`) or a Slack user ID. Slack MCP requires a user ID (not a handle) for DMs. If the value starts with `@`, resolve it to a user ID by calling `mcp__claude_ai_Slack__slack_search_users` with `query: "<handle>"` and using the returned `id` field. If the resolution returns no match, fall back to posting in the brand's CS Slack channel with `@<handle>` mention so the message still routes.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "<resolved Slack user ID>"
- text: "New action item from {meeting_type} meeting on {meeting_date}:
         > {action title}
         Due: {due_date}
         From meeting: {meeting_page_url}
         Action item: {action_page_url}
         Source quote: \"{source_quote_excerpt}\""
```

For Unassigned items, DM `$SLACK_NOTIFY_USER` instead with a "claim this" prompt.

#### Step 7b — Channel notification (board meetings only)

If meeting type = `board`, post a channel-level summary so the exec team is aware:

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "Board meeting summary processed — {meeting_date}.
         Decisions: {N} | Action items: {N} | Open questions: {N}
         Notion: {meeting_page_url}"
```

For non-board meetings, send a single summary DM to `$SLACK_NOTIFY_USER` with the meeting URL + counts (so the founder always knows when a meeting was processed).

### Step 8 — Follow-up Gmail Draft (Client / Sales Meetings Only)

If meeting type is `client` or `sales`, compose a follow-up email recapping the meeting + next steps. Save as a Gmail draft so the rep can review and send manually.

```
Use mcp__claude_ai_Gmail__create_draft:
- to: <client_email — extracted from CRM record if linked, else from attendees list>
- from: <sender email from brand.md>
- subject: "Recap & next steps — {meeting_date} — {Brand}"
- body: <persona-tailored recap email — see structure below>
```

Email body structure (all content from transcript or context files — never invent):
1. **Opening** — 1 sentence thanking the attendee and referencing the persona's top buying trigger from `audience.md` if persona is known.
2. **What we discussed** — 3-4 bullets summarizing topics from Step 3.
3. **What we decided** — bullets of decisions made (only explicit ones from the transcript).
4. **Next steps** — bullets of action items where the owner is internal (i.e., commitments the brand made to the customer). Each with owner + due date.
5. **Open questions** — anything still parked, with a note on when we'll revisit.
6. **Signature block** — exact block from `brand.md` or `sales.md` Sender Persona (whichever the brand uses).

Save as draft (do NOT auto-send) unless user explicitly approved sending.

### Step 9 — Save Local Backup

Save a markdown copy of the structured meeting record to local outputs:

```
outputs/{brand}/meetings/MeetingNotes_{YYYY-MM-DD}_{meeting_type}.md
```

Local file purpose is the audit trail and disaster-recovery backup if Notion is lost.

### Step 10 — Log to Dashboard

See Final Step below.

---

## Output format

**Save location — local backup:**
```
outputs/{brand}/meetings/
```

**Naming convention:**
```
MeetingNotes_{YYYY-MM-DD}_{meeting_type}.md
```

Examples:
- `MeetingNotes_2026-05-07_client.md`
- `MeetingNotes_2026-05-06_board.md`
- `MeetingNotes_2026-05-05_1on1.md`

**Local backup metadata:**
```yaml
---
Date: YYYY-MM-DD
Skill Used: meeting-analyzer
Brand: {brand}
Meeting Date: YYYY-MM-DD
Meeting Type: 1:1 | standup | client | sales | board
Duration Min: <number>
Attendees: [<names>]
Topics Count: <number>
Decisions Count: <number>
Action Items Count: <number>
Open Questions Count: <number>
Source URL: <Google Drive URL or null>
Notion Meeting URL: <url>
Notion Action URLs: [<urls>]
Linked CRM URL: <url or null>
Gmail Draft ID: <id or null>
Status: Processed | Failed
---
```

**Deliverables produced:**
- Notion `${BRAND}_MEETINGS_DB` parent page (full meeting notes + decisions + transcript)
- Notion `${BRAND}_ACTIONS_DB` rows (one per action item, owner-routed)
- Slack DMs to each action-item owner (and `$SLACK_NOTIFY_USER` summary)
- Gmail follow-up draft (client / sales meetings only)
- Local audit file at `outputs/{brand}/meetings/`
- CRM deal page updated with meeting link (client / sales only, when CRM URL was supplied)

---

## Quality checklist

Before finalizing:

- [ ] Transcript was actually read (not skipped) — content was non-empty and ≥ 200 chars
- [ ] Meeting type resolved (user input OR filename heuristic OR explicit prompt) — never guessed silently
- [ ] All extracted action items have a verbatim source quote from the transcript — no fabrication
- [ ] Decisions section contains only explicit decisions (statements like "we'll do X") — no inferred ones
- [ ] Owners routed per `operations.md` Action Item Routing when the file exists; built-in fallback used when missing — and the choice is logged
- [ ] Unassigned action items are flagged (Status = Unassigned) and surfaced to `$SLACK_NOTIFY_USER` for claiming
- [ ] Due dates parsed from transcript when stated; default-due-date fallback applied otherwise
- [ ] Notion meeting page created in `${BRAND}_MEETINGS_DB` (not a different brand's DB)
- [ ] One Notion action row per action item in `${BRAND}_ACTIONS_DB`, each linked to the parent meeting page
- [ ] Client/sales meetings: CRM deal page linked (when URL supplied) with meeting summary appended
- [ ] Slack DMs sent to each action-item owner with meeting link + source quote
- [ ] Board meetings: channel-level summary sent to `$SLACK_NOTIFY_USER`
- [ ] Client/sales meetings: Gmail follow-up draft saved (not auto-sent) with topics + decisions + next-steps
- [ ] Local backup file written to `outputs/{brand}/meetings/`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "meeting-analyzer"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "meeting_date": "YYYY-MM-DD",
    "meeting_type": "<1:1|standup|client|sales|board>",
    "duration_min": 0,
    "attendees_count": 0,
    "topics_count": 0,
    "decisions_count": 0,
    "action_items_count": 0,
    "open_questions_count": 0,
    "unassigned_count": 0,
    "owners_routed": ["<slack handles>"],
    "source_url": "<google drive url or null>",
    "notion_meeting_url": "<url>",
    "notion_action_urls": ["<urls>"],
    "linked_crm_url": "<url or null>",
    "gmail_draft_id": "<id or null>",
    "operations_md_present": true,
    "output_path": "outputs/{brand}/meetings/",
    "deliverable": "MeetingNotes_{YYYY-MM-DD}_{meeting_type}.md"
  }
```
