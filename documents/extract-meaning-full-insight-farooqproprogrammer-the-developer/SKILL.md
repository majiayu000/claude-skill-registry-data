---
name: extract-meaning-full-insight
description: >
  Extract full meaning and structured insights from a user-provided document
  (PDF, DOCX, Markdown, text, notes, specs, transcripts). Use when the user
  asks to extract meaning, insights, themes, key points, or deep understanding
  from a document, or invokes /extract-meaning-full-insight.
---

# Extract meaning — full insight

Take a **document from the user**, then produce a structured insight pack. Do not invent content that is not grounded in the source.

## Inputs

Accept any of:

1. Attached / pasted file contents
2. A path in the workspace the user names
3. Pasted text in the chat

If no document is present, ask once: *“Please attach or paste the document (or give its path).”* Do not proceed without source text.

Prefer reading the file with tools when a path is given. For binary formats (PDF/DOCX), use available extractors in the environment; if extraction fails, say so and ask for pasted text or Markdown export.

## Process

```
Progress:
- [ ] 1. Obtain document text
- [ ] 2. Note genre, audience, and stated purpose (if any)
- [ ] 3. Extract claims, decisions, and open questions
- [ ] 4. Surface themes, tensions, and implications
- [ ] 5. Deliver insight pack (template below)
```

Rules:

- Quote or paraphrase tightly; mark uncertainty when the source is ambiguous.
- Separate **what the document says** from **inference**.
- Prefer completeness over brevity for decisions and action items.
- Do not rewrite the whole document unless asked.

## Output template

Use this structure:

```markdown
# Insight pack — <document title or filename>

## Source
- File / origin:
- Length / scope (pages, sections, or approx. words):
- Genre (spec, PRD, transcript, contract, notes, …):

## Core meaning (1 paragraph)
What this document is really about, in plain language.

## Key insights
1. …
2. …
3. …
(5–12 bullets; each insight = finding + why it matters)

## Claims & decisions
| Item | Type (claim / decision / assumption) | Evidence (section or quote cue) |
|------|--------------------------------------|----------------------------------|
| … | … | … |

## Themes
- …

## Tensions & risks
- Contradictions, gaps, or risks the text implies

## Open questions
- What the document does not settle

## Actionable takeaways
1. …
2. …

## One-line gist
<single sentence the user can reuse>
```

## Optional follow-ups

Only if the user asks:

- Executive summary (≤150 words)
- Stakeholder-specific brief (e.g. eng / product / legal)
- Diff of insights vs another document they provide
