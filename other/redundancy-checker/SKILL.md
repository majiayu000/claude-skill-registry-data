---
name: redundancy-checker
description: "Scans a draft for repeated ideas, redundant phrases, and unnecessary word clusters, then delivers a flagged report and a tightened version of the text without altering meaning or voice."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, clarity, concision, repetition, wordcount]
---
# Redundancy Checker

## What This Skill Does
Scans a draft for repeated ideas, redundant phrases, and unnecessary word clusters, then delivers a flagged report and a tightened version of the text without altering meaning or voice.

## When To Use This Skill
- When a piece is over its word count and you need cuts that do not hurt the reporting
- When a reader or editor has said the copy "feels padded" or "goes in circles" but hasn't specified where
- Before submitting a long-form feature, investigation, or script to a commissioning editor for the first time
- When reviewing your own draft after time away and want a systematic redundancy audit rather than impressionistic re-reading

## What You Need To Provide
**Required:** The full text of the article, script, or document you want checked.
**Optional:** Target word count or percentage reduction goal; any sections marked as deliberately repetitive for rhetorical effect (a refrain in a documentary narration, for example) that should be left unchanged.

## How the Assistant Approaches This
1. Reads the entire text before flagging anything, building a map of ideas, arguments, and phrases to identify repetition across the whole piece, not just within individual sentences.
2. Identifies three types of redundancy: (a) **phrase-level** — word clusters where one word does the work of several (for example, "at this point in time" instead of "now"); (b) **sentence-level** — sentences that repeat information already established earlier; (c) **structural** — paragraphs or passages that circle back to a point already fully made without adding new information.
3. For each flag, notes the location, identifies what is being repeated or what words are surplus, and proposes a specific cut or rewrite. Where a rhetorical repetition is intentional and effective, the assistant notes it as a deliberate choice rather than flagging it for removal.
4. Produces a structured report followed by the full tightened text.

## Output Format
Two sections:

**Section 1 — Redundancy report:** A numbered list grouped by type (phrase-level / sentence-level / structural). Each entry shows the original text, the type of redundancy, and the proposed cut or rewrite. The report includes a word count before and after.

**Section 2 — Tightened text:** The full revised text with all accepted cuts applied, formatted identically to the original. No editorial commentary in this section — clean copy only.

A 600-word article typically produces 8–15 phrase-level flags, 2–5 sentence-level flags, and 0–2 structural flags.

## Quality Criteria
- [ ] No redundancy is flagged that would require changing the meaning of the text
- [ ] Every cut proposed is specific — not "this section is wordy" but the exact words to remove
- [ ] The tightened text reads as a complete, coherent draft, not a series of amputations
- [ ] Deliberate rhetorical repetition (anaphora, refrains, emphasis through restatement) is identified as intentional and not flagged for removal
- [ ] Word count before and after is clearly stated so the journalist can verify the reduction

## Example

### Input
The following is an excerpt from a 320-word draft news feature on urban cycling infrastructure. Target: tighten without losing any reporting.

> The city council announced yesterday that it will be making the decision to expand the existing network of cycle lanes in the downtown core area of the city. The announcement was made at a press conference held on Wednesday morning. Council members said that the expansion, which will be a significant expansion of the current infrastructure, is expected to be completed by the end of the coming year of 2026. The cycling advocacy group Pedal Forward said it was welcoming the news and called it a positive step forward in the right direction. However, critics and opponents of the plan have raised concerns about the fact that the construction work involved will cause disruption to traffic and will also cause disruption to local businesses in the area during the period of construction.

Word count: 142 words. Target: 100 words or fewer.

### Output

**Section 1 — Redundancy report**

**Phrase-level redundancies**

1. "will be making the decision to expand" → "will expand" — three surplus words. The decision is implied by the action.
2. "existing network of cycle lanes in the downtown core area of the city" → "cycle lane network in the downtown core" — "existing" and "of the city" are redundant context already clear from the story.
3. "The announcement was made at a press conference held on Wednesday morning" → cut entirely — the word "yesterday" in the opening sentence already establishes when; the press conference detail adds no new information already stated.
4. "which will be a significant expansion of the current infrastructure" → cut — restates "expand the existing network" from the sentence above.
5. "is expected to be completed by the end of the coming year of 2026" → "is expected to finish by end of 2026" — "coming year of" is redundant alongside the year itself.
6. "welcoming the news and called it a positive step forward in the right direction" → "welcomed the move" — "positive step forward in the right direction" is a cliche that adds no information.
7. "critics and opponents" → "critics" — the two words mean the same thing here.
8. "cause disruption to traffic and will also cause disruption to local businesses" → "disrupt traffic and local businesses" — the verb repetition and "also" are surplus.
9. "in the area during the period of construction" → "during construction" — "in the area" is already clear from context; "the period of" is padding.

**Sentence-level redundancies**

10. Sentence 2 ("The announcement was made...") — fully covered by "announced yesterday" in sentence 1. Proposed action: delete the sentence.

**Word count:** Before: 142. After applying all cuts: 92. Reduction: 35%.

---

**Section 2 — Tightened text**

The city council announced yesterday it will expand its cycle lane network in the downtown core. The expansion is expected to finish by end of 2026. Cycling advocacy group Pedal Forward welcomed the move. Critics, however, raised concerns that construction would disrupt traffic and local businesses.

## Known Limitations
- This skill does not evaluate whether the reporting itself is complete. It identifies surplus language, not missing information — those are different problems.
- Very dense technical or legal text (contracts, regulatory filings) may produce false flags where repetition is a structural requirement, not a stylistic weakness. Flag instructions before submitting that kind of document.
- Intentional stylistic choices — long sentences for rhythm, deliberate parallelism — may be flagged. The journalist should review all flags before accepting cuts.
- The tightened text in Section 2 applies all proposed cuts automatically. Always review Section 1 before using Section 2.

## Related Skills
- [passive-voice-checker](../../magazine-journalism/editing/passive-voice-checker/SKILL.md)
- [copy-editor](../copy-editor/SKILL.md)
- [structure-flow-checker](../structure-flow-checker/SKILL.md)
- [jargon-flagger](../../magazine-journalism/editing/jargon-flagger/SKILL.md)
