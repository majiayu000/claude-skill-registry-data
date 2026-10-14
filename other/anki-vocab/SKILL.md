---
name: anki-vocab
description: "Trigger: anki, vocab, vocabulary cards, vocabulario, tarjetas anki, learn vocab. Preview and export selected natural phrases for supplied target/native languages."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "2.0.0"
---

# Anki Vocab

## Activation

Prepare a selectable vocabulary batch for any supplied target/native language pair. A learning path, registry, named agent, and sibling skills are optional, never required.

## Inputs

Words, natural phrases, or a situation; target and native languages; optional known units and exported inventory. Ask for missing languages rather than infer a project. An explicit destination permits saving selected output; otherwise return it inline.

## Method

Use common natural phrases/chunks as anchors and full situational sentences, reusing supplied familiar material when useful. For a theme, propose a small batch (up to 12 initially); explicit user scope wins.

Separate candidates from exported rows. Compare duplicate keys using target-language tag plus Unicode NFKC normalization, lowercase, and collapsed whitespace. Preserve natural display text. Only already exported anchors in the supplied inventory are duplicates; unexported candidates remain eligible. Report the limits of an absent inventory.

Preview exact five-field rows before export. Let the learner select a subset, edit/reconfirm, postpone, or save none. Export only their unchanged selection. A candidate list is not approval. Export never creates an internal review item or a review date; learning or importing the phrase is always a separate, explicit learner activity.

Format plain UTF-8, one row per card, no header or quoting:

`unit;meaning;part of speech;example;native translation`

The unit, gloss, and example use the target language. The last field translates the full example into the native language. Forbid semicolons, double quotes, and newlines inside fields; rephrase and preview again when meaning changes. The example must naturally contain its anchor. `assets/batch-format.txt` is a format example, not a language default.

## Output

Return the selected batch inline or at the authorized destination, with row count, skipped exported duplicates, and proposed registry entries. The caller commits export and registry together; do not claim either from a draft. Export is separate from learner import into Anki (File > Import, separator `;`) and proves no mastery. No directory discovery, sibling calls, automatic registry writes, or Anki import.
