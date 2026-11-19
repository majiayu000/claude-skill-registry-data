---
name: council-review
description: No account, API key or paid service; optional Deep mode uses literature
  skills only if already installed. Adversarial empirical review of papers, proposals,
  or code and results against a gate ladder for variance, confounds and overclaiming,
  returning ACCEPT / MAJOR REVISION / REJECT with ranked findings.
---
# Council Review

## What this is

A scientific work is only as strong as the worst objection it survives. This skill
stops you from being a polite reviewer. It convenes the **Council of Elrond** - a
fixed panel of skeptics who each attack from one angle - and forces the work
through an **empirical gate ladder** before any verdict is allowed.

The gates are not generic peer-review etiquette. They encode the empirical
discipline that has actually killed real in-silico findings:

- A headline single-run improvement that turned out to be **seed variance**
  (Cohen's *d* = -1.20 across 20 seeds once tested properly).
- A correlation that was **real but scale-confounded** (raw p = -0.83, *p* = .04;
  partial correlation controlling for log-params p = -0.67, *p* = .14, NS).
- A "brain-like" component that was present but **functionally redundant** under
  ablation (8.6x less load-bearing than the components doing the actual work).
- A synthetic-data pilot that fingerprinted "subjects" perfectly because they
  were different random seeds, archived forever as `DO_NOT_CITE`.

The Council exists so that the work being reviewed dies *here*, in private, rather
than in front of a NeurIPS reviewer or - worse - after publication.

## When to use it

Use it whenever the user wants empirical scrutiny of a scientific claim or
artifact: reviewing a paper/proposal/preregistration, auditing their own results
before submission, deciding whether a finding is real, checking whether an
abstract overclaims, or pressure-testing a method. It works on external papers
*and* on the user's own running experiments.

It is domain-tuned for in-silico neuroscience / neuro-AI (encoding models, RSA,
attention-topology, fMRI alignment, manipulation/footprint metrics) but the gate
ladder is general to any quantitative empirical claim. For non in-silico
empirical work (clinical, biomedical, observational, meta-analysis), see
`references/domain-adaptation.md` for how the gates map onto CONSORT, STROBE,
PRISMA, ARRIVE, and general clinical-trial reporting.

## How to run a review

### 1. Establish the target and mode

Identify what you're reviewing and in which mode:

- **Manuscript mode** - a paper, proposal, preregistration, or draft. Read it
  fully. Extract the *central claims* (what the abstract/contributions assert),
  not just the prose.
- **Artifact mode** - a repo, results JSON, notebook, or stats output. Open the
  actual numbers. Do not trust the prose summary of a result you can recompute.
- **Both** (most powerful) - a manuscript *with* its code/results present.
  Cross-check every headline number in the text against the artifact that
  produced it. Mismatches are findings.

Also fix the **stance**, orthogonal to the target type:

- **Gatekeeper stance** (default) - "is this real / tear it apart / pre-submission."
  The verdict is the product; findings are ruthless and terminal where warranted.
- **Development stance** - "help me write / strengthen this / is my argument clear."
  The verdict still runs (rigor is not optional on a draft), but the emphasis shifts
  to generative feedback: every finding pairs with the concrete edit that fixes it,
  plus an Exposition pass and a Reviewer-2 pre-mortem. See
  `references/paper-development.md`. When the stance is ambiguous, ask in one line.

State the mode, the stance, and list the central claims before judging anything. A
review that hasn't named the claims is just vibes.

### Scope the review to the ask

Infer the review's depth from the user's phrasing, or ask in one line if unclear:

- **Quick** (a gut check / "is this obviously broken") - run the core gates 0-6 on
  the central claim only, the error-analysis pass on the headline number, and
  report the top 1-3 findings plus the verdict. Skip orchestrated lookups.
- **Standard** (default, pre-submission review) - full gate ladder as relevant, all
  standing seats, specialists as the design invites, error-analysis pass,
  conditional gates.
- **Deep** (exhaustive audit / "tear it apart completely") - everything in Standard
  plus orchestrated literature/verification lookups, recompute every checkable
  number, convene all specialists, and run the reviewer self-guard explicitly.

**Executing the user's code is opt-in.** Recomputing a number from a static
results file, notebook output, or statistical table needs no permission - that
is reading. But *running the user's code* (e.g. re-executing a training or
analysis script via `verification-loop`) can have side effects - it can write
files, hit the network, cost compute, or mutate state. Never run it silently:
do it only when the user has asked for it or after you confirm in one line
("re-run `train.py` to verify the headline? it will train for ~N steps"). When
the user declines or is absent, mark the number **evidence-blocked** rather than
executing to fill the gap. This holds at every scope, Deep included.

