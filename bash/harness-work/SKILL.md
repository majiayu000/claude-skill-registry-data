---
name: harness-work
description: "Executes plans.json tasks — solo, parallel, or breezing team mode. Use when implementing tasks or running the work loop."
when_to_use: "implement task, run task, execute plans, work on task, run all tasks, parallel workers, breezing"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Task"]
argument-hint: "[all|task-number|range|--codex|--opencode|--parallel N|--commit|--resume id|--breezing|--auto-mode]"
effort: high
model: sonnet
---

# Harness Work

Unified execution skill for Harness.
Consolidates the following legacy skills:

- `work` — plans.json task implementation (auto scope detection)
- `impl` — Feature implementation (task-based)
- `breezing` — Full team auto-execution
- `parallel-workflows` — Parallel workflow optimization
- `ci` — CI failure recovery

## Quick Reference

| User Input | Subcommand | Behavior |
|------------|------------|----------|
| `harness-work` | **auto** | Auto-selects based on task count (see below) |
| `harness-work all` | **auto** | Executes all incomplete tasks in auto mode |
| `harness-work 3` | solo | Immediately executes task 3 only |
| `harness-work --parallel 5` | parallel | Forces parallel execution with 5 workers |
| `harness-work --codex` | codex | Delegates to Codex CLI (explicit only) |
| `harness-work --opencode` | opencode | Delegates to OpenCode CLI (explicit only) |
| `harness-work --breezing` | breezing | Forces team execution |

## Execution Mode Auto Selection (auto-selection when no flag is specified)

When no explicit mode flag (`--parallel`, `--breezing`, `--codex`, `--opencode`) is provided,
the optimal mode is automatically selected based on the number of target tasks:

| Target Task Count | Auto-Selected Mode | Reason |
|-------------------|-------------------|--------|
| **1 task** | Solo | Minimal overhead. Direct implementation is fastest |
| **2-3 tasks** | Parallel (Task tool) | Threshold where Worker isolation benefits emerge |
| **4+ tasks** | Breezing | Lead coordination + Worker parallelism + Reviewer independence is effective |

### Rules

1. **Explicit flags always override auto mode**
   - `--parallel N` → Parallel mode (regardless of task count)
   - `--breezing` → Breezing mode (regardless of task count)
   - `--codex` → Codex mode (regardless of task count)
   - `--opencode` → OpenCode mode (regardless of task count)
2. **`--codex` activates only when explicitly specified**. Not auto-selected because Codex CLI may not be installed in some environments
3. `--codex` can be combined with other modes: `--codex --breezing` → Codex + Breezing
4. **`--opencode` activates only when explicitly specified**. Not auto-selected because opencode-plugin-cc may not be installed in some environments

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `all` | Target all incomplete tasks | - |
| `N` or `N-M` | Task number/range specification | - |
| `--parallel N` | Number of parallel workers | auto |
| `--sequential` | Force sequential execution | - |
| `--codex` | Delegate implementation to Codex CLI (explicit only, not auto-selected) | false |
| `--opencode` | Delegate implementation to OpenCode via opencode-plugin-cc (explicit only, not auto-selected) | false |
| `--commit` | Commit after each task is done (default: off) | false |
| `--resume <id\|latest>` | Resume previous session | - |
| `--breezing` | Lead/Worker/Reviewer team execution | false |
| `--no-tdd` | Skip TDD phase | false |
| `--no-simplify` | Skip Auto-Refinement | false |
| `--auto-mode` | Explicitly enable Auto Mode rollout. Only considered when the parent session's permission mode is compatible | false |

> **Token Optimization (v2.1.69+)**: For lightweight tasks that don't involve git operations,
> enable `includeGitInstructions: false` in plugin settings to
> reduce prompt token usage.

> **1-Hour Prompt Cache** (breezing sessions > 30 min): `source "${CLAUDE_PLUGIN_ROOT}/scripts/enable-1h-cache.sh"` before starting. Exports `ANTHROPIC_CACHE_CONTROL=max-age=3600` so all spawned Workers, Reviewers, and hooks share a cached system prompt — reduces token cost and latency across long sessions.

## Scope Dialog (when no arguments provided)

> **Note**: A lightweight drift check (`bash "${CLAUDE_PLUGIN_ROOT}/scripts/plans-drift-check.sh"`) runs before the scope dialog regardless of which option the user chooses. If stale markers are detected, the dialog is preceded by a drift summary and a confirmation prompt.

```
harness-work
How far do you want to go?
1) Next task: The next incomplete task from plans.json → Execute in Solo mode
2) All (recommended): Complete all remaining tasks → Auto-select mode based on task count
3) Specify numbers: Enter task numbers (e.g., 3, 5-7) → Auto-select mode based on count
```

If arguments are provided, execute immediately (skip dialog):
- `harness-work all` → All tasks, auto mode selection
- `harness-work 3-6` → 4 tasks, so Breezing is auto-selected

