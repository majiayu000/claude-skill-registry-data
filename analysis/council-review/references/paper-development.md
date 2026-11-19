# Paper development - helping the work land, not just gating it

The gate ladder decides whether a finding is real. This file covers the other job
the Council does: helping a paper that is *still being written* become the strongest
version of itself. A review that only says "REJECT, Gate 1 fails" is a gatekeeper. A
review that also says "here is the paragraph to rewrite and the figure to add" is a
collaborator. The Council should be both, and it should know which one the user needs
right now.

## Two modes

Detect and state which mode you are in. When ambiguous, ask in one line.

- **Gatekeeper mode** (pre-submission / "is this real" / "tear it apart"). The bar is
  the verdict. Findings are ruthless, severity-ranked, and terminal where warranted.
  Development feedback is secondary.
- **Development mode** ("help me write this", "strengthen this section", "is my
  argument clear", a draft in progress). The verdict still runs, but the center of
  gravity shifts to **generative feedback**: every finding pairs with the concrete
  edit that fixes it, and the review adds an Exposition pass and a Reviewer-2
  pre-mortem the gatekeeper mode can skip.

The gate ladder and the Council seats run in **both** modes. Empirical rigor is not
optional just because the paper is a draft; catching a seed-variance problem early is
the most valuable thing development mode can do.

## Map findings onto the review criteria the paper will actually face

Real reviewers (NeurIPS-style venues, and most journals) score on a small fixed set
of axes. Translate Council findings into that language so the author can see the
review they are heading toward:

| Axis | The question a reviewer asks | Which Council machinery covers it |
|---|---|---|
| **Quality / Soundness** | Are the claims supported by the analysis/experiments? Honest about weaknesses? | Gates 0-6, all stat seats |
| **Clarity** | Is it clearly written and organized? Could an expert reproduce it? | Exposition pass, Gate F (figures), reproducibility check |
| **Significance** | Will people use or build on this? Does it advance understanding? | Legolas (novelty), "so what" test below |
| **Originality** | New insight, or novel combination? (need not be a brand-new method) | Legolas, hostile-retelling |
| **Limitations** | Are the limits stated honestly, not buried? | Boromir, limitations audit below |
| **Reproducibility** | Seeds, configs, data splits, compute, code available? | Aragorn, Gandalf, modern-ML checklist |

State, per central claim, the axis on which it is currently weakest. That is the axis
a reviewer will attack first.

## The Exposition pass (development mode)

Rigor can be perfect and the paper still fail because the argument doesn't track.
Check the argument chain, not just the numbers:

- **Contribution traceability.** Every contribution claimed in the intro should map to
  a specific result, and ideally a specific figure. List them. A contribution with no
  home in the results is a promise the paper doesn't keep.
- **Claim -> evidence -> interpretation.** For each result: is it stated, is the
  evidence adjacent, and is the interpretation separated from the evidence (not fused
  into it)? Fused claim-and-interpretation is where overclaims hide.
- **The "so what" test.** After the main result, can you answer "so what" in one
  sentence that a non-specialist would care about? If not, the significance is
  under-argued even if the result is sound.
- **Signposting & arc.** Abstract promises -> intro frames -> methods enable ->
  results deliver -> discussion interprets and bounds. Flag where the chain breaks:
  an abstract promise with no result, a result with no discussion, a discussion
  claiming more than the results.
- **Abstract discipline.** The abstract is a contract. Every sentence should be
  cashable by a specific result. Non-cashable abstract sentences are the first
  overclaim finding.

## Limitations audit

Reviewers reward honest limitations and punish buried ones.

- Are the real limitations stated, or only safe ones ("future work: more datasets")
  while the load-bearing weakness (N=4, single model, in-silico only) goes unmentioned?
- Does each limitation have a scope sentence that keeps the contribution intact
  ("this establishes X in-silico; the in-vivo claim is future work") rather than
  either hiding it or over-apologizing it away?

## Reviewer-2 pre-mortem (the most useful development output)

Before the paper meets a hostile reviewer, simulate that reviewer here. For each
central claim, write the **strongest objection a skeptical expert will raise**, then
the **rebuttal-ready response** the author should have loaded. Three outcomes per
objection:

1. **Defensible now** - the response exists; make sure it's in the paper.
2. **Fixable before submission** - name the analysis/figure/edit that neutralizes it.
3. **Structural** - it can't be answered without new work; the author must either do
   the work or scope the claim down to what survives.

This is the bridge between "here is what's wrong" and "here is the paper that
survives review." It is also the single feature that most helps the continuing
writing process: the author leaves knowing exactly which objections to pre-empt in the
next draft.

## Generative feedback discipline

In development mode, a finding without a fix is half-done. For each finding give:

- the fix (the specific edit, analysis, or figure), and
- why it strengthens the paper in reviewer terms (which axis it lifts).

Keep attacking the *claims* and supporting the *author*. The goal of development mode
is that the next draft is measurably harder to reject.
