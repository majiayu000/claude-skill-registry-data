---
description: >
  Run the full autonomous research pipeline end-to-end: investigate the
  literature, discover a solution via parallel explore-exploit branches,
  write an evidence-tagged paper, and verify every claim. The ScientistOne
  pipeline as one command.
argument-hint: "\"<topic>\" [--task digits] [--branches 5] [--iterations 2] [--offline] [--votes 1]"
disable-model-invocation: true
---

# /research — end-to-end pipeline conductor

You (the main agent) are the orchestrator. Drive the pipeline below in order.
The filesystem is the message bus: pass the run directory path in every
subagent task message; expect each subagent to end with
`{"ok": ..., "outputs": [...], "notes": ...}`.

Arguments received: `$ARGUMENTS`

## 0. Scaffold the run

```
python3 .claude/scripts/new_run.py $ARGUMENTS
```

Capture the printed run id; RUN = `workspace/runs/<run-id>`. Read
`RUN/run-config.json` for B (branches), I (iterations), offline flag, topic.
If new_run.py fails, report and stop.

## 1. Investigate

Launch the `problem-investigator` subagent: task message = run directory,
topic, offline flag; ask for `brief.md` + `bibliography.jsonl` +
`literature/` + `investigation/` per its protocol.
- If it returns `ok: false` (relevance gate ABORT), report the reason to the
  user and STOP the pipeline.
- Then: `python3 .claude/scripts/bib_validate.py RUN` must pass.
- Ledger: `python3 .claude/scripts/ledger.py append '{"event":"stage_investigate","detail":"complete"}'`

## 2. Discover — I iterations of Parallel Explore-Exploit

For each iteration `iN` in i1..iI:

1. **Ideate**: launch `ideator` (run dir, iteration, B; from i2 also point it
   at all previous distilled-feedback.md files — the ideator then applies
   top-K retention: p1..pK refine the previous iteration's top-K surviving
   branches). Expect `iterations/iN/ideas.md` + `proposals/p1..pB.md`.
   Ledger event `stage_ideate`.
2. **Solve — PARALLEL**: launch ALL B `solver` subagents IN ONE SINGLE
   MESSAGE (one Agent call per branch). Each task message: run dir, its own
   branch dir `iterations/iN/branches/bK/`, its proposal `proposals/pK.md`.
   Never launch solvers sequentially.
3. **Evaluate — PARALLEL**: after all solvers finish, launch B `evaluator`
   subagents in one message (one per branch). Expect `eval.json` per branch.
4. **Audit — PARALLEL**: launch B `auditor` subagents in one message.
   Expect `audit.md` per branch.
5. **Rank + Select** (you, the orchestrator): read every branch's eval.json +
   audit.md. Disqualify audit-FAIL branches. Write
   `iterations/iN/ranking.md`: table (branch, proposal one-liner, score,
   audit verdict, rank) + selection rationale.
6. **Distill feedback** (you): invoke the `distill-feedback` skill (Skill tool,
   `skill: distill-feedback`) and write `iterations/iN/distilled-feedback.md`
   with exactly its section template — do not improvise the format from
   memory; the next ideator round consumes this file. Ledger event
   `stage_iteration_iN`.

After the last iteration: pick the best surviving (audit-PASS) branch across
ALL iterations by official score. Copy its `solution.py`, `eval.json`,
`solve.log`, `plan.md` into `RUN/best/` and write `RUN/best/SELECTED.json`:
`{"iteration": "iN", "branch": "bK", "score": <score>}`.
Ledger event `stage_discover` complete.
If ZERO branches survive audits in all iterations, report and stop.

Then launch `ablation-analyst` (run dir) → `best/ablations/{ablations.json,
ablation.md}`; ledger event `stage_ablation`. Ablations are secondary
evidence — on `ok: false`, record and continue; never block the pipeline.

## 3. Write paper

1. Launch `paper-writer` with stage=conceive → `paper/research-representation.md`.
2. Run `python3 .claude/scripts/ground_check.py RUN` — if exit 1, relaunch
   paper-writer (stage=conceive, "fix every non-SUPPORTED check in
   paper/ground-report.json") once and re-run ground_check. If it still
   fails, STOP and show the user the unsupported list — never compose a draft
   on an ungrounded representation.
3. Launch `paper-critic` → `paper/critic-report.md`.
4. Launch `paper-writer` with stage=resolve-compose → `paper/draft.md`.
5. Convergence round (Ground→Critic→Resolve, max 2 rounds total): if the
   critic report contained any BLOCKER, relaunch `paper-critic` against
   `paper/draft.md`. If BLOCKERs remain, relaunch `paper-writer`
   (stage=resolve-compose) once more with them, then stop regardless
   (plateau) and report residual issues honestly.
Ledger event `stage_write_paper`.

## 4. Verify claims

1. `python3 .claude/scripts/extract_claims.py RUN`
2. Launch `claim-verifier` → verdicts in `paper/claims.jsonl` +
   `paper/verification-report.md`. If `run-config.json#verifier_votes` is
   N ≥ 2, follow the best-of-N vote protocol in the `verify-claims` skill
   instead of a single launch (sequential verifier launches interleaved with
   `verdict_votes.py snapshot`, then `verdict_votes.py merge`).
3. If any claim is FAIL: launch `refiner`; then re-run
   `python3 .claude/scripts/verify_claims.py RUN`; if FAILs remain, one more
   refiner round (max 2), then accept honestly reported residuals.
4. Copy the final draft: `paper/draft.md` → `final/paper.md`.
5. `python3 .claude/scripts/chain_of_evidence.py RUN` — the four integrity
   checks. Ledger event `stage_verify`.

## 5. Report

Summarize for the user: run id, best branch + official score, grounding
ratio (paper/ground-report.json), claim tally, chain-of-evidence table
result, and the path `RUN/final/paper.md`. Mention `/paper-to-latex` if they
want a .tex/PDF.
