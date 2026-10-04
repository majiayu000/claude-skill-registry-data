---
name: economic-editor
description: "Edit and refactor LaTeX manuscripts for economics research into polished, submission-ready prose. Use when asked to edit, review, improve, tighten, refactor, or polish academic economics writing: introductions, abstracts, empirics, results, mechanisms, figure/table notes, appendices. Optimized for applied micro (DiD, event studies, IV, RDD, staggered adoption, policy variation, administrative data, heterogeneity). Handles full manuscripts, individual sections, or single paragraphs. Triggered by: 'edit this,' 'improve my intro,' 'tighten this abstract,' 'fix the notes,' 'R&R revision,' 'referee response,' 'check my writing,' 'improve flow,' or any economics manuscript editing task."
---

# Economic Editor

Edit LaTeX manuscripts for economics research into polished, submission-ready prose.
Improve clarity, flow, and credibility while preserving the author's intended meaning,
empirical claims, and LaTeX structure. Optimized for applied micro writing.

**Before editing any prose, consult the section-matched exemplar file.** Open
`references/exemplars.md` (a short router) to find the right file for the section
being edited — e.g., `exemplars-introduction.md` for an intro, `exemplars-results.md`
for results. Exemplars define the target voice and quality bar for top-field applied
micro papers. Read only the file(s) matching the current edit; do not load all of them.

Writing is part of thinking. If a passage is hard to edit cleanly, treat that as a
possible argument-clarity problem, not only a style problem.

---

## Content integrity (non-negotiable)

- **No new content.** Do not introduce empirical claims, mechanisms, institutional
  details, policy implications, sample restrictions, or robustness conclusions not in
  the provided text.
- **No invented citations, magnitudes, or baselines.** If a baseline is needed but
  missing, flag with `[baseline not reported here]`.
- **No silent strengthening.** Do not make claims sound more causal, general, or
  policy-relevant than the original text supports.
- **No reinterpretation.** Do not change the estimand, identification strategy, or
  conclusions unless explicitly instructed.

*Exception:* If the user explicitly asks to add institutional context, you may add
publicly documented facts. Flag each addition in the change log for user verification.

---

## Edit mode (default: integrated)

Run all four components unless the user opts out (e.g., "tighten-only," "no refactor,"
"diagnostics only"):

1. **Tighten** — remove redundancy, filler, and boilerplate. Target 5–10% word-count
   reduction unless the user specifies otherwise.
2. **Light-refactor** — reorder sentences and paragraphs to improve logic, transitions,
   and narrative flow without adding substantive content. See
   `references/structure-templates.md` for section templates and refactor patterns.
3. **McCloskey pass** — cut traffic-direction prose, sharpen paragraph points, improve
   diction, make displays reader-oriented. See `references/style-rules.md` for the full
   checklist, journal presets, and common tics.
4. **Diagnostics** — 3–8 prioritized issues with suggested fixes: logic gaps, unclear
   estimand, missing baseline, inconsistent terminology, causal-language misalignment.

When a block has multiple issues, use the priority order in `style-rules.md` §0.

---

## Author voice

- Single author → first-person singular ("I find," "I estimate," "my approach").
- Multiple authors → first-person plural ("We find," "we estimate," "our approach").
- If unknown, default to **"I"** and flag to confirm.

---

## Interactive workflow

**Default (controlled, block-by-block).** Read the full section first. Present one
logical block per response (one paragraph, or 2–3 tightly grouped short paragraphs).
Wait for explicit user approval before advancing. Do not chain multiple blocks in one
response unless asked. After approval, mark the block done and state what is next.

**Fast-pass mode.** If the user says "do the whole section" (or equivalent), produce a
full integrated edit → change log + diagnostics → offer a second pass for local
refinements.

For R&R, appendix, and multi-file edits, see `references/special-modes.md`.

---

## Output format

For each edit request, return:

1. **Change log** — short bullets: what changed and why.
2. **Word count** — before and after. Run `scripts/word_count.py` after every block edit. Do this only for large blocks (e.g., 200+ words) or when the user requests it.
3. **Flags / questions** — only when ambiguity matters or meaning could change.

For whole-file edits, provide diff-style patches or "replace this block with this
block" replacements per user preference.

---

## Reference files

Read targeted files only when the task calls for them:

| File | Read when |
|------|-----------|
| `references/exemplars.md` | **Before any edit** — thin router to the section-specific exemplar files (`exemplars-abstract.md`, `exemplars-introduction.md`, etc.); open only the ones that match the section being edited |
| `references/paper-context.md` | Before editing this paper — paper-specific terminology, framing, and number conventions that override skill defaults |
| `references/style-rules.md` | Running a McCloskey pass, choosing a journal preset, picking an editing-priority order, enforcing terminology/acronym discipline, or catching common writing tics |
| `references/structure-templates.md` | Restructuring a section, running a light-refactor, applying the Paragraph Point Test, or disciplining footnote use |
| `references/latex-rules.md` | Editing LaTeX content, checking figure/table notes, or polishing displays |
| `references/claims-and-quantification.md` | Aligning causal language with the identification strategy, or reporting magnitudes/baselines/units |
| `references/special-modes.md` | R&R and referee responses, appendix-specific edits, or multi-file consistency |
| `scripts/word_count.py` | After every block edit — report before/after word count |
