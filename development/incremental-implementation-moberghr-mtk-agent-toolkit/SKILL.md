---
name: incremental-implementation
description: Use when executing an approved multi-file implementation to ensure each batch compiles, tests, and stays within the approved manifest.
type: skill
license: MIT
compatibility:
  - claude-code
  - codex
user-invocable: false
---

# Incremental Implementation

## Overview

Implement in thin slices. Each slice must compile, test, and remain explainable before moving on.

## When To Use

- Any approved multi-file implementation
- Refactors that still require verification
- Any task where the cost of late failure is high

### When NOT To Use

- Single-file, single-function changes already minimal enough for the fix workflow

## Workflow

1. Before each batch, re-read the shared references that batch's files match (`context-engineering` step 3).
2. Implement only the files listed for the batch, with the smallest correct change.
3. Write the tests in the same batch, failing first where the batch adds or fixes behavior (see **Batch policy** below).
4. Run the batch checkpoint using the build and test commands from the active tech stack skill's `## Build & Test Commands`.
5. **Capture analyzer output.** Write the build output to a log, then feed the log
   to the build diagnostics parser. (No `tee /dev/tty`: agent shells have no
   terminal, so it fails.) The parser ships with the plugin; resolve it
   plugin-first, then the project copy:
   ```bash
   # Example for .NET (adapt command from tech stack skill's Build & Test Commands):
   PBD="${CLAUDE_PLUGIN_ROOT}/hooks/parse-build-diagnostics.sh"; [ -f "$PBD" ] || PBD=hooks/parse-build-diagnostics.sh
   mkdir -p .mtk; rc=0; dotnet build > .mtk/build.log 2>&1 || rc=$?; tail -n 30 .mtk/build.log
   [ -f "$PBD" ] && bash "$PBD" --file .mtk/build.log > .mtk/analyzer-output.json; [ "$rc" -eq 0 ]
   ```
   Surface any critical analyzer findings immediately — they block the batch just like
   build failures. Warning-level findings carry forward to the pre-commit review.
   If the parser resolves nowhere, skip this step.
6. Read `.claude/references/pre-commit-review-list.md` if present and fix any violations immediately.
7. Mark the batch complete in `tasks/todo.md`. Record the per-batch gate decision and progress on the workflow artifact **in the same shell call as the checkpoint test run** — `<test cmd> && "$WFA" batch "$MTK_WF_UUID" gate phase_exit_gate pass --reason "batch <id> green" -- set results.batches_completed=<n> -- checkpoint --next "<next batch id: intent>" --verify "<test cmd> => <result>"` (`checkpoint` must be the LAST op; exit 3 means `--next` names a finished unit — fix it and re-run `checkpoint` alone; on red: `|| "$WFA" gate … fail …` to trigger remediation). A standalone bookkeeping turn is a wasted turn. Also checkpoint when a PR is opened, before waiting on a usage limit (`--wait-until <ISO>`), and when the context guard nudges. See `.claude/references/orchestration-gates.md`.
8. **Churn check:** After completing each batch, run `git diff --stat` and count net lines changed **since the last review** (intermediate or Phase 4), **excluding generated and mechanical files** — lockfiles, `*.Designer.cs`, `*.g.cs`, `*.generated.*`, EF migration snapshots, `*.min.js`/`*.min.css`, built bundle output (e.g. `wwwroot/dist/**`). Generated churn is not review load. Thresholds are `MTK_CHURN_REVIEW_LINES` (default **300**) and `MTK_CHURN_HALT_LINES` (default **500**); at rigor HIGH/MAX — the subagent path or the inline-MAX profile — the defaults **double** to 600/1000, because every batch there is already isolated and drift-checked and a full two-stage review is guaranteed at Phase 4, so the mid-run review is a safety net, not the primary review. If the count exceeds the review threshold, pause and trigger an early review checkpoint:
   - Run the pre-commit review list if present
   - Assess whether the scope is still within the approved manifest
   - If the count exceeds the halt threshold without a review, stop and run `compliance-reviewer` before continuing; the count resets after that review
   - This catches large unplanned changes mid-implementation rather than at the end
9. After all batches, run the full test command from the tech stack and write an explicit behavioral diff.
10. **Append the `implement` section to the JSON handoff artifact** at
    `docs/specs/<date>-<slug>.json`. Schema:
    `.claude/schemas/handoff.schema.json`. Required keys:
    ```json
    "implement": {
      "actual_files": ["..."],         // git diff --name-only <base>...HEAD
      "completed_batches": ["B1","B2"],
      "deviations": [
        { "kind": "extra-file", "detail": "src/Helper.cs",
          "justification": "needed to unblock B2; spec did not anticipate" }
      ],
      "behavioral_diff": "..."
    }
    ```
    Be honest about deviations — `spec-drift-detection` will diff
    `change_manifest` against `actual_files` regardless. Run
    `bash scripts/validate-handoff.sh docs/specs/<date>-<slug>.json` to
    surface drift before handing off to review.

## Batch policy

- **Tests:** test level per the stack skill's `## Test Level Guidance`; never an in-memory provider to prove database semantics (constraints, transactions, query translation). A bug fix gets a test that failed before the fix.
- **Uncertain library behavior:** read the dependency's real exception/return surface from local source before trusting the call; surface whatever stays unverified.
- **Isolation at HIGH/MAX:** recommend a dedicated worktree before Phase 3 (Claude Code's native `EnterWorktree`, or `isolation: "worktree"` on implementer `Agent` calls) and pin the branch: record `git branch --show-current` at the gate and re-check it before every batch checkpoint. A branch switch in a shared checkout mid-run is a stop, not a warning.

## Rules

- Never touch a file outside the manifest without re-planning.
- Never defer all tests to the end.
- Never continue across batches on a failing build.
- New public behavior must be test-covered.
- Keep changes rollback-friendly and dependency-focused.
- Do not mix unrelated cleanup into implementation batches.

## Verification

- [ ] Each batch compiles and tests cleanly before the next begins
- [ ] Full solution tests pass at the end
- [ ] Behavioral diff is explicit and matches the request
- [ ] No files outside the approved manifest were touched without re-planning
