---
name: ste
description: Rewrite, review, or check text against ASD-STE100 (Simplified Technical English), the aerospace/defense controlled-language specification. Use when user asks to write, rewrite, or review text in "Simplified Technical English", "STE", or "ASD-STE100", asks to check a document for unapproved words or non-STE constructions, pastes technical or maintenance or procedural text and asks to simplify it for non-native English readers, or asks about STE dictionary approval status of a specific word.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Simplified Technical English (ASD-STE100)

Rewrite or review text so it follows the ASD-STE100 controlled-language
specification: a curated dictionary of ~3000 approved/unapproved words plus
53 writing rules across 9 sections.

This skill ships its own copy of the dictionary and rules extracted from the
official PDF — it does not rely on the model's approximate memory of STE.

## Reference files

- `reference/ste_dictionary.json` — ~3000 word entries. Each entry:
  `{"word": str, "pos": str, "approved": bool, "page": int, "alternatives": [{"meaning_alt": str, "approved_example": str, "not_approved": str}]}`.
  `approved: true` means the word is on the approved list; `false` means it's
  listed as unapproved with one or more suggested replacements.
- `reference/grammar-rules.md` — all 53 rules + 4 general recommendations
  (Sections 1–9: Words, Noun clusters, Verbs, Sentences, Procedural writing,
  Descriptive writing, Safety instructions, Punctuation and word counts,
  Writing practices), with the normative rule wording and one example each.
- `scripts/check_ste.py` — flags unapproved words in a text and prints
  suggested replacements, using the dictionary directly (no LLM guessing).
- `scripts/extract_ste_dictionary.py` — regenerates `ste_dictionary.json`
  from the source PDF if the spec is ever updated (uses `pdfplumber`, column
  positions calibrated to Issue 7 layout).

## Workflow

1. **Check first, don't guess.** Before flagging or replacing a word, run
   `check_ste.py` against the user's text (or look the word up directly in
   `ste_dictionary.json`) rather than relying on memorized STE vocabulary —
   the dictionary is the authority, not your training data.

   ```bash
   python3 skills/ste/scripts/check_ste.py <file>
   # or
   echo "some text" | python3 skills/ste/scripts/check_ste.py -
   ```

2. **Rewrite using suggested replacements**, but verify each substitution
   preserves meaning (per Rule 1.3/9.2 — never blind word-for-word swap if
   the sentence needs restructuring instead).

3. **Apply the writing rules** from `grammar-rules.md` relevant to the text
   type: procedural (instructions/steps) → Section 5 + 7 (safety); descriptive
   (system/theory of operation) → Section 6; any text → Sections 2–4 and 8–9
   for noun clusters, verb tense, sentence length, punctuation.

4. **Note technical names/verbs as an exception**: STE explicitly allows
   words outside the dictionary if they qualify as a "technical name" (19
   categories, Rule 1.5) or "technical verb" (4 categories, Rule 1.12) — see
   Section 1 in `grammar-rules.md`. Don't flag those as errors.

5. **When reviewing** (not rewriting), report each unapproved word with its
   dictionary-approved alternative and cite the rule number if a structural
   issue applies (e.g., noun cluster too long → Rule 2.1).

## Known limitation

A handful of multi-sense dictionary entries (words with numbered senses like
"1. ... 2. ..." packed in one table cell — e.g. BOND, ABSORB) have slightly
garbled `alternatives` text due to PDF table extraction quirks. If a
suggestion looks garbled, cross-check that specific word against the PDF
directly rather than trusting the JSON blindly.
