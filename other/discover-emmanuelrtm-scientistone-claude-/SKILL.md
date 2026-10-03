---
description: >
  Run (or re-run) Stage 2 only — Discovery: Ideator plus Parallel
  Explore-Exploit branches (Solve → Evaluate → Audit → Rank+Select →
  distilled feedback), for the configured number of iterations. Requires
  brief.md from /investigate.
argument-hint: "[--run <run-id>] [--iterations N]"
disable-model-invocation: true
---

# /discover — Stage 2: Ideator + Parallel Explore-Exploit

Arguments: `$ARGUMENTS`

Current state: !`python3 .claude/scripts/ledger.py status`

Preconditions: resolve the run (`--run` or ACTIVE_RUN); `brief.md` and a
valid `bibliography.jsonl` must exist — otherwise stop and point to
`/investigate`. Read B and I from `run-config.json` (`--iterations` here
overrides I; create missing `iterations/iN/branches/bK` dirs as needed).

For each iteration iN:

1. Launch `ideator` (run dir, iN, B, prior `distilled-feedback.md` files if
   any — also from previous /discover invocations). Expect `ideas.md` +
   `proposals/p1..pB.md`. From i2 on the ideator applies top-K retention
   (p1..pK refine the previous iteration's top-K surviving branches).
2. Launch ALL B `solver` subagents IN ONE MESSAGE — one Agent call per
   branch, each given only its own `iterations/iN/branches/bK/` dir and
   `proposals/pK.md`. This parallel fan-out is the point of PEE; sequential
   launches are a protocol violation.
3. When all solvers are done: launch B `evaluator` subagents in one message.
4. Then B `auditor` subagents in one message.
5. Rank + Select (you): read all eval.json + audit.md; audit-FAIL branches
   are disqualified regardless of score; write `iterations/iN/ranking.md`
   (table + rationale).
6. Distilled feedback (you): invoke the `distill-feedback` skill (Skill tool,
   `skill: distill-feedback`) and write `iterations/iN/distilled-feedback.md`
   with exactly its section template — never improvise the format.
7. Ledger: `python3 .claude/scripts/ledger.py append '{"event":"stage_iteration_iN","detail":"best=<branch>:<score>"}'`

After the final iteration: select the best audit-PASS branch across all
iterations, copy `solution.py`, `eval.json`, `solve.log`, `plan.md` to
`best/`, write `best/SELECTED.json` `{"iteration":"iN","branch":"bK","score":<s>}`,
append ledger event `stage_discover`. If nothing survived audits, report and
stop.

Then **Ablation**: launch `ablation-analyst` (run dir). Expect
`best/ablations/{ablations.json, ablation.md}`; ledger event
`stage_ablation`. Ablations are secondary evidence for the paper — on
`ok: false`, record the failure and continue; never let ablation block the
pipeline. Show the user the final scoreboard (+ ablation deltas if present).

Next stage: `/write-paper`.
