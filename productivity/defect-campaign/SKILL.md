---
name: defect-campaign
description: Turn a selected Radar defect cluster into a bounded discovery specification using existing ATE, fuzz, oracle and replay assets, then triage evidence for separately approved remediation. Use for Radar-to-campaign planning or explicitly approved discovery; not for strategy-only findings or automatic repair.
---

# Defect campaign

Start with one selected Radar report/cluster and produce a reviewable experiment contract.
Radar recommends; it neither proves a bug nor authorizes execution. Reuse its
[verification-asset handoff](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/3-weekly/radar/SKILL.md#sibling-recommend-the-repos-own-verification-assets),
landed in [PR #946](https://github.com/HiQS-Labs/XYZ-forge/pull/946).
This skill adds instructions, not another engine, scheduler or repair loop.

## Suitability and ownership

Pin the target repository, source SHA, report/cluster signature, prior counterexamples and
results. Record live issue/PR reads with UTC observation time separately from source revision.
Read current repo guidance and inspect existing issues, PRs and local owners before proposing
work. In XYZ, use the existing prior_art_recon utility and read-only `tick claims --json` in
relevant maintained/active clones; inspect driver locks, processes and task checkout state.
An empty fresh clone's claim log is not global clearance. Unknown or overlapping ownership
means hold and report the owner/dependency; never steal claims or modify peer work.

Choose by problem class, with a concrete target, falsifiable invariant, safe fixture and useful
oracle. If one is missing, return a held specification naming the gap rather than run anyway.

| Problem | Existing asset to inspect | Limit |
|---|---|---|
| CLI grammar/input boundaries | [fuzz_engine.py](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/py/fuzz_engine.py): seeded argv mutation/replay | Error text or exit status alone may be expected refusal |
| Configuration/environment interactions | [adaptive_ate.py](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/py/adaptive_ate.py): constrained pairwise grid | Pairwise coverage does not establish higher-order sequence coverage |
| State transitions, resume, concurrency | Structured operation sequences with a domain adapter and semantic predicate; inspect [domain_oracles.py](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/py/domain_oracles.py) | Containment, idempotence and crash-recovery checks do not prove business semantics; generic argv mutation supplies no stateful adapter |
| Documentary drift, prioritization, strategy | Analysis and existing review workflow | Do not force a fuzz campaign |

Reuse [gen4_campaign.py](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/py/gen4_campaign.py)
when its argv/clone contract fits; use [repro_builder.py](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/py/repro_builder.py)
for compatible argv/environment minimization. Its default reproduction predicate is return
code plus optional output substring, not an arbitrary semantic oracle. Missing adapters or
predicate integration are future separately scoped work, never an implied implementation task.
[ATE](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/4-occasional/ate/SKILL.md)
and [#435](https://github.com/HiQS-Labs/XYZ-forge/issues/435) provide existing variation/offline-clone
precedent; [#460](https://github.com/HiQS-Labs/XYZ-forge/issues/460) provides disposition context.

## Specify before requesting execution approval

Keep one contract in the existing task/results record, with:

- Target SHA, owner, report link, hypothesis and a precise semantic oracle/falsifier; distinguish
  expected refusals from defects. Specify known-failing and clean controls and their expected
  observations. Identify retained source evidence for each; do not claim unrun controls passed.
- Allowed input mutations/operation sequences, fixture reset boundary, sanitized environment,
  offline dependency stubs, seed and immutable corpus snapshot; exclude production/shared state.
- Exact commands, dependencies and permitted effects. Set finite wall-time, total case/mutation,
  per-command timeout, batch/corpus and no-new-signal limits, reserving replay/minimization and
  cleanup time inside the total budget. Never inherit a multi-hour default without approval.
- Disposable standalone full clones (not primary or linked worktrees), host/sandbox identity
  baselines, owned process groups and verified descendant cleanup. Reuse existing process-group
  facilities such as [proc_group.py](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/py/proc_group.py).
  Check actual nested process behavior: an outer process group alone does not contain a child
  that starts its own session. If existing controls cannot meet the contract, hold; build no adapter.
- Stop on containment/identity violation, surviving processes, invalid observations or oracle,
  missing dependency, exhausted budget or the declared repeated no-new-signal limit. Preserve
  evidence and clean only owned disposable state; do not retry by increasing budgets.

Obtain explicit operator approval for this bounded execution and permitted effects before
running discovery. Planning or invoking this skill is not campaign approval. Every individual
new CI test, case, assertion or parametrization requires its own explicit operator approval;
approving discovery does not approve synthesis or turning discovery inputs into CI cases.
No new suites, fixtures or registry entries by default. Preserve [#1131](https://github.com/HiQS-Labs/XYZ-forge/issues/1131):
no full development-suite preflight or repeated full gate; follow current qualification policy.
Older SOP/ATE instructions for auto-filing, new regression tests, full preflight or fixes do
not supersede these boundaries. No automatic fix, push, merge, deployment, issue closure or
schedule activation. Any external filing or publishing needs separate explicit authorization.

## Verify current CLI safety before an approved run

Read the exact pinned source and `--help` first, without invoking a default mode. Currently
`gen4_campaign.py` defaults to `--mode suite`, and synthesis defaults ON. Discovery must use
explicit `--mode run --no-synth`, with all approved numeric/target bounds supplied; omit
`--tier2-cmd` and `--heal-generator-cmd`. Verify those omissions still disable model/healing
paths at the inspected revision. Keep automatic filing off: omit ATE `--gh-repo` and do not
invoke `compile_issue.py`, filing helpers or auto-filing wrappers. If safety flags/semantics
have drifted or cannot be established, stop and revise the contract before execution.

Inspect the exact target allowlist; do not blindly accept defaults or include `validate.sh`:
mutated arguments can launch a full gate. The campaign's duration is checked between batches
and replay/cleanup can extend it; host violations are recorded, not necessarily immediate
abort conditions. Do not present telemetry as enforcement. Use existing supervision and
verified timeouts/cleanup that satisfy the approved stops, or hold execution as unsupported.
Recheck live/local ownership immediately before launch. No campaign is authorized by this doc.

## Replay, classify and hand off

Replay each candidate on the pinned revision, then minimize using the **same semantic
predicate**, not a weaker error hash/exit code. Verify clean controls still pass and failing
controls still fail. If the existing minimizer cannot preserve the predicate, retain the
unminimized observation and name that limitation; do not invent semantic coverage.
Retain exact argv/operation sequence, input/corpus snapshot, source/tool versions, sanitized
environment/dependency versions, outputs and relevant timing/interleaving plus before/after
state. A seed alone is insufficient for stateful or concurrent replay. Report flakiness honestly.

Dedupe by target + violated invariant + root cause against live issues, PRs, prior results and
active local owners; hashes are candidate grouping only. For **every** counterexample record
an accountable owner, evidence link, replay result, severity/real-world impact and disposition:
new defect, known rediscovery, expected refusal, flaky/inconclusive observation, or faulty oracle.
Promptly surface critical/high impact for review; defer lower severity unless selected. Link
back to the Radar tracking context or existing results issue within authorized destinations;
otherwise return the proposed backlink/update for approval. Do not silently file duplicates.

A report may contain zero defects. State exercised, excluded and unresolved coverage and
budgets actually used; a clean bounded run never proves an entire bug class eradicated.
Remediation is separately approved through existing start-task/review ownership. Preserve
before/after reproduction evidence if a later authorized fix is made. This skill never
implicitly authorizes that fix, a CI addition or consequential follow-up.

## Held pilot specification: merge-batch stale captured state

Source: [Radar #1138](https://github.com/HiQS-Labs/XYZ-forge/issues/1138) and
[#1143](https://github.com/HiQS-Labs/XYZ-forge/issues/1143); source inspected at
`e93214feb45dc95f32ee2d9080c1d4f6f3b8ab69`. Relevant existing seam:
`skills/2-daily/merge-cleanup/scripts/batch_record.py` (`extend`, `landed`, `qa_pending`,
`continuable`) and `merge_cleanup.py` batch selection/sweep inputs.

**HELD, not executable:** #1140 batch persistence/orchestration and #1136 accepted-start work
are active/excluded at the 2026-10-18 intake inspection. #1133 stays paused. Refresh tracker and
local ownership before reconsidering; first reuse #1140's eventual counterexamples and landed
revision. No competing pilot, adapter, fixture or bug repair is part of this skill delivery.

Proposed hypothesis: refresh of an unlanded PR updates overlap inputs without rewriting landed
history; a fresh execution cannot hide matching pending QA. Oracle compares refreshed planned
file sets to the observed PR snapshot, preserves landed order/merge identity and requires QA
coverage for all landed identities before continuation. A failed post-merge refresh must
retain verified merge identity; repeated equivalent reads/recomputations preserve semantics.

Controls specified, **not run**: reuse #1073's stale-overlap counterexample (changed unlanded
file set) and #1084's QA-bypass/merge-identity-loss evidence as known-failing historical controls,
after resolving their exact pre-fix revisions/artifacts. Clean controls: unchanged unlanded file
set and fully QA-covered landed set with no pending PR changes; expected stable semantics and
no pending QA. Reuse existing gh436/gh534 assets only; no permission to add CI cases/assertions.

Proposed budget for later approval: at most 12 declared operation sequences, 30 seconds per
sequence and 10 minutes total, with the last 4 minutes reserved for replay/minimization/cleanup;
stop after 3 consecutive sequences with no new signal or any safety/observation failure.
Use sanitized offline tracker snapshots in an owned standalone clone, no live merge/push/API
writes. Preserve each snapshot and operation/interleaving trace; seed-only replay is rejected.
A structured-state adapter and predicate-preserving replay/minimization integration are missing:
generic campaign argv mutation cannot provide them. These are future separately reviewed work;
until suitable existing assets are identified, the pilot stays held even if ownership clears.
