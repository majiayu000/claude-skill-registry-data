---
name: honest-conjecture-resolution
description: >-
  Drive a hard mathematical conjecture toward resolution across competing proof
  routes while staying epistemically honest: test the right adversaries,
  distinguish false claims from lossy tools, reduce to named crux lemmas,
  calibrate evidence, develop reusable theory and standalone contributions,
  avoid route proliferation, and keep ledgers/drafts/
  dashboards synchronized. Use for multi-round open-problem campaigns,
  plateau audits, proof/disproof alternation, side-route decisions, subagent
  packet design, and converting route state into readable mathematical drafts.
  Load targeted references only when needed.
---

# Honest Conjecture Resolution

This skill selects and reviews work on hard conjectures. `conjecture-explorer` handles computational
experiments; `proof-developer` handles proof construction. This skill owns campaign progress and
stopping rules, including when those other skills are used. User-defined goals and budgets govern.

## Load References On Demand

Use this main file for every campaign round. Load only the relevant reference file when the task
needs detail:

- `references/adversaries-and-proxies.md`: adversary design, proxy failures, assembly traps, exact
  dual targets, and compute hygiene.
- `references/state-compression.md`: proof-contract accounting, plateau gates, route walkback,
  consolidation, side quests, and subagent discipline.
- `references/methodological-pivots.md`: native-structure audits, census/proxy/local-to-global
  failure modes, stronger-statement quarantine, and perspective-pivot triggers distilled from
  prior campaigns.
- `references/artifact-discipline.md`: ledgers, side drafts, dashboards, inventories, generated
  outputs, and source-of-truth synchronization.
- `references/existing-results.md`: finding earlier campaign and related-repo results, comparing
  statements, preserving provenance, and distinguishing new contributions from rediscovery.
- `references/full-playbook.md`: historical material, not an additional operating checklist. Current
  instructions in this file and the focused references supersede its workflow rules.

## When To Use

- A conjecture has several candidate routes, live subclaims, or possible counterexample families.
- A route looks numerically robust but lacks a proof.
- A bound or proxy is growing and you need to decide whether the target is false or the tool is lossy.
- The campaign is plateauing, looping through reductions, or expanding the dashboard without closing
  proof debt.
- Subagents or side quests may help, but only if their contracts are precise and mergeable.
- The ledger has become chronological clutter and needs conversion into a current-state proof map.

## Cardinal Rules

1. **Lossy bound does not mean false target.** Measure the actual target and the proxy separately.
   A proxy can grow while the theorem remains true.
2. **Numerical robustness is not proof.** Robust tests count only against the right adversaries and
   should be paired with a proved analytic core or a precise reduced lemma.
3. **A counterexample has a scope.** Verify the witness and identify the claim it refutes. Explain
   which live decision changes. Refuting another convenient shortcut is not automatically progress
   toward the user's goal; do not minimize or vary a witness without a reason that affects the goal.
4. **Every active claim needs a status.** Use `proved`, `reduced`, `conditional`, `verified
   computationally`, `plausible`, `stalled`, or `refuted`. Avoid “morally” or “essentially” proved.
5. **Test the vulnerable indispensable step early.** Work backward from the conclusion, check cheap
   eligibility conditions, and attack the uncertain step before developing its routine consequences.
   For constructions, distinguish producing a witness from admissible inputs from proving those
   inputs exist jointly. Preserve the choices allowed by the target. See the input-existence audit
   in `references/methodological-pivots.md`. Alternate proof and falsification where informative.
6. **Recognize both conjecture progress and reusable theory.** Track direct advances separately
   from general tools, structural understanding, decision-changing learning, local results, and
   verification. A new theory can be a substantive research outcome before its implication for the
   original conjecture is known. State its scope and demonstrated mathematical value; definitions,
   page counts, and parameterized versions of a niche example do not establish that value alone.
7. **Give exploration room, then select.** A bounded creative pass can end without a theorem.
   Continued investment needs either a credible route toward the conjecture or a worthwhile theory
   objective within the user's research scope, a useful next test, and a reason to prefer it to
   alternatives. Theory milestones may concern new objects, operations, or structural laws; they
   need not be smaller versions of the conjecture. See `references/state-compression.md`.
