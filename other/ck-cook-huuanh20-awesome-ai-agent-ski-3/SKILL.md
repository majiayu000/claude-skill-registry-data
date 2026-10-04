---
name: ck:cook
description: Implement a feature phase by phase from a phased JSON master or Markdown plan. Before each phase, confirm whether to create/run unit tests and whether to run ck:quality, unless explicit flags supply those choices. Supports token-budgeted execution, resumable state, and TDD handoff to ck:test.
user-invocable: true
---

# ck:cook — Budget-Aware Implementation Pipeline

Cook implements code and performs a compile/syntax check. `ck:test` owns tests and `ck:quality` owns quality review; Cook orchestrates either only after user consent.

Modes are mutually exclusive; Standard is the default:

- **Standard** — ask for the phase's test and quality choices, then auto-continue after the selected checks finish.
- **`--fast`** — default the current phase to no unit tests and no quality gate unless explicit check flags are supplied.
- **`--hard`** — default both checks to yes and require human confirmation after the selected checks and before the final push.

Composable flag:

- **`--tdd`** — select tests=yes and require a `RED_READY` artifact before implementation.
- **`--tests` / `--no-tests`** — select whether `ck:test --unit` creates/runs unit tests for the current phase.
- **`--quality` / `--no-quality`** — select whether `ck:quality --gate` runs for the current phase.
- **`--checks-all-phases`** — apply explicitly supplied test/quality choices to every remaining phase; without it, ask again at the next phase.

Reject contradictory flag pairs. No old single-file JSON or mixed-format compatibility is supported. Markdown `plan.md` remains a separate input format.

### Step 0.5 — Phase Checkpoint

Before reading implementation files or activating each phase, resolve two independent choices: `Unit tests: yes/no` and `Quality gate: yes/no`.

- Honor explicit flags without asking. In Standard mode, ask one concise question containing both choices that remain unresolved. Do not silently infer consent from a previous phase unless `--checks-all-phases` was supplied.
- In `--fast`, unresolved choices default to no. In `--hard`, unresolved choices default to yes.
- State the token/risk tradeoff briefly: tests catch behavioral regressions; quality checks architecture and maintainability; skipping either saves tokens but reduces assurance.
- Record the decision before activation/completion in a separate phase-state write. For JSON, a skipped gate requires `quality.status: skipped_by_user` and `quality.decision: user_confirmed_skip`; it is never `approved`. Later complete the phase and master in separate phase-first/master-second writes so receipt hooks validate persisted consent. For Markdown, append `[quality: skipped_by_user; decision: user_confirmed_skip]` to that phase's checkbox line. A skipped test run remains `not_started` with a note that the user declined it.
- If tests=yes without `--tdd`, run `/ck:test --unit <phase-file>` after implementation and the Build Gate. If `--tdd`, use the RED/GREEN handoff described below.

---

### Step 0 — Resolve the Plan

Accept:

- `--json <path>` — phased JSON master `plan.json` entry point.
- `--plan <path>` — Markdown `plan.md` entry point with sibling `phase-XX-*.md` files.

When no path is supplied, search `plans/` for a master `plan.json`, then for `plan.md`, and ask before using the discovered plan. If neither exists, suggest `/ck:plan-json` or `/ck:plan`.

Load adjacent `spec.md` when present. The spec supplies user-story coverage and TDD acceptance anchors.

---

### Step 1 — Preflight (Engineering Quality Profile)

Run once per phase, before implementing its steps.

Skip re-discovery when resuming a phase that already has this recorded: JSON — `quality_profile.applicable_rules` is a non-empty array; Markdown — a "Preflight:" line already exists under `## Design Constraints`. Either signal alone is sufficient to skip; do not re-read sibling files just because some sub-field looks sparse.

1. Read the phase's own `## Design Constraints` (Markdown) or `design_constraints` (JSON), plus the plan's Architecture Decisions and Risks — these are phase-specific constraints, not invented generically.
2. Read 2-3 sibling files outside the phase's scope to learn actual naming, constants/error, module-structure, and DI conventions already in use in this repository. Existing convention always outranks a generic default.
3. Record the result as the phase's `quality_profile` (JSON: `repository_conventions`, `boundaries`, `applicable_rules`, `allowed_exceptions`) or as a "Preflight:" line appended to the phase's Design Constraints section (Markdown). This is read later by both Cook's own implementation and by `ck:quality --gate` — write it once, don't duplicate the discovery.

