---
name: tone-consistency-checker
description: "Identifies passages where the tone or register shifts unexpectedly within a piece of writing, and explains how to bring the text back to a consistent voice."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, tone, register, voice, consistency, copy-editing]
---
# Tone Consistency Checker

## What This Skill Does
Identifies passages where the tone or register shifts unexpectedly within a piece of writing, and explains how to bring the text back to a consistent voice.

## When To Use This Skill
- After a draft has been written across multiple sessions and the voice may have drifted
- When multiple writers collaborated on a single article, script, or report and their individual styles are in conflict
- Before publishing a branded publication (newsletter, institutional report, podcast script) that must maintain a specific register throughout
- When an editor suspects a piece feels uneven but cannot pinpoint exactly where the problem lies

## What You Need To Provide
**Required:** The full text to be checked.
**Optional:** A description of the intended tone (e.g., "authoritative but accessible, like a quality broadsheet feature"; "warm and conversational, like a podcast host talking to a friend"; "neutral and precise, broadcast news style"); the publication or format this is written for; any passages the writer considers the tonal benchmark — the parts they are happiest with.

## How the Assistant Approaches This
1. Reads the entire text first to establish what the dominant tone appears to be — or, if a target tone description was provided, uses that as the reference standard. Notes vocabulary level, sentence rhythm, use of contractions, formality of address, emotional temperature, and use of first or second person.
2. Re-reads paragraph by paragraph, flagging any passage where one or more of those dimensions shifts sharply relative to the established baseline — a sudden use of jargon in a plain-language piece, an informal aside in a formal investigation, a shift from third-person reporting voice to first-person opinion.
3. Produces a structured report: each flagged passage is quoted in full, the tonal problem is named clearly in plain language, and a rewrite suggestion is provided so the editor can either adopt it or use it to prompt their own revision.

## Output Format
A structured editorial report divided into two parts. Part one: a one-paragraph tonal profile of the piece as it stands — what register it occupies, where it is working well. Part two: a numbered list of flagged passages, each with the quoted text, a plain-language description of the tonal issue, and an alternative version that brings the passage into line. Closes with one overall recommendation (e.g., "anchor to the register of paragraphs 3–5, which best match the stated brief"). Tone of the report is direct and editorial — not apologetic. Length reflects the number of flags: a tonally clean text gets a brief confirmation plus the tonal profile.

## Quality Criteria
- [ ] The tonal profile in part one accurately describes the dominant register of the text
- [ ] Each flagged passage has a specific, nameable reason for being flagged — not a vague sense that it "feels different"
- [ ] Rewrite suggestions preserve the meaning and factual content of the original passage
- [ ] No passages are flagged for stylistic variation that serves a clear editorial purpose (e.g., a deliberate shift to informal address in a sidebar, a quote that intentionally contrasts with the main voice)
- [ ] The overall recommendation is actionable — the editor knows exactly where to look for the tonal benchmark

## Example

### Input
Text to check:

---
**Paragraph 1:** The coastal flooding that swept through the delta region last month displaced more than 40,000 residents, overwhelming emergency shelters and exposing long-standing failures in the country's infrastructure planning.

**Paragraph 2:** Officials were, like, completely caught off guard — nobody had really thought this through, you know? The whole thing was kind of a mess from the start.

**Paragraph 3:** The government's emergency response unit deployed 1,200 personnel within 72 hours of the initial breach, prioritising evacuation of low-lying settlements identified as high-risk by the 2019 disaster preparedness review.

**Paragraph 4:** Here's the thing though: people are mad. Really mad. And honestly? You can't blame them. Years of broken promises, and now this.

**Paragraph 5:** Independent assessors from the regional development authority have submitted a formal findings report to the national legislature, recommending a structural audit of all coastal flood defences built before 2005.
---

Intended tone: Authoritative, neutral news feature — quality print journalism. Third-person throughout. The benchmark is paragraph 3, which the writer is confident about.

### Output

**Tonal Profile**
At its best — paragraphs 1, 3, and 5 — this piece occupies a confident, authoritative news-feature register: precise, third-person, factually grounded, with formal but readable sentence structures. The vocabulary is appropriate for a quality print audience without being academic. This is the register to protect.

---

**Flagged Passages**

**1. Paragraph 2 — Register collapse into casual speech**

Quoted text:
> "Officials were, like, completely caught off guard — nobody had really thought this through, you know? The whole thing was kind of a mess from the start."

Issue: This paragraph reads as informal spoken commentary, not print journalism. The markers "like," "you know," and "kind of a mess" belong to a conversational or opinion blog register. They undercut the authority established in paragraph 1.

Suggested revision:
> Officials acknowledged that the scale of the flooding had not been anticipated. Internal communications seen by this publication indicate that contingency planning for a surge of this magnitude had not been updated since 2017.

Note: If the informal register is a deliberate structural choice — e.g., this paragraph represents a paraphrased source perspective — that should be signalled to the reader ("Critics described the response as…" or "Residents affected said…").

---

**2. Paragraph 4 — Shift to first-person opinion**

Quoted text:
> "Here's the thing though: people are mad. Really mad. And honestly? You can't blame them. Years of broken promises, and now this."

Issue: This paragraph breaks from third-person reporting into direct editorial address ("Here's the thing," "honestly," "you can't blame them"). The emotional register — while defensible in a signed opinion column — contradicts the neutral news-feature framing of all other paragraphs. "And now this" is particularly informal and functions as a rhetorical aside rather than reported fact.

Suggested revision:
> Anger among displaced residents is widespread and, according to community organisers, more intense than after any previous flood event in the region. Many point to a pattern of unfulfilled commitments from local and national government spanning more than a decade.

---

**Overall Recommendation**
Use paragraphs 1, 3, and 5 as the tonal anchor throughout. Any passage that cannot be rewritten in the same register as paragraph 3 should be attributed to a named perspective (an official, a resident, an assessor) rather than presented as the narrator's voice. Two revisions required before this piece is tonally publishable.

## Known Limitations
- Tone is partly subjective. If you do not supply a target register or benchmark paragraph, the assistant will infer one from the text — and may infer it from passages that you consider the weaker parts.
- Deliberate tonal contrast used as a structural device (e.g., a journalist's personal aside in a first-person reported essay) may be flagged as an inconsistency. Provide context about the form so the assistant can distinguish intentional shifts from errors.
- This skill addresses register and voice. It does not check factual accuracy, grammar, or terminology — use the companion skills for those tasks.
- For long texts (10,000+ words), submit in sections of 2,000–3,000 words with the same target tone description repeated in each prompt, so the analysis remains consistent across sections.

## Related Skills
- [terminology-consistency-checker](../terminology-consistency-checker/SKILL.md)
- [copy-editor-assistant](../../magazine-journalism/editing/copy-editor-assistant/SKILL.md)
- [column-voice-adapter](../../magazine-journalism/writing/column-voice-adapter/SKILL.md)
- [house-style-enforcer](../../magazine-journalism/editing/house-style-enforcer/SKILL.md)
