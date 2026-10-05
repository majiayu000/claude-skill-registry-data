---
name: quote-translator
description: "Translates individual quotes or quoted passages from one language to another, preserving the speaker's voice, intent, and attribution context while following target-language journalistic conventions."
status: stable
category: translation
subcategory: text
version: 1.0
eval_score: 4.39
tags: [translation, quotes, interviews, tone, nuance, attribution]
---
# Quote Translator

## What This Skill Does
Translates individual quotes or quoted passages from one language to another, preserving the speaker's voice, intent, and attribution context while following target-language journalistic conventions.

## When To Use This Skill
- You conducted an interview in one language and need to render the quotes in another for publication
- You are incorporating quotes from a foreign-language source into an English-language article (or vice versa)
- You need to present both the original-language quote and a faithful translation side by side for editorial review
- You have a transcript excerpt with multiple speakers and need all quoted passages translated consistently

## What You Need To Provide
**Required:** The quote(s) to translate; the source language; the target language; the speaker's name and role/title.

**Optional:** The context in which the quote was spoken (press conference, one-on-one interview, public speech, written statement); whether to present the original alongside the translation; the target publication's style for handling translated quotes (e.g., "use square brackets for translated material," "paraphrase unless the exact wording matters"); the speaker's typical register (formal official, casual conversational, academic).

## How the Assistant Approaches This
1. **Reads the full quote and its surrounding context.** Identifies the speaker's intent, emotional register, and rhetorical devices — sarcasm, understatement, emphasis, hedging — before selecting equivalent phrasing in the target language.

2. **Translates for meaning and voice, not word count.** A faithful quote translation captures what the speaker meant and how they said it. If the speaker was blunt, the translation is blunt. If they were evasive, the translation preserves the evasion. Literal translations that distort tone are avoided.

3. **Applies target-language attribution conventions.** Adjusts "said" placement, title formatting, and punctuation to match the target language's journalism standards. French quotes get guillemets and comma-separated attribution; German quotes get low-high quotation marks; English quotes use standard double quotation marks with attribution after the first natural clause break.

4. **Flags ambiguity and untranslatable elements.** If a word or phrase has no direct equivalent, or if the quote contains a pun, idiom, or cultural reference that does not survive translation, the assistant notes the issue and provides the closest alternative with an explanation.

5. **Provides dual-language format when requested.** If the user asks for original-plus-translation, presents them in a clean parallel format suitable for editorial review or publication as a bilingual excerpt.

## Output Format
Each translated quote presented with full attribution, formatted for the target language's journalistic conventions. If multiple quotes are provided, they appear in the order given. After all quotes, a "Translation Notes" section (2–5 bullet points) flags any significant choices — ambiguous phrasing, adapted idioms, or terms where the user should confirm the preferred rendering. Total output scales with input: one quote produces 3–5 lines plus notes; a batch of quotes produces a correspondingly longer document.

## Quality Criteria
- [ ] The translated quote preserves the speaker's intent — no meaning added, removed, or softened
- [ ] The speaker's register and emotional tone carry through (blunt stays blunt, cautious stays cautious)
- [ ] Attribution follows the target language's standard journalistic conventions
- [ ] Quotation mark style matches the target language (guillemets, low-high marks, double quotes, etc.)
- [ ] Idioms and cultural references are adapted rather than translated literally
- [ ] Translation notes flag every significant decision for editorial review
- [ ] If dual-language format is requested, both versions are clearly labeled and aligned

## Example

### Input
**Source language:** Spanish
**Target language:** English
**Speaker:** Elena Vargas, Director of Urban Planning, City of Maraverde (fictional)
**Context:** Press conference about a new waterfront development
**Register:** Formal official

**Quotes:**

1. "Este proyecto no es un regalo para los promotores inmobiliarios. Es una deuda que la ciudad tenia con sus vecinos del sur, y hoy empezamos a pagarla."

2. "No vamos a repetir los errores del paseo maritimo norte. Alli se construyo pensando en los turistas. Aqui se construye pensando en quien vive aqui todo el ano."

### Output

1. "This project is not a gift to property developers. It is a debt this city owed to its southern residents, and today we begin to repay it," said Elena Vargas, Director of Urban Planning for the City of Maraverde.

2. "We will not repeat the mistakes of the northern waterfront. That was built with tourists in mind. This is being built for the people who live here year-round," Vargas said.

---

**Translation Notes**
- "Vecinos del sur" translated as "southern residents" rather than the literal "southern neighbors" — in this municipal context, "vecinos" refers to registered residents of a district, not neighbors in the informal English sense.
- "Paseo maritimo norte" translated as "northern waterfront" rather than retained in Spanish. If the publication prefers to keep the Spanish place name with a gloss (e.g., "the Paseo Maritimo Norte, the northern waterfront"), this can be adjusted.
- "Se construyo pensando en los turistas" uses an impersonal passive in Spanish that deflects blame. The translation "that was built with tourists in mind" preserves this evasion — the speaker avoids naming who made the decision.

## Known Limitations
- The assistant cannot hear tone of voice, pauses, or emphasis. If the speaker's delivery is important to understanding the quote (e.g., sarcasm that is clear when spoken but ambiguous in print), provide a note about the delivery so the translation can account for it.
- For languages with significant dialectal variation (Arabic, Chinese, Spanish), the assistant defaults to the standard written register unless a specific dialect is requested. A quote from a speaker using regional slang may lose its colloquial texture in translation.
- Legal or regulatory quotes (court testimony, official depositions) require professional certified translation. This skill is designed for journalistic and editorial use, not legal proceedings.

## Related Skills
- [article-translator](../article-translator/SKILL.md) — translate a full article including embedded quotes
- [press-release-translator](../../institutional/press-release-translator/SKILL.md) — translate institutional quotes within press releases
- [translation-reviewer](../../quality/translation-reviewer/SKILL.md) — review a completed translation for accuracy
- [interview-transcript-editor](../../../magazine-journalism/writing/interview-transcript-editor/SKILL.md) — clean up raw interview transcripts before translation
