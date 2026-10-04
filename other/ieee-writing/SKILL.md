---
name: ieee-writing
description: >-
  Draft, restructure, or plan IEEE communications-journal manuscript sections (JSAC, TWC,
  TC/TCOM, WCL, CL): abstract + Index Terms, introduction with a contributions list, related
  work, system model, problem formulation, proposed solution/algorithm, performance analysis
  (theorems/proofs), numerical results, discussion, conclusion, title — from author claims,
  derivations, simulation results, figures, notes, or Chinese drafts. Use this whenever the user
  wants to WRITE or REBUILD comms paper text: "help me write my paper", "draft the introduction",
  "写系统模型", "问题建模", "restructure this section", "把我的中文草稿写成英文论文", "写贡献点", "改写算法部分" — not merely fix
  grammar (use ieee-polishing). For a WCL/CL letter, use ieee-letter. Bilingual: turns Chinese
  notes into submission-ready English plus short Chinese explanations.
---

# IEEE-Style Scientific Writing

Use this skill to **create or rebuild** IEEE manuscript prose — to construct the argument,
not only to polish finished sentences. For sentence-level language work, hand off to
`ieee-polishing`.

## Core stance

- **Author evidence comes first.** Never invent results, numbers, mechanisms, references,
  benchmark schemes, channel models, simulation parameters, network architectures, training data,
  novelty claims or limitations. If essential evidence is missing, write an explicit
  `[PLACEHOLDER: ...]` or ask the user — do not fill the gap.
- **Write the argument before the sentences.** Decide what each paragraph must prove, then draft.
- **Make the paper easy to judge** on relevance, novelty, soundness, and reproducibility —
  these are the axes IEEE reviewers actually score.
- **Ambitious but bounded claims.** Tie every claim to the evidence that supports it and stop
  the claim where the evidence stops.
- **IEEE register**, not magazine narrative: precise, technical, US English, numbered citations
  `[n]`, equations numbered only for the skeleton of the argument.

## When to open extra files

Keep this file lean. Open a reference only when its row matches the task.

| File | Open when |
|---|---|
| [references/journal-fit.md](references/journal-fit.md) | The user names or is choosing JSAC, TWC, TC/TCOM, WCL, or CL; deciding whether a draft fits a transaction vs. a letter; adapting argument depth, evidence depth, or page strategy to the target journal |
| [references/abstract.md](references/abstract.md) | Drafting/revising the abstract and Index Terms |
| [references/introduction.md](references/introduction.md) | Drafting/revising the Introduction, the technical-challenge build-up, the contributions list, or the paper-organization paragraph |
| [references/method.md](references/method.md) | Writing the System Model, Problem Formulation, and Proposed Solution/Algorithm: signal flow, optimization problem, transformations, notation, equation-numbering, convergence/complexity |
| [references/learning-based-comms.md](references/learning-based-comms.md) | The contribution is a neural network or learning algorithm for a PHY/MAC task (DL/CNN/GNN/Transformer, deep unfolding, DRL): architecture, training methodology, loss tied to a comms metric, generalization and inference-complexity claims |
| [references/system-model-paradigms.md](references/system-model-paradigms.md) | Writing the System Model for an emerging architecture (RIS, NOMA, ISAC, near-field/XL-MIMO, movable/fluid antenna, cell-free, mmWave/hybrid, semantic comm): the must-have model elements, the distinctive variable/constraint, the signature metric, and per-paradigm pitfalls |
| [references/theory-and-proofs.md](references/theory-and-proofs.md) | Writing the optimization solution (SCA/SDR/ADMM/fractional programming) or the Performance Analysis: theorem/lemma/proof structure, appendix placement, convergence and complexity claims |
| [references/results-discussion-conclusion.md](references/results-discussion-conclusion.md) | Writing the Numerical Results narrative, Discussion interpretation, or a bounded Conclusion |
| [references/body-revision.md](references/body-revision.md) | Tightening, compressing, or restructuring existing body text; fixing logic flow, term consistency, table/prose overlap, or task-hierarchy confusion |
| [references/chinese-author-workflow.md](references/chinese-author-workflow.md) | The user's input is Chinese, mixed Chinese-English, or lab-note style rather than manuscript prose |

For simulation *content* (which benchmark schemes/metrics/sweeps to run) use the `ieee-experiments`
skill; for figures use `ieee-figure`; for reference formatting use `ieee-citation`; for a WCL/CL
letter use `ieee-letter`.

## Intake — establish before drafting

- **section**: title, abstract, Index Terms, introduction, related work, system model, problem
  formulation, proposed solution/algorithm, performance analysis, numerical results, discussion,
  conclusion, or full outline
- **paper type**: optimization/resource-allocation design, performance analysis (closed-form
  outage/BER/rate), new system/architecture (RIS, NOMA, ISAC, cell-free, ...), learning-based
  (DL/deep-unfolding/DRL for a PHY/MAC task), signal-processing algorithm, or measurement/empirical
  study
- **core claim**: what the paper actually demonstrates, in one sentence
- **evidence**: derivations/theorems, simulation curves, benchmark comparisons, complexity analysis
- **boundary**: where the claim stops (CSI assumption, channel model, scope, conditions)
- **target**: the specific journal (JSAC/TWC/TCOM = transactions; WCL/CL = letter) and its current
  page/abstract rules; if the target is unclear, use `references/journal-fit.md` before drafting

If `target`, `core claim`, `evidence`, or `boundary` is missing, surface the gap first. You may
still produce a scaffold with explicit placeholders.