If `--tdd`, also check for `plans/{slug}/tests/{phase}-tdd-ready.json` (or Markdown equivalent) with `status: RED_READY`. Missing artifact blocks with:

```text
BLOCKED: --tdd requires RED tests. Run /ck:test --tdd --prepare {phase} first.
```

---

### Step 2 — Validate and Resume a Phased JSON Plan

Run the Python bundle validator against the master before implementation:

```text
python {ck-plan-json-skill-root}/hooks/plan_validator.py plans/{slug}/plan.json
```

Resolve `{ck-plan-json-skill-root}` from the installed skill directory for the active client.

The validator may read the whole bundle mechanically; do not load inactive phase details into AI context. Read global context from the master once, and load or read detailed steps for only the active phase.

`current_phase` selects the active phase reference. The active phase uses `current_step` to select its next step. Report `Phase {current_phase}, step {current_step}` with status:

```text
Plan: {plan_id} — {goal}
Plan status: {status}
Phase: {current_phase}/{phase_count} — {phase name} ({phase status})
Step: {current_step}/{step_count} — {step status}
Mode: {Standard | Fast | Hard}
Quality: {quality_status} · Testing: {testing_status}
Context: {framework} · {architecture}
```

If bundle validation reports a phase/master status mismatch, inspect only the master and its active phase:

1. If both identities match and the phase is exactly one legal monotonic transition ahead, reconcile the master with `reconcile_master`, write the master, and rerun bundle validation.
2. If the master is ahead, identities differ, dependencies differ, or more than one transition must be inferred, block without mutation and request guidance.
3. A matching state is a no-op.

An `in_progress` plan may point to a pending next phase after the previous phase completed. This is the valid ready-between-phases state.

Dependency checks confirm every prerequisite phase is completed before any write, mutation, or activation. Invalid, incomplete, or forward dependencies block and stop execution.

---

### Step 3 — Execute the Active JSON Phase

Use full-document writes or reconstructable edits so the PreToolUse validator checks proposed content.

#### Activate

Activation writes the phase file first, setting its status and active step to `in_progress`; activation writes the master second, mirroring phase and plan status without advancing `current_phase`. Rerun bundle validation at the stable checkpoint.

#### Implement Steps

For the current step:

1. Read its `input_files` for context.
2. Implement its `description` and update only declared `output_files`.
3. Verify every `success_criteria`.
4. Record written paths in `ai_generated_code`.

Step success only advances the phase `current_step`; step success does not update the master or `current_phase`. Mark the successful step `completed`, and activate the next phase-local step when one remains.

On failure, keep `debug_logs` step-local in the phase file. Append a concise `{timestamp, error, attempted_fix}` record and retry with a different approach for up to 3 remediation cycles. Cycle 4 stops and escalates.

#### Steps Complete → Build Gate

When every step in the phase is `completed`, do not yet write the phase `status = completed` transition — that transition is quality-gated (Step 5). First run the Build Gate (Step 4).

Blocking writes the phase file first with the active step and phase blocked; blocking writes the master second, mirrors blocked status, and does not advance either cursor. Preserve the failure diagnostics and request guidance.

---

### Step 3.M — Execute a Markdown Plan

For each `phase-XX-*.md` in order:

1. Read phase requirements, Design Constraints, and steps.
2. In `--tdd`, confirm the `RED_READY` artifact from Step 1 before implementing.
3. Implement and verify the phase's Success Criteria.
4. Record spec coverage when `spec.md` exists.
5. Run the Build Gate, then the checks selected at Step 0.5, before updating `plan.md` progress or Session Notes.

---

### Step 4 — Build Gate

Compilation or syntax validation only — Cook does not run unit or integration tests.

1. Run the project's build/compile/lint/type-check command relevant to the changed files.
2. On failure, use up to three distinct remediation approaches (spawn `debugger` if the failure is non-trivial) and rerun the Build Gate.
3. A fourth failed cycle stops and escalates with the exact command, error, and attempted approaches.