Empirical rigor (never rubber-stamp) is constant across levels; only breadth and
orchestration scale.

### 2. Build the Claim Ledger

For each central claim, record: the claim as stated, the **evidence tier** it
actually rests on, and which gates it must pass. Evidence tiers, weakest to
strongest:

| Tier | Description |
|---|---|
| T0 | Assertion / intuition, no evidence |
| T1 | Single run / anecdote / illustrative example |
| T2 | Descriptive statistic, no inference (means, single *p*) |
| T3 | Inferential with effect size + CI, but no robustness/confound control |
| T4 | Robust: multi-seed, confound-controlled, specificity-tested |
| T5 | Mechanistic: necessity established (ablation/lesion), pre-registered confirmatory |

A claim's language must not exceed its tier. "X causes Y" on T3 evidence is an
overclaim finding, full stop.

### 3. Walk the gate ladder

Run every claim through the gates **in order**. Read
`references/empirical-gates.md` for the full definition, worked examples, and the
exact statistical checks each gate demands. The ladder in brief:

- **Gate 0 - Provenance & Integrity.** Is the data real (not synthetic stand-in)?
  Any train/test leakage? Is the split fixed and honest? Is a noise ceiling /
  chance baseline established? A failure here is terminal. → **REJECT** if it fails.
- **Gate 1 - Variance / Replication.** Is the headline from one run or many seeds?
  Effect size *and* CI reported, not *p* alone? Could this be seed variance?
- **Gate 2 - Specification Robustness.** Does it survive reasonable analytic
  choices (thresholds, preprocessing, hyperparameters)? Or is it knife-edge?
- **Gate 3 - Specificity.** Is the *named* mechanism specifically responsible, or
  would a generic alternative of equal strength do as well? (The ablation test.)
- **Gate 4 - Confound Control.** Does the effect survive controlling for the
  obvious confounds (scale/size, length, surprisal, base rate)?
- **Gate 5 - Mechanism / Necessity.** Is there a necessity test? Does the proposed
  driver actually carry the functional load, or is it present-but-redundant?
- **Gate 6 - Claim Calibration.** Does each claim's language match its evidence
  tier? In-silico is not in-vivo. Correlational is not causal.
Gates 0-6 are the terminal-ordered empirical core (is the finding real?). Gates 7-11
are the **methodology-completeness tier** (was the study well built and reported?) and
apply as the design invites; Gate F is conditional on figures; Gate M is conditional
on topic (fires only for in-silico neuro/AI work - encoding models, RSA, fMRI/EEG
alignment, attention-topology, brain-vs-model comparisons). Full definitions and
worked examples for all of them in `references/empirical-gates.md`.

- **Gate M - Multiverse Robustness (conditional on topic).** Fires only when the
  work deals with the brain, AI, or both together (in-silico neuro/AI). Extends
  Gate 2 from spot-checked alternatives to a systematically enumerated analytical
  multiverse (preprocessing, ROI/parcellation, embedding/checkpoint, alignment
  metric, correction) with the fraction of the space that preserves the effect
  reported explicitly - not neuro/AI -> mark **N/A**.

- **Gate 7 - External Validity & Generalization.** Does it hold beyond the exact
  sample/dataset/model/site tested? OOD or transfer test, or generalization asserted
  from one split? Representative sample or convenience sample the claim outgrows?
- **Gate 8 - Measurement Validity & Reliability.** Does the instrument measure the
  construct, and reliably (test-retest / internal consistency / inter-rater)? Does the
  effect fit under the reliability ceiling? Ceiling/floor effects, manipulation checks.
- **Gate 9 - Reproducibility & Computational Provenance.** Seeds, configs, splits,
  code, environment, versioned data released? Nondeterminism controlled? Compute/cost
  reported so "better" is separable from "bigger budget"?
- **Gate 10 - Ethics, Safety & Responsible Disclosure.** IRB/consent/privacy for
  subjects; licensing/PII for data; dual-use/release-gating for misuse-capable work;
  honest broader impacts; subgroup-harm checks where warranted.
- **Gate 11 - Analytic Integrity.** Preregistration / analysis plan? Confirmatory and
  exploratory results separated, or an exploratory finding narrated as a priori
  (HARKing)? Forking paths pre-committed? Stopping rule and outcomes fixed?
