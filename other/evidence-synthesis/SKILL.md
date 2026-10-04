---
name: evidence-synthesis
shapes: [evidence-synthesis]
description: >
  Turn a pile of sources into a defensible claim. Use for "what does the literature
  actually say?", conflicting studies or benchmarks, "is this result trustworthy?",
  arguments that need claim-evidence-warrant structure, qualitative data needing
  coding, or a theory with no catalog of its own contradicting evidence.
portable:
  package: zetetic-reasoning
  references: [cochrane, darwin, feynman, gadamer, geertz, laplace, strauss, toulmin]
---

# Evidence Synthesis

**Problem shape:** multiple sources (papers, benchmarks, interviews, texts)
must be combined into one graded conclusion — and the current draft cherry-picks,
skips heterogeneity, or has no explicit warrant connecting evidence to claim.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [cochrane](../../agents/genius/cochrane.md) | studies must be systematically found, graded, and pooled; publication bias suspected; effect sizes needed, not vote-counting |
| [toulmin](../../agents/genius/toulmin.md) | an argument needs explicit claim-evidence-warrant structure with qualifiers and rebuttals; standards differ by field |
| [feynman](../../agents/genius/feynman.md) | a result is suspiciously clean; a citation is used without the ability to rederive it; integrity audit before publishing |
| [darwin](../../agents/genius/darwin.md) | evidence accumulates over a long horizon; the theory needs a difficulty book of its own contradictions; hardest case first |
| [laplace](../../agents/genius/laplace.md) | evidence must update a belief quantitatively — priors, likelihoods, calibration |
| [gadamer](../../agents/genius/gadamer.md) | sources must be interpreted, not just counted — pre-understandings audited, the charitable reading found first |
| [strauss](../../agents/genius/strauss.md) | qualitative data (interviews, tickets, reviews) needs open/axial coding until saturation, not anecdote-picking |
| [geertz](../../agents/genius/geertz.md) | the evidence is behavior in context — thick description and emic vs etic separation before conclusions |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. Every synthesized claim carries its evidence grade and
   its strongest known counter-evidence (coding-standards §8: no source, no claim).
4. Typical chain: cochrane grades the corpus → toulmin structures the argument
   → feynman audits the integrity. Run via
   `tools/genius-invoker.sh compose cochrane toulmin -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The conclusion is fixed in advance and only supporting sources are wanted.
- Primary sources are unavailable and only summaries-of-summaries exist —
  say "I don't know" rather than synthesize hearsay.
