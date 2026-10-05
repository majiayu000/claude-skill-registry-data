---
name: proofreader
description: "Proofread a piece of text and return it with all spelling, grammar, punctuation, and typographical errors corrected — preserving the author's voice and intentional style choices throughout."
status: stable
category: editing
subcategory:
version: 1.0
eval_score: 5.0
tags: [editing, proofreading, grammar, spelling, punctuation, journalism, quality]
---
# Proofreader

## What This Skill Does
Proofread a piece of text and return it with all spelling, grammar, punctuation, and typographical errors corrected — preserving the author's voice and intentional style choices throughout.

## When To Use This Skill
- You are doing a final check before publishing an article, caption, press release, or broadcast script
- You need to verify that translated or adapted copy has not introduced language errors during revision
- You are reviewing user-generated or community-submitted content before it goes live
- You have written a draft quickly under deadline and want a clean error pass before sending to an editor
- You need to check headlines, subheadings, pull quotes, or captions that are often missed in a full-document proofread

## What You Need To Provide
**Required:** The text to proofread.

**Optional:** Language variant (British English, American English, Australian English — defaults to British English if not specified); house style notes (e.g. "Oxford comma: yes", "spell out numbers under ten", "capitalise 'Government' when referring to the UK Government"); whether to flag style choices for review rather than correcting them silently.

## How the Assistant Approaches This
1. Reads the full text for meaning before making any corrections — understanding the author's intent, register, and deliberate style choices (sentence fragments for effect, informal voice, rule-breaking for emphasis)
2. Makes a correction pass for spelling errors, grammatical mistakes, punctuation errors, and typographical issues (doubled words, missing words, transposed letters), distinguishing between genuine errors and intentional stylistic decisions
3. Returns the corrected text in full, followed by a numbered change log listing every correction made — the original, the corrected version, and the reason — so the author can review and accept or reject each change individually

## Output Format
Two sections:

**Corrected text** — the full text with all errors fixed. No annotations or markup in the text itself unless track-changes format was requested.

**Change log** — a numbered list. Each entry contains: (1) the original text with the error, (2) the corrected version, (3) the reason in plain language. If no errors are found, states "No corrections needed" followed by a one-sentence confirmation of what was checked (word count, language variant, any house style notes applied).

## Quality Criteria
- [ ] Every correction in the change log corresponds to an actual change in the corrected text — no phantom corrections
- [ ] Intentional style choices (fragments, informal register, deliberate repetition) are preserved and not "corrected"
- [ ] No new errors have been introduced during the correction process
- [ ] The author's voice is unchanged — the corrected text reads as the author's work, not a rewrite
- [ ] Corrections follow the specified language variant (e.g. "realise" not "realize" in British English)
- [ ] House style rules, if provided, are applied consistently throughout

## Example

### Input

Text to proofread:

> The committee announced it's findings on wednesday, confirming that three seperate departments had failed to meet there targets for the second consecutive quarter. "We are deeply dissapointed," said the chair, who declined to names the departments publicly. Each of the department heads were given 30 days to submit a improvement plan.

Language variant: British English
House style: Spell out numbers under ten. Oxford comma: yes.

### Output

**Corrected text:**

The committee announced its findings on Wednesday, confirming that three separate departments had failed to meet their targets for the second consecutive quarter. "We are deeply disappointed," said the chair, who declined to name the departments publicly. Each of the department heads was given 30 days to submit an improvement plan.

---

**Change log:**

1. **"it's findings"** → **"its findings"** — "it's" is a contraction of "it is"; the possessive form has no apostrophe.
2. **"wednesday"** → **"Wednesday"** — Days of the week are capitalised in English.
3. **"seperate"** → **"separate"** — Spelling error.
4. **"there targets"** → **"their targets"** — Wrong homophone; "their" is the possessive pronoun.
5. **"dissapointed"** → **"disappointed"** — Spelling error (doubled 's').
6. **"to names"** → **"to name"** — Verb form error; infinitive required after "declined to".
7. **"Each of the department heads were"** → **"Each of the department heads was"** — Subject-verb agreement: "each" takes a singular verb.
8. **"a improvement"** → **"an improvement"** — The indefinite article "an" is required before a vowel sound.

*Note: "30 days" retained as a numeral — house style specifies spelling out numbers under ten, and 30 falls above that threshold.*

## Known Limitations
- Cannot reliably detect errors in specialised terminology (medical, legal, scientific, technical) without additional context — incorrect technical terms may be left uncorrected if they appear plausible.
- May flag or "correct" intentional informal register in opinion pieces, columns, or personality-driven writing unless explicitly told the register is deliberate.
- Does not check factual accuracy — a sentence can be grammatically perfect and factually wrong; this skill addresses language mechanics only.

## Related Skills
- [copy-editor](../copy-editor/SKILL.md)
- [passive-voice-checker](../../magazine-journalism/editing/passive-voice-checker/SKILL.md)
- [jargon-flagger](../../magazine-journalism/editing/jargon-flagger/SKILL.md)
