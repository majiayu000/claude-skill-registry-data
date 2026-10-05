---
name: terminology-consistency-checker
description: "Scans a text for inconsistent use of key terms, names, titles, and technical vocabulary, then produces a flagged report with recommended corrections."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, consistency, terminology, copy-editing, style]
---
# Terminology Consistency Checker

## What This Skill Does
Scans a text for inconsistent use of key terms, names, titles, and technical vocabulary, then produces a flagged report with recommended corrections.

## When To Use This Skill
- Before submitting a long-form article, feature, or investigation for publication
- When multiple writers or sources have contributed to a single piece and terminology may have drifted
- When an editor wants to enforce a house style or field-specific vocabulary standard (e.g., medical, legal, financial)
- When revisiting a draft after a long break and suspect terms have been used interchangeably

## What You Need To Provide
**Required:** The full text to be checked.
**Optional:** A preferred terminology list or house style glossary (e.g., "use 'climate change' not 'global warming'"); names of people or organisations whose styling should be standardised; target publication and its style guide (AP, Guardian, Chicago, etc.).

## How the Assistant Approaches This
1. Reads the full text and builds an internal inventory of every significant term, name, title, and proper noun it encounters — including all spelling variants and capitalisations.
2. Compares each term across its occurrences, flagging pairs or groups where the same referent is expressed differently (e.g., "the Minister" vs. "the minister" vs. "Minister Chen"; "AI" vs. "A.I." vs. "artificial intelligence" used interchangeably).
3. Produces a structured report: one entry per inconsistency, showing every variant found, the line-level location (quoted context), and a recommended single form to adopt throughout — with a brief reason where the choice isn't obvious.

## Output Format
A structured flagged report, organised into sections by type of inconsistency (names and titles / technical terms / abbreviations and acronyms / capitalisation). Each entry includes: the variants found, quoted context showing where each appears, the recommended standard form, and a one-line rationale. Closes with a summary count of total flags. Tone is editorial and precise — written for a copy editor, not a general reader. Length scales with the number of issues found; a clean text returns a short confirmation with zero flags.

## Quality Criteria
- [ ] Every flagged inconsistency is supported by at least two quoted examples from the text
- [ ] Each flag identifies a genuine inconsistency — not a stylistic choice or acceptable variation
- [ ] The recommended form is defensible (matches supplied glossary, named style guide, or common professional convention)
- [ ] No flags are raised for deliberate variation (e.g., pronoun alternation, direct quotes reproducing a source's own spelling)
- [ ] The report is complete: no inconsistency visible on a re-read should have been missed

## Example

### Input
Text to check:

---
The Secretary-General met with regional governors last Tuesday to discuss the emergency relief framework. She told reporters the government's response had been "swift and co-ordinated."

Later that day, Secretary General Amara Diallo addressed a press conference at the Department of Emergency Management. Officials from the Dept. of Emergency Management confirmed the timeline.

The 3-point plan — which the Secretary-General described as a "co-ordinated, swift response" — was drawn up by the DEM working group. A spokesperson for the Department said the framework would be reviewed in 90 days.

AI-assisted monitoring tools were deployed across six provinces. The artificial intelligence systems flagged three high-risk zones within 48 hours. An A.I. dashboard will provide real-time updates going forward.
---

Preferred style: AP Style. Treat "Secretary-General" as the correct title form.

### Output

**Terminology Consistency Report**
Text submitted: 4 paragraphs | Flags raised: 4

---

**1. Title: Secretary-General**
Variants found:
- "Secretary-General" (paragraphs 1 and 3) — recommended form
- "Secretary General" (paragraph 2, no hyphen)

Quoted context:
> "The Secretary-General met with regional governors…"
> "Secretary General Amara Diallo addressed a press conference…"

Recommendation: Use "Secretary-General" throughout (hyphenated). This matches your supplied preference and AP Style for hyphenated compound titles used before a name or standing alone.

---

**2. Organisation name: Department of Emergency Management**
Variants found:
- "Department of Emergency Management" (paragraphs 2 and 4) — recommended form
- "Dept. of Emergency Management" (paragraph 2)
- "DEM" (paragraph 3, undefined on first use)

Quoted context:
> "…at the Department of Emergency Management. Officials from the Dept. of Emergency Management confirmed…"
> "…drawn up by the DEM working group."

Recommendation: Use "Department of Emergency Management" on first reference, then "the Department" or "DEM" (introduced in parentheses after first use: "Department of Emergency Management (DEM)"). Do not mix "Dept." with the full name in the same paragraph.

---

**3. Hyphenation: co-ordinated**
Variants found:
- "co-ordinated" (paragraph 1, direct quote)
- "co-ordinated" (paragraph 3, paraphrase)

Note: These are consistent with each other. If your house style uses "coordinated" (no hyphen, per AP), both instances require correction. Flag is raised for style-guide alignment, not internal inconsistency.

Recommendation: AP Style uses "coordinated" (no hyphen). If both instances are outside direct quotes, change both. The instance in paragraph 1 is a direct quote — preserve the source's spelling there; correct the paraphrase in paragraph 3.

---

**4. Abbreviation: AI / A.I. / artificial intelligence**
Variants found:
- "AI" (paragraph 4, first sentence)
- "artificial intelligence" (paragraph 4, second sentence)
- "A.I." (paragraph 4, third sentence)

Quoted context:
> "AI-assisted monitoring tools were deployed…"
> "The artificial intelligence systems flagged…"
> "An A.I. dashboard will provide…"

Recommendation: AP Style: spell out "artificial intelligence" on first reference, then use "AI" (no periods) for all subsequent references. Remove "A.I." entirely.

---

**Summary:** 4 flags | 3 require corrections | 1 is a style-alignment note
Unambiguous internal inconsistencies: 2 (Secretary-General, AI variants)
Style-guide alignment issues: 2 (co-ordinated, DEM abbreviation handling)

## Known Limitations
- The assistant cannot flag inconsistencies it has no basis to resolve — if you do not supply a preferred form and no style guide is named, it will note the variants but may present multiple defensible options rather than a single recommendation.
- Direct quotes are treated as fixed text. The assistant will flag them for your awareness but will not recommend changing the wording inside quotation marks.
- For very long documents (10,000+ words), provide the text in sections to avoid missed flags near the end.
- The assistant does not have live access to subscription style guides (AP, Chicago, etc.). Recommendations for contested style questions are based on training data and may not reflect the most recent edition.

## Related Skills
- [house-style-enforcer](../../magazine-journalism/editing/house-style-enforcer/SKILL.md)
- [copy-editor-assistant](../../magazine-journalism/editing/copy-editor-assistant/SKILL.md)
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md)
