---
name: scientific-style-polisher
description: Polish scientific manuscript text into clear, journal-ready English or Chinese while preserving meaning, evidence strength, statistics, references, and author voice. Use for 论文润色, SCI润色, 去AI味, humanize manuscript, abstract polish, discussion polish, cover letter polish, grammar/style improvement, or when text should sound natural without exaggerating the science.
---

# Scientific Style Polisher

## Purpose

Improve clarity, flow, concision, and academic tone without altering the underlying science. This skill is for language refinement, not content invention.

## Typical Inputs

- Manuscript titles, abstracts, introductions, results, discussions, limitations, or figure legends.
- Cover letters and short journal-facing summaries.
- Chinese or English scientific prose that needs a more natural academic style.

## Core Rules

- Preserve all numbers, statistics, references, figure/table references, gene names, drug names, database names, and technical abbreviations.
- Do not fabricate citations, data, methods, experiments, results, limitations, or clinical implications.
- Do not convert association, enrichment, or correlation into causation.
- Do not hide methodological weaknesses with polished language.
- Keep the author's intended meaning and evidence strength.
- Recommend final human review before submission.

## Workflow

1. Identify the manuscript section and target audience.
2. Detect whether the text needs light grammar cleanup, substantial style polishing, or claim-safety editing.
3. Preserve all technical tokens before rewriting.
4. Improve sentence structure, transitions, terminology consistency, and redundancy.
5. Replace generic AI-like phrasing with specific scientific wording.
6. Add a short risk note if the original text contains overclaims or unsupported statements.

## Preferred Language

Use cautious, defensible phrasing:

- "These findings support..."
- "This pattern is consistent with..."
- "The analysis suggests..."
- "A possible explanation is..."

Avoid unsupported certainty:

- "proves"
- "guarantees"
- "drives"
- "prevents"
- "is responsible for"
- "causal mechanism"

## Output Modes

Default output:

- Polished text only.

When the user asks for edit rationale:

- Polished text.
- Major edits.
- Claim-safety notes.

## Quality Checklist

- The science was not changed.
- No new references or results were added.
- Causal language is used only when evidence supports it.
- Terminology is consistent.
- The final text is ready for author review, not automatic submission.
