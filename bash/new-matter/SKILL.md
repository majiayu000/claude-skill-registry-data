---
name: new-matter
description: "Creates a new client matter from intake consultation. Use when Mandy says 'new matter', 'new client', 'new claim', 'intake', 'just had a consult', or discusses a new client's injury details. Handles WorkCover, TAC, Public Liability, TPD, and Common Law claims. Runs conflict check, calculates deadlines, drafts initial letters."
---

# New Matter — Conversation-First Intake

## Important
- This skill is manual-only. Never auto-invoke.
- ALWAYS run conflict check before creating matter files.
- Extract client details from conversation FIRST. Only ask questions for gaps.

## Instructions

### Step 1: Extract from Conversation
Scan the full session for client details: name, claim type, date of injury, mechanism, employer, treating doctors, work status, client goals, and any corrections.
If Mandy corrected herself during conversation, use the final stated version.
If no conversation data found, fall back to guided intake using `intake-questions.md`.

### Step 2: Conflict Check
Read `matters/index.jsonl`. Search for:
- Same client name (partial, case-insensitive)
- Same employer appearing as client in another matter
- Same claim number

If conflict found:
```
"⚠️ Potential conflict: {client/employer} matches {existing_matter_id} ({existing_client}).
This may be a returning client or a genuine conflict. Proceed?"
```
Log result in activity-log regardless. Record in matter.json compliance section.

### Step 3: Present Summary for Confirmation
Show all extracted data in structured format. Ask Mandy to confirm.

### Step 4: Ask About Gaps Only
Consult `intake-questions.md` for which fields are essential vs typically unknown at intake.
Do NOT ask about: insurer claim number, specific diagnoses, WPI, CoC details, settlement value.

### Step 5: Generate Matter ID
Read `matters/index.jsonl`, find highest sequence number for this claim type + year, increment.
Format: `{TYPE}-{YEAR}-{SEQ}` (e.g., WC-2026-012)

### Step 6: Create Directory and Files
```bash
mkdir -p matters/{id}/documents matters/{id}/letters matters/{id}/chronology matters/{id}/notes
```
Create `matter.json` from `reference/matter-schema.json`.
Create empty `activity-log.jsonl`.
Create `notes/strategy.md` with client goals from conversation.

### Step 7: Calculate Deadlines
Read `rules/deadlines.json`. Calculate all applicable deadlines for this claim type.
Calculate `dates.limitation_expiry`. If already expired or within 6 months: ALERT prominently.

### Step 8: Ingest Existing Documents
Check `matters/{id}/documents/` for any PDFs. If found, run analyse-document logic for each.

### Step 9: Draft Initial Letters
Based on claim type:
- WorkCover / TAC: `insurer/notice-of-involvement.md` + `client/engagement-retainer.md`
- Public Liability / TPD: `client/engagement-retainer.md`
Personalise from consult details. Save as drafts.

### Step 10: Capture Client Questions
If Mandy or client raised questions during consult, save to `notes/client-questions.md`.

### Step 11: Final Steps
1. Update `matters/index.jsonl`
2. Append to `activity-log.jsonl`
3. `git -C matters/ add -A && git -C matters/ commit -m "new-matter: {id} — Created. Client: {name}. {type}. DOI: {date}."`

### Step 12: Present Summary
```
MATTER CREATED: {id}
Client: {name} | Type: {type} | DOI: {date}
Limitation: {expiry_date} ({days} remaining)
Conflict check: {result}
Captured: {list of populated fields}
Unknown: {list of empty fields}
Documents: {n} ingested
Letters drafted: {list}
Next steps: {prioritised actions}
```

## Error Handling
- **index.jsonl missing or empty:** Create it with this matter as first entry.
- **matters/ directory doesn't exist:** Run `scripts/setup.sh` first.
- **Git commit fails:** Check if matters/.git exists. If not: `cd matters/ && git init && git config user.name "Karlos AI Assistant" && git config user.email "ai@karloslawyers.com.au"`.

## Example
```
Mandy says: "Just had a consult with Sarah Chen, she hurt her back lifting boxes
at Woolworths on January 12th. WorkCover claim. She's off work, seeing Dr Smith
as her GP. She wants to know if she can get surgery approved."

→ Extract: name=Sarah Chen, employer=Woolworths, DOI=2026-01-12, type=workcover,
  mechanism=lifting injury, work_status=off work, treating_gp=Dr Smith,
  client_goal=surgery approval
→ Conflict check against index.jsonl
→ Generate WC-2026-012
→ Create matter, calculate deadlines, draft notice + retainer
→ Present summary
```