8. **Enumeration needs a purpose.** Complete finite coverage when the user requests it or it closes
   a proved finite reduction. For a structural goal, extending a census needs a discriminating test
   or a credible path to a reusable principle. More cases alone do not justify the next range.
9. **Do not flatten away native structure.** Before importing a generic theorem, proxy, or local
   criterion, record which data it preserves and which it forgets. Signs, colors, paired layers,
   endpoint provenance, quotient/gauge choices, and global compatibility often carry the theorem.
10. **Preserve correctness; control overhead.** Fix errors and preserve evidence promptly. Promote
    results and update derived views according to relevance and actual status changes, not a ritual
    of producing new TeX, dashboard nodes, and skill rules every round.

## Check Existing Results Before Investing

When configured, use `research-knowledge` to sync the shared index and read a bounded context bundle
for the current task at campaign start/resume. Search it across campaign and sibling sources, then
inspect original proofs and corrections. Register substantive writeups as internal packets; keep
result cards and source fingerprints current. Use direct source searches for gaps in index coverage.
Apply that skill's bounded recovery procedure when retrieval fails; do not repeat unchanged failing
index calls every round.

Before a substantial attempt or reopening a route, search the current campaign's earlier results
and failures, relevant sibling repositories, and the shared literature. After a handoff or
compaction, recover the linked result map before selecting work. Search statements, equivalent
formulations, and older terminology; the latest dashboard and the literature catalog do not cover
all campaign artifacts. Inspect source proofs and later corrections before importing a claim.

Before reporting a new result, compare it with the closest existing statement: hypotheses,
quantifiers, conclusion, and proof mechanism. Cite the original source and identify the actual
addition. Rediscovery counts as reuse or verification, not a new theorem or a reset of the last
advance. A new proof, extension, or application can matter; state exactly what changed. Reuse recent
search coverage for unchanged work rather than rescanning all repos every turn. For the search and
recording procedure, read `references/existing-results.md`.

## Minimal Campaign-State Invariant

Before another serious round, the active ledger opening should answer:

```text
Current exact target:
What would constitute completion, including coverage/quantifiers:
Last goal advance (with round/date) and remaining essential obligations:
Active theory objective and last reusable mathematical advance, if applicable:
Current route, last exact reduction, and key proved inputs:
Existing-result map and related-repo sources checked (link); actual unresolved difference:
First unproved indispensable implication; supplied inputs and choices the method freezes:
Why this route is preferable now; proposed new ingredient:
Next test, possible outcomes, and decisions they would change:
Effort spent since route review; next review point:
Parked mechanisms and evidence needed to reopen them (link):
```

If this does not fit in one screen, consolidate before proving more lemmas.

## Round Contract

Use a short entry in the existing ledger for a significant attempt. Reuse unchanged context rather
than copying the whole campaign state:

```text
Before: conjecture obligation or theory capability sought; reason to pursue it; decision to resolve;
        closest existing results/failures (links) and intended addition;
        first unproved implication, supplied inputs and allowed choices;
        proposed new ingredient; cheapest useful test; effort limit and stop condition.
After: new statement or capability; evidence/confidence; conjecture effect and theory effect;
       decision changed; first unproved implication remaining;
       contribution beyond prior work, or reuse/verification; effort used; next action or reopening.
```

Count effort against the same unresolved implication across names, turns, workers, and compactions,
both per route and for the campaign. Use available elapsed time, compute, or substantive attempts;
do not invent cost estimates or completion percentages. Local
results, maintenance, and route switches do not reset the campaign review counter. Track the last
conjecture advance and last theory advance separately; progress on one need not advance the other.

At strategy selection, set a review point. Default to a review after four substantive attempts,
including attempts on different routes, sooner if a test fails or cost exceeds the stated allowance.
This is a review trigger, not a claim that hard proofs should take four attempts. Compare continuing, changing the
mechanism, and returning to the original formulation. Renew a difficult route when concrete new
evidence improves its prospects; a renamed lemma or another variant of the same failure is not
enough. Record the review outcome: continue with a named new reason and test, change mechanism,
pursue a distinct theory objective within scope, or hold with a reopening condition. Apply that
outcome to the next assignment. See `references/state-compression.md` for the review procedure.

## Proof-Debt Table