---

### Step 5 — Selected Test and Quality Checks

If unit tests=yes, invoke `ck:test --unit <phase-file>` after the Build Gate. Fix production-code failures within the phase remediation limit; let `ck:test` own test files and reports. In TDD mode, invoke `ck:test --tdd --verify` instead. A `failed` or blocked test result blocks phase completion; after three distinct remediation cycles, escalate rather than silently converting the choice to skipped.

If quality=no, write `quality.status: skipped_by_user`, `quality.decision: user_confirmed_skip`, and mirror `quality_status: skipped_by_user`; leave report and receipt empty. Continue the completion transition, but label the phase as completed without quality approval. This records consent for validation and audit but is not cryptographic proof of user identity.

If quality=yes, run this gate:

Treat `ck:quality` as a black box: invoke it, act on its verdict, never second-guess or reimplement its severity rules here (those live in `ck:quality`'s own contract and may change independently of Cook).

1. Invoke `ck:quality --gate <phase-file>` against exactly the files this phase created or modified.
2. **`CHANGES_REQUIRED`** — fix every finding it lists as blocking, at the location it cites, then rerun the gate (`--verify` against the same report is acceptable once every listed finding has been addressed). Up to 3 remediation cycles; a 4th `CHANGES_REQUIRED` escalates to the human with the outstanding findings and attempted fixes.
3. **`APPROVED`** — `ck:quality` has already issued the receipt. Write the phase file's `quality` object (`status: approved`, `report`, `receipt`) and the master's `quality_status: approved` mirror, then perform the completion transition: phase file first (`status: completed`, `current_step = step_count + 1`), master second (mirrors completion, advances `current_phase`). The receipt-gate hook enforces that this transition cannot happen without the fresh receipt just issued.

`--hard` additionally pauses here for explicit human confirmation before the completion transition. Other modes continue after the selected checks finish.

If another phase remains, the master stays `in_progress` and points to the pending next phase — return to Step 1 (Preflight) for it. If the final phase completes, set plan `status = completed` and `current_phase = phase_count + 1`, and proceed to Step 6.

---

### Step 6 — Checked Handoff (Finalize)

Runs once, after the final phase finishes its selected checks and its completion transition succeeds.

- For JSON, verify every phase and step is completed with `quality_status: approved` or `skipped_by_user`, verify both `count + 1` sentinels, then run strict bundle validation.
- For Markdown, mark implemented phases complete and record whether quality was approved or skipped.
- Report the actual test choice and outcome. When tests were skipped, print explicitly:

```text
Testing: skipped by user. Run /ck:test or your project's test suite before code review or release.
```

- Update user-facing documentation only when the implementation changed its contract (`docs-manager`; skip for `--fast`).
- Sync Markdown plan progress (`project-manager`; Markdown plans only).
- Prepare conventional commit details and ask before pushing (`git-manager`, always) — the commit message must not claim tests pass, since Cook did not run them.
- If the completed work changes a service in a Docker Compose microservice system, identify the exact Compose service name from the repository and include a copy-ready command that affects only that service. Use `docker compose restart <service>` when the existing image/container is sufficient; use `docker compose up -d --no-deps --build <service>` when code or image contents must be rebuilt. Include `-f <compose-file>` and `--profile <profile>` when the repository requires them. Never guess the service name, never suggest restarting the entire stack, and present the command as a user-run suggestion rather than executing it automatically.

Final summary:

```text
Plan: {plan_id}
Result: {completed_phases}/{phase_count} phases, {completed_steps}/{step_count} steps
Quality: {approved_count} approved, {quality_skipped_count} skipped by user
Blocked: {blocked_count}
Debug cycles: {debug_log_count}
Testing: {passed_count} passed, {testing_skipped_count} skipped by user
```

## Agents / Skills

| Agent / Skill  | Step | Modes |
|----------------|------|-------|
| `debugger`     | 4    | Build Gate remediation |
| `ck:test`      | 5    | When tests=yes |
| `ck:quality`   | 5    | When quality=yes |
| `project-manager` | 6 | Markdown plans |
| `docs-manager` | 6    | Standard, `--hard` (skipped by `--fast`) |
| `git-manager`  | 6    | All modes |
