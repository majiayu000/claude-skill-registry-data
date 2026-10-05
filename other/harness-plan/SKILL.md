---
name: harness-plan
description: "Plans and tracks tasks in .claude/harness/plans.json. Use when creating plans, adding tasks, updating markers, checking progress, or brainstorming an idea into tasks."
when_to_use: "create a plan, add a task, mark task done, where am I, check progress, sync plans, archive phases, brainstorm idea, rough idea, design spec"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "WebSearch", "Task"]
argument-hint: "[create|add|update|sync|archive|brainstorm|sync --no-retro|sync --snapshot|--ci]"
effort: xhigh
model: opus
---

# Harness Plan

## Bootstrap Check (runs before any subcommand)

Before executing any subcommand, ensure the JSON plans storage is initialised:

1. If `.claude/harness/plans.json` exists → proceed normally.
2. If `Plans.md` exists but `.claude/harness/plans.json` does not → auto-migrate:
   ```bash
   harness plan-cli migrate
   ```
3. If neither exists → no action needed; the JSON file is created automatically on the first write (`harness plan-cli add-phase ...`).

This check is performed silently. Inform the user only if migration was triggered.

## Quick Reference

| User Input | Subcommand | Behavior |
|------------|------------|----------|
| "create a plan" | `create` | Default behavior, interactive interview → `harness plan-cli add-phase`/`add-task` |
| "add a task" | `add` | Add new task via `harness plan-cli add-task` |
| "mark complete" | `update` | Change task status to cc:done via `harness plan-cli update` |
| "where am I?" / "check progress" / `harness-plan sync` / "sync status"| `sync` | Compare implementation with plan state (`harness plan-cli list`/`get`) and sync via `harness plan-cli update` |
| `harness-plan sync --snapshot` | `sync --snapshot` | Save point-in-time progress snapshot |
| "rough idea" / "brainstorm" / `harness-plan brainstorm` | `brainstorm` | Shape idea → design spec → tasks via `harness plan-cli add-phase`/`add-task` |
| "archive old phases" / `harness-plan archive` | `archive` | Archive phases via `harness plan-cli archive <phase-id>` (sets `status: archived` in plans.json) |

## Subcommand Details

Each subcommand has its own reference file. Open the matching file when invoking that subcommand.

| Subcommand | Reference |
|------------|-----------|
| `create` | [references/create.md](${CLAUDE_SKILL_DIR}/references/create.md) — interview flow, TDD decision rules, plan generation via `harness plan-cli` |
| `add` | [references/add.md](${CLAUDE_SKILL_DIR}/references/add.md) — insertion rules, DoD/Depends auto-inference |
| `update` | [references/update.md](${CLAUDE_SKILL_DIR}/references/update.md) — marker mapping, single-task status changes |
| `sync` | [references/sync.md](${CLAUDE_SKILL_DIR}/references/sync.md) — discrepancy detection, retrospective, --snapshot |
| `brainstorm` | [references/brainstorm.md](${CLAUDE_SKILL_DIR}/references/brainstorm.md) — two-stage idea → spec → plan flow |
| `archive` | [references/archive.md](${CLAUDE_SKILL_DIR}/references/archive.md) — phase archival, retention, naming |
| _(CLI reference)_ | [cli-reference.md](${CLAUDE_SKILL_DIR}/../../references/cli-reference.md) — all subcommands, flags, exit codes, agent examples |
| _(quality gate)_ | [references/planning-quality.md](${CLAUDE_SKILL_DIR}/references/planning-quality.md) — 8-step planning quality contract for `create` and high-impact `add` |

**CI mode** (`--ci`) — applies to `create` only: no interview; uses the existing plan state (`harness plan-cli list`) and only performs task decomposition. See [references/create.md](${CLAUDE_SKILL_DIR}/references/create.md) "CI Mode" section.

**Retrospective skip** (`--no-retro`) — applies to `sync` only: skips the automatic retrospective pass. See [references/sync.md](${CLAUDE_SKILL_DIR}/references/sync.md) "Step 6: Retrospective".

## Plans Format Conventions

