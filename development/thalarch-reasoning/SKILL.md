---
name: thalarch-reasoning
description: >
  Adaptive deliberation layer for difficult engineering and design work. Use when a task is
  ambiguous, high-risk, multi-step, architecture-heavy, debugging-heavy, version-sensitive,
  cross-module, or otherwise likely to reward slower reasoning. Forces explicit problem framing,
  competing hypotheses/approaches, disconfirmation, independent challenge, evidence-based
  adjudication, uncertainty tracking, and a final falsifiable proof without exposing private
  chain-of-thought or adding ceremony to trivial work.
---

# Thalarch Reasoning Harness

The goal is not to imitate another model's writing style. The goal is to make the current model
behave more deliberately: delay commitment, separate facts from guesses, generate real alternatives,
seek disconfirming evidence, use independent contexts when useful, and stop only when the conclusion
is supported by evidence appropriate to the claim.

Do **not** expose private chain-of-thought. Externalize only compact decision artifacts: facts,
unknowns, candidate explanations, evidence, rejected alternatives, decisions, risks, and proofs.

## 1. Choose deliberation depth

Pick the smallest depth that fits the task.

### D0 — Direct

Use for trivial, deterministic, reversible edits with obvious scope.

- understand the exact request;
- make the smallest change;
- run the nearest check;
- stop.

No hypothesis theatre and no multi-agent ceremony.

### D1 — Guarded

Use for small but non-trivial work.

- frame the contract;
- identify the main assumption that could be wrong;
- inspect the relevant evidence;
- implement;
- verify.

### D2 — Deliberate

Default for meaningful debugging, feature, refactor, API/data, or design work.

Before commitment:

1. build a compact problem representation;
2. separate `FACT`, `INFERENCE`, and `UNKNOWN`;
3. generate at least two plausible explanations/approaches **when the problem genuinely has
   alternatives**;
4. state what evidence would falsify the leading candidate;
5. gather discriminating evidence;
6. commit only after weaker candidates are eliminated or explicitly dominated;
7. verify the selected path against acceptance criteria.

Do not manufacture a second option when the task is mechanically determined.

### D3 — Deep

Use for architecture, elusive regressions, concurrency, security-sensitive boundaries, broad
migrations, distributed/data correctness, major UI redesigns, or repeated failed attempts.

Add:

- independent specialist reasoning in a clean context;
- explicit contradiction/counterexample search;
- a pre-mortem: “If this fails in production, what assumption was most likely wrong?”;
- comparison of alternatives by evidence, reversibility, compatibility, and blast radius;
- an adjudication step that receives candidate conclusions and evidence, not persuasive narratives;
- cold verification after implementation.

### D4 — Critical

Use only when consequences or uncertainty justify the cost: destructive migrations, auth/security,
financial/data integrity, release-critical architecture, or a bug that survives several disciplined
hypotheses.

Add:

- two independent reasoning passes when practical;
- explicit invariants and failure modes;
- negative/adversarial tests or simulations;
- rollback/recovery thinking before mutation;
- independent final verifier with no access to implementer reasoning;
- unresolved uncertainty reported rather than hidden.

D4 is not “think forever”. It is stronger independence and falsification.

## 2. Build the problem representation first

For D2+ create a compact internal working packet:

- **Goal** — observable user outcome;
- **Constraints** — scope, compatibility, safety, forbidden changes;
- **Facts** — supported by repository/tool/runtime evidence;
- **Unknowns** — information that could change the decision;
- **Invariants** — behavior/contracts that must remain true;
- **Candidates** — plausible hypotheses/approaches;
- **Discriminators** — observations/tests that separate the candidates;
- **Proof target** — what must be true before completion can be claimed.

Do not start implementation merely because the first explanation feels plausible.

## 3. Hypothesis tournament

For debugging or diagnosis:

1. list the smallest set of plausible root-cause hypotheses;
2. rank them by explanatory power **and** how cheaply they can be falsified;
3. test the most discriminating observation first;
4. eliminate hypotheses explicitly when evidence contradicts them;
5. never quietly revive a rejected hypothesis without new evidence;
6. once one causal explanation dominates, design the smallest regression proof before fixing.

A symptom match is not a root cause.

After three disproven fix hypotheses, stop patching and reassess the model of the system, hidden
shared state, environmental assumptions, or architecture.

## 4. Alternative tournament

For architecture/design/refactor/implementation decisions where multiple paths are reasonable:

