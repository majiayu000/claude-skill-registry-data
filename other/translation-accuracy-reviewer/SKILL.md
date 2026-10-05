---
name: translation-accuracy-reviewer
description: "Compares a source text against its translation, flags potential inaccuracies and mistranslations, and explains each issue so an editor can make an informed correction."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, translation, accuracy, localization, fact-checking, multilingual]
---
# Translation Accuracy Reviewer

## What This Skill Does
Compares a source text against its translation, flags potential inaccuracies and mistranslations, and explains each issue so an editor can make an informed correction.

## When To Use This Skill
- Before publishing a translated article, press release, interview transcript, or official statement
- When a machine translation (DeepL, Google Translate) has been used as a first draft and needs human-quality review
- When a freelance translation arrives and the editor is not fluent in the source language
- When a quoted source's words have been translated and accuracy is legally or editorially critical (court testimony, official denials, diplomatic statements)

## What You Need To Provide
**Required:** The original source text (any language) and the translated version side by side, with the source and target languages clearly labelled.
**Optional:** The publication context (news article, documentary subtitle, legal document, press release); the intended audience for the translation; any known sensitivities (e.g., "the source's phrasing on this point is politically significant"); a note on whether the translation should be literal or idiomatic.

## How the Assistant Approaches This
1. Reads the source text in full to understand its meaning, tone, register, and any culturally specific references or idioms before looking at the translation.
2. Works through the translation sentence by sentence against the source, flagging: omissions (content present in the source that is missing from the translation), additions (content in the translation with no basis in the source), mistranslations (words or phrases rendered inaccurately), register mismatches (source is formal, translation is casual, or vice versa), and cultural or idiomatic equivalence issues where a literal rendering distorts the intended meaning.
3. Produces a structured report: each flag is numbered, the source passage and translated passage are quoted together, the problem is named clearly in plain language, and a more accurate alternative is provided. Closes with an overall accuracy assessment.

## Output Format
A structured comparison report. Each entry shows: the source-language passage (quoted), the translated passage as submitted (quoted), the type of issue (omission / addition / mistranslation / register mismatch / idiomatic distortion), a plain-language explanation of what went wrong, and a suggested corrected translation. Entries are numbered and ordered as they appear in the text. Closes with a one-paragraph overall assessment: is this translation publishable with minor corrections, or does it require substantial rework? Tone is precise and editorial. The report is written entirely in English regardless of the source and target languages involved.

## Quality Criteria
- [ ] Every flag is supported by both the source quote and the translated quote placed side by side
- [ ] The type of issue is correctly identified — a mistranslation is not labelled an omission, and vice versa
- [ ] Suggested corrections are accurate to the source meaning and natural in the target language
- [ ] The report does not flag stylistic choices as errors when both the source and translation are internally consistent
- [ ] The overall assessment gives the editor a clear, actionable verdict on the translation's fitness for publication

## Example

### Input
Source language: Spanish
Target language: English (for publication)
Context: News article quoting a government minister at a press conference. Accuracy of the minister's words is editorially critical.

**Source (Spanish):**
> "No hemos tomado ninguna decisión definitiva sobre el cierre de la planta. Lo que sí puedo confirmar es que se están evaluando todas las opciones, incluyendo una posible reducción de la capacidad productiva, pero cualquier medida que se adopte será comunicada con anticipación a los trabajadores y sus representantes."

**Translation submitted:**
> "We have not made any decision about closing the plant. I can confirm that we are looking at all options, including possibly reducing production, and any measures will be communicated to workers."

### Output

**Translation Accuracy Report**
Source: Spanish | Target: English | Context: Ministerial press conference quote

---

**Flag 1 — Mistranslation: "ninguna decisión definitiva"**

Source:
> "No hemos tomado ninguna decisión definitiva sobre el cierre de la planta."

Translation submitted:
> "We have not made any decision about closing the plant."

Issue: Mistranslation — the word "definitiva" (final / definitive) has been dropped. The source says no *final* decision has been made, which implies that discussions or preliminary decisions may be underway. Removing "definitiva" makes the denial sound more absolute than it is — a significant difference in a politically sensitive context.

Suggested correction:
> "We have not made any final decision about closing the plant."

---

**Flag 2 — Register mismatch: "se están evaluando" (passive) → active voice shift**

Source:
> "Lo que sí puedo confirmar es que se están evaluando todas las opciones…"

Translation submitted:
> "I can confirm that we are looking at all options…"

Issue: Minor register shift. The source uses a formal Spanish passive construction ("all options are being evaluated") which creates slight distance between the minister and the evaluation process — a common device in official statements. "We are looking at" is more informal and makes the minister sound more personally involved. This is a defensible idiomatic choice for English, but flag it for editorial review given the political context.

Suggested correction (if literal register matters):
> "I can confirm that all options are being evaluated…"

---

**Flag 3 — Omission: "con anticipación a los trabajadores y sus representantes"**

Source:
> "…cualquier medida que se adopte será comunicada con anticipación a los trabajadores y sus representantes."

Translation submitted:
> "…any measures will be communicated to workers."

Issue: Omission. The source includes two elements absent from the translation: (1) "con anticipación" — the minister commits to communicating *in advance*, not merely at some point; and (2) "sus representantes" — union or worker representatives are explicitly included as recipients. Both are substantively meaningful commitments that the translation removes.

Suggested correction:
> "…any measures taken will be communicated in advance to workers and their representatives."

---

**Overall Assessment**
The translation is not publishable as submitted. It contains one significant mistranslation that softens a ministerial denial beyond what the source supports (Flag 1), and one omission that removes two specific commitments from the public record (Flag 3). The register shift in Flag 2 is a minor editorial judgement call. Corrections to Flags 1 and 3 are required before this quote can be printed accurately. Estimated revision time: under five minutes.

## Known Limitations
- The assistant's accuracy is strongest for widely spoken languages (Spanish, French, German, Portuguese, Mandarin, Arabic, Italian). For less common languages or regional dialects, treat the report as a starting point and have a specialist verify flagged passages.
- The assistant cannot assess stylistic nuance in languages it has less training data for — in those cases it will focus on factual accuracy and flag potential idiomatic issues rather than confirm them.
- This skill reviews accuracy against the source text. It does not assess whether the source text itself is accurate — for that, use fact-checking skills separately.
- Legal translations (contracts, court documents, depositions) require a certified human translator. This skill can support that process but must not replace it.
- Highly idiomatic or poetic language (song lyrics, proverbs, dialect speech) often has no single correct translation. In those cases the report will present options and note the trade-offs rather than a single recommendation.

## Related Skills
- [terminology-consistency-checker](../terminology-consistency-checker/SKILL.md)
- [dubbing-script-adapter](../../tv-documentary/localization/dubbing-script-adapter/SKILL.md)
- [subtitles-rewriter](../../tv-documentary/post-production/subtitles-rewriter/SKILL.md)
- [festival-synopsis-writer](../../tv-documentary/localization/festival-synopsis-writer/SKILL.md)