Task data is stored in `.claude/harness/plans.json` (repo root — **never** the plugin cache path). The canonical schema is defined in `plan_types.go`. Key invariants:

- **Newest phase first** — `add-phase` prepends; phases are listed newest-on-top.
- **Phases are never reordered** — gaps in IDs are allowed (archived phases are soft-deleted via `status: archived`).
- **DoD must be verifiable** — yes/no answerable; banned: "looks good", "works properly".
- **All writes go through the CLI** — never edit `plans.json` directly; use `harness plan-cli` subcommands.
- **Location rule** — see [`harness/rules/plans-json-location.md`](${CLAUDE_SKILL_DIR}/../../rules/plans-json-location.md); plugin cache copies are frozen snapshots and must not be read or written.

## Marker List

Compact summary. For full semantics (including the `cc:done [hash]` artifact format and `blocked` reason annotation), see [references/task-fields.md](${CLAUDE_SKILL_DIR}/references/task-fields.md) "Status Markers".

| Marker | Meaning |
|--------|---------|
| `pm:requested` | Requested by PM |
| `cc:TODO` | Not started |
| `cc:WIP` | In progress |
| `cc:done` | Worker completed |
| `pm:confirmed` | PM review completed |
| `blocked` | Blocked (reason must always be noted) |
| `[ralph]` | Iterative loop task — executed by `harness-ralph-loop`; requires `Verify:` line. See [references/ralph-tasks.md](${CLAUDE_SKILL_DIR}/references/ralph-tasks.md) |

## Optional Briefs / Manifest

`harness-plan create` attaches briefs only when needed.

- Tasks involving UI get a `design brief`
- Tasks involving API get a `contract brief`
- Briefs are supplementary materials that briefly define what to build; they do not replace the plan
- A machine-readable JSON list of skill frontmatter can be generated with `scripts/generate-skill-manifest.sh`

Reference:

- `docs/plans/briefs-manifest.md`

## Delegation to `harness-planner` Agent

For mechanical plans mutations (mark task status, add a row, archive completed phases), skills and agents may delegate to the **`harness-planner` agent** (Haiku, low effort) instead of running the edit inline.

The planner agent now calls the `harness plan-cli` binary — it **does not edit Plans.md or `plans.json` directly**. All writes go through the CLI so atomic I/O guarantees are preserved.

| Subcommand handled by agent | CLI call used internally |
|------------------------------|--------------------------|
| `update` | `harness plan-cli update <task_id> --status <status>` |
| `add` | `harness plan-cli add-phase` or `harness plan-cli add-task <phaseID>` |
| `archive` | `harness plan-cli archive <phaseID>` |

> The same CLI calls apply when this skill performs the edit **inline** (without delegating): the SSOT is `.claude/harness/plans.json`, and every read goes through `harness plan-cli list`/`get`, every write through a `harness plan-cli` subcommand.

Subcommands **not** delegated (require Opus reasoning, stay in this skill): `create`, `brainstorm`, `sync`.

**Invocation pattern** — callers use the `Agent` tool with `subagent_type: "harness-planner"` and pass a `planner-request.v1` JSON payload. The agent returns a `planner-response.v1` JSON. See [`harness/agents/harness-planner.md`](${CLAUDE_SKILL_DIR}/../../agents/harness-planner.md) for the full schema and per-operation flows.

The `harness-plan` skill itself remains the user-facing entry point — delegation is opt-in for callers that want cheap, deterministic edits without burning Opus tokens.

## Team Mode / Issue Bridge

`.claude/harness/plans.json` is maintained as the source of truth, and GitHub Issue integration is only used in opt-in team mode.

- Do not use the bridge for solo development
- Team mode creates one tracking issue and generates dry-run sub-issue payloads for each task underneath it
- `scripts/plans-issue-bridge.sh` does not actually update GitHub; it always returns dry-run payloads
- This bridge does not modify the plan

Reference:

- `docs/plans/team-mode.md`

## Related Skills

- `harness-work` — Implement planned tasks
- `harness-review` — Review implementation
- `harness-setup` — Project initialization

## Related Agents

- `harness-planner` — Haiku worker for mechanical plan mutations via `harness plan-cli` (see "Delegation" section above)
