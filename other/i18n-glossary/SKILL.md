---
name: i18n-glossary
version: 1.0.0
description: Build a bilingual terminology glossary and style guide that enforces consistency across a translation project.
author: matrixx0070
tags: [glossary, terminology, style-guide, consistency]
capabilities: []
---

## When to use

Use this at the start of any multi-document or multi-translator project, or when you notice a term rendered inconsistently. The glossary fixes the approved target-language equivalent for each key term, plus do-not-translate lists and style rules (tone, capitalization, punctuation), so every downstream translation stays consistent.

**Not for:** translating running prose (use `i18n-translate`), locale formatting (use `i18n-localize`), tone shifts (use `i18n-tone-adapt`), or subtitles (use `i18n-subtitle`).

## Method

1. Harvest candidate terms: product names, features, recurring domain jargon, UI labels, legal terms, and anything a wrong translation would confuse.
2. For each term, decide status. Decision point: TRANSLATE (with the single approved equivalent), DO-NOT-TRANSLATE (brand/code), or FORBIDDEN (renderings to avoid).
3. Record part of speech, gender/plural where the target language needs it, and a one-line usage note or example.
4. Add style rules: preferred register, capitalization conventions, quotation-mark style, number formatting, Oxford-comma policy, spacing (e.g. French non-breaking space before `:`).
5. Decision point: when two valid equivalents exist, pick one as canonical and list the other under "avoid" to prevent drift.
6. Version the glossary and note the date; treat it as the source of truth reviewers check against.

## Example

Project: SaaS dashboard, en → de.

| Source | Approved (de) | Status | Note |
|---|---|---|---|
| Dashboard | Dashboard | Do-not-translate | Anglicism accepted in market |
| Sign in | Anmelden | Translate | Not "Einloggen" |
| Workspace | Arbeitsbereich | Translate | n., m. |
| Boost | — | Forbidden literal | Use "Verstärken", never "Boosten" |

Style rule: address the user with formal "Sie", not "du".

## Pitfalls

- **Multiple equivalents in the wild.** Without a canonical choice, three translators produce three words for one feature.
- **No do-not-translate list.** Brand names and code identifiers get "helpfully" translated.
- **Missing grammatical metadata.** Omitting gender/plural forces guesswork in gendered languages.
- **Static and unversioned.** A glossary nobody updates or dates silently rots as the product changes.

## Output format

```
Project: <name>   Pair: <src> → <tgt>   Version: 1.0 (<date>)

## Terminology
| Source | Approved target | Status | POS/gender | Note |
|--------|-----------------|--------|-----------|------|

## Do-not-translate
- <term>

## Style rules
- Register: <...>
- Capitalization: <...>
- Punctuation/spacing: <...>
```
