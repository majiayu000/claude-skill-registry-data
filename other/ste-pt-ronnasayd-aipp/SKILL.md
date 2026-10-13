---
name: ste-pt
description: Rewrite, review, or check Portuguese text against ASD-STE100 (Simplified Technical English) by translating through English and back, delegating the actual rule and dictionary checking to the `ste` skill. Use when user asks to check or rewrite Portuguese text against "STE" or "ASD-STE100" and wants the final result in Portuguese.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# STE for Portuguese text (translation wrapper)

No official ASD-STE100 dictionary/spec exists in Portuguese — the
standard is English-only. This skill does not invent a Portuguese
dictionary. Instead it wraps the real `ste`
skill with a translate-out / translate-back step.

## Workflow

1. **Translate PT → EN.** Produce a faithful English translation of the
   user's Portuguese text. Keep a mental (or written) mapping of key terms
   so back-translation stays consistent.

2. **Run the real skill.** Invoke `ste` on the
   English translation — check against `ste_dictionary.json` via
   `check_ste.py`, apply `grammar-rules.md`. Never skip this step or
   approximate STE rules from memory.

3. **Translate EN → PT.** Translate the STE-compliant English result back
   to Portuguese, preserving the simplified structure (short sentences,
   one action per sentence, active voice, controlled vocabulary) as much
   as Portuguese grammar allows.

4. **Verify round-trip fidelity.** Compare final Portuguese against the
   original for meaning drift. Flag any place where translation forced a
   meaning change (e.g., an approved-word substitution that doesn't have
   a clean PT equivalent).

5. **When reviewing (not rewriting)**, report findings in Portuguese, but
   cite the original English unapproved word + STE rule number so the
   user can verify against the real spec.

## Notes

- If the user only wants a compliance check (not a rewrite), still
  translate to English first — `check_ste.py` only understands English
  text.
- Technical names/verbs exception (Rule 1.5/1.12) applies to the English
  intermediate text, not the Portuguese original.
