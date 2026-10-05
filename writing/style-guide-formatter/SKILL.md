---
name: style-guide-formatter
description: "Applies a named style guide — AP, Chicago, or a custom house style — to a manuscript, flagging and correcting capitalisation, punctuation, number formatting, abbreviations, and usage inconsistencies throughout."
status: stable
category: production-support
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [style-guide, copy-editing, formatting, AP, Chicago, house-style]
---
# Style Guide Formatter

## What This Skill Does
Applies a named style guide — AP, Chicago, or a custom house style — to a manuscript, flagging and correcting capitalisation, punctuation, number formatting, abbreviations, and usage inconsistencies throughout.

## When To Use This Skill
- A writer has submitted copy that doesn't match your publication's style
- You are preparing a draft for copy-edit and want a first-pass clean before a human editor reads it
- You are switching a piece originally written for one outlet to a different outlet with different style rules
- A contributor has used mixed conventions (sometimes AP, sometimes their own preferences) within the same article

## What You Need To Provide
**Required:** The full draft text you want formatted. The name of the target style guide (AP, Chicago, or "house style").
**Optional:** Your house style sheet as a list of rules — essential if you choose "house style." Specific problem areas to prioritise (e.g., "we always spell out percent, never use the % symbol"). Any words or names that should be treated as exceptions (proper nouns, brand names with unusual capitalisation).

## How the Assistant Approaches This
1. Identify the target style and load its conventions — number thresholds, title case rules, Oxford comma policy, date formats, abbreviation standards, and punctuation around quotes.
2. Read through the manuscript systematically, flagging every deviation from the target style, including inconsistencies within the text itself (e.g., "healthcare" in paragraph two, "health care" in paragraph seven).
3. Apply corrections and return the revised text with an annotated change log: each change listed as a numbered note showing what was changed, where, and which rule it follows — so the editor can accept or override each decision.

## Output Format
Two sections: (1) the fully formatted manuscript, ready to hand to a layout editor; (2) a numbered change log in plain English, grouped by category (capitalisation, numbers, punctuation, abbreviations, word choice). Change log entries are brief — one line each. Total length scales with the source manuscript. No editorial commentary on content — only style-level changes.

## Quality Criteria
- [ ] Every flagged change cites a specific rule, not a vague preference
- [ ] The manuscript text itself is altered — not just annotated
- [ ] Proper nouns and brand names provided by the user are left untouched
- [ ] Changes are confined to style and formatting — no rewriting of sentences
- [ ] The change log is complete: nothing is silently altered without appearing in the log

## Example

### Input
**Style guide:** AP

**Manuscript:**
> The Prime Minister announced on Tuesday, March 4th, that 3 new hospitals would be built before 2030. The Health Minister, Dr. Jane Ellsworth, said the investment — totalling $4.2 billion dollars — would create more than 11,000 jobs.
>
> "We are committed to fixing healthcare," Ellsworth said. "This is the single biggest investment in health-care infrastructure in 40 years."
>
> The announcement came after months of pressure from the British Medical Association (BMA). The BMA has called for increased funding since January, 2022.

### Output
**Formatted manuscript (AP style):**

> The prime minister announced Tuesday that three new hospitals would be built before 2030. Health Minister Jane Ellsworth said the investment — totaling $4.2 billion — would create more than 11,000 jobs.
>
> "We are committed to fixing health care," Ellsworth said. "This is the single biggest investment in health care infrastructure in 40 years."
>
> The announcement came after months of pressure from the British Medical Association. The BMA has called for increased funding since January 2022.

---

**Change log:**

1. "Prime Minister" → "prime minister" — AP lowercases titles not used directly before a name.
2. "Tuesday, March 4th" → "Tuesday" — AP omits the date when the day of the week is given and the date adds no essential information. (If the specific date is editorially important, restore "March 4" without the ordinal suffix.)
3. "3 new hospitals" → "three new hospitals" — AP spells out whole numbers below 10.
4. "The Health Minister, Dr. Jane Ellsworth" → "Health Minister Jane Ellsworth" — AP drops the courtesy title Dr. for non-medical contexts; title used directly before name, no comma.
5. "$4.2 billion dollars" → "$4.2 billion" — "dollars" is redundant after the $ symbol.
6. "totalling" → "totaling" — AP follows American English spelling.
7. "healthcare" (first instance) → "health care" — AP style: two words.
8. "health-care infrastructure" → "health care infrastructure" — AP does not hyphenate "health care" as a modifier before a noun.
9. "(BMA)" → removed on first reference — AP does not require parenthetical abbreviation when the full name is not repeated in close proximity; BMA is reintroduced naturally in the following sentence.
10. "January, 2022" → "January 2022" — AP omits the comma between month and year when no day is given.

## Known Limitations
- Custom house style rules must be provided explicitly — the assistant cannot infer unstated conventions from context alone. The more complete your house style sheet, the more accurate the output.
- Highly technical or scientific manuscripts (with discipline-specific notation, units, or citation formats) may need a specialist copy editor for elements outside the named style guide's scope.
- This skill corrects style, not grammar or factual accuracy. A human copy editor should still review content-level issues.
- AP and Chicago evolve; conventions here reflect widely accepted current practice but may lag the latest printed edition for niche rulings.

## Related Skills
- [footnotes-formatter](../footnotes-formatter/SKILL.md)
- [print-web-reformatter](../print-web-reformatter/SKILL.md)
- [transcript-qa-formatter](../transcript-qa-formatter/SKILL.md)
