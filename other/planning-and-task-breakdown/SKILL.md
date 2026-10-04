---
name: planning-and-task-breakdown
description: Breaks work into ordered, parallel-dispatchable tasks with an execution DAG. Output format is consumable by CI matrices and parallel agent runners — each task has a stable ID, declared file writes, conflict edges, and branch suffix. Use when you have a spec, brief, or shaper output and need to decompose it into implementable units. Use when a task feels too large, when scope spans multi-repo or multi-week work, or when parallel execution across multiple agents is on the table.
when_to_use: |
  Use after a `prompt-shaper` or `marketing-shaper` brief when the work spans multiple repos, multiple weeks, or needs parallel agent execution — specifically when the implementation order is not obvious or tasks can safely be dispatched concurrently. Use when a spec or task feels too large to start in one session.

  Not when: the change is single-file with obvious scope — implement it directly. Not when the work has not yet been shaped into a brief — use `prompt-shaper` first. Not when there is no spec yet and requirements are unclear — produce the spec first, then return to decompose it.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Planning and Task Breakdown

Decompose work into small, verifiable tasks with a parallel-dispatchable structure. The output is a plan document — never code — that downstream runners (CI matrices, single-agent execution sessions) consume to do the work.

## When to use

- After a `/shape` brief covering multi-repo, multi-week, or multi-slice work
- When a spec or task feels too large to start in one session
- When work needs to parallelize across agents or sessions
- When implementation order isn't obvious

**When not to use.** Single-file changes with obvious scope, or specs that already contain well-defined tasks.

## The planning process

1. **Plan mode.** Read in read-only mode. Map dependencies, note risks. *Do not write code during planning.*
2. **Identify the dependency graph.** Bottom-up — foundations first.
3. **Slice vertically.** Each task is a feature path through every layer it needs (schema + API + UI), not a horizontal layer of the system. Horizontal slicing produces half-finished branches.
4. **Write task blocks.** Each task is YAML frontmatter (id, depends_on, parallel_safe, conflicts_with, files_write, files_read, branch_suffix, scope) plus prose (description, acceptance, verification). Format and field semantics: [`references/task-block-format.md`](references/task-block-format.md).
5. **Order and checkpoint.** Phases are *presentational*; the DAG is the execution order. Checkpoints are synchronization barriers — dispatch pauses until they clear.
6. **Declare the Execution DAG.** Top-of-document summary of edges using `→` and `||`. Format and dispatcher contract: [`references/execution-dag.md`](references/execution-dag.md).

## Universal rules

- **Stable IDs, never renumbered.** Use content-based slugs (`T-auth-schema`). Renumbering breaks every reference. Retire dropped IDs rather than reusing them.
- **`files_write` is authoritative, not advisory.** The dispatcher uses it for conflict detection. Under-declare → parallel collisions; over-declare → false serialization.
- **The DAG is a summary, not the source of truth.** Per-task `depends_on` is authoritative. The verification checklist enforces that they agree.
- **Day-zero ready set must be non-empty.** At least one task has `depends_on: []`. If none do, the plan is malformed.
- **`scope: L` must be split before dispatch.** Agents perform best on XS / S / M.
- **Plan, do not implement.** This skill never writes code. The output is a plan document; execution is a separate step.
- **Every plan carries a `**Status:**` line.** Lifecycle `proposed` → `in-progress` → `shipped` | `superseded`. A fresh plan starts at `proposed`; keep it current as the work moves. It is the signal for retiring completed plans (prune `shipped`/`superseded` plans manually), so an unmarked plan never gets recognized as done. See [`assets/plan-document-template.md`](assets/plan-document-template.md).

## References

- [`references/task-block-format.md`](references/task-block-format.md) — per-task YAML frontmatter and prose structure, field-by-field semantics
- [`references/execution-dag.md`](references/execution-dag.md) — DAG syntax, dispatcher contract, checkpoints, worked example
- [`assets/plan-document-template.md`](assets/plan-document-template.md) — full document template
- [`references/parallelization-decisions.md`](references/parallelization-decisions.md) — when to set each YAML field; contract-first, barrel-file, migration patterns
- [`references/task-sizing-and-redflags.md`](references/task-sizing-and-redflags.md) — sizing table, when to split, common rationalizations, red flags

## Verification

Before starting implementation, confirm:

- [ ] The plan has a `**Status:**` line (a fresh plan starts at `proposed`)
- [ ] Every task has a stable `id` (content-based slug, not a number)
- [ ] Every task has acceptance criteria and a verification step
- [ ] Every task declares `depends_on`, `parallel_safe`, `files_write`
- [ ] Every pair of tasks whose `files_write` overlap is in each other's `conflicts_with`
- [ ] At least one task has `depends_on: []` (a non-empty day-zero ready set)
- [ ] No task is `scope: L` (split it before dispatch)
- [ ] No task touches more than ~5 files
- [ ] The Execution DAG matches the per-task `depends_on` (no orphan IDs, no missing edges)
- [ ] Checkpoints exist between major phases and are referenced in the DAG
- [ ] The human has reviewed and approved the plan
