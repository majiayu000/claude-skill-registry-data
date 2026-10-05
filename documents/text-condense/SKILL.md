---
name: text-condense
description: Condense rebuttal prose into fewer words without changing the original meaning. Use when a response block, paragraph, or selected passage is too long but all technical content, citations, and commitments must stay intact. Supports academic English.
tags: [Writing, Rebuttal, Condense, Concise, Polish]
version: 1.0.0
---

# Text Condense for Rebuttal Prose

> **RebuttalStudio Utility**
> Apply this skill when a selected passage is too long and needs to be tighter without changing what it says.

Condense the text by removing redundancy, filler, and repeated phrasing while preserving the original meaning, evidence, and technical content.

## Goal

Produce a shorter version of the selected text that says the same thing more efficiently.

## Rules

1. Preserve the original meaning exactly.
2. Remove filler, repetition, and unnecessary hedging.
3. Preserve all technical claims, numbers, citations, equations, named entities, and placeholder tokens.
4. Preserve reviewer quotations and structural labels if they appear.
5. Do not add new information, interpretations, promises, or evidence.
6. Do not change stance, polarity, or confidence level.
7. Keep the original paragraph, list, and markdown structure whenever possible.
8. If the text is already concise, make only minimal edits.

## Output

Return strict JSON:

```json
{ "text": "..." }
```

## Good Use Cases

- A Stage 2 response that repeats the same defense twice
- A Stage 3 response block that is clear but too long
- A Stage 4 follow-up answer that can be made tighter before submission
- A Stage 5 summary paragraph that needs a shorter version

## What Not to Change

- Technical substance
- Numerical values
- Citations
- Placeholder tokens such as `{{reviewerId}}`
- Reviewer comment labels such as `> **Reviewer's Comment**:` and `**Response**:`