- **Gate F - Figure & Visualization Integrity (conditional).** Fires **only if the
  work contains figures** you can actually inspect. Each figure: one clear takeaway
  stated in its caption, self-explanatory, honest encoding (axes not truncated, error
  bars and chance line present), readable and colorblind-safe, and actually showing
  what the text claims. A figure that contradicts a central claim is a Blocker. No
  figures -> mark **N/A**. Full rubric in `references/figure-review.md`.
- **Gate T - Theoretical Soundness (conditional).** Fires only when the work makes
  formal/mathematical claims (theorems, proofs, derivations, complexity/convergence
  results). Are assumptions stated and realistic, is each proof step valid, do the
  theorem's conditions match how it's actually applied, is the result novel, are bounds
  tight rather than vacuous? No formal claims -> mark **N/A**. Owned by Elrond. Full
  rubric in `references/empirical-gates.md`.

- **Gate S - Venue Scoring & Synthesis (conditional).** Fires only when a
  NeurIPS-style venue is named or a score/rating is requested. Translates the verdict
  onto the five-axis NeurIPS reviewer form (Soundness/Presentation/Contribution/Overall
  /Confidence). Owned by **Elrond** as part of verdict synthesis - the score aggregates
  the whole ladder and must sit inside the verdict's band. No score request -> mark
  **N/A**. Full rubric in `references/neurips-scoring.md`.

**Every gate has a reviewer.** Each gate is owned by one Council seat, who is
accountable for that failure mode. This keeps coverage total and the panel legible:

| Gate | Reviewer |
|---|---|
| Gate 0 Provenance & Integrity | Aragorn |
| Gate 1 Variance / Replication | Gandalf |
| Gate 2 Specification Robustness | Gandalf |
| Gate 3 Specificity | Gimli |
| Gate 4 Confound Control | Galadriel |
| Gate 5 Mechanism / Necessity | Gimli |
| Gate 6 Claim Calibration | Boromir |
| Gate 7 External Validity | Faramir |
| Gate 8 Measurement Validity | Galadriel |
| Gate 9 Reproducibility | Eowyn |
| Gate 10 Ethics / Safety | Treebeard |
| Gate 11 Analytic Integrity | Bilbo |
| Gate F Figure Integrity | Samwise |
| Gate M Multiverse Robustness (topic-conditional) | Gandalf |
| Gate T Theoretical Soundness | Elrond |
| Gate S Venue Scoring & Synthesis | Elrond |

(Legolas owns no numbered gate; he anchors novelty/prior-art, which feeds the
Contribution axis of Gate S.)

Mark each gate **PASS / FAIL / N/A** with the specific evidence (a recomputed
number, a `file:line`, a quote). N/A is allowed (a theory paper has no Gate 0; a
text-only draft has no Gate F), but say why.

**The degenerate all-N/A case.** For a pure position/theory/opinion paper, most or all of
the empirical gates (0-5, 7-9) will legitimately be N/A - there is no data to leak, no
seeds to vary, no sample to generalize. That is a valid, honest state, not a shortcut. The
review still runs: Gate 6 (claim calibration), Gate T if the work makes formal claims, the
Exposition pass (Samwise), and Legolas (novelty). The verdict then rests on calibration,
novelty, and argument quality rather than the empirical ladder - say so explicitly rather
than forcing empirical gates to apply where they don't.

**Quantitative error-analysis pass.** For every quantitative headline, run the
statistical robustness battery in `references/statistical-robustness.md` and show the
arithmetic. Name the error most at risk here: **Type I** (false positive: is the
"significant" result just `m x alpha` chances at the null? does it survive correction?
what is the binomial by-chance tail?) or **Type II** (underpowered null: what is the
minimum detectable effect size at this N? is the CI wide enough that "no effect" is
really "no power"?). Then run the hostile-reviewer hard checks the numbers permit:
reported-stat <-> p consistency (statcheck), SE/SD/CI coherence, GRIM/GRIMMER,
caliper/p-curve for p-hacking, Fisher-z CI on correlations, expected false discoveries
under FDR, positive predictive value at the true prior, leave-one-out fragility, and
the minimum-Bayes-factor / s-value translation of the headline p. Adjectives do not
substitute for the computed bound.

### 4. Convene the Council

Each seat attacks from one fixed angle. The full charge sheet is in
`references/council-seats.md`. The panel:

