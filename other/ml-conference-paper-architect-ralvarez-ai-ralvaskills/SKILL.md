---
name: ml-conference-paper-architect
version: 1.0.0
description: ML conference paper formatting for NeurIPS, ICML, ICLR, and AAAI — official style-file usage, anonymization and camera-ready toggles, page-limit accounting, natbib citations, standard paper skeleton, reproducibility checklists, appendix and supplementary rules, desk-reject checks. Use when writing, formatting, or submitting a machine-learning conference paper.
---

# ML Conference Paper Architect

Formatting and structural conventions for **NeurIPS, ICML, ICLR, and AAAI** submissions. Sits on top of [latex-architect](../../languages/latex-architect/SKILL.md), which owns general LaTeX practice — build, preamble order, floats, math, semantic markup. This skill owns only what is venue-specific.

Venue template sources and the classic-look preamble live in [assets/VENUE_TEMPLATES.md](assets/VENUE_TEMPLATES.md); worked skeletons in [RECIPES.md](RECIPES.md); pinned template years in [STACK.md](STACK.md).

## 1. The one rule that overrides everything

**Read the current year's Call for Papers and author kit before applying anything below.** Every number in this skill — page limits, deadline structure, checklist requirements — is revised annually, sometimes substantially. This skill encodes the *shape* of the requirements and the failure modes; the CFP encodes the current values. Where the two disagree, the CFP wins, and the fix belongs in [STACK.md](STACK.md).

Corollary: **never hand-copy a preamble from a previous paper.** Download the official style file for the target year. Reusing last year's `.sty` is the single most common cause of a paper that looks right locally and gets flagged by the venue's format checker.

## 2. Before drafting: confirm

1. **Venue and year** — determines the `.sty`, the page limit, and the checklist.
2. **Track** — main conference, datasets & benchmarks, workshop, or findings-style track. Limits and review criteria differ; workshop tracks are usually 4 pages and often *not* anonymous.
3. **Stage** — submission (anonymous), camera-ready (de-anonymized, +1 page at most venues), or preprint (arXiv).
4. **Whether code and data will be released** — this changes what the checklist and reproducibility statements can honestly claim, and it is not a question to answer at the deadline.

## 3. Venue matrix