## Effort Level Control (v2.1.68+, simplified in v2.1.72)

Claude Code v2.1.68 sets **medium effort** (`◐`) as default for Opus 4.6.
v2.1.72 removed the `max` level, simplifying to 3 levels: `low(○)/medium(◐)/high(●)`.
`/effort auto` resets to default.
For complex tasks, use the `ultrathink` keyword to enable high effort (`●`).

### Multi-Factor Scoring

At task start, the following scores are summed, and **ultrathink is injected when the threshold reaches 3 or above**:

| Factor | Condition | Score |
|--------|-----------|-------|
| File count | 4+ files to be changed | +1 |
| Directory | Includes core/, guardrails/, security/ | +1 |
| Keywords | Contains architecture, security, design, migration | +1 |
| Failure history | Agent memory contains failure records for the same task | +2 |
| Explicit specification | PM template includes ultrathink notation | +3 (auto-adopted) |

### Injection Method

When score >= 3, prepend `ultrathink` to the Worker spawn prompt.
The same logic applies in breezing mode (managed centrally by harness-work).

## Execution Modes

| Mode | Reference | When |
|------|-----------|------|
| **Solo** | [`references/solo-mode.md`](${CLAUDE_SKILL_DIR}/references/solo-mode.md) | 1 task (auto) or any task number |
| **Parallel** | [`references/parallel-mode.md`](${CLAUDE_SKILL_DIR}/references/parallel-mode.md) | 2-3 tasks (auto) or `--parallel N` |
| **Breezing** | [`references/breezing-mode.md`](${CLAUDE_SKILL_DIR}/references/breezing-mode.md) | 4+ tasks (auto) or `--breezing` |
| **Codex** | [`references/codex-work.md`](${CLAUDE_SKILL_DIR}/references/codex-work.md) | `--codex` explicit only |
| **OpenCode** | [`references/opencode-work.md`](${CLAUDE_SKILL_DIR}/references/opencode-work.md) | `--opencode` explicit only |
| **Ralph** | `harness-ralph-loop` skill | Task has `[ralph]` marker — pre-dispatch, any mode |

> **`[ralph]` marker pre-dispatch rule**: Before any standard worker dispatch (solo or breezing),
> harness-work checks the task description for the `[ralph]` marker. If present, it delegates to
> `harness-ralph-loop` instead of the standard worker flow. Ralph tasks serialize within a session
> (only one Ralph loop runs at a time). See [`references/solo-mode.md`](${CLAUDE_SKILL_DIR}/references/solo-mode.md)
> and [`references/breezing-mode.md`](${CLAUDE_SKILL_DIR}/references/breezing-mode.md) for dispatch details.

## Worker Contracts

| Topic | Reference |
|-------|-----------|
| NG rules (plans.json ownership via harness plan-cli, no embedded git, no nested spawn) | [`references/worker-ng-rules.md`](${CLAUDE_SKILL_DIR}/references/worker-ng-rules.md) |
| Self-review gate (worker-report.v1 schema + Lead validation) | [`references/worker-self-review.md`](${CLAUDE_SKILL_DIR}/references/worker-self-review.md) |
| Universal violations session injection | [`references/universal-violations.md`](${CLAUDE_SKILL_DIR}/references/universal-violations.md) |
| Testing anti-patterns (mocks, test-only methods, incomplete stubs) | [`references/testing-anti-patterns.md`](${CLAUDE_SKILL_DIR}/references/testing-anti-patterns.md) |

## Failure & Review

| Topic | Reference |
|-------|-----------|
| Review loop (Codex exec / Reviewer fallback, verdict criteria, fix cycle) | [`references/review-loop.md`](${CLAUDE_SKILL_DIR}/references/review-loop.md) |
| CI failure handling (3-strike auto-fix loop) | [`references/ci-failure.md`](${CLAUDE_SKILL_DIR}/references/ci-failure.md) |
| Automatic re-ticketing of failed tasks | [`references/re-ticketing.md`](${CLAUDE_SKILL_DIR}/references/re-ticketing.md) |

## Templates

| Template | Description |
|----------|-------------|
| [`templates/worker-report.v1.json`](${CLAUDE_SKILL_DIR}/templates/worker-report.v1.json) | Worker self-review JSON schema (SR-1 through SR-5) |
| [`templates/completion-report.md`](${CLAUDE_SKILL_DIR}/templates/completion-report.md) | Rich Completion Report skeleton (solo + breezing formats) |

## Task Status SSOT

`.claude/harness/plans.json` is the sole source of truth for task status. All reads via `harness plan-cli list`/`get`, all writes via `harness plan-cli update`. See [harness/references/cli-reference.md](${CLAUDE_SKILL_DIR}/../../references/cli-reference.md). The native Claude Code task list is not mirrored.

## Related Skills

- `harness-plan` — Plan the tasks to execute
- `harness-sync` — Sync implementation with plans.json
- `harness-review` — Review implementations
- `harness-release` — Version bump and release
