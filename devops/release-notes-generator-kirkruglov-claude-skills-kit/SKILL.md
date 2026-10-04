---
name: release-notes-generator
description: "Generate user-facing release notes from a plain-language sprint summary file — no git required. Produces 4 ready-to-use formats: changelog, email, in-app push, and social post. Triggers: 'generate release notes', 'write release notes', 'create release notes from', 'turn sprint results into release notes', 'сгенерируй release notes', 'напиши release notes', 'создай релизные заметки', 'оформи итоги спринта'."
version: 1.0.0
---

# Release Notes Generator

This skill transforms a plain-language sprint summary or product update file into polished, user-facing release notes for 4 communication channels — without git, CLI, or developer tooling. Designed for non-technical PMs, product owners, and team leads who write sprint results in plain text and need to distribute them across multiple channels.

**Input:**
- One local file (`.md` or `.txt`) with sprint results or product update notes
- Optional: product name, version / sprint number, audience type (`users` | `customers` | `internal`)

**Output:**
- **Changelog entry** — markdown-formatted, ready to paste into CHANGELOG.md
- **Email announcement** — subject line + body (2–4 paragraphs)
- **In-app / push notification** — 1–2 sentences, max 160 characters
- **Social post** — LinkedIn / X version, conversational tone

---

## Language Detection

Detect the language of the **input file**:
- If the file content is in Russian: generate all 4 output formats in Russian
- If the file content is in English: generate all 4 formats in English
- If mixed-language content: default to English; add note "Mixed-language input detected — generated in English. Say 'по-русски' to switch."
- If the user's trigger phrase is in Russian but the file is in English: use English for outputs (follow the file)

---

## Instructions

### Step 1: Find and Read the Input File

1. Look for the file the user mentioned by name
   - If no filename given: scan the Cowork workspace for `.md` and `.txt` files; if exactly one such file exists, use it; if multiple exist, list them and ask which one to use
2. Read the file
3. Validate:
   - If no file found: stop — "No input file found. Please place your sprint summary or product update notes (.md or .txt) in the Cowork workspace and try again."
   - If the file is empty or contains fewer than 3 meaningful lines: stop — "The file is too short to generate release notes from. Add at least a few bullet points describing what was released."
   - If file is `.docx` or `.pdf`: stop — "release-notes-generator works with .md and .txt files. Please export your document to text format and try again."

### Step 2: Extract Context

1. Scan the first 5–10 lines for:
   - Product name
   - Version number or sprint number (e.g., `v1.4.2`, `Sprint 23`, `Release 2026-05`)
   - Date (release date or sprint end date)
   - Audience type (look for signals: "for customers", "internal only", "user-facing")

2. If product name, version, or date cannot be inferred:
   - Ask in **one consolidated question**: "A few quick details: What's the product name? What version or sprint number is this? What's the release date? (Feel free to skip any you don't need.)"
   - Do not ask multiple separate questions

3. Set audience type:
   - Default: `users`
   - Override if the file explicitly states `internal` or `customers`

### Step 3: Filter for User-Facing Content

1. Read all update items in the file
2. Classify each item:
   - **Include — New:** new features or capabilities (user-visible)
   - **Include — Improved:** enhancements to existing features, performance gains users notice, UI/UX changes
   - **Include — Fixed:** bug fixes that affected users
   - **Exclude:** internal refactors, technical debt cleanup, infrastructure changes, developer tooling updates, CI/CD changes, database migrations, dependency upgrades with no user impact

3. Do NOT silently drop excluded items — collect them for the "Internal Changes" note at the end of output

4. If **all items** are technical/internal:
   - Stop and ask: "All items appear to be internal technical changes (refactors, infrastructure). These are typically not suitable for user-facing release notes. Should I write internal-team notes instead, or do you have user-facing changes to add?"

5. Group user-facing items into 3 categories: **New**, **Improved**, **Fixed**
   - Omit any category with zero items (do not print empty sections)

### Step 4: Generate All 4 Formats

Generate formats in this order. Use clearly delimited sections with emoji labels.

