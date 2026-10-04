---
name: prompt-library-curator
description: "Organize and tag your personal prompt collection into a structured markdown catalog with an index table. Use when you have accumulated saved prompts and want to structure, deduplicate, and label them for reuse. Triggers: 'organize my prompts', 'prompt library', 'tag my prompts', 'structure my prompt collection', 'организуй мои промпты', 'библиотека промптов', 'структурируй промпты'."
version: 1.0.0
---

# Prompt Library Curator

This skill organises a personal collection of saved prompts into a structured, navigable markdown catalog. It assigns categories, tags, summaries, and complexity ratings to each prompt, detects duplicates, and outputs a clean `prompt-library.md` file ready for reuse and sharing.

**Input:**
- Raw prompts as pasted text, an inline list, or a `.md`/`.txt` file

**Output:**
- `prompt-library.md` — structured catalog with index table, categorised prompts, and flagged duplicates

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian, use Russian category names in output, and generate the entire catalog in Russian
- If English (or other Latin-script language): respond in English, use English category names, and generate the entire catalog in English
- If ambiguous: respond in the language of the trigger phrase used and generate catalog in that language

---

## Instructions

### Step 1: Accept and Validate Input

1. Determine input source:
   - Pasted text block in chat
   - Uploaded or referenced `.md` / `.txt` file
   - Inline numbered or bulleted list

2. Validate input is non-empty
   - If empty: stop and respond — "No prompts found. Paste your prompts directly or attach a .md/.txt file."

3. Check for unsupported file formats (`.docx`, `.xlsx`, `.pdf`, etc.)
   - If detected: stop and respond — "Unsupported format. Please paste your prompts as plain text or upload a .md or .txt file."

4. Check if input looks like a conversation log rather than a prompt collection
   - Heuristic: high ratio of questions and conversational turns with no clear prompt-style structure
   - If detected: respond — "This looks like a chat log, not a prompt collection. Paste the prompt texts you want to organise, or specify which lines are prompts."

---

### Step 2: Split into Individual Prompts

1. Attempt to split the raw input into individual prompts using these separator heuristics (in priority order):
   - Horizontal rules (`---`)
   - Numbered list items (`1.`, `2.`, etc.)
   - Blank-line-separated paragraphs
   - Double newlines

2. If no separators are detected and input is a wall of text:
   - Split conservatively at double newlines
   - Add a note at the top of the output: "⚠ Separation uncertain — review split points"

3. Count the total number of prompts identified; store as `N`.

4. If `N = 1`:
   - Proceed with a single-entry catalog
   - Add note at the bottom: "Add more prompts to build a full library"
   - Skip the index table (single entry doesn't warrant it)

---

### Step 3: Analyse Each Prompt

For each prompt, determine:

1. **Category** — assign one from this set (or create a new label if none fits):
   - Writing, Research, Coding, Analysis, Meeting, Planning, Personal, Learning, Marketing, Other

2. **Tags** — assign 2–4 short keyword tags (e.g., `email`, `summary`, `b2b`, `template`)

3. **One-line summary** — ≤10 words describing what the prompt does (e.g., "Summarise a long PDF report")

4. **Complexity** — one of: `Simple` / `Moderate` / `Advanced`
   - Simple: short, single-step prompt
   - Moderate: multi-step or context-dependent prompt
   - Advanced: complex chain-of-thought, multi-role, or system-prompt level

5. **Template flag** — if prompt contains placeholder variables (`{{topic}}`, `[PERSON]`, `<context>`, etc.):
   - Preserve variables verbatim in the prompt text
   - Add `template` to the prompt's tag list

---

### Step 4: Detect Duplicates

1. Compare prompts for near-identical intent or wording (semantic similarity heuristic):
   - Exact duplicates: identical text after whitespace normalisation
   - Near-duplicates: same core instruction with minor wording differences

2. For each duplicate pair:
   - Keep both in their respective category sections
   - List them in the **Duplicates** section with a note
   - Do not delete either prompt automatically

---

### Step 5: Build Index Table

1. Sort all prompts by: Category (A→Z) → Complexity (Simple → Advanced)

2. Create an index table with columns: `#`, `Category`, `Summary`, `Tags`, `Complexity`

3. If `N > 20`: add a **Quick Find** section above the index with anchor links to each category heading

---

### Step 6: Assemble Output Catalog

Build `prompt-library.md` using the Output Format structure:

1. Header block (title, date, stats: total prompts, categories, duplicates flagged)
2. Quick Find section (if N > 20)
3. Index table
4. Horizontal rule separator
5. One `## Category` section per category, sorted A→Z
   - Under each: named prompt heading, frontmatter line (tags + complexity), original prompt text in a code block
6. Duplicates section (always present; states "No duplicates detected." if none found)

7. If user has file system access (Cowork mode): save as `prompt-library.md` in workspace folder and confirm path
8. If no file system access: display full output inline in chat

---

### Step 7: Handle Partially Organised Input

If the user's input already contains their own headings, categories, or tags:
- Preserve existing structure and user-defined category names
- Enhance only missing metadata (add tags/complexity where absent)
- Do not overwrite or rename user-defined categories

---

## Output Format

`prompt-library.md` structured as follows:

```markdown
# Prompt Library
**Last updated:** YYYY-MM-DD
**Total prompts:** N  |  **Categories:** X  |  **Duplicates flagged:** Y

---

## Quick Find
[Writing](#writing) · [Research](#research) · [Coding](#coding) · ...
*(Present only if N > 20)*

---

## Index

| # | Category | Summary | Tags | Complexity |
|---|----------|---------|------|------------|
| 1 | Writing | Draft a cold email | email, outreach, b2b | Simple |
| 2 | Research | Summarise a PDF report | pdf, summary, analysis | Moderate |

---

## Writing

### Draft a cold email
`tags: email, outreach, b2b | complexity: Simple`

```
Write a cold email to [PROSPECT] introducing [PRODUCT].
Focus on the pain point of [PROBLEM] and propose a 15-min call.
```

---

## Research

...

---

## Duplicates
> Prompts flagged as near-duplicates. Review and keep one.

- "Summarise this document" ≈ "Give me a summary of this file" (similarity: high)

*(If none: "No duplicates detected.")*
```

**Field rules:**
- Each prompt's original text is preserved verbatim inside a code block — no edits
- Tags and complexity are on a single inline frontmatter line between the heading and the code block
- Template variables (`{{}}`, `[]`, `<>`) are kept as-is and the prompt is tagged `template`
- The Duplicates section is always present in the output

---

## Negative Cases

- **Empty input:** Respond — "No prompts found. Paste your prompts directly or attach a .md/.txt file." Do not generate output.
- **Unsupported file format (.docx, .xlsx, .pdf):** Respond — "Unsupported format. Please paste your prompts as plain text or upload a .md or .txt file." Do not generate output.
- **Input is a conversation log:** Respond — "This looks like a chat log, not a prompt collection. Paste the prompt texts you want to organise, or specify which lines are prompts."
