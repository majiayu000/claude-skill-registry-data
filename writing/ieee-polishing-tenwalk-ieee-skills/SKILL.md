---
name: ieee-polishing
description: >-
  Polish academic prose to IEEE-journal style at the sentence level — clarity, sentence length,
  section-appropriate tense, calibrated hedging, US English, acronym discipline,
  numbered-citation phrasing, and unit/number formatting. Also translate Chinese drafts into
  IEEE-style English. Use this whenever the user wants to "polish", "proofread", "improve the
  English", "make it publishable / native", "fix the grammar", "润色", "改成地道英文", "改成投稿级" on
  existing text. Tuned for IEEE communications papers (per-section tense for system model /
  problem formulation / proposed solution / numerical results). For building or restructuring the
  argument and sections, use ieee-writing instead.
---

# IEEE-Style Language Polishing

Use this skill to bring **existing** sentences to IEEE journal standard. If the text needs its
argument or structure rebuilt, use `ieee-writing` first, then polish here.

## Core stance

- **Preserve meaning; never add claims.** Polishing changes wording, not facts. Do not introduce
  numbers, citations, or assertions the author did not make.
- **Clarity over elegance.** A plain, precise sentence beats an ornate one. IEEE values
  verifiable clarity, not literary flair.
- **US English by default** (IEEE house style): `color`, `analyze`, `modeling`, `behavior`,
  `optimize`, `center`, `fiber`. (This is the opposite of Nature's British spelling.)
- **Calibrate claim strength to evidence** (see hedging ladder below).
- **Return plain, copy-pasteable text.** Do not wrap output in commentary the user must strip out.

## When to open extra files

| File | Open when |
|---|---|
| [references/sentence-and-style.md](references/sentence-and-style.md) | Sentence length, acronyms, articles, voice, numbers/units, US-English list, words to avoid, citation phrasing |
| [references/section-moves.md](references/section-moves.md) | Choosing tense and hedging for a specific section (Abstract / Intro / Method / Results / Discussion / Conclusion) |

## Hedging ladder (match the verb to the evidence)

```
strong, directly measured     show, demonstrate, establish
inferential                   indicate, suggest, imply
possible / partial            may, can, could, appear to, is consistent with
```

Over-claim is the most common reviewer irritation. If the evidence is one experiment, do not say
"prove" or "in all cases". Downgrade the verb instead of adding qualifiers like "very".

## Polishing workflow

1. **Split into sentences.** Inspect each individually — the last sentence of a paragraph fails most.
2. **Identify the section** (it sets tense and hedging; see `references/section-moves.md`).
3. **Length and one-idea check.** Aim for ≤ ~25 words; break any sentence carrying two ideas.
4. **Tense audit.** Results = past + numbers; method-as-procedure = past; the proposed method as
   a standing object = present; Introduction background = present / present perfect.
5. **Edit each sentence** for subject-action clarity, articles, and US spelling.
6. **Vocabulary upgrade.** Replace vague verbs ("get", "do", "make") with precise ones; remove
   filler ("it is worth noting that", "as we all know", "obviously").
7. **Acronym pass.** Define each at first use in the body; do not define in the title; avoid
   undefined acronyms in the abstract.
8. **Citation phrasing.** Numbered `[n]`; for author-prominent sentences use `Smith et al. [12]`,
   otherwise `... has been studied [12]`. Do not use `[12]` as a noun ("in [12], the authors...").
9. **Overclaim sweep.** Flag absolutes, unwarranted causation, scope creep, and unverified "first".
10. **US-English + house style** (units, numbers, hyphenation).
11. **Proofread** for articles, plurals, agreement — the classic non-native slips.
12. **Return plain text** plus a short change log of the substantive edits.

## Output format

1. `Polished:` the revised text, plain and copy-pasteable.
2. `Changes:` a short list of the *substantive* edits (not every comma) — e.g. "downgraded
   'prove' → 'indicate' (one experiment)", "split a 41-word sentence", "color/behavior to US".
3. `Flags:` any sentence where wording could not be fixed without a fact the author must supply.

For Chinese input, give the polished English, then a brief 中文说明 of the main changes, and a
list of any claims that need a number or citation. (See `ieee-writing`'s chinese-author-workflow.)
