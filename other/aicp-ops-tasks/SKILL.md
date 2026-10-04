---
name: aicp-ops-tasks
description: Manage AICP's two task surfaces — workflow tasks in `wiki/backlog/tasks/` (gated by Layer B PreToolUse hook via `aicp --task-cmd switch/show/list/clear`) and runtime tasks tracked by the in-process task manager (`aicp --tasks`). Replaces the deprecated aicp_task_status MCP tool per `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`. Loads when the operator says "what task am I on" / "switch to T<NNN>" / "list active tasks" / "clear active task" / "show recent runtime tasks" / "what's running" / "drift between state.yaml and task file".
allowed-tools: Bash, Read
effort: low
---

# aicp-ops-tasks

Manage AICP's TWO distinct task surfaces via the CLI:

1. **Workflow tasks** (`wiki/backlog/tasks/T<NNN>-<slug>.md`) — manage via
   `aicp --task-cmd switch/show/list/clear`. Writes `.aicp/state.yaml`
   (gitignored) which Layer B PreToolUse hook reads to enforce stage gates.
2. **Runtime tasks** (in-process task_manager) — view via `aicp --tasks`.
   Tracks per-invocation lifecycle (pending → running → completed/failed/killed).

This skill teaches BOTH surfaces and clarifies their distinct concerns.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb (workflow)**: operator says "what task am I on", "switch to
  T001", "list backlog tasks", "clear active task", "what stage am I in",
  "drift between state and task file"
- **Direct verb (runtime)**: operator says "show recent runs", "what tasks
  are pending", "any failed tasks", "what's running"
- **Hook diagnosis**: PreToolUse hook denied an operation — operator wants
  to know why (state.yaml current_stage forbids the path)
- **Stage transition**: operator advancing a task from one stage to the next
  (document → design → scaffold → implement → test → done)
- **Task cleanup**: removing inactive workflow task or stuck runtime task

Do NOT load when:

- The concern is the task FILE FORMAT (load `feature-document` for the
  document-stage skill that creates the file)
- The concern is the hook BEHAVIOR / DESIGN (load `infra-security` —
  PreToolUse hook is in scope there) — this skill is about USING the state,
  not modifying the hook
- The concern is the runtime task MANAGER's internals (`aicp/core/tasks.py`
  is the implementation; this skill is operator-facing only)

## Operations

### Operation 1 — Show the current workflow task + stage

**When**: operator wants to know which task is active and what stage Layer B
hook is enforcing.

**Process**:

