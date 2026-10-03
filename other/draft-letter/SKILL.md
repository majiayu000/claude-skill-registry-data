---
name: draft-letter
description: "Drafts correspondence for a matter using templates and matter data. Use when Mandy says 'draft letter', 'write to', 'letter to insurer', 'notice of involvement', 'treatment dispute', 'client update', or any request to create correspondence. Supports all letter types: insurer, doctor, IME, employer, WIC, client, settlement."
---

# Draft Letter

## Important
- Manual-only. Never auto-invoke.
- ALWAYS save letter to disk BEFORE displaying to Mandy.
- ALWAYS cite specific Act sections from `rules/` files — never guess.
- Consult `letter-routing.md` to determine which template to use.

## Instructions

### Step 0: Resolve Matter
Follow `_shared/resolve-matter.md`. If only letter-type given (e.g., "/draft-letter notice-of-involvement"), resolve matter from conversation context.

### Step 1: Determine Letter Type
If specified: use directly.
If unclear: consult `letter-routing.md` for mapping. Present available types grouped by recipient.

### Step 2: Gather Data
1. Read `matter.json` fully
2. Read template from `templates/{recipient}/{letter-type}.md`
3. Read `rules/{claim_type}.md` for legislative section numbers
4. Check template `[DOCUMENT-TIER:]` marker — read extracts accordingly
5. Read `templates/letterhead.json` for firm details

### Step 3: Check Previous Versions
If `letters/` contains a file with same letter type: this is a redraft.
Rename old file to `{type}-{date}-v{n}.md`, update status to "superseded".

### Step 4: Draft
- Replace all `{{variables}}` with matter.json data
- Follow `[INSTRUCTION:]` blocks for generated content
- Apply `[TONE:]` marker
- Fill `[CITE:]` markers with actual section numbers from rules/
- Tier 2: reference specific document findings with page numbers
- Follow `reference/style-guide.md` for formatting

### Step 5: Save and Update
1. Save to `letters/{letter-type}-{date}.md`
2. Update `matter.json` letters array: status "draft", date_created, version
3. Update `matters/index.jsonl`
4. Append to `activity-log.jsonl`
5. `git -C matters/ add -A && git -C matters/ commit -m "draft-letter: {id} — Drafted {letter-type} to {recipient}."`

### Step 6: Present and Prompt
Display the letter. Then:
```
"Review this draft. You can:
- Request changes (tell me what to adjust)
- /approve-letter {name} {filename} — mark ready to send
- /send-letter {name} {filename} — approve and send via Outlook"
```

### Step 7: Proactive Stage Check
Check `rules/stage-expectations.json` and `dates.limitation_expiry`.

## Error Handling
- **Template not found:** "No template found for '{letter-type}'. Available types:" then list from letter-routing.md.
- **Missing matter data for template variable:** "matter.json is missing {field}. Update with `/update-matter` first, or provide the value now."
- **Rules file missing:** "Cannot find rules/{claim_type}.md. Legislative references will be incomplete."

## Example
```
/draft-letter chen treatment-rejection-dispute
→ Resolve: WC-2026-012 (Sarah Chen)
→ Template: insurer/treatment-rejection-dispute.md
→ Tier 2: read relevant extract sections
→ Draft with legislative citations from rules/workcover.md
→ Save to letters/treatment-rejection-dispute-2026-03-28.md
→ Present and prompt for review
```