Evaluate candidates against the same contract:

- correctness / requirement fit;
- compatibility;
- blast radius;
- reversibility;
- operational complexity;
- testability / evidence strength;
- performance/security implications when relevant;
- consistency with existing project conventions;
- migration cost.

Always include the simplest viable option when it is genuinely plausible. Do not choose a more
complex architecture merely because it sounds sophisticated.

## 5. Disconfirmation before confirmation

For the current leading conclusion ask:

- What would make this wrong?
- Which assumption is least evidenced?
- Is there a counterexample in the code, logs, tests, runtime, or requirements?
- Could the same evidence support a different explanation?
- Am I mistaking correlation, sequence, or naming for causation?
- Is a remembered API/version fact being treated as current truth?

Prefer evidence that distinguishes candidates over evidence that merely agrees with the favorite.

## 6. First-answer resistance

For D2+ the first internally generated solution is provisional.

Before mutation, perform one challenge pass:

- restate the proposed change in one sentence;
- name the strongest reason it might be wrong;
- check that reason against evidence;
- only then proceed.

This is a cognitive forcing function against premature closure, not a requirement to produce long
visible analysis.

## 7. Independent contexts

Use independent subagents when independence adds information, not as a ritual.

Good uses:

- elusive root cause;
- architecture with meaningful competing approaches;
- security/concurrency/data-integrity review;
- adjudicating a disputed reviewer finding;
- visual/design critique where the producer's taste may bias self-review.

Give the independent reasoner:

- the requirement/problem;
- bounded repository paths/evidence;
- explicit constraints;
- the question to decide.

Do **not** give it the producer's chain-of-thought or conclusion unless the task is specifically to
critique that conclusion. Preserve independence.

## 8. Evidence-based adjudication

When multiple agents/candidates disagree, the orchestrator decides by:

1. documented requirement;
2. direct repository/runtime evidence;
3. reproducible test/log/tool result;
4. current primary documentation for version-sensitive external facts;
5. project conventions;
6. risk/reversibility when evidence remains incomplete.

Do not decide by verbosity, confidence, senior-sounding language, or majority vote alone.

If evidence cannot distinguish candidates, keep the uncertainty explicit and choose the safest
reversible experiment when authorized.

## 9. Reasoning state compression

Long tasks lose quality when the model repeatedly reconstructs the problem from conversation memory.
Maintain a compact state packet:

- `FACTS`;
- `UNKNOWNS`;
- `ACTIVE HYPOTHESES`;
- `REJECTED HYPOTHESES + EVIDENCE`;
- `DECISIONS + RATIONALE`;
- `INVARIANTS`;
- `NEXT DISCRIMINATING CHECK`;
- `VERIFICATION STATUS`.

Update this packet after meaningful evidence. Reuse it after context compaction instead of restarting
reasoning from scratch.

## 10. Tool-first epistemics

Use tools to reduce uncertainty instead of reasoning harder about facts that are inspectable.

Examples:

- version/API uncertainty → inspect manifests and current primary docs;
- control-flow uncertainty → search/read actual callers;
- regression uncertainty → Git history/diff/test;
- runtime uncertainty → logs/reproduction/profiling;
- visual uncertainty → rendered screenshot/image inspection;
- data/query uncertainty → real schema/query plan/integration boundary.

Reasoning is for interpreting evidence and choosing experiments, not replacing available evidence.

## 11. Uncertainty calibration

Use three states internally and in user-facing conclusions when relevant:

- **KNOWN** — directly supported;
- **LIKELY** — best explanation but not fully proven;
- **UNKNOWN / UNVERIFIED** — evidence missing or inaccessible.

Do not upgrade `LIKELY` to `KNOWN` because implementation succeeded once. Do not hide unknowns to
make the report sound confident.

## 12. Stop conditions

Stop deliberating when:

- one candidate is supported and meaningful alternatives are falsified or dominated;
- acceptance criteria are executable and the implementation path is sufficiently bounded;
- further reasoning would only repeat existing evidence;
- the next uncertainty can only be resolved by a user/domain decision or unavailable environment.

Then act or report the blocker.

Do not create infinite self-review loops.

## 13. User-visible output

Do not dump hidden reasoning or internal monologue.

When useful, expose only:

- the decision;
- the key evidence;
- important alternatives rejected and why;
- residual risk/uncertainty;
- verification result.

The user should receive a stronger answer, not a transcript of the model thinking.