1. Run `aicp --task-cmd show`
2. Output:
   - `Active task: T<NNN>` + `Active stage: <stage>` + `Mode: <think|edit|act>` + `Updated: <ISO>`
   - Task file path
   - WARN line if drift detected (state.yaml stage ≠ task file's current_stage)
3. The output's `NEXT:` recommends "proceed with stage-appropriate work" or
   "resync via `--task-cmd switch`" if drift detected

**Quality bar**: drift between state.yaml and task file frontmatter is the
most common source of confusion — always re-check after any task file edit.

### Operation 2 — Switch the active workflow task

**When**: operator advancing through stages OR moving to a different task.

**Process**:

1. Optionally list available tasks: `aicp --task-cmd list`
2. Switch: `aicp --task-cmd switch --task-arg T<NNN> [--task-arg2 <stage>] [--mode <think|edit|act>]`
   - If `--task-arg2 <stage>` omitted, reads `current_stage` from task file
   - If `--mode` omitted, defaults to `edit`
3. Output confirms: "Switched to task T<NNN> (stage=X, mode=Y)" + state file path
4. The output's `NEXT:` recommends "proceed with stage work" — Layer B hook
   now enforces the stage's forbidden zones

**Quality bar**: switching mid-edit is fine — the hook enforces forbidden
zones per state, not per session. Just re-read the output's NEXT line and
respect the new stage's allowed paths.

### Operation 3 — List workflow tasks

**When**: operator wants to see the backlog or pick a task to switch to.

**Process**:

1. Run `aicp --task-cmd list`
2. Output: table of `ID  Stage  Status  Slug` with `*` marker on the active task
3. The output's `NEXT:` adapts:
   - No tasks: "create wiki/backlog/tasks/T<NNN>-<slug>.md, then switch"
   - Tasks but no active: "switch to one to enable Layer B"
   - Tasks with active: "show details, or switch to a different one"

**Quality bar**: the `*` marker is the source of truth for "active" — if it
disagrees with `--task-cmd show`, .aicp/state.yaml is corrupt; clear and re-switch.

### Operation 4 — Clear the active workflow task

**When**: operator finishes a task arc and doesn't yet have a next one, OR
needs to disable Layer B stage enforcement temporarily.

**Process**:

1. Run `aicp --task-cmd clear`
2. Output: "Active task cleared. Hook falls back to Layer A only (no stage-gate)."
3. The output's `NEXT:` recommends switching to a new task to re-enable Layer B
4. State file `.aicp/state.yaml` is removed; only Layer A safety hook remains

**Quality bar**: clearing is reversible (just `--task-cmd switch` again);
nothing is destroyed. But Layer B IS off until you switch back, so resist
clearing as a way to bypass stage enforcement — change the stage instead.

### Operation 5 — Show runtime task lifecycle

**When**: operator wants to see what AICP is currently executing or recently
ran (DIFFERENT from workflow tasks above — runtime tasks are per-invocation).

**Process**:

1. Run `aicp --tasks`
2. Output: count summary (`Tasks (N active / M total):`) + per-task icon +
   id + status + truncated prompt + duration
3. Status icons: ⏳ pending, 🔄 running, ✅ completed, ❌ failed, 🛑 killed
4. The output's `NEXT:` recommends `--history <N>` for full history or
   `--health-report` if many failed

**Quality bar**: a healthy fleet shows mostly ✅ completed; high ❌ failed
count signals upstream issues (likely DLQ has entries — see `aicp-ops-dlq`).

### Operation 6 — Diagnose a Layer B hook denial

**When**: PreToolUse hook denied a Bash/Write/Edit operation citing R05_STAGE_GATE.

**Process**:

1. Read the denial message — it names the stage and the forbidden path
2. Run `aicp --task-cmd show` to confirm current_stage matches expectation
3. If the operation is genuinely needed for the current stage, the stage is
   wrong — switch: `aicp --task-cmd switch --task-arg T<NNN> --task-arg2 <correct-stage>`
4. If the operation is genuinely forbidden for this stage, the operator is
   doing the wrong work for the current stage — STOP, complete the current
   stage's deliverables first
5. Refer to `wiki/config/domain-profiles/backend-ai-platform-python.yaml`
   for the per-stage `forbidden_zones` definitions

**Quality bar**: NEVER bypass the hook by clearing state.yaml — that's a
process violation. Either move to the right stage or do the right work.

## Gotchas

- **Detection**: agent uses `aicp_task_status` MCP tool.
  **Rule**: NEVER call deprecated MCP tools — use `aicp --tasks` (runtime) or
  `aicp --task-cmd show/list` (workflow).
  **Reasoning**: MCP overhead is paid per turn; CLI+Skills loads on demand.

- **Detection**: agent confuses workflow tasks (`--task-cmd`) with runtime tasks (`--tasks`).
  **Rule**: workflow tasks live in wiki/backlog/tasks/T<NNN>-<slug>.md and
  drive Layer B stage enforcement. Runtime tasks live in the in-process
  task_manager and track per-invocation lifecycle. They are unrelated.
  **Reasoning**: same word "task", two different concerns. The hint: workflow
  task IDs are `T<NNN>`; runtime task IDs are timestamp-based.

- **Detection**: agent clears the active workflow task to bypass a hook denial.
  **Rule**: hook denials mean the operation is wrong for the stage — clear is
  not the fix; switching to the right stage is.
  **Reasoning**: bypassing the hook defeats the whole stage-gate enforcement.
  Per the layered defense decision (pretooluse-hooks-layered-approach), the
  hook is structural prevention; bypassing it accepts higher failure risk.

- **Detection**: agent assumes drift between state.yaml and task frontmatter is harmless.
  **Rule**: drift means the hook is enforcing X while the operator thinks
  the stage is Y — re-switch to resync (`--task-cmd switch --task-arg <id>`
  with no `--task-arg2` reads from frontmatter).
  **Reasoning**: drift produces silent surprises later — the hook will deny
  an operation the operator expected to be allowed, or vice versa.

- **Detection**: agent edits `.aicp/state.yaml` directly instead of using `--task-cmd switch`.
  **Rule**: always use `--task-cmd switch` — it validates the task ID, stage,
  and mode against schema; direct edit can produce corrupt state.
  **Reasoning**: validated writes prevent silent corruption; direct edits
  bypass the validation that the CLI provides.

## Reference exemplars

- `aicp/cli/main.py` `_run_task_cmd()` — workflow task implementation (the most heavily contract-compliant handler in the codebase)
- `aicp/core/state.py` — `.aicp/state.yaml` read/write helpers
- `tools/hooks/pretool_safety.py` — Layer B hook that reads state.yaml
- `wiki/config/domain-profiles/backend-ai-platform-python.yaml` — per-stage forbidden_zones
- `wiki/decisions/01_drafts/aicp-active-state-mechanism-for-hooks.md` — design rationale for state.yaml
- `wiki/decisions/01_drafts/pretooluse-hooks-layered-approach.md` — layered defense (R01-R05)
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` — Category D rationale for this skill's existence

## Domain context

AICP's task surfaces are intentionally split: WORKFLOW tasks (long-lived,
stage-gated, in wiki/backlog/) drive what's allowed via Layer B hook; RUNTIME
tasks (per-invocation, in-process) track what AICP is/was doing right now.
The `--task-cmd` flag is the most-extensively contract-compliant handler in
the CLI (4 subcommands × multiple paths each, all with NEXT lines). The
`.aicp/state.yaml` file is gitignored — it's per-operator state, not project
state.

## Related skills

| Skill | When to use |
|-------|-------------|
| `feature-document/-plan/-implement/-test/-review` | When advancing a workflow task through a specific stage |
| `aicp-ops-dlq` | When runtime tasks failed → check DLQ |
| `aicp-ops-metrics` | When concerned about runtime task performance trends |
| `infra-security` | When the concern is the PreToolUse hook design itself |