1. **Elrond - Convener & Statistician.** Verdict synthesis and statistical rigor.
2. **Gandalf - Replication Skeptic.** "Would this survive 20 seeds?"
3. **Aragorn - Provenance Auditor.** "Is this data real? Where is the noise ceiling?"
4. **Galadriel - Construct Validity.** "Does the metric measure what it claims?"
5. **Boromir - Overclaim Sentinel.** "Where did the claim outrun the data?"
6. **Gimli - Single-Instrument Devil's Advocate.** "Strip the favorite instrument. Does the finding stand?"
7. **Legolas - Literature Anchor.** "Is this novel? Do citations support the sentences they attach to?"
8. **Samwise - Figure & Exposition Auditor.** "Do the figures show, clearly and honestly, what the text claims? Is every contribution traceable to a result?" (Owns Gate F; fires figure duties only when figures are present. On a text-only target, contributes the exposition pass alone.)

Seats 1-8 are the standing panel (they sit on every review). Four **specialist seats**
convene when the design invites them; say in one line why each is seated or skipped:

9. **Faramir - External Validity.** "Does it hold beyond this one sample/model/site?" (Gate 7)
10. **Eowyn - Reproducibility & Open Science.** "Could someone else re-run it? Seeds, configs, code, data?" (Gate 9)
11. **Bilbo - Preregistration & Analytic Integrity.** "Was this confirmatory or exploratory? Where's the plan? Any HARKing?" (Gate 11)
12. **Treebeard - Ethics, Safety & Responsible Disclosure.** "Consent, licensing, dual-use, broader impact, subgroup harms?" (Gate 10)

Two adversarial disciplines apply to every seat: **steelman then break** (attack the
strongest honest reading, not a strawman), and **name the experiment that would
embarrass the author** (the specific plot/seed-sweep/ablation whose likely outcome
would sink the claim). The scariest such experiment is a candidate for "what would
change the verdict."

### 5. Orchestrate supporting skills

See `references/orchestration.md` for the routing table. In short:

- Novelty / prior-art → `literature-review` or `deep-research`
- Biomedical claims, citation verification → `pubmed-database`
- Scholarly-writing quality → `scholar-evaluation`
- Recomputing code/results → `verification-loop` (running the user's code is
  opt-in: ask or confirm first, per "Executing the user's code is opt-in" above)

### 6. Render the verdict

- **REJECT** - any Gate 0 failure, or the central claim collapses below what it asserts.
- **MAJOR REVISION** - plausibly real but a gate fails fixably.
- **ACCEPT** - all relevant gates pass and every claim's language matches its tier.

**Methodology-tier and conditional gates.** Gates 7-11 and Gate F do not all carry
the same weight as Gate 0, but they are not automatic MAJOR REVISIONs either:

- **Gate 0 failure is terminal** - REJECT regardless of everything else.
- **Gate 10 (ethics/safety) failure can be terminal on its own**, independent of
  technical quality - IRB/consent gaps, unaddressed dual-use risk, or licensing/PII
  problems can force REJECT or desk-reject-level treatment even when the empirical
  core is sound.
- **Gate 11 (analytic integrity) failure** - an exploratory result relabeled
  confirmatory forces re-scoping the claim (T3, not T5). This is usually **MAJOR
  REVISION**, not REJECT, since the fix is to re-scope the language rather than redo
  the study.
- **Single failures in Gates 7/8/9** (external validity, measurement, reproducibility)
  are usually **MAJOR REVISION** (fixable with an added test, a released recipe, or a
  reliability check) - not REJECT - unless the failure invalidates the central claim
  itself (e.g. the effect turns out to be a measurement artifact).
- **Gate F failure on a central claim** - a figure that contradicts a central claim is
  treated like a core Blocker (see Gate F rubric) and can move the verdict the same way
  a Gates 0-6 failure would.

Always end with **"What would change the verdict"**: name a single, concrete,
minimal experiment, analysis, or edit - not "do more validation." State its
expected outcome and the decision level it would move the work to if it
succeeds: "run X (N seeds / this control / this partial correlation); if it
shows Y, the verdict moves to ACCEPT [or MAJOR REVISION]." A vague direction is
not an answer here; a reviewer who cannot name the one check has not finished
walking the ladder.

**Verify the load-bearing finding first.** Before rendering REJECT or MAJOR
REVISION, identify the single load-bearing finding: the one Blocker/Major that
most drives the decision. Apply the same steelman-then-break discipline to that
finding that the Council applies to the work: steelman the authors' side, try to
refute your own finding, and confirm the evidence (recompute the number, re-read
the `file:line`, re-read the claim as actually stated). A verdict should never
hinge on an unverified finding. This is Gate 1's adversarial discipline turned on
the review's own decision.

