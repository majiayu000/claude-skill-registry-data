---
name: i18n-translate
version: 1.0.0
description: Translate text faithfully into a target language while preserving meaning, register, and intent.
author: matrixx0070
tags: [translation, i18n, language, fidelity]
capabilities: []
---

## When to use

Use this when you need a target-language rendering that a native reader would accept as natural, while keeping the source's meaning, register, and intent intact. Ideal for documents, UI strings, emails, marketing copy, and technical prose where accuracy and tone both matter.

**Not for:** deep cultural adaptation of units/dates/idioms (use `i18n-localize`), building reusable term lists (use `i18n-glossary`), reshaping formality for a new audience (use `i18n-tone-adapt`), or time-coded captions (use `i18n-subtitle`).

## Method

1. Identify source and target languages, and the domain (legal, medical, casual, technical). If the target locale is ambiguous (e.g. "Spanish"), default to the most widely understood variant and label it an assumption.
2. Read the whole source first. Note register (formal/informal), voice (active/passive), and any terms of art.
3. Translate for meaning, not word-for-word. Decision point: if a literal rendering distorts meaning, prefer the idiomatic equivalent and flag it.
4. Preserve non-translatables: proper nouns, code, placeholders (`{name}`, `%s`), URLs, numbers, and trademarks. Never translate inside code or variables.
5. Decision point: if a term is ambiguous or untranslatable, pick the best fit and add a translator note rather than silently guessing.
6. Self-review: back-translate mentally and check that no clause was dropped, added, or softened.

## Example

Source (EN, support email): "We're sorry for the hiccup — your refund of {amount} is on its way."

Poor (literal FR): "Nous sommes désolés pour le hoquet — votre remboursement de {amount} est en route." ("hoquet" = the bodily hiccup — wrong.)

Good (FR): "Toutes nos excuses pour ce désagrément — votre remboursement de {amount} est en cours de traitement."

Note: rendered the idiom "hiccup" as "désagrément"; kept `{amount}` placeholder intact; matched the apologetic-but-professional register.

## Pitfalls

- **Literal idiom translation.** Rendering figures of speech word-for-word produces nonsense; translate the meaning.
- **Register drift.** A formal contract turned casual (or vice versa) changes the document's legal or emotional weight.
- **Breaking placeholders.** Translating or reordering `{var}`/`%s` without care corrupts runtime output.
- **Silent omission or padding.** Dropping a hedge ("may") or adding emphasis the source lacked changes commitment level.

## Output format

```
Source language: <lang>
Target language: <lang/locale>   [assumption: <if inferred>]
Register: <formal | neutral | informal>

--- Translation ---
<translated text, placeholders preserved>

--- Translator notes ---
- <term/choice>: <why>
```
