---
name: causal-explanation
description: Prepare a substantive, source-backed causal account of an existing behavior, incident, or historical design decision when reconstructing and documenting the evidence is the selected deliverable. Do not trigger for routine rationale, explanation of your own recommendation, ordinary technical questions, current-task updates, or active failure diagnosis.
---

# Causal Explanation

Answer the selected causal question with evidence calibrated to the claim. Keep
observed facts, source-backed inference, competing explanations, and unknowns
distinct. Do not turn an explanation request into implementation work.

## Route The Request

- Bind the question to the exact behavior, decision, regression, threshold, or
  tradeoff. Infer the referent from current context only when the interpretation
  is safe; otherwise ask one targeted question.
- Use `jcode` for a symbol lookup, file map, caller trace, or adjacent source
  context. Use the repo's QA intake or attribution lane for reproducing,
  diagnosing, or attributing an active failure, including a request to find an
  unknown root cause. An established cause alone does not select this skill;
  use it when reconstructing and documenting the causal account is the selected
  deliverable, or when the user explicitly invokes it.
- Use the applicable architecture or performance skill when the requested
  outcome is a design review or benchmark judgment rather than an explanation.

## Build A Proportionate Evidence Record

1. Include firsthand user reports and relayed client updates as evidence;
   preserve their uncertainty and distinguish observations from causal claims.
   Do not demand independent corroboration merely because the user is the source.
   Identify the existing sources that can answer the question. Choose the
   cheapest authoritative evidence; pure historical recall uses memory first,
   while a current mechanism may be settled directly from source or an artifact.
2. Consult only sources likely to resolve the causal question. Use `jcode` for
   source structure and callers, `jdocs` for authored documentation or reference
   trees, direct QMD retrieval plus `get` or `multi_get` for exact prior wording
   or history, and `jdata` only when tabular evidence is material. Consult a
   relevant issue or review connector only when current evidence points there.
   Do not require an all-source sweep or enumerate and sweep connectors.
3. Record each source actually consulted. Mark relevant searches that returned
   nothing, unavailable sources that leave a material gap, and deliberately
   omitted categories whose evidence could not affect the answer.
4. For a regression, compare relevant successful and failed runs under like
   source/build, input, scenario, and environment conditions, and inspect the
   intervening changes. Completed qualification and later successes constrain
   the claim; timing is a hypothesis, not proof of cause.

Code shape and runtime behavior can establish mechanism. They do not, by
themselves, establish the motivation, rejected alternatives, or original
intent. Attribute motivation only to an explicit source; otherwise label it as
an inference or competing hypothesis.

## Calibrate The Explanation

Separate the result into the smallest useful set of these categories:

- **Direct observations:** current behavior or explicit source statements with
  precise citations.
- **Causal inference:** the evidence chain connecting observations to the
  proposed explanation. State the confidence and why it is warranted.
- **Alternatives:** explicitly rejected alternatives when the record says so;
  otherwise plausible competing hypotheses with evidence for and against.
- **Gaps:** contradictions, empty searches, unavailable evidence, and questions
  the record cannot answer.

Do not manufacture certainty. If the evidence proves mechanism but not
motivation, say exactly that. Prefer a bounded `unproven` conclusion to a
smooth story.

## Output Contract

Lead with the supported answer or the fact that the cause is not proven. Then
give the direct evidence, causal chain, material alternatives, gaps and
confidence, and a compact sources-consulted record. Omit empty presentation
sections when their absence cannot hide uncertainty.

If this explanation belongs to an already selected implementation task, return
the resulting preserve, change, avoid, and verification constraints to that
same task. Do not create a ticket, next prompt, thread, worker plan, or successor
task. Completion is terminal unless the user has already selected further work.

For source and license details, read
[references/provenance.md](references/provenance.md) only when auditing this
skill's provenance.
