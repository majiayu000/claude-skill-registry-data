---
name: openspec-apply-change
description: Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.
allowed-tools: Read, Glob, Grep, Edit, Bash(git rev-parse:*), Bash(*scripts/openspec.sh":*)
license: MIT
compatibility: Requires the repository-pinned scripts/openspec.sh wrapper.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.11.0"
---

Implement tasks from an OpenSpec change.

**Pinned wrapper:** Every OpenSpec command MUST invoke
`"$(git rev-parse --show-toplevel)/scripts/openspec.sh"` so execution is
anchored to the repository root; never use a cwd-relative wrapper path.

**Store selection:** If the user names a store (a store is a standalone OpenSpec repo registered on this machine) or the work lives in one, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" store list --json` to discover registered store ids, then pass `--store <id>` on the commands that read or write specs and changes (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `schemas`, `view`). Once selected, treat `--store <id>` as sticky for the rest of the workflow. Every unscoped example of those commands below is shorthand: before running it, append the flag. For example, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" status --change "<name>" --json --store "<id>"`, not the unscoped form shown below. Other commands do not take the flag. Hints printed by commands already carry the flag; keep it on follow-ups. Without a store, commands act on the nearest local `openspec/` root.

**Input**: Optionally specify a change name (e.g., `/openspec-apply-change add-auth`). If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" list --json` to get available changes and ask the user to select one

   Always announce: "Using change: `<name>`" and how to override (e.g., `/openspec-apply-change <other>`).

2. **Check status to understand the schema**

   ```bash
   "$(git rev-parse --show-toplevel)/scripts/openspec.sh" status --change "<name>" --json
   ```

   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - `planningHome`, `changeRoot`, and `actionContext`: planning scope and edit constraints
   - Which artifact contains the tasks (typically "tasks" for spec-driven, check status for others)

3. **Get apply instructions**

   ```bash
   "$(git rev-parse --show-toplevel)/scripts/openspec.sh" instructions apply --change "<name>" --json
   ```

   This returns:
   - `contextFiles`: artifact ID -> array of concrete file paths (varies by schema - could be proposal/specs/design/tasks or spec/tests/implementation/docs)
   - Progress (total, complete, remaining)
   - Task list with status
   - Dynamic instruction based on current state
   - Optional `context`: current required project instruction input from the selected root
   - Optional `operationGuidance`: current advisory guidance for apply

   **Handle states:**
   - If `state: "blocked"` (missing artifacts): show message, suggest using `/openspec-continue-change` (if it is not installed, run `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" status --change "<name>" --json` to see the next artifact and `"$(git rev-parse --show-toplevel)/scripts/openspec.sh" instructions <artifact-id> --change "<name>" --json` for how to create it)
   - If `state: "all_done"`: treat it as a task-file projection, not yet as
     authoritative completion. Read the task artifact's apply-mode declaration
     before accepting it. In issue-mapped mode, resolve every linked issue again:
     only `state: CLOSED` with `stateReason: COMPLETED` preserves `all_done`.
     Any open or reopened issue makes its task pending again, so discard the
     stale `all_done` state and continue to progress and selection using issue
     state. A `NOT_PLANNED` or `DUPLICATE` closure, or an unreadable, missing, or
     ambiguous issue state, is indeterminate and stops apply. Only after every
     linked issue is authoritatively complete may you congratulate and suggest
     archive. In default mode, the task file remains authoritative and
     `all_done` may be accepted as returned.
   - Otherwise: proceed to implementation

   Before reading a task as implementable or starting any implementation, run:

   ```bash
   "$(git rev-parse --show-toplevel)/scripts/openspec.sh" validate "<name>" --type change --strict --no-interactive
   ```

   A non-zero or indeterminate validation result stops apply. Report the
   structural or semantic errors and refuse to begin a task until the complete
   change validates strictly; artifact existence and apply state alone never
   authorize implementation.

   Treat `context` as a required prompt-level input. Read and consider it, and
   apply relevant project facts, conventions, and constraints while implementing.
   Treat `operationGuidance` as optional additive advice. Read and consider every
   entry, and follow entries that are applicable and compatible with the built-in
   workflow.

   Keep both fields separate from CLI-returned state, missing artifacts, tasks,
   progress, `contextFiles`, and the built-in `instruction`. They are not
   evidence of task completion, do not replace the built-in instruction, and do
   not permit bypassing a blocked state. If context conflicts with the built-in
   instruction, an explicit user choice, or a CLI-controlled value, report the
   conflict and preserve the controlling value. If guidance is inapplicable or
   conflicts with those controlling inputs, do not follow it and explain why.
   These are prompt-level behavior contracts, not enforceable checks.

4. **Read context files**

   Read every file path listed under `contextFiles` from the apply instructions output.
   The files depend on the schema being used:
   - **spec-driven**: proposal, specs, design, tasks
   - Other schemas: follow the contextFiles from CLI output

   Do not copy `context` or `operationGuidance` verbatim into implementation
   files or planning artifacts unless the user separately asks for that content.

5. **Resolve apply mode and show current progress**

   Read the task artifact for an explicit apply-mode declaration.

   - **Issue-mapped mode:** When the change declares `apply-mode: issue-mapped`
     and links each task to one tracker issue, tracker state is authoritative.
     Only `state: CLOSED` with `stateReason: COMPLETED` is complete; an open
     issue is pending regardless of the task checkbox. A `NOT_PLANNED` or
     `DUPLICATE` closure, or any unreadable issue state, is indeterminate:
     surface it to the operator, block selection, and never auto-complete or
     silently skip that task. Display progress from completed versus open
     linked issues and report indeterminate closures separately.
   - **Default mode:** Without that declaration, follow OpenSpec's normal apply
     flow. Display CLI progress and use task checkboxes as completion state.

   In either mode, display the schema, resolved apply mode, progress, remaining
   work overview, and dynamic instruction from the CLI.

6. **Select work according to the resolved mode**

   - **Issue-mapped mode:** Select one task whose linked issue is open. If the
     user did not name a task or issue, show the open linked issues and ask for
     a selection. Then **stop** and ask the operator to run `/claim <issue>`;
     this apply skill never invokes, delegates, or emulates the user-invocable
     claim workflow. Resume only after the operator confirms `/claim` completed
     and the issue's dedicated feature branch/worktree required by `AGENTS.md`
     is active.
   - **Default mode:** Process pending tasks in the normal OpenSpec order. Keep
     the implementation within the repository's small-PR convention; stop at a
     coherent PR boundary rather than accumulating an oversized change.

7. **Implement according to the resolved mode**

   - Show which task is being worked on and keep changes minimal and focused.
   - In issue-mapped mode, drive the selected issue through the complete Dev Loop
     to its own ready-for-review PR, then stop. Do not edit the task checkbox in
     that PR: the issue closes on merge and is the durable completion record.
     Checkbox reconciliation belongs only in a change that lands on `main` after
     issue-closing merges, or in archival reconciliation. Concurrent task PRs
     therefore share no `tasks.md` state write.
   - In default mode, mark each fully implemented task complete in the task file
     (`- [ ]` → `- [x]`) and continue until done, blocked, interrupted, or at the
     small-PR boundary resolved in step 6.

   **Pause if:**
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - A task needs work beyond what the spec and tasks describe, or you are tempted to drop, narrow, defer, or accept exceptions to specified behavior to make it fit → surface the added scope and ask; do not absorb it silently
   - Error or blocker encountered → report and wait for guidance
   - User interrupts

8. **On completion or pause, show status**

   Display:
   - Apply mode and work handled this session
   - Overall progress from the mode's authoritative state source
   - Branch and PR handoff state where applicable
   - If all tasks are done: suggest archive
   - If tasks remain: stop and name the next apply invocation as the handoff
   - If paused: explain why and wait for guidance

**Output During Implementation**

```text
## Implementing: <change-name> (schema: <schema-name>, mode: <apply-mode>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Ready-for-review PR handed off

Issue state remains authoritative until merge closes it.
```

**Output On Completion**

```text
## Apply Run Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Mode:** issue-mapped
**Progress:** 2/7 linked issues closed

### Completed This Session
- Task 3 — ready-for-review PR <reference>; issue remains open until merge

This issue-mapped apply run is complete. Start a new invocation for another open issue.
```

**Output On Pause (Issue Encountered)**

```text
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

**Guardrails**
- Honor the apply mode and authoritative state source resolved from task metadata
- Reconcile issue-mapped `all_done` against current linked-issue state before accepting completion
- Always read context files before starting (from the apply instructions output)
- If task is ambiguous, pause and ask before implementing
- If implementation reveals issues, pause and suggest artifact updates
- Keep code changes minimal and within the repository's small-PR convention
- Update task checkboxes only in default mode; issue-mapped mode uses issue state
- Pause on errors, blockers, or unclear requirements - don't guess
- When a task needs work beyond what the spec describes, surface the added scope and pause - never silently narrow, defer, or simplify away specified behavior
- In default mode, mark a task `- [x]` only when its specified behavior is fully implemented, not when it is partially done or deferred
- Use contextFiles from CLI output, don't assume specific file names
- Do not use context or operation guidance as proof that a task is complete
- Apply relevant project context; report conflicts with controlling workflow inputs
- Consider every guidance entry; explain any inapplicable or conflicting advice
- Do not copy runtime context or operation guidance into implementation files or planning artifacts
- Preserve CLI-controlled blocked/ready/all-done behavior and completion criteria
- Never invoke the user-invocable `/claim` workflow; stop for the operator and resume only after confirmation

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
