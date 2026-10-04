---
name: technical-microcopy-editor
description: "Run an accuracy, clarity, and brevity edit on technical design case-study copy. Use when prose contains vague UX jargon, imprecise system claims, passive voice, inconsistent terms, inflated ownership, unsupported metrics, long captions, or when the draft should become materially shorter without losing quantitative evidence or technical meaning."
---

# Technical Microcopy Editor

Edit in three ordered passes. Read `references/acb-edit.md`.

## Pass 1 — Accuracy

Verify names, numbers, units, ownership, sequence, system behavior, and claim status against supplied artifacts. Flag contradictions and unverifiable statements. Do not polish a false claim.

## Pass 2 — Clarity

Replace abstract jargon with concrete actors, actions, objects, states, and consequences. Give each sentence one primary job. Keep terminology consistent with the product and architecture. This is McKay's "clear and natural" test applied to prose about the product rather than the product itself: use the language a competent person would actually say out loud, not a system emitting status (McKay).

## Pass 3 — Brevity

Target a 30% word-count reduction unless doing so would remove evidence or necessary causal explanation. Delete repetition, throat-clearing, and self-congratulation. Prefer direct verbs and information-bearing headings. Kubie's distinction is the filter: keep THE THING (the claim, the evidence, the causal link) and cut NOT THE THING (the process narration, the hedging, the credit-taking) — most bloat is NOT THE THING dressed up as content (Kubie).

Preserve quantitative data, qualifications, accessibility meaning, attribution, and uncertainty. Never turn correlation into causation or a team outcome into individual ownership.

## Output

Return:

1. the edited copy;
2. before/after word counts and reduction percentage;
3. an accuracy issue list;
4. a terminology normalization list;
5. any sentence retained despite length because it carries necessary evidence.

## Example

Input:

```text
I designed an intuitive and seamless workflow that significantly improved outcomes.
```

Expected outcome:

```text
I redesigned the retry flow. In the moderated test, 8 of 10 participants recovered
without support. [Evidence needed: baseline and attribution.]
```

## Sources

- **Everett McKay**, *UI Is Communication* (Morgan Kaufmann, 2013) — the clarity pass's "clear and natural" standard: language a person would actually say, not system-speak.
- **Scott Kubie**, *Writing for Designers* (A Book Apart, 2018) — the brevity pass's THE THING vs NOT THE THING cut.
- **Michael J. Metts & Andy Welfle**, *Writing Is Designing* (Rosenfeld Media, 2020) — plain-language grounds for why brevity and accuracy can't trade against each other; cut filler, never cut a caveat.