**Format 1 — Changelog Entry**
- Markdown code block, valid CHANGELOG.md format
- Version header with date: `## [version] — YYYY-MM-DD`
- Grouped by: `### New`, `### Improved`, `### Fixed`
- Each item: `- [Feature/fix name]: [one-line plain-language description of the user benefit]`
- No technical jargon; no commit hashes; no dev abbreviations

**Format 2 — Email Announcement**
- Subject line: specific, benefit-first (e.g., "Sprint 23 updates: new report filters, faster exports")
  - Do NOT use: "Newsletter", "Update", "Announcement", "We are pleased to announce"
- Body structure:
  - Opening sentence: lead with the biggest user benefit ("Starting today, you can...")
  - Paragraph 1: highlight 2–3 top improvements in plain language
  - Paragraph 2: list remaining changes briefly
  - Closing: 1 sentence CTA or "thank you" — keep it short
- Tone: professional but direct; no corporate fluff

**Format 3 — In-App / Push Notification**
- Exactly 1–2 sentences
- Maximum 160 characters (count carefully)
- Structure: verb-first + specific benefit + optional CTA
- Example shape: "[Feature] is now live — [what users can do]. [CTA]"
- If character limit is hard to hit with multiple items: pick the single most impactful update

**Format 4 — Social Post (LinkedIn / X)**
- 3–5 sentences
- Conversational tone — not a press release
- Opens with a hook (a question, a surprising stat, or a direct statement of value)
- Names 2–3 highlights by name
- Ends with one CTA or question
- No emojis unless user specifically requested them

**After generating all 4 formats:**
- List excluded technical items under `### Internal Changes (not in user-facing notes)`
- If list is empty: omit this section

### Step 5: Offer Blog Intro

After the 4 formats, add a single line:
> "Want me to add a blog intro paragraph? Just say so."

Do not generate it unless requested.

---

## Negative Cases

- **File not found:** Stop — "No input file found. Please place your sprint summary (.md or .txt) in the Cowork workspace and try again."
- **File too short:** Stop — "The file is too short to generate release notes from. Add at least a few bullet points describing what was released."
- **All items are internal/technical:** Stop and ask — "All items appear to be internal technical changes. Should I write internal-team notes instead, or do you have user-facing changes to add?"
- **No version or sprint number found:** Ask once (consolidated with other missing fields in Step 2).
- **Hotfix / patch release:** Detected from keywords (`hotfix`, `patch`, `urgent fix`) in the **filename or the first 3 lines of the file** — adjust email tone to reassurance-first: "We've just pushed a fix for [issue]. Everything is back to normal."
- **File is .docx or .pdf:** Stop — "release-notes-generator works with .md and .txt files. Please export your document to text format and try again."
- **User asks for a format not in the list (e.g., Slack message):** After generating the 4 standard formats, offer: "I can also write a Slack announcement — want me to add it?"

---

## Output Format

```
## Release Notes — [Product Name] [Version] · [Date]

---

### 📋 Changelog Entry

[markdown code block]

---

### 📧 Email Announcement

**Subject:** [Subject line]

[Email body]

---

### 📱 In-App / Push Notification

[1–2 sentences, ≤ 160 characters]

---

### 🔗 Social Post (LinkedIn / X)

[3–5 sentences]

---

### Internal Changes (not in user-facing notes)
- [List of excluded technical items — omit section if empty]
```

---

## Edge Cases

- **Single-item release:** Generate all 4 formats even for one feature — scale length proportionally
- **Hotfix release:** Detected from keywords (`hotfix`, `patch`, `urgent fix`) in the filename or the first 3 lines of the file — reassurance-first tone; email opens with "We've resolved [issue]"; push says "Fixed: [issue] — all systems normal"
- **Major release (many items, "major" keyword):** Add a note after outputs: "This looks like a major release — a dedicated blog post might be worth the effort. Want me to draft an intro?"
- **Mixed EN/RU file:** Default to English; note "Mixed-language input detected — generated in English. Say 'по-русски' to switch."
