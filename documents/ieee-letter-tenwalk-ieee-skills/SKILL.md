---
name: ieee-letter
description: >-
  Write or compress an IEEE communications LETTER for WCL (IEEE Wireless Communications Letters)
  or CL (IEEE Communications Letters): a single-contribution paper with a compressed
  introduction, no standalone related-work section, one system model, one core result (an
  algorithm OR a closed-form expression), and a tight simulation section under the current WCL/CL
  page budget. Use this whenever the target is a letter rather than a transactions paper — "write
  a WCL letter", "turn this into a letter", "我的论文要投WCL/CL", "压缩成letter", "写一篇通信快报",
  "letter写不下了怎么删", "cut my letter to fit", EDICS selection, and the WCL/CL submission checklist.
  For full transactions papers (JSAC/TWC/TCOM) use ieee-writing; for the results narrative use
  ieee-writing + ieee-experiments; for figures use ieee-figure. Bilingual: turns Chinese notes
  into a submission-ready English letter plus short Chinese explanations.
---

# IEEE Communications Letter (WCL / CL)

A letter is **not a short transactions paper**. It is a single, sharp contribution presented under
a tight page budget (currently a 5-page maximum for both WCL and CL, with page charges beyond the
free page budget under ComSoc guidance). The job is to make one result land — fast — and to cut
everything that does not serve it. Use this skill to draft a letter from scratch or to compress an
over-length draft.

## Core stance

- **One contribution, stated once.** A letter carries a single advance: one algorithm, one
  closed-form expression, one new scheme, or one decisive finding. If the draft has two, it is a
  transactions paper — say so and use `ieee-writing`.
- **The free-page budget is a design constraint, not a trim at the end.** Plan the budget before
  drafting (see page budget below). Treat a paid fifth page as a strategic decision for essential
  evidence, not as permission to write a small transaction.
- **No standalone Related Work section.** Prior work is folded into the Introduction as the gap.
- **Author evidence comes first.** Never invent results, numbers, channel models, benchmark
  schemes, or limitations. Missing evidence → `[PLACEHOLDER: ...]` or ask the user.
- **Same IEEE register as a transactions paper**: US English, numbered citations `[n]`, bold-vector
  / bold-matrix notation, equations numbered only for the skeleton of the argument.

## WCL vs CL — know the target

| | IEEE WCL (Wireless Comms Letters) | IEEE CL (Communications Letters) |
|---|---|---|
| Page limit | Currently 5 pages maximum; the 5th page incurs an over-length charge | Currently 5 pages maximum; pages beyond 4 incur over-length charges |
| Abstract | Short letter abstract, commonly 75–100 words | Short letter abstract, commonly 75–100 words |
| EDICS | not required | **required** at submission |
| Scope | wireless / PHY-MAC | all communications |
| Anonymity | single-blind (default) | **double-anonymous option** available |
| Figures | submit vector (EPS/PDF) | submit vector (EPS/PDF) |

Always confirm the current page/fee/EDICS rules in the journal's author kit before submitting;
these defaults change. If the user has not named WCL vs CL, ask — the EDICS and anonymity rules differ.

## Page budget (IEEEtran, two-column, 10pt) — plan this first

Aim for the free 4-page budget by default. Use the paid fifth page only when it protects the one
contribution's proof, experiment, or critical validation.

```
Title + abstract + Index Terms              ~0.25 page
I.  Introduction (gap + contribution)       ~0.75 page
II. System Model (+ problem if needed)      ~1.0 page
III. Proposed Scheme / Analysis (core)      ~1.0 page
IV. Simulation Results (2–4 figures/tables) ~0.75 page
V.  Conclusion (3–4 sentences) + refs       ~0.25 page
```

This is a starting allocation, not a rule. The core (III) and the result (IV) are the paper; protect
their space and compress I–II. Verify how references and appendices count in the target journal's
current Author Kit.

## When to open extra files