For each active theorem-level target, maintain rows like:

```text
Claim:
Relation to objectives: equivalent / necessary / sufficient / special-case / independent theory / heuristic
Status: proved / refuted / reduced / computational / plausible / stalled / open
Evidence:
Missing implication:
Smallest falsifier profile:
Next decisive test:
```

Most rabbit holes start when a sufficient condition is refined as if it were equivalent. Track the
direction on every arrow.

## Core Operating Loop

1. State the user's research objectives. Locate the route's contribution to a solution or identify
   the general tool or theory being developed on its own merits, with its connection to the objects.
2. At route selection or review, compare two or three materially different approaches by potential
   payoff, evidence, hardest missing step, and cost of a discriminating test. Do not redo this menu
   during every implementation step.
3. Choose a bounded creative pass, proof attempt, adversarial experiment, exact literature match,
   or consolidation. Use delegation only when authorized and useful for independent work.
4. Check existing results and prerequisites, then run the most informative test or proof step with
   compute hygiene. Reuse a matching proof or witness instead of reconstructing it by default.
5. Record what is proved and what decision changes; apply the route review even if local output
   keeps appearing. Correctness work remains required regardless of its strategic classification.
6. Update the authoritative status and evidence. Update linked views when their displayed claims
   change; promote selected results to a manuscript under `references/artifact-discipline.md`.

## Mode Selection

- **Need to test a lemma or search for witnesses:** use `conjecture-explorer`; read
  `references/adversaries-and-proxies.md` for adversary patterns.
- **Proxy or bound looks wrong:** read `references/adversaries-and-proxies.md`; measure proxy and
  target separately.
- **Dashboard/ledger is growing faster than theorem progress:** read `references/state-compression.md`.
- **A case split, census, or classification table is expanding:** read
  `references/state-compression.md`; run the census-pivot audit before adding more cases.
- **A route keeps using generic proxies, local tests, or broad imported theorems:** read
  `references/methodological-pivots.md`; run the native-structure and local-to-global audits before
  adding another lemma.
- **The campaign may need a change of perspective:** read `references/methodological-pivots.md`;
  consider the whole target or a solved analogue in a bounded discovery pass. Select an import,
  abstraction, dual formulation, or invariant search for a concrete consequence in the original
  problem; report inconclusive discovery honestly.
- **Delegation is authorized and useful:** read `references/state-compression.md`; assign independent
  evidence contracts rather than asking multiple agents to elaborate the same route.
- **Need an exact literature match or theorem import:** use `shared-literature` first to search
  local extracted results and project notes, then `literature-reviewer` for any web search still
  needed. Reuse or reserve the packet in the common library, preserve precise statements and
  separate project context, refresh the shared index, and link results from the ledger/dashboard.
- **Need to clean route records or write a readable synthesis:** read
  `references/artifact-discipline.md`.
- **Need dashboard format/rendering details:** use the `conjecture-dashboard` skill.

## Compute Hygiene On EC2

The EC2 instance also serves the research site and may host other work.

- Start small, estimate memory/CPU growth, and scale gradually.
- Before launching any nontrivial numerical computation, read `MemAvailable` from `/proc/meminfo`
  and set `prlimit --as` to at most 75% of that value. Do not include swap in the budget and do not
  rely on swap to finish a run.
- Prefer a bounded, lower-priority launch such as:
  ```bash
  mem_cap=$(awk '/MemAvailable:/ {printf "%.0f\n", $2 * 1024 * 0.75}' /proc/meminfo)
  nice -n 10 prlimit --as="$mem_cap" --cpu=3600 -- uv run python scripts/explore_foo.py ...
  ```
- Limit worker counts; do not launch several all-core or high-memory jobs at once.
- Use timeouts, sample limits, chunking, checkpointing, or symmetry reduction.
- Stop jobs that start swapping, peg all cores for too long, or threaten server responsiveness.

## Exit Criteria

A round may end with a proved result, a verified refutation, a bounded inconclusive attempt, or a
completed review. Report the result's effect on the original goal separately from its mathematical
status. Continuing a route requires a concrete next step within its current allowance or a recorded
renewal at review. A local plateau does not by itself establish that the original problem is
impossible, out of reach, or resolved. Follow the user's instructions about continuing the campaign.