**Coherence pass.** Immediately before emitting, reconcile the whole review for
internal consistency: the gate ladder PASS/FAIL, the Claim Ledger's actual
tiers, the Council's objections, the severity-ranked findings, and the verdict
must all agree with each other. A gate marked PASS while a seat raises a
Blocker on that same issue is a self-contradiction. A Claim Ledger "actual tier"
that a gate result contradicts (e.g. T4 "robust" next to a failed Gate 4) is a
self-contradiction. Fix these before output, not after - a review that ships
with a visible internal contradiction has not finished the job. When a
NeurIPS-style score is emitted, reconcile it too: Overall must sit inside the
verdict's band, Soundness must be ≤ 1 if any Gate 0 failed, and Confidence must
not exceed what the evidence supports (an abstained central number caps it).

When a target venue is known or given, the verdict may optionally be translated
into that venue's scale (e.g. a journal's accept/minor/major/reject scale), but the
ACCEPT/MAJOR REVISION/REJECT decision remains primary.

**NeurIPS-style scoring.** When a NeurIPS-style (or generic top-ML) venue is named,
or the user asks for a score/rating/"would this get in," translate the verdict onto
the five-axis NeurIPS reviewer form - **Soundness /4, Presentation /4, Contribution
/4, Overall /10, Confidence /5** - using the rubric and band-mapping in
`references/neurips-scoring.md`. Every axis must cite a gate result or a named finding
that already appears in the review; a score the ladder does not support is the
review's own overclaim. The Overall number lives inside the verdict's band (REJECT
1-4, MAJOR REVISION 4-6, ACCEPT 6-9), a Gate 0 failure caps Soundness at 1, and an
evidence-blocked central number caps Confidence. The scores translate the decision
for a venue; they never become the headline. Emit the score block from that reference
directly under the Verdict line, and reconcile the bands against the verdict in the
coherence pass.

## Calibrate the review itself

The review is subject to the same Type I discipline it applies to the work under
review. A confidently-stated finding you cannot support is the review's own false
positive.

- Every finding carries an explicit confidence (**High / Medium / Low**), or is
  marked **evidence-blocked** when the artifact does not provide what is needed to
  judge it.
- When evidence-blocked, **abstain** and name exactly what the author must provide
  (the missing seed sweep, the unreleased config, the absent CI) rather than
  guessing a severity to fill the slot.
- Do not inflate a Nit to a Blocker to look rigorous. Do not bury a Blocker as a
  Nit to be polite. Severity is a claim about the work, not a performance of scrutiny.

### Reviewer failure-modes self-guard

The review is itself an experiment, and these are its confounds. The Council must
self-check the same systematic biases it hunts for in the work under review:

- **Anchoring** (first impression fixes the verdict) -> form the verdict from the
  gate ladder, not the first read.
- **Elegance / halo** (a beautiful method waved through) -> an elegant method still
  must pass Gate 0-6; beauty is not evidence.
- **Confirmation** (finding the flaw you expected) -> run the steelman before the
  attack; let a clean gate be clean.
- **Severity inflation / harshness performance** (inflating nits to look rigorous)
  -> severity is a claim about the work, not a display of scrutiny.
- **Base-rate neglect** (assuming something must be wrong) -> "no objection" is a
  valid, honest seat entry; a strong work earns a fast ACCEPT.
- **Novelty / prestige / authorship bias** (over- or under-crediting by source) ->
  judge the artifact, not the byline.

## Output format

