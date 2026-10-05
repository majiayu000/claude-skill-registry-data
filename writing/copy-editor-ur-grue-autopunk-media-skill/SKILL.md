---
name: copy-editor
description: "Copy-edit a piece of text for clarity, consistency, style, and readability — going beyond proofreading to tighten prose, improve sentence structure, and enforce consistent style throughout, while flagging substantive issues for the author's attention."
status: stable
category: editing
subcategory:
version: 1.0
eval_score: 5.0
tags: [editing, copy-editing, style, clarity, consistency, journalism, writing]
---
# Copy Editor

## What This Skill Does
Copy-edit a piece of text for clarity, consistency, style, and readability — going beyond proofreading to tighten prose, improve sentence structure, and enforce consistent style throughout, while flagging substantive issues for the author's attention.

## When To Use This Skill
- You have already proofread a draft and want a deeper editorial pass before publication
- You need to prepare copy for a specific publication context (news, long-form magazine, web, academic) and want it shaped accordingly
- You are working with content that has multiple authors and needs a consistent voice and style throughout
- You have received feedback that copy is "too wordy", "hard to follow", or "inconsistent in tone" and want targeted improvements
- You are editing translated or adapted copy that has been proofread but still reads unnaturally in English

## What You Need To Provide
**Required:** The text to edit; the publication context (news article, magazine feature, web, academic, broadcast script, newsletter).

**Optional:** House style guide reference or key style rules (e.g. "AP style", "sentence-case headings only", "no Oxford comma"); target reading level (general public, specialist, executive); specific concerns to address ("too many passive constructions", "inconsistent tense throughout", "paragraph three is unclear").

## How the Assistant Approaches This
1. Reads the full text for structure, flow, and recurring patterns before touching a word — identifies the main editorial issues (wordiness, tense inconsistency, passive-voice overuse, logical gaps, unclear attribution) rather than fixing sentence by sentence
2. Works paragraph by paragraph: tightens wordy constructions, ensures consistent tense and person, removes redundancies, and improves sentence rhythm — without changing the author's meaning or making substantive decisions (what to argue, what to conclude) that belong to the author
3. Flags substantive issues — unclear attribution, unsupported claims, logical leaps, missing context — in the editorial note rather than silently rewriting them, because these require author judgment
4. Returns the edited text plus a concise editorial note summarising the recurring patterns addressed and any substantive issues that need the author's attention

## Output Format
Two sections:

**Edited text** — the full text with all copy-editing changes applied. Changes are made inline; no track-changes markup unless the author requests it.

**Editorial note** — three to five bullet points (50–100 words total) summarising: (a) the recurring patterns found and addressed, (b) any substantive issues flagged for the author that were not silently edited, (c) any remaining concerns if the text would benefit from further work.

## Quality Criteria
- [ ] Prose is tighter and clearer without losing the author's distinctive voice
- [ ] Style is consistent throughout — tense, person, capitalisation, number format, and punctuation conventions do not shift mid-text
- [ ] Substantive issues (unattributed claims, logical gaps) are flagged in the editorial note, not silently rewritten
- [ ] The editorial note identifies patterns and recurring issues, not just a list of individual fixes
- [ ] No meaning has been changed without being flagged
- [ ] Readability is improved — shorter average sentence length, preference for active voice, concrete language over abstractions

## Example

### Input

**Text:**

> Streaming platforms are now offering original documentary content at a scale which was previously unthinkable, according to industry analysts. In the past, documentary filmmakers would have relied on broadcaster commissions in order to fund their projects. But the landscape had shifted. Three major platforms have increased their documentary budgets by an average of 40% over the last two years, data from a trade association shows. Filmmakers are now finding that the pitching process is becoming more competitive, and it was being noted by several producers who were interviewed for this piece that the approval cycles are getting longer. The question of whether this benefits independent filmmakers or primarily consolidates power in the hands of platform commissioning editors is one that remains deeply contested.

**Publication context:** Web, general audience

### Output

**Edited text:**

Streaming platforms are now commissioning original documentary content at a scale previously unthinkable, according to industry analysts. Traditionally, documentary filmmakers depended on broadcaster commissions to fund their work — but that landscape has changed. Three major platforms have increased their documentary budgets by an average of 40% over the past two years, according to trade association data.

The pitching process has grown more competitive. Several producers interviewed for this piece said approval cycles are getting longer. Whether this benefits independent filmmakers — or simply consolidates power in the hands of platform commissioning editors — remains contested.

---

**Editorial note:**

- **Tense inconsistency addressed:** The original mixed present and past tense within the same time frame. Standardised to present tense throughout.
- **Passive constructions reduced:** "it was being noted by several producers" and similar constructions converted to active voice.
- **Wordiness tightened:** Phrases such as "in order to fund", "at a scale which was previously", and "the question of whether" shortened without losing meaning.
- **Flag for author:** The 40% budget increase figure is attributed to "a trade association" without naming it. If the source can be named, doing so would strengthen the claim.

## Known Limitations
- Cannot enforce a specific publication's house style without seeing the style guide — style references like "AP style" or "Guardian style" are applied from general knowledge, which may differ from the publication's current internal guidelines.
- Makes judgment calls about voice preservation that may not match every editor's preference — some authors will find the edits too conservative, others too aggressive; the editorial note makes all significant changes transparent so the author can review them.
- Does not fact-check claims — unattributed or questionable claims are flagged in the editorial note, but verifying them is the author's responsibility.

## Related Skills
- [proofreader](../proofreader/SKILL.md)
- [tone-rewriter](../../writing/articles/tone-rewriter/SKILL.md)
- [paragraph-clarity-rewriter](../../writing/articles/paragraph-clarity-rewriter/SKILL.md)
