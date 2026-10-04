---
name: thalarch-autoresearch
description: >
  Runs bounded evidence-driven experiment loops for measurable optimization, repeated hypothesis
  testing, agent/prompt tuning, benchmark improvement, difficult debugging with a stable evaluator,
  and implementation search. Establishes a reproducible baseline, changes one causal surface at a
  time, measures under comparable conditions, keeps only demonstrated improvements, reverts failed
  candidates, records an experiment ledger, protects correctness guardrails, and stops on budget or
  convergence. Never self-modifies durable rules, merges, releases, force-pushes, or broadens scope
  merely to improve a score.
---

# Thalarch Autoresearch

Autoresearch is a **bounded engineering experiment protocol**, not permission for an agent to edit
indefinitely until a number happens to look better.

Use it when the task has a meaningful evaluator and several plausible changes can be tested against
that evaluator. The loop must remain subordinate to the user's scope, repository rules, correctness,
safety, and external-action boundary.

## 1. Activation gate

Use this skill when at least one is true:

- the user asks to optimize a measurable property;
- several plausible implementations can be compared objectively;
- a performance/build/startup/latency problem has a reproducible benchmark;
- a difficult bug has repeated falsifiable hypotheses and a stable reproduction/test;
- an agent, prompt, skill, heuristic, or workflow is being tuned against a frozen evaluation set;
- an existing benchmark suite can discriminate candidate changes.

Do **not** activate merely because a task is difficult. Prefer ordinary `thalarch-debug`,
`thalarch-performance`, `thalarch-test`, or `thalarch-code-craft` when one well-supported change is
enough.

Do not run an optimization loop when the evaluator is subjective, easily gamed, unstable, or
materially weaker than the real requirement. Improve the evaluator first or keep the result
`UNVERIFIED`.

## 2. Research contract

Before the first candidate, freeze a compact contract:

- **objective** — what real outcome should improve;
- **primary metric** — exact name, unit, direction (`minimize` or `maximize`);
- **minimum improvement** — smallest change worth keeping;
- **noise tolerance** — range inside which results are treated as inconclusive;
- **correctness guardrails** — tests, invariants, compatibility, resource ceilings, visual or API
  constraints that must not regress;
- **baseline scenario** — exact command/workload/input/environment/cache state;
- **search scope** — files/modules/configuration surfaces that may change;
- **experiment budget** — maximum candidates, elapsed effort, or both;
- **external-action boundary** — whether branch/push/PR or other side effects are authorized;
- **stop conditions** — success target, convergence, repeated failure, unstable evaluator, or budget.

If changing the primary metric, workload, guardrails, or environment would make comparison invalid,
close the current series and establish a new baseline instead of pretending the runs are comparable.

## 3. Baseline gate

A candidate may not be judged until the baseline is credible.

1. Prove the exact evaluator command/scenario from repository evidence.
2. Run the correctness guardrails before optimization when execution is available.
3. Measure the baseline under the same conditions intended for candidates.
4. Repeat enough times to detect obvious noise when the metric is noisy.
5. Record environment/toolchain/cache state that materially affects comparability.

If baseline variance is larger than the expected improvement, reduce noise, widen the threshold, use
better aggregation, or mark small differences `INCONCLUSIVE`.

Never compare cold vs warm, debug vs release, different test sets, different devices, changed
network conditions, or otherwise different work and call the difference an improvement.

## 4. Hypothesis selection

Each candidate starts with one concise falsifiable hypothesis:

`Because <evidence>, changing <one causal surface> should improve <metric> without violating <guards>.`

Prefer experiments with high information value:

1. eliminate unnecessary work or obvious duplicated cost;
2. test the suspected bottleneck or causal boundary directly;
3. use ablation/toggle/binary-search experiments when they discriminate competing explanations;
4. prefer reversible, local changes before broad redesign;
5. change one causal surface at a time when practical.

Do not produce random parameter sweeps without a reasoned search space. Do not bundle unrelated
changes that make attribution impossible.

After three disciplined hypotheses fail, rebuild the problem model with `thalarch-context`,
`thalarch-debug`, `thalarch-doubt`, or an independent deliberation role instead of making tiny
variations of the same guess.

## 5. Workspace isolation

Preserve the user's working state.

- inspect Git status before experimentation;
- never overwrite unrelated dirty work;
- prefer a temporary branch/worktree/workspace for candidate mutations when the host supports it;
- do not run two mutation experiments against the same files concurrently;
- keep read-only research/review parallel only when it cannot change experiment state;
- never use destructive reset/clean/force operations as an automatic rollback mechanism.

A rejected candidate should be reverted by the safest host-native mechanism that restores only the
candidate's intended changes.

## 6. Experiment loop

For each candidate, in order:

1. assign an experiment id;
2. record hypothesis and expected discriminator;
3. apply the smallest candidate change;
4. run the cheapest guardrail that can fail fast;
5. run the exact comparable evaluator;
6. run remaining guardrails required by the contract;
7. classify the evidence with the deterministic decision gate when compatible;
8. `KEEP`, `REVERT`, or mark `INCONCLUSIVE`;
9. append the result to the ledger;
10. if kept, the candidate becomes the new baseline and evidence invalidated by the mutation must be
   rerun before completion.

### Decision semantics

- **KEEP** — primary metric improves by at least the configured meaningful threshold, the change is
  outside the noise band, and every required guardrail passes.
- **REVERT** — any required guardrail fails, the metric materially regresses, the candidate violates
  scope/compatibility, or the mechanism is disproven.
- **INCONCLUSIVE** — the difference is too small relative to threshold/noise, evidence is incomplete,
  or the environment changed enough to break comparability.

Never call an inconclusive candidate a win because its single best run looks favorable.

When available, use `scripts/experiment_gate.py` for the numeric KEEP/REVERT/INCONCLUSIVE decision.
The helper deliberately does not edit Git, run commands, or publish anything.

## 7. Correctness outranks score

Optimization is lexicographic:

1. user scope and safety;
2. correctness/compatibility guardrails;
3. primary objective;
4. secondary cost and complexity.

A faster implementation that fails a regression test is not a candidate improvement. A higher
benchmark score achieved by deleting required behavior, narrowing the workload, weakening tests,
changing expected output, skipping security checks, or exploiting evaluator artifacts is rejected.

For performance work, combine this skill with `thalarch-performance`. For behavior search, use
`thalarch-test`. For causal bug exploration, use `thalarch-debug`.

## 8. Avoid benchmark overfitting

When tuning prompts, agents, skills, ranking heuristics, or general-purpose engineering behavior:

- freeze the evaluation set before the series;
- keep at least one holdout scenario when practical;
- do not inspect hidden expected outputs during candidate generation;
- prefer improvements that explain failures across several cases;
- reject brittle special cases whose only justification is one benchmark item;
- re-run a holdout/generalization check before promoting a durable generic change.

A generic Thalarch rule or skill should not self-modify from one successful task. Durable skill
changes require evidence that the lesson generalizes beyond the producing case.

## 9. Self-improvement boundary

Autoresearch may **propose** changes to Thalarch skills, prompts, routing, heuristics, or evaluation
logic when that is the user's task. It must not silently rewrite its own durable instructions while
solving an unrelated repository task.

Before promoting a generic skill/process change:

1. identify the repeated failure class;
2. derive the candidate rule from evidence, not one anecdote;
3. test it against multiple representative cases when available;
4. include at least one holdout or counterexample that could expose overfitting;
5. inspect whether the new rule conflicts with existing user/repository/platform precedence;
6. require independent review/cold verification for the durable change.

Use `thalarch-compound` for verified reusable lessons, but persist them only where the user or the
project has authorized a durable knowledge sink.

## 10. Experiment ledger

Keep a compact ledger rather than narrative chain-of-thought.

For every experiment record:

- id;
- baseline id;
- hypothesis;
- changed surface/files;
- evaluator command/scenario;
- primary metric before/after;
- noise/threshold assumptions;
- guardrail results;
- decision: `KEEP` / `REVERT` / `INCONCLUSIVE`;
- evidence paths/log ids when available;
- concise lesson or next discriminator.

Do not store private reasoning. Store only decision-relevant artifacts and evidence.

## 11. Search discipline

Prefer causal search over brute force:

- ablation before addition when unnecessary work may be the cause;
- binary search over ordered configuration spaces;
- one-factor-at-a-time while locating a sensitive surface;
- small factorial comparisons only when interactions are genuinely plausible and budget allows;
- profiling/tracing before tuning many knobs;
- explicit stopping when marginal gains fall below the meaningful threshold.

Do not spend the entire budget polishing a local maximum if evidence points to a different
architecture or bottleneck. Conversely, do not escalate to architecture because two tiny candidates
failed.

## 12. Stop conditions

Stop the loop when any applies:

- success target is reached and guardrails pass;
- budget is exhausted;
- recent candidates are below the meaningful improvement threshold;
- the evaluator becomes unstable or non-comparable;
- three disciplined hypotheses fail without a new discriminator;
- further improvement requires scope expansion not authorized by the user;
- the remaining change is high-risk/destructive and needs a new authorization boundary.

Stopping with `UNVERIFIED` or “no demonstrated improvement” is valid. Continuing until something
looks positive is not.

## 13. Completion

Before reporting success:

- rerun the final relevant guardrails after the final kept mutation;
- run the final comparable evaluator against the accepted baseline;
- inspect the final diff for accidental experiment residue;
- remove/revert rejected candidates and temporary instrumentation unless it is part of the accepted
  solution;
- report baseline, final metric, guardrail status, experiments kept/rejected/inconclusive, and any
  residual uncertainty;
- use `thalarch-git` only for publication actions the user explicitly authorized.

The final claim is **“demonstrated under this contract”**, not “globally optimal”.