```
# Council Review - <title>

## Verdict: ACCEPT | MAJOR REVISION | REJECT

## NeurIPS-style score      (include when a NeurIPS-style venue is named or a score is asked; see references/neurips-scoring.md)
- Soundness:    _/4  - <gate/finding that fixes it>
- Presentation: _/4  - <...>
- Contribution: _/4  - <...>
- Overall:      _/10 - <one-line justification; must sit inside the verdict's band>
- Confidence:   _/5  - <why this and not higher/lower>
- Flags: reproducibility <YES/NO> · ethics <none/see Gate 10> · borderline <n/a or the tipping factor>

## Strengths
- <what is genuinely sound and should be preserved>
- <...>

## Claim Ledger
| # | Claim (as stated) | Asserted tier | Actual tier | Gate status |

## Gate Ladder      (each gate names its reviewer)
- Gate 0 Provenance ......... [Aragorn]  PASS/FAIL/N/A - <evidence>
- Gate 1 Variance ........... [Gandalf]  PASS/FAIL/N/A - <evidence>
- Gate 2 Spec Robustness .... [Gandalf]  PASS/FAIL/N/A - <evidence>
- Gate M Multiverse Robust .. [Gandalf]  PASS/FAIL/N/A - <evidence, or "N/A - not neuro/AI">
- Gate 3 Specificity ........ [Gimli]    PASS/FAIL/N/A - <evidence>
- Gate 4 Confound Control ... [Galadriel] PASS/FAIL/N/A - <evidence>
- Gate 5 Mechanism .......... [Gimli]    PASS/FAIL/N/A - <evidence>
- Gate 6 Claim Calibration .. [Boromir]  PASS/FAIL/N/A - <evidence>
- Gate 7 External Validity .. [Faramir]  PASS/FAIL/N/A - <evidence>
- Gate 8 Measurement ........ [Galadriel] PASS/FAIL/N/A - <evidence>
- Gate 9 Reproducibility .... [Eowyn]    PASS/FAIL/N/A - <evidence>
- Gate 10 Ethics/Safety ..... [Treebeard] PASS/FAIL/N/A - <evidence>
- Gate 11 Analytic Integrity  [Bilbo]    PASS/FAIL/N/A - <evidence>
- Gate F Figure Integrity ... [Samwise]  PASS/FAIL/N/A - <evidence, or "N/A - no figures">
- Gate T Theoretical Sound .. [Elrond]   PASS/FAIL/N/A - <evidence, or "N/A - no formal claims">
- Gate S Venue Scoring ...... [Elrond]   PASS/FAIL/N/A - <see NeurIPS-style score block, or "N/A - no score requested">

## Error Analysis            (per quantitative headline)
- Claim <n>: dominant risk = Type I | Type II; <the number that bounds it: m*alpha
  expectation / binomial tail / survivors after correction / MDES / PPV / fragility>;
  settle-it check = <the one recomputation that would resolve it>

## Council Objections      (Blocker | Major | Minor | Nit)
- **Elrond (stats):** ...
- **Gandalf (replication):** ...
- **Aragorn (provenance):** ...
- **Galadriel (construct validity):** ...
- **Boromir (overclaim):** ...
- **Gimli (single-instrument):** ...
- **Legolas (literature):** ...
- **Samwise (figures/exposition):** ...   (figure points only if figures present)
- **Faramir (external validity):** ...    (specialist; seat/skip with reason)
- **Eowyn (reproducibility):** ...        (specialist; seat/skip with reason)
- **Bilbo (analytic integrity):** ...     (specialist; seat/skip with reason)
- **Treebeard (ethics/safety):** ...      (specialist; seat/skip with reason)

## Severity-ranked findings
1. [Blocker | High] ... Fix: ...
2. [Major | Medium] ...
3. [Minor | High] ...
4. [evidence-blocked] ... Needed: <what the author must provide>

## What would change the verdict
<one concrete, minimal experiment/analysis/edit, its expected outcome, and the
decision level it would move the work to if it succeeds - e.g. "run the 20-seed
sweep on X; if d stays > 0.5, verdict moves to ACCEPT.">

## Evidence log
<citations, file:line refs, every recomputed number with its source>
```

**Development-stance add-ons** (include only when the stance is development; see
`references/paper-development.md`):

```
## Exposition pass
- Contribution traceability: <each claimed contribution -> its result/figure, or "no home">
- Argument-chain breaks: <abstract-promise-without-result / result-without-discussion / ...>
- "So what" in one sentence: <the significance a non-specialist would care about>

## Figure feedback (generative)   (only if figures present)
- <figure>: takeaway + the one edit that makes it land harder (caption/encoding/money-figure)

## Reviewer-2 pre-mortem
- Claim <n>: strongest objection -> [defensible now | fixable: <edit> | structural: <scope down / new work>]
```

## Operating principles

- **Recompute before you trust.** In artifact mode, verify every number you can.
- **Severity honestly.** A Blocker invalidates a central claim. A Nit is cosmetic.
- **Attack the work, support the author.** Every finding pairs with the fix.
- **Name the strongest work too.** Note what should be preserved, not only the flaws. A
  review that lists only faults miscalibrates the author about what actually works.
- **No verdict without the ladder.** The ladder is the empiricism; the rest is presentation.
