# NeurIPS-style scoring

**Gate S · Owned by Elrond (Convener & Statistician).** The score is Elrond's
synthesis duty: it fires only when a NeurIPS-style venue is named or a score/rating is
requested, and it aggregates the whole gate ladder into a venue-legible rating.

This maps the Council's gate ladder and findings onto the NeurIPS reviewer form.
The **ACCEPT / MAJOR REVISION / REJECT** decision stays primary; the scores are a
translation of that decision into a venue-legible scale, never a replacement for it.
Every score must be **derived from gate results and findings that already appear in
the review** - a score the ladder does not support is the review's own overclaim.

Fill this whenever a NeurIPS-style (or generic top-ML-venue) target is named, or the
user asks for a score, rating, or "would this get in." Otherwise it is optional.

## The five axes

NeurIPS reviewers rate four numeric axes plus a confidence. Score each, and in one
line cite the gate/finding that fixes the number.

### Soundness — 1 to 4
Technical soundness of claims, methods, and whether conclusions are supported by
evidence. This is the axis the gate ladder speaks to most directly.

| Score | Label | Meaning | Gate signal |
|---|---|---|---|
| 4 | Excellent | Claims fully supported; robust, confound-controlled, mechanism/necessity where claimed | Gates 0-6 PASS, T4/T5 evidence |
| 3 | Good | Central claim supported but a robustness/confound/specificity gap remains | one of Gates 1-5 FAIL, fixable |
| 2 | Fair | Central claim rests on evidence weaker than its language; multiple gate gaps | ≥2 of Gates 1-6 FAIL, or a calibration overclaim |
| 1 | Poor | Central claim unsupported or contradicted (leakage, synthetic-as-real, artifact) | any Gate 0 FAIL, or central claim collapses |

**Anchor:** a Gate 0 failure caps Soundness at 1. A confirmed-artifact central claim
is Soundness 1 regardless of polish.

### Presentation — 1 to 4
Quality of writing, clarity, contextualization vs prior work, and figures.

| Score | Label | Signal |
|---|---|---|
| 4 | Excellent | Clear, well-structured, figures honest and self-explanatory (Gate F PASS), contributions traceable |
| 3 | Good | Readable; minor clarity/figure/exposition gaps (Samwise Minors) |
| 2 | Fair | Argument-chain breaks, an unclear central figure, or contributions without a home |
| 1 | Poor | Figure contradicts a claim (Gate F Blocker), or the reader cannot reconstruct what was done |

### Contribution — 1 to 4
Significance and originality of the contribution relative to prior work.

| Score | Label | Signal |
|---|---|---|
| 4 | Excellent | Novel and important; Legolas confirms genuine prior-art gap; changes how the problem is approached |
| 3 | Good | Solid, incremental-plus; a real gap but bounded impact |
| 2 | Fair | Marginal delta over existing work, or novelty asserted but not established |
| 1 | Poor | Not novel (Legolas finds prior art), or contribution is negated by a soundness failure |

### Overall — 1 to 10
The summary rating. Use the standard NeurIPS anchors; the decision band on the left
must agree with the Council verdict.

| Verdict band | Overall | NeurIPS anchor |
|---|---|---|
| REJECT | 1 | Trivial or wrong; award for the worst paper |
| REJECT | 2 | Strong reject |
| REJECT | 3 | Clear reject |
| REJECT / MAJOR REVISION | 4 | Borderline reject — reasons outweigh reasons to accept |
| MAJOR REVISION | 5 | Borderline accept — could go either way |
| MAJOR REVISION / ACCEPT | 6 | Weak accept — decent, some issues, more good than bad |
| ACCEPT | 7 | Accept — technically solid, good impact, no major concerns |
| ACCEPT | 8 | Strong accept — high impact, one of a good fraction |
| ACCEPT | 9 | Very strong accept — seminal, top of the field |
| ACCEPT | 10 | Award quality |

**Mapping rule.** REJECT → 1-4, MAJOR REVISION → 4-6, ACCEPT → 6-9 (10 reserved).
The verdict is the anchor; the Overall number lives inside its band. If you find
yourself wanting an Overall that sits outside the verdict's band, the verdict or the
score is wrong — reconcile in the coherence pass before emitting.

### Confidence — 1 to 5
The reviewer's own confidence, and honest about it (this is the review's Type I
discipline turned on itself).

| Score | Meaning |
|---|---|
| 5 | Absolutely certain; deeply familiar, checked the math/code |
| 4 | Confident but not certain; unlikely but possible some part was misunderstood |
| 3 | Fairly confident; plausible a detail was missed, or unfamiliar with some related work |
| 2 | Willing to defend but likely didn't understand central parts, or unfamiliar area |
| 1 | Educated guess; hard to assess, area far from expertise |

**Calibrate honestly.** If the review is **evidence-blocked** on a load-bearing
number (unreleased config, absent seed sweep), Confidence drops to 2-3 and the
review says so, rather than posting a confident score it cannot support. Deep-mode
reviews that recomputed numbers earn 4-5; a quick gut-check caps at 3.

## Optional NeurIPS extras

Add only when the target venue actually asks for them or the user requests:

- **Borderline flag** — for Overall 4-6, one line: what single thing tips it.
- **Ethics review flag** — raise iff Gate 10 (Treebeard) surfaced a concern; state
  whether it warrants a dedicated ethics review.
- **Reproducibility flag** — YES/NO from Gate 9 (Eowyn): are code, seeds, configs,
  and data sufficient to reproduce? A NO here is a Presentation/Confidence drag,
  not automatically a reject.

## Output block

Emit this directly under the Verdict line when scoring is requested:

```
## NeurIPS-style score
- Soundness:    _/4  — <gate/finding that fixes it>
- Presentation: _/4  — <...>
- Contribution: _/4  — <...>
- Overall:      _/10 — <one-line justification; must sit in the verdict's band>
- Confidence:   _/5  — <why this and not higher/lower>
- Flags: reproducibility <YES/NO> · ethics <none/see Gate 10> · borderline <n/a or the tipping factor>
```

## Guardrails

- **No score without the ladder.** Every axis cites a gate or a named finding. A
  bare number is not a review.
- **Bands must agree.** Overall sits inside the verdict's band. Soundness ≤ 1 whenever
  Gate 0 fails. These are checked in the coherence pass.
- **Confidence is not padding.** Low evidence → low confidence, stated plainly. Do not
  post Confidence 5 on a review that abstained on the central number.
- **The decision is still ACCEPT/MAJOR REVISION/REJECT.** The scores translate it for
  a venue; they never override it or become the headline.
