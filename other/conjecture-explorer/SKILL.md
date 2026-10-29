---
name: conjecture-explorer
description: Explore and test mathematical conjectures computationally before attempting proofs. Use this skill when the user formulates a conjecture, hypothesis, or pattern and wants to test it on small cases, search for counterexamples, enumerate structures, or build computational evidence. Designs bounded, decision-relevant experiments, distinguishes exact evidence from unresolved searches, and connects computational findings to proof attempts.
---

# Conjecture Explorer

Use computation to learn something that changes the mathematical next step. In a campaign,
`honest-conjecture-resolution` owns strategy selection, progress accounting, and route reviews.
Computation can help formulate or falsify a conjecture; it is not a prerequisite for every proof.

## Define The Experiment Before Coding

State the claim with its quantifiers, input class, parameters, and conclusion. Identify what is
already known and the unresolved decision. For each possible result, say what action it would support.
If success and failure would both lead to the same larger search, reconsider the experiment.

Choose ranges and resource limits from the task and known costs; clarify only when missing user
information matters. Distinguish these purposes:

| Purpose | Suitable experiment | What it can establish |
|---------|---------------------|-----------------------|
| Refute a universal claim | Targeted adversaries and boundary cases; exhaustive small cases when useful | One verified counterexample refutes the exact claim. Passing cases do not prove it. |
| Find an existence witness | Structured construction or bounded search | A verified witness proves existence under the checked hypotheses. |
| Distinguish mechanisms | Examples on which candidate explanations predict different outcomes | Evidence for selecting or rejecting those explanations. |
| Solve a finite reduction | Complete enumeration with justified coverage | The finite claim, if all cases and checks are exact and complete. |
| Explore asymptotics | Parameter families that distinguish proposed growth laws | Finite-range evidence, not an asymptotic theorem. |
| Test a correspondence | Explicit maps and inverse tests on small instances | Diagnostics; equal counts alone do not establish a bijection. |

For an agent-proposed auxiliary claim, explain why it is plausible and how it serves the conjecture
or a general theory objective. Experiments may test the laws of a new operation, natural scope of a
representation, or consequences of an emerging invariant before a return to the conjecture is known.
Do not invent easily refuted shortcuts just to produce another counterexample.

## Check Cheap Preconditions First

Before an expensive search, verify that the selected input actually belongs to the intended class
and lacks any easy certificate that makes the question moot. Try cheap exact identities, invariants,
and witness constructions before branching over many dependent cases.

A greedy procedure may supply a valid positive certificate; its failure need not certify a negative
answer. A timeout, state limit, heuristic failure, incomplete enumeration, or memory limit is
`unknown`, not `false`. Keep these outcomes distinct in output and downstream decisions.

For an existence target, record which choices the search permits changing. Distinguish failure for
fixed auxiliary data from exclusion of every allowed choice; the latter needs complete coverage or
a valid nonexistence certificate. Known-positive inputs can calibrate a new construction or falsify
a stronger supplier claim, but passing them does not enlarge the known positive domain.

## Implement The Mathematical Test

Use `explore_<topic>.py` for working scripts and run them with `uv run python`. Prioritize transparent
mathematical logic over software polish. Reuse a trusted representation when possible.

- State the conjecture, tested domain, coverage assumptions, and stop condition in the script.
- Validate on simple positive, negative, and degenerate examples before scaling.
- Check target and proxy separately. Preserve data the claim depends on.
- Report concise summaries; save enough detail to reconstruct any witness and inspect why it works.
- For random experiments, record the seed and sampling restrictions. For exhaustive claims, explain
  completeness and any symmetry reduction.
- Stop at a decisive result unless additional computation serves a separately stated question.

When a computation becomes proof evidence, replay the certificate or check the result through a
meaningfully different formulation where feasible. Repeating the same predicate twice is not
independent verification. Match verification effort to the claim's importance; do not build a large
test suite around disposable exploratory code.

## Execute Within Resource Limits

Start with small parameters to check implementation and estimate growth. Scale only when the next
range could change the decision or is required for the specified finite coverage.

- Be a good EC2 citizen: do not saturate CPU or memory with unconstrained searches. Start with small
  limits, estimate memory growth before scaling, and avoid launching several heavy jobs at once.
- Before any numerical run that could grow beyond a trivial toy case, check current RAM with
  `/proc/meminfo` and set a hard address-space cap no larger than 75% of `MemAvailable`; do not
  count swap as usable memory. A standard launch pattern is:
  ```bash
  mem_cap=$(awk '/MemAvailable:/ {printf "%.0f\n", $2 * 1024 * 0.75}' /proc/meminfo)
  nice -n 10 prlimit --as="$mem_cap" --cpu=3600 -- uv run python explore_<topic>.py ...
  ```
- If the resulting cap is too small for the intended run, shrink the parameters, stream/chunk the
  computation, checkpoint intermediate output, or ask before using a larger fraction of RAM. Do not
  rely on swap to finish a search.
- If the script supports worker counts, set a conservative value instead of using every core. Use
  timeouts, `prlimit --cpu`, or explicit max-parameter limits for exploratory runs.
- If a job starts swapping, consuming all cores for a long time, or threatening the shared web/server
  workload, stop it and restart with smaller parameters, chunking, checkpointing, or a sampled search.

## Interpret And Act

**A counterexample:** verify all hypotheses and the failed conclusion, then revisit the claim's role
in the proof. Minimize it only if minimality matters to the user's goal, the explanation, or a next
experiment. A repair needs a structural reason and a surviving implication toward the goal; do not
automatically add conditions until a formerly useful conjecture becomes irrelevant.

**No counterexample within the tested domain:** report the exact domain, whether coverage was
exhaustive, and which plausible failure mechanisms were tested. Use the observed structure to attempt
a proof or design a qualitatively different adversary. Do not extend the range merely because all
previous cases passed.

**Unknown or inconclusive:** report the limit and remaining uncertainty. Consider a better certificate,
representation, or proof argument before allocating more compute. Further search needs a reason to
expect useful information; running out of resources does not prove nonexistence.

**A new pattern:** state a conjecture and its purpose. Test it against examples that could distinguish
it from existing explanations before treating it as a new active route.

## Stop And Hand Off

Stop when the decision is resolved, the stated allowance is exhausted, or more of the same experiment
would only repeat existing evidence. User-requested enumeration and proved finite reductions remain
valid reasons to complete an entire range.

Preserve the precise claim, evidence scope, script command, useful witnesses, and any mechanism
suggested for a proof. State what advanced in the conjecture, reusable theory, or route selection. For a
promising proof step, use `proof-developer`; do not wait for an arbitrary amount of computational
confirmation. Record negative routes compactly so a renamed variant does not restart the same search.