Verify each row against the current CFP — see [§1](#1-the-one-rule-that-overrides-everything).

| | NeurIPS | ICML | ICLR | AAAI |
|---|---|---|---|---|
| Style file | `neurips_<year>.sty` | `icml<year>.sty` | `iclr<year>_conference.sty` | `aaai<yy>.sty` |
| Review | Double-blind | Double-blind | Double-blind (OpenReview, public) | Double-blind |
| Main-text limit | 9 pages | 8 pages | 9 pages | 7 pages |
| References | Unlimited, excluded | Excluded | Excluded | Counted separately (~2 pages) |
| Camera-ready | +1 page | +1 page | +1 page | Fixed; copyright block required |
| Final-mode toggle | `\usepackage[final]{neurips_<year>}` | `\usepackage[accepted]{icml<year>}` | `\iclrfinalcopy` | `\pdfinfo` block + copyright |
| Preprint mode | `[preprint]` option | — | — | — |
| Mandatory checklist | Yes, in-paper | Impact statement | Reproducibility statement | Reproducibility checklist |

**AAAI is the outlier.** Its style file bans packages the others tolerate (`geometry`, `fullpage`, `authblk`, and historically `hyperref`), mandates Type 1 fonts and an embedded `\pdfinfo` block, and runs an automated format checker that rejects on violation. Read AAAI's author kit in full; do not assume NeurIPS habits transfer.

## 4. Anonymization

Double-blind failures are desk rejects, not review-score penalties. The submission-mode style file handles author blocks automatically — everything else is on you:

- **No author names, affiliations, emails, or acknowledgements** in submission mode. Acknowledgements go in a section you add at camera-ready.
- **Cite your own prior work in the third person.** "Prior work [12] showed…", never "In our earlier work [12] we showed…" — the latter deanonymizes even with the citation intact.
- **Anonymize links.** No GitHub URLs with your username, no personal-domain project pages. Use an anonymized repo host, and check the repo itself for names in the README, LICENSE, and commit history.
- **Strip PDF metadata.** The compiled PDF carries author fields from your editor or OS. Verify with `pdfinfo main.pdf` before uploading.
- **Check figure provenance** — plots exported from a notebook can embed a file path containing your name or institution.
- **Know your venue's arXiv policy.** ICLR/OpenReview submissions are public; NeurIPS and ICML have specific rules on preprinting during the review window. This is a policy question, not a formatting one — read the CFP.

## 5. Page-limit accounting

The limit applies to **main text**; what counts as main text is venue-defined. References are typically excluded and the appendix always is, but figures, tables, and the checklist usually are not.

The failure mode is uniform across venues: papers that hit the limit by shrinking. **Every one of these is a rejection risk and some are explicit violations:**

- Reducing font size, `\baselinestretch`, or margins from the style file's values.
- Negative `\vspace` around floats, sections, or equations to claw back lines.
- `\small`/`\footnotesize` on body text (captions and tables are fine, and are usually already set by the `.sty`).
- Shrinking the reference list font or squeezing `\bibsep`.

Format checkers detect all of these mechanically. **Cut content instead** — move derivations, extended results, and ablation details to the appendix, which is unlimited. If the paper does not fit, the paper is too long, not the template.

## 6. Structure

The ML conference paper has a de-facto fixed skeleton. Deviating costs reviewer goodwill for no gain:

1. **Abstract** — problem, gap, what you did, headline result with a number. Under ~200 words.
2. **Introduction** — ending in an explicit contributions list. Reviewers look for this; make it a bulleted list of claims the paper actually substantiates.
3. **Related work** — position against the closest prior work. Either §2 or after the method, depending on whether the reader needs context to understand the approach.
4. **Method** — notation defined once, then the approach. A figure of the architecture or pipeline earns its space.
5. **Experiments** — setup (datasets, baselines, metrics, hyperparameters, compute, seeds), then results, then **ablations**. Missing ablations is the most common reviewer complaint.
6. **Limitations** — mandatory at NeurIPS, expected everywhere. Write it honestly; reviewers penalize an obviously sanitized limitations section harder than a real weakness.
7. **Conclusion** — short. No new claims.
8. **Broader impact / ethics** — per venue requirements.
9. **References**, then **Appendix**.

Writing rules that matter more here than in general LaTeX:

- **Every claim in the abstract and intro must map to a specific experiment.** Reviewers check this correspondence directly.
- **Takeaway-led captions.** "Figure 3: \model outperforms all baselines beyond 10k steps" beats "Figure 3: Results". Reviewers read figures and captions before the body.
- **Report variance.** Single-seed numbers with no error bars invite methodological objections regardless of the result.

## 7. Citations

Venue templates ship `natbib` with a venue `.bst`. **Keep it** — do not convert to biblatex, which is the standing carve-out in [latex-architect §8](../../languages/latex-architect/SKILL.md#8-bibliography).

- `\citep{x}` parenthetical, `\citet{x}` when the author is a sentence element. Mixing these up is visible and looks careless.
- **Cite the published version, not the arXiv preprint**, when one exists. Bulk-exported `.bib` files default to the preprint.
- **Brace-protect capitals**: `{B}ayesian`, `{ImageNet}`, `{GPT}`. Venue `.bst` files lowercase titles and will mangle these.
- Fix the export's author lists — `and others` truncation and inconsistent name forms are the usual damage.

## 8. Reproducibility

Every one of these venues now requires some form of reproducibility artifact, and the answers are checked against the paper body:

- **Answer the checklist honestly.** "No" with a stated reason is accepted; "Yes" contradicted by the paper is worse than either.
- **Report the full experimental setup**: hyperparameters, search ranges and selection method, hardware, wall-clock or GPU-hours, number of seeds, and the exact dataset splits.
- **Compute cost is a required disclosure at several venues** and increasingly a review criterion. Estimate it rather than omitting it.
- **Anonymized code at submission, permanent link at camera-ready.** A promise to release code later is weaker evidence than a working anonymous repo.

## 9. Appendix and supplementary

- Appendix goes **after references**, introduced by `\appendix`, with sections numbered `A`, `B`, … and referenced from the main text via `\cref`.
- Whether the appendix ships in the same PDF or a separate supplementary file is venue-specific. Check before restructuring.
- **The main text must stand alone.** Reviewers are not obligated to read the appendix, so no load-bearing claim may depend on it.
- Appendix content is unlimited but not free — a 40-page appendix signals a paper that was not edited.

## 10. Pre-submission checks

Run all of these before uploading; the list in [RECIPES §4](RECIPES.md#4-pre-submission-checklist) is the executable version.

- [ ] Official style file for the **correct year**, unmodified, in submission (not final) mode.
- [ ] Page count within limit, with no spacing or font hacks.
- [ ] No author names, affiliations, acknowledgements, or identifying links; PDF metadata stripped.
- [ ] All figures legible at print size and in grayscale; no raster text.
- [ ] Every citation resolves; no `?` marks in the compiled PDF.
- [ ] Checklist / impact statement / limitations section present and consistent with the body.
- [ ] Fonts embedded (`pdffonts main.pdf` shows no non-embedded entries) — AAAI enforces this mechanically.
- [ ] Compiles from a clean checkout with `latexmk` and no manual steps.

## 11. Out of scope

- **General LaTeX practice** (build, preamble, floats, math, cross-references) → [latex-architect](../../languages/latex-architect/SKILL.md)
- **Journal and institutional formats** → [uru-scientific-paper-architect](../../personal/uru-scientific-paper-architect/SKILL.md), [uru-thesis-architect](../../personal/uru-thesis-architect/SKILL.md)
- **Talk and poster design** → [demo-presentation-architect](../../personal/demo-presentation-architect/SKILL.md)
- **Research content** — this skill formats and structures a paper; it does not generate claims, results, or citations. Never fabricate a number, a baseline, or a reference.