## Writing workflow

1. **One-sentence argument:** `In [problem/system], we show [advance] using [approach],
   supported by [evidence], under [boundary].` Get the user to confirm it.
2. **Choose section architecture** (see Section defaults below).
3. **Map each paragraph to one job:** context, gap, prior-method limitation, contribution,
   design, result, comparison, mechanism, implication, or limitation. One paragraph, one job.
4. **Draft from evidence outward.** Keep each claim next to the data that support it.
5. **Calibrate verbs to evidence:** `show / demonstrate` (strong, measured) →
   `indicate / suggest` (inferential) → `may / could` (possible). Downgrade if evidence is thin.
6. **Remove unsupported novelty and universal claims** ("first ever", "optimal", "in all cases").
7. **Paragraph-flow check:** does the first sentence of each paragraph state its message, and
   does each sentence follow from the previous one? (See `references/body-revision.md`.)
8. **Return prose plus a claim–evidence map and a short note on assumptions / missing inputs.**

## Section defaults (IEEE)

### Title
`object/system + method/capability + task or consequence`. Concrete over slogan. Avoid
grant-style aims and overbroad field claims. Keep abbreviations minimal and standard.

### Abstract + Index Terms
Single self-contained paragraph: ~150–250 words for transactions, usually ~75–100 words for WCL/CL
letters under current ComSoc guidance, **no citations, no undefined abbreviations, no equations**.
Default order:
`context/problem → gap → approach → key quantitative result → implication/boundary`.
Follow immediately with **Index Terms** (5–8 items, alphabetical, lower case except proper
nouns). Details and method-paper variants: `references/abstract.md`.

### Introduction (Section I)
`application/importance → how prior methods work → their limitation + the technical reason →
the unresolved gap this paper targets → our approach and why it works → contributions list →
paper organization`.
End with an explicit contributions list ("The main contributions of this paper are
summarized as follows:") and a one-sentence organization paragraph
("The remainder of this paper is organized as follows..."). Reason **backward** (what
challenge, what contribution, why it works) before writing **forward**. Templates and
sentence skeletons: `references/introduction.md`.

### Related Work (Section II, optional)
`topic scope → representative methods grouped by approach → limitation tied to this paper →
our distinction`. Group by technical theme and mechanism, never by year. Do not re-prove the
gap already made in the Introduction.

### System Model (Section II)
`network/topology → channel model → transmit & receive signal → performance metric (as an
equation)`. Describe the **signal flow** (what is sent, how the channel transforms it, what is
received, why it matters), not a symbol dump. End by defining the metric the paper optimizes or
analyses. Put a "Notation" paragraph (vector/matrix/set conventions) at the end of Section I or the
start of Section II. Details: `references/method.md`. For an emerging architecture (RIS, NOMA, ISAC,
near-field, movable antenna, cell-free, mmWave/hybrid, semantic), check the per-paradigm must-have
elements, distinctive constraint, and pitfalls in `references/system-model-paradigms.md`.

### Problem Formulation (Section III)
`objective → every constraint, each explained → problem class → why it is hard`. State which
quantities are optimization variables; classify the problem (non-convex / MINLP / fractional) and
name the difficulty that motivates the solution. Details: `references/method.md`.

### Proposed Solution / Algorithm (Section IV)
`reformulation/transformation → algorithm box → convergence → complexity`. Make the path from the
hard problem to a solvable one explicit and motivated; label each step exact vs approximate. For
SCA/SDR/ADMM/fractional-programming patterns and proof structure: `references/theory-and-proofs.md`.

### Proposed Network / Learning-based Solution (learning papers)
`architecture (layers, dimensions, parameter count) → input/output and normalization → loss
function tied to a comms metric → training algorithm → inference complexity & latency vs the
model-based benchmark`. Prefer deep unfolding (unrolled WMMSE/ADMM/SCA) over a black-box net, and
justify the choice; the loss must be a communications metric (NMSE, negative sum rate), not an
abstract proxy. Details: `references/learning-based-comms.md`.

### Performance Analysis (analytical papers)
`assumptions → derivation → theorem (closed-form outage/BER/rate) → asymptotic corollary
(diversity order / DoF)`. Long proofs go to an Appendix; plan a simulation overlay to validate every
derived expression. Details: `references/theory-and-proofs.md`.

### Numerical / Simulation Results
`simulation setup (parameters table) → benchmark schemes → analysis-vs-simulation validation →
performance vs benchmarks → parameter sweeps (SNR / antennas / users) → convergence & complexity →
robustness (imperfect CSI)`. Build an evidence ladder, claim-first per subsection. For *what to
produce*, use `ieee-experiments`; for narrative, `references/results-discussion-conclusion.md`.

### Discussion (if separate)
`central advance → what the curves mean → relation to prior work → constraints (CSI / scope) →
outlook`. Interpretation and limitations live here; do not replay results figure by figure.

### Conclusion
`contribution → decisive evidence → implication → boundary/future work`. No new data, no
unsupported promises, no re-derivation of equations.

## Output format

1. `Draft:` the requested prose (or LaTeX if the user is in IEEEtran).
2. `Section outline:` 3–7 compact bullets when drafting a whole section.
3. `Claim–evidence map:` `Claim … | Evidence … | Status: supported / needs evidence`.
4. `Assumptions or missing inputs:` only material issues.
5. `Why this structure:` 2–4 short bullets.

For Chinese input, give polished English first, then brief Chinese notes on the major
structural choices (see `references/chinese-author-workflow.md`).
