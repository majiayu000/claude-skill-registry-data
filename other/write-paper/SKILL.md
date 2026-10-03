---
description: >
  Run (or re-run) Stage 3 only — the Paper Writer pipeline: CONCEIVE (LLM) →
  GROUND (deterministic script) → CRITIC (fresh-context LLM) →
  RESOLVE+COMPOSE (LLM) producing the evidence-tagged paper draft. Requires
  best/SELECTED.json from /discover.
argument-hint: "[--run <run-id>]"
disable-model-invocation: true
---

# /write-paper — Stage 3: CONCEIVE → GROUND → CRITIC → RESOLVE → COMPOSE

Arguments: `$ARGUMENTS`

Current state: !`python3 .claude/scripts/ledger.py status`

Preconditions: resolve the run (`--run` or ACTIVE_RUN); `best/SELECTED.json`
and `best/eval.json` must exist — otherwise stop and point to `/discover`.

1. **CONCEIVE**: launch `paper-writer` (stage=conceive, run dir). Expect
   `paper/research-representation.md`, fully evidence-tagged.
2. **GROUND**: `python3 .claude/scripts/ground_check.py <run>`.
   - Exit 1 (grounding ratio < 0.85): relaunch `paper-writer`
     (stage=conceive) once with instruction "fix every non-SUPPORTED check in
     paper/ground-report.json". Re-run ground_check; if still failing, stop
     and show the unsupported list to the user.
3. **CRITIC**: launch `paper-critic` (run dir). Expect
   `paper/critic-report.md`.
4. **RESOLVE + COMPOSE**: launch `paper-writer` (stage=resolve-compose,
   run dir). Expect `paper/draft.md` with all tags intact.
5. **Convergence round** (the paper's Ground→Critic→Resolve loop, max 2
   rounds, terminating on convergence — zero blockers — or plateau): if
   step 3's report contained any BLOCKER, relaunch `paper-critic` against
   `paper/draft.md`. If BLOCKERs remain, relaunch `paper-writer`
   (stage=resolve-compose) once more with them; then stop regardless and
   report residual issues honestly.
6. Ledger: `python3 .claude/scripts/ledger.py append '{"event":"stage_write_paper","detail":"draft complete, ratio=<r>"}'`

Report: grounding ratio, critic issue count (blockers), draft section list.
Next stage: `/verify-claims`.
