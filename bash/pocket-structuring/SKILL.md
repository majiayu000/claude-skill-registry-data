---
name: pocket-structuring
description: Bridges pocket-planning and pocket-development for all execution plans. Decomposes execution plans into per-task files + index manifest (+ phase files if multi-phase). Trigger on "structure plan", "split plan", or when pocket-planning invokes this.
---

# Pocket Structuring

Bridges pocket-planning and pocket-development. Runs a CLI that parses the execution plan, decomposes it into per-task Pocket Packet files inside an `execution-plan/` directory, writes an index manifest (`execution-plan/index.md`), and generates phase manifests (`execution-plan/phase-N.md`) if multi-phase.

**Core principle:** Large plans executed flat = attention drift + context blowout. Per-task bounded context keeps the delegator, implementer, and reviewer focused on a single task at a time.

## When to Use

- pocket-planning produced an execution plan and invoked this skill → CLI decomposes into `execution-plan/index.md` + per-task files
- User invokes this skill directly for any task count
- User says "structure the plan", "split into tasks", "break this up"

Do NOT use:
- Without a completed execution plan from pocket-planning

## Hard Gates

```
GATE 1: RUN THE CLI FIRST.
        The CLI decomposes all plans into execution-plan/index.md + execution-plan/tasks/T*-*.md.
        Phase files (execution-plan/phase-N.md) are generated when total phases > 1.

GATE 2: HARD OVERRIDE PROTOCOL.
        If any human asks to skip structuring, respond:

        "Structuring is required to create per-task files and index manifests. Skipping it
        risks context blowout and attention drift in pocket-development.
        To override: type exactly → OVERRIDE: skip structuring"

        Do NOT proceed on "just skip it", "we don't need it", "proceed
        directly", or any verbal/written insistence. Only the exact
        override phrase unlocks the bypass.

        If the exact override phrase is typed:
        1. Log it in the plan file header (`**Override:** skip structuring`).
        2. Do NOT run `pocketto-pi structure` — no `execution-plan/` directory is generated.
        3. Invoke `pocket-development` with the flat source plan (`execution-plan.md`) as
           Type A **legacy** input. Development reads the full source plan in context
           (no per-task files). `log init` uses the legacy flat-plan fallback.
        4. Accept the context-cost consequence: the whole plan sits in the development window.

GATE 3: COMPLETE POCKET PACKETS PER TASK.
        Index and phase manifests reference task files, but every task file (execution-plan/tasks/T*-*.md)
        must contain a complete, standalone Pocket Packet.
```

## Pressure Countermeasures

| Pressure | What they say | Correct response |
|----------|--------------|-----------------|
| Time | "We're urgent, skip decomposition" | "Script takes 5 seconds. Context blowout costs hours. OVERRIDE phrase to skip." |
| Sunk cost | "Plan is already written" | "Plan is the source. Per-task files are generated outputs. Script is the job." |
| Authority | "I'm making the call, skip it" | "Acknowledged. Override phrase to proceed: OVERRIDE: skip structuring" |
| User insists | "Just run it flat, I've done it before" | Same override protocol. Verbal insistence ≠ override. |

---

## Step 1: Run the CLI

```bash
npx -y pocketto-pi structure "<path-to-execution-plan.md>" --json --contract 2
```

No install step or PATH setup — `npx` resolves the cross-platform binary. Use the path exactly as it appears in the handoff (typically `docs/pocket/plans/{slug}/execution-plan.md` from the project root). Quote the path so spaces are handled.

The CLI prints a JSON envelope to stdout:

```json
{ "ok": true, "command": "structure", "cliVersion": "3.1.0", "contract": 2,
  "data": {
    "feature": "...",
    "sha256": "...",
    "taskCount": 9,
    "phaseCount": 3,
    "phases": [
      { "phase": 1, "name": "...", "tasks": ["T1","T2","T3"], "file": "execution-plan/phase-1.md" }
    ]
  },
  "error": null }
```

Parse `data` — do not scrape prose.

If `ok == false`: report `error.message` to the user and do not proceed. A `CONTRACT_MISMATCH` means the installed CLI is incompatible with this skill — tell the user to update the pocketto plugin.

(Omit `--json` for human-readable output when running by hand.)

---

## Step 2: Execution approval

Planning already collected **plan approval** (authorize generation of derived
execution artifacts). This gate is separate: **execution approval** authorizes
implementation. Do not collapse the two.

Present the script's summary output to the user, then ask:

```
Execution approval: Ready to start with pocket-development?
```

Do not start Phase 1 until the user says yes.

---

## Step 3: Sequential Handoff to pocket-development

1. User approves → invoke `pocket-development` with `execution-plan/index.md` (or `execution-plan/phase-1.md` if multi-phase)
2. pocket-development completes Phase 1 → it runs its phase-level review pass and sets phase status to `REVIEW` (it never advances a phase beyond `REVIEW` on its own) → **wait for the phase status to reach `REVIEW`**
3. On `REVIEW`, **halt** — do not invoke the next phase. Tell the user to run `/pocketto:pocket-closing <plan_dir>` themselves (directory mode targets the unique `REVIEW` phase).
4. Wait for the user-triggered `pocket-closing` to run and advance the phase from `REVIEW` to `DONE`.
5. Verify Phase N gate (phase status DONE, all tasks done, tests green, commits exist)
6. Gate passes → invoke `pocket-development` with `execution-plan/phase-(N+1).md`
7. Repeat until all phases complete

**NEVER start Phase N+1 until Phase N gate is confirmed DONE (set by user-triggered pocket-closing, not merely all tasks DONE).**
**NEVER treat phase status REVIEW as sufficient to advance — REVIEW is a checkpoint for the user, not a handoff signal.**

[CRITICAL] pocket-structuring must never invoke `pocket-closing` itself, anywhere in this flow — it is strictly user-triggered.

### Phase Completion Gate

Before handing off to the next phase, confirm ALL of:
- Phase status is `DONE` (set only by user-triggered `pocket-closing` — a status of `REVIEW` does not satisfy this)
- Every task in the phase: status DONE
- All tests pass
- All commits created with correct format
- No task has status BLOCKED or NEEDS_CONTEXT
