---
name: unattributed-claims-checker
description: "Reads a draft article or script and flags every assertion of fact that lacks a named source, adding an inline `[NEEDS SOURCE]` marker so editors can see exactly where attribution is missing."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [attribution, fact-checking, sourcing, editing, journalism]
---
# Unattributed Claims Checker

## What This Skill Does
Reads a draft article or script and flags every assertion of fact that lacks a named source, adding an inline `[NEEDS SOURCE]` marker so editors can see exactly where attribution is missing.

## When To Use This Skill
- Before you send a draft to a senior editor or legal review
- When a piece has had multiple authors and sourcing discipline may be inconsistent
- Any time you want a quick audit of a draft before publication or broadcast
- When preparing an article that involves serious allegations, statistics, or expert claims

## What You Need To Provide
**Required:** The full text of the draft — paste it directly into your message.
**Optional:** A note about which claims are already known to have internal documentation (e.g., "the unemployment figures in paragraph 3 come from a government data release we have on file"). This prevents the assistant from flagging things you have already verified off-page.

## How the Assistant Approaches This
1. Reads the draft sentence by sentence and identifies every declarative claim — statistics, allegations, descriptions of events, characterisations of individuals or organisations, and predictions stated as fact.
2. Checks whether each claim is clearly attributed to a named or sufficiently identified source (e.g., a person, institution, document, or data release) either within the sentence or in the immediately surrounding context.
3. Appends `[NEEDS SOURCE]` directly after any claim that lacks attribution, then returns the full annotated draft so you can see every flag in context. It also produces a numbered list of flagged claims at the end, so you can work through them without scrolling the whole piece.

## Output Format
- The complete draft returned with `[NEEDS SOURCE]` inserted inline after each flagged claim — no other text is altered.
- A numbered summary list beneath the draft: one line per flagged claim, quoting the flagged phrase and briefly explaining what type of attribution is missing (named source, official data, on-the-record quote, etc.).
- Tone is neutral and editorial — no suggestions for how to find the source, no rewrites.
- Length of output equals the draft length plus the summary list.

## Quality Criteria
- [ ] Every unattributed claim in the draft receives a `[NEEDS SOURCE]` marker — nothing is missed.
- [ ] No correctly attributed claim is flagged (no false positives on quotations, named sources, or clearly identified data).
- [ ] The original wording of the draft is preserved exactly — the only additions are the `[NEEDS SOURCE]` tags.
- [ ] The numbered summary list matches the inline flags precisely — no extra entries, no omissions.
- [ ] The summary description for each flagged item clearly states what kind of attribution is missing.

## Example

### Input

The unemployment rate rose sharply in the third quarter, driven mainly by layoffs in the manufacturing sector. Consumer confidence is now at its lowest point in five years. Regional governments have struggled to respond adequately, and several have been accused of suppressing local data.

"We are seeing real hardship on the ground," said Dr. Amara Osei, an economist at the National Institute for Economic Research. "The recovery has stalled in every metric we track."

Housing costs in the capital remain 40 percent above the national average, a situation that disproportionately affects young workers. The government has privately acknowledged that its housing strategy has failed, according to two officials familiar with internal discussions.

### Output

The unemployment rate rose sharply in the third quarter, driven mainly by layoffs in the manufacturing sector. [NEEDS SOURCE] Consumer confidence is now at its lowest point in five years. [NEEDS SOURCE] Regional governments have struggled to respond adequately, and several have been accused of suppressing local data. [NEEDS SOURCE]

"We are seeing real hardship on the ground," said Dr. Amara Osei, an economist at the National Institute for Economic Research. "The recovery has stalled in every metric we track."

Housing costs in the capital remain 40 percent above the national average, [NEEDS SOURCE] a situation that disproportionately affects young workers. [NEEDS SOURCE] The government has privately acknowledged that its housing strategy has failed, according to two officials familiar with internal discussions.

---

**Flagged claims — 5 items requiring attribution:**

1. "The unemployment rate rose sharply in the third quarter, driven mainly by layoffs in the manufacturing sector." — Needs a named data source (e.g., national statistics office, labour ministry report).
2. "Consumer confidence is now at its lowest point in five years." — Needs a named index or survey source with a date.
3. "Several [regional governments] have been accused of suppressing local data." — Needs an on-the-record source or document; anonymous accusation as stated is legally exposed.
4. "Housing costs in the capital remain 40 percent above the national average." — Needs a named data source (e.g., housing authority, real estate index).
5. "A situation that disproportionately affects young workers." — Needs supporting data or a named source making this assessment.

*The attribution from "two officials familiar with internal discussions" in the final sentence is noted but flagged as anonymous — verify your editorial policy permits unnamed sourcing here before publication.*

## Known Limitations
- The assistant cannot verify whether an attribution is accurate, only whether one is present. A quote attributed to a real-sounding name still passes the check even if the person does not exist — this skill audits form, not truthfulness.
- In densely reported passages where attribution is implied by context across multiple paragraphs (e.g., an extended interview), the assistant may flag claims that are implicitly covered by an earlier attribution. Review flagged items in full context before acting.
- Opinion columns and explicitly labelled commentary may produce a high false-positive rate, since analytical assertions in opinion pieces do not always require sourcing by convention. Consider noting the piece type in your prompt.

## Related Skills
- [libel-risk-checker](../libel-risk-checker/SKILL.md)
- [fact-check-prompt](../../magazine-journalism/editing/fact-check-prompt/SKILL.md)
- [copy-editor](../copy-editor/SKILL.md)
