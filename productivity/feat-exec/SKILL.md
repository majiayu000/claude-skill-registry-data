---
name: feat-exec
description: >
  Use when the user wants to execute an existing pwdev-feat action plan — 'executar o plano
  user-crud', 'exec latest', 'rodar o plano', 'retomar a execução'. Dispatches the executor
  (subagent when the runtime has one, inline otherwise) in IMPLEMENT or REPORT mode, handles
  NEEDS_ADVICE with the advisor, and supports --resume. Do NOT use to create plans
  (feat-feature, feat-backend, feat-frontend, feat-test, feat-review) or for tasks without a
  plan (feat-quick).
metadata:
  version: 3.2.1
---

# Execute plan

You orchestrate; the executor implements. Dispatch mechanics per runtime and the inline
fallback: `references/runtime.md`. Prompts: `references/spawn-contracts.md`.

Arguments: `<slug>` or `latest` (default), optional `--resume`.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Load** — `python3 "<plugin-root>/scripts/feat_state.py" precheck <slug|latest>`.
   - `PLAN_NOT_FOUND` → show how to create one (feat-feature / feat-backend / feat-frontend /
     feat-test / feat-review) and stop.
   - `already_executed` with no `resume_step` → warn and ask whether to re-run.
   - `resume_step` present → offer to resume from that step (implied by `--resume`).
3. **Lint** — `python3 "<plugin-root>/scripts/plan_lint.py" <plan>`. Errors → show them and
   stop (suggest fixing the plan with the skill that created it). Warnings → mention them.
4. **Working tree** — `dirty_planned_files` not empty → list them and ask whether to proceed
   (the executor may commit them). Note `branch`; on the default branch, ask before
   committing there.
5. **Memory (optional, read-only)** — if `.planning/memory/MEMORY.md` exists (curated by
   pwdev-code; never write there), pick ≤3 entries by keyword overlap with the plan
   (`convention` first; 1 hop via `[rel: ...]` within the cap) into a RELEVANT MEMORY block.
6. **Confirm with the human** (gate):
   ```
   📋 Executing plan: {plan}
   Type: {type} | Mode: {IMPLEMENT | REPORT (no commit)} | Runtime: {runtime} ({subagent|inline})
   Objective: {objective}
   Files: {N} | Criteria: {N} | Steps: {N}{ | resuming at step n}
   Base commit: {sha}
   Proceed? (y/n)
   ```
7. **Record** (audit on): `sh "<plugin-root>/scripts/audit-log.sh" event exec "" started <plan> "<MODE>"`.
   **Dispatch the executor** with the executor prompt (full plan, MODE, SLUG, BASE COMMIT,
   PLUGIN ROOT, LANGUAGE, context documents for the plan type, RELEVANT MEMORY, and
   `RESUME FROM STEP n` when resuming). Model per `references/model-profiles.md` (key
   `feat-executor`). Record: `sh "<plugin-root>/scripts/audit-log.sh" spawn exec ""
   pwdev-feat:executor <model|inherited|inline>`. No subagent mechanism → follow
   `references/executor-contract.md` inline yourself.
8. **React to the ≤10-line status** (never open the reports unless the status requires it):
   - Blocked-write fallback: if the reply carries `--- BEGIN FILE <path> ---` blocks, write each
     content verbatim to its path (only paths under `.planning/feat/features/{slug}/`), and make
     sure `plan.done.md` exists, rendered from `templates/plan.done.md` with its
     `<!-- feat-status: ... -->` marker; note in the Deviations that the orchestrator persisted it.
   - `COMPLETE` / `CAVEATS` → step 9.
   - `STOPPED:<condition>` → present it and wait for the human.
   - `NEEDS_ADVICE` → at most ONE consultation per plan: dispatch the advisor with the advisor
     prompt (advice request + plan §1/§2/§7; key `feat-advisor`), log
     `audit-log.sh event exec "" advice_requested` and `... advice_given`, then re-dispatch the
     executor with the ADVICE block. `NEEDS_ADVICE` again → present to the human and stop.
   - `FAILED` → re-dispatch ONCE with the retry block; fails again → stop and report both notes.
   Advice and retry counters are independent: at most 1 advice + 1 retry per plan.
9. **Record** the outcome: `sh "<plugin-root>/scripts/audit-log.sh" event exec "" <completed|failed>
   <plan> "<STATUS>"` (`completed` for COMPLETE/CAVEATS, `failed` otherwise). **Check the tree**:
   `git status --porcelain --untracked-files=all` — report any change outside `.planning/` left by
   the run instead of hiding it.
   **Present**:
   ```
   ✅ Plan {slug} executed — {COMPLETE | CAVEATS | FAILED} ({IMPLEMENT | REPORT})
   Commit: {hash | none — findings at .planning/feat/features/{slug}/{review.md | test-audit.md}}
   Report: .planning/feat/features/{slug}/plan.done.md
   👉 Next: feat-review {base_commit}..HEAD   (IMPLEMENT only)
   ```

## Prohibitions

- Never implement code yourself while a subagent mechanism is available — dispatch the executor.
- Never execute without the human's confirmation at step 6.
- Never commit in REPORT mode.
- Never paste `plan.done.md` or the findings file into your context — status lines only (the
  blocked-write fallback is written straight to disk, not summarized).

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
