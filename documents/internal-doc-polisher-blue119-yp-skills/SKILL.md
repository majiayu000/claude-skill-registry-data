---
name: internal-doc-polisher
description: Transform raw or transcript-like text into a polished Markdown document for internal sharing. Use when the user provides a text file (any mix of zh_tw, zh_cn, or en) and wants sentence repair, structured headings, concise paragraphs, a 3–7 bullet summary, and an Action Items section when tasks are mentioned.
---

# Internal Doc Polisher

## Overview
Turn unstructured text into a clean Markdown document with repaired sentences, clear sections, and an executive summary. Preserve meaning, keep language consistent with the source, and output a `.md` file.

## Workflow

### 1) Intake
- Ask for the input file path if not provided.
- Accept any text file containing zh_tw, zh_cn, or en (mixed language is fine).
- Ask for an output path if the user specifies one; otherwise default to `<input_basename>.polished.md` in the same directory.

### 2) Repair And Clean
- Fix fragments, grammar, and punctuation without changing meaning.
- Remove obvious speech artifacts (stutters, repeated fillers) when they do not change intent.
- Keep proper nouns, numbers, and domain terms intact.
- Normalize spacing rules for the dominant language:
  - zh: no extra spaces between Chinese characters; keep English/number tokens spaced.
  - en: standard English spacing and punctuation.

### 3) Restructure
- Create clear headings (`##`, `###`) that match the content flow.
- Group related content into concise paragraphs.
- Convert list-like text into bullets.
- Keep the document in the same language as the source unless the user requests translation.

### 4) Add Summary
- Add a summary section at the beginning with 3–7 bullets.
- Cover key points, outcomes, risks, and action items.
- Keep bullets short and specific.

### 5) Action Items
- If tasks or next steps are mentioned, add an `## Action Items` section.
- Convert tasks into bullet points; keep owners/dates if present.

### 6) Output
- Write the final result to the requested `.md` file.
- Confirm the output path in the response.

## Output Template
Use this structure, adjusting headings to fit the content:

```markdown
- Summary bullet 1
- Summary bullet 2
- Summary bullet 3

## Section Title
Concise paragraph.

### Subsection Title
- Bullet
- Bullet

## Action Items
- Task 1
- Task 2
```