| File | Open when |
|---|---|
| [references/letter-format.md](references/letter-format.md) | Drafting the letter section by section, or deciding what a letter keeps vs. what only a transactions paper carries |
| [references/compression-tactics.md](references/compression-tactics.md) | An existing draft exceeds the free budget or the 5-page maximum and must be cut without losing the argument; or fitting figures/tables/equations into the budget |

For the argument of each section, defer to `ieee-writing` (its section defaults apply, compressed).
For simulation content use `ieee-experiments`; for figures use `ieee-figure`; for references and
EDICS use `ieee-citation`; for the cover/response letters use `ieee-response`.

## Intake — establish before drafting

- **target**: WCL or CL (they differ on EDICS and anonymity)
- **the one contribution**: in a single sentence — the advance the letter exists to deliver
- **type**: algorithm/design letter, or closed-form analysis letter (changes Section III)
- **evidence**: the algorithm + convergence, or the derivation + a simulation overlay
- **boundary**: the CSI/channel assumption and scope where the claim holds
- **starting point**: drafting fresh, or compressing an over-length draft (→ compression-tactics.md)

If "the one contribution" is actually two, flag it: a letter cannot carry both well.

## Drafting workflow

1. **One-sentence contribution.** `We propose/derive [the one advance] for [system], which [benefit],
   under [boundary].` Confirm it with the user.
2. **Check it fits a letter.** One contribution, one model, one core result. If not, route to
   `ieee-writing`.
3. **Allocate the page budget** (above), then draft core-first: Section III, then IV, then the
   compressed Introduction, then System Model, then Abstract and Conclusion last.
4. **Draft from evidence outward**; keep each claim beside its support. Use `ieee-writing` section
   logic, compressed: Introduction ends with a *short* contribution statement (often 1–2 sentences,
   not a numbered list of four).
5. **Fit the figures**: 2–4 decisive figures/tables maximum, vector (EPS/PDF), readable at column
   width — see `ieee-figure`. One should validate analysis (line + Monte-Carlo markers) if the
   letter derives an expression.
6. **Page-fit pass**: if over the free budget, decide whether the paid fifth page is justified; if
   over the maximum, apply `references/compression-tactics.md` in order (cut repetition and
   over-fine detail before touching the core result).
7. **Return** the letter (LaTeX if IEEEtran), a page-budget estimate, a claim–evidence map, and a
   note on what was cut to fit.

## Letter-specific section defaults

- **Abstract:** ~75–100 words unless the current Author Kit says otherwise, one quantified headline.
- **Introduction:** compress to gap → contribution. Fold prior work into the gap; no separate
  Related Work. End with a *one- or two-sentence* contribution statement, not a 4-item list.
- **System Model:** only the symbols the core result needs. Cut generality the result does not use.
- **Proposed Scheme / Analysis (the core):** the algorithm box *or* the theorem/derivation — the one
  thing the letter exists for. Label transformations exact vs approximate; state convergence target
  (KKT/stationary/global) honestly. Long proofs are usually cut or sketched, not appended (letters
  rarely have appendices — confirm with the author kit).
- **Simulation Results:** 2–4 decisive figures/tables, claim-first. Validate the derived expression
  first if there is one; then the single most important comparison vs benchmark schemes. A compact
  measurement/testbed result is worth the space only if it supports the one contribution. State the
  fairness boundary in one sentence.
- **Conclusion:** 3–4 sentences. Contribution → decisive result → boundary/outlook. No new data.

## Output format

1. `Draft:` the letter prose (or IEEEtran LaTeX).
2. `Page budget:` estimated pages per section vs. the free-page budget and the 5-page maximum.
3. `Claim–evidence map:` `Claim … | Evidence … | Status: supported / needs evidence`.
4. `Cut list:` what was removed (or must be) to fit, and what was protected.
5. `Assumptions or missing inputs:` only material issues.

For Chinese input, give the polished English letter first, then brief Chinese notes on what was
compressed or cut and why.
