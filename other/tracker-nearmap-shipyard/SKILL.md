---
name: tracker
description: >-
  Own issue-tracker mechanics behind one contract, dispatching to the configured adapter
  (Jira or GitHub Projects): hierarchy, lifecycle, dependencies, comments, machine logs,
  attachments, and decomposition. Workflow skills own decisions; this skill owns durable
  representation and mutation.
argument-hint: "[tracker operation or issue key]"
---

Own tracker mechanics behind the contract in `${CLAUDE_PLUGIN_ROOT}/skills/tracker/CONTRACT.md`. Workflow skills (`/sy:plan`, `/sy:spec`, `/sy:ship`, `/sy:spike`) decide *what* the lifecycle should do in canonical terms; this skill turns that into concrete calls against the selected tracker.

$ARGUMENTS

## Select the adapter

Resolve the tracker through the config resolver, which owns the layer precedence:

```
get_config {"key": "tracker"}
```

The `value` it reports is `<tracker>` below. `CONTRACT.md` states how a tool's exposed name resolves; the same rule covers every tool named in this file.

Then load exactly two files and use nothing else for tracker mechanics:

1. `${CLAUDE_PLUGIN_ROOT}/skills/tracker/CONTRACT.md` — the canonical verbs, statuses, and types.
2. `${CLAUDE_PLUGIN_ROOT}/skills/tracker/<tracker>/ADAPTER.md` — the native implementation.

This is the **single point** where tracker selection happens. No other skill or agent branches on the tracker. One call — the `validate_config` tool — covers every presence check below, and fails with the offending key and the layer it came from.

It fails fast before any work when:

- `tracker` names no adapter under `skills/tracker/`;
- any required column name is unset — `columns.backlog`, `columns.ready`, `columns.in_progress`, `columns.in_review`, `columns.done` (shared by every adapter);
- the selected adapter's required configuration is absent (each adapter declares it in its own `config-map.json`);
- a retired `SY_*` environment variable is still set, which is an error rather than an override.

Report the actionable error and stop; never fall through to a default that silently writes to the wrong system.

### Liveness: cached, not just presence

The presence checks above do not prove the config is *live* — a credential can be set and still be dead. Once presence passes, call the canonical `preflight` verb **once**; it gates itself on the shared cache, its declared live check is adapter knowledge (each `ADAPTER.md` documents what "a real read" means for that tracker), and the caching and `force` mechanics are `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md`'s to state.

A failure at any step — presence or liveness — stops here with the single named `## Action needed` block `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md` defines; never a fall-through and never a crash discovered later inside a write.

## What core may ask for

Core speaks only the contract: canonical verbs (`preflight`, `create-issue`, `create-child`, `get-issue`, `update-issue`, `find-issues`, `set-status`, `assign`, `link-parent`, `add-dependency`, `add-label`, `type-convert`, `post-comment`, `post-log`, `attach-artifact`, `attachment-download`, `attachment-update`, `link-pr`), canonical statuses (`backlog`, `ready`, `in-progress`, `in-review`, `done`), and canonical types (`epic`, `task`, `bug`). Issue IDs are opaque; bodies and comments are Markdown. The adapter maps all of it.

## Conventions that live here, not in an adapter

- **Standalone machine logs.** `post-log` is its own tool, taking a single-line `title` (`Claude Code usage`, `Claude Code ship metrics`) and the record as a `payload` object it fences itself, so a log posted through it is its own comment by construction — its signature has no field a second block or a detached paragraph could ride in. Choosing that tool over `post-comment` is still yours. Generate usage from the transcript tree with the `usage_summarize` tool.
- **The highest plan version is the plan** per task/bug. A posted comment is never edited, so superseding is additive: post the next version naming the one it replaces, then re-read to confirm it is the highest.
- **Closure is not delivery.** Merged/delivered closure satisfies a dependency; decomposed or superseded closure does not — follow replacement links until delivered capability is reached.
- **Canonical decomposition** when replacing one task with smaller ones:
  1. create/approve replacements as direct children of the same epic;
  2. record replacement dependencies with `add-dependency`;
  3. `post-comment` a `# Decomposition` note: `human` is the reason for the decomposition, `agent_detail` is the replacement IDs;
  4. `add-label` the old task `decomposed` (labels preserved);
  5. `set-status` the old task `done`;
  6. ensure the old and replacement work are never simultaneously actionable;
  7. represent the old task as a conceptual parent branch in the epic roadmap.

## Durable comment types

- `# Execution Plan vN` — human-readable plan; `N` selects it, and the highest `N` on the item is the plan.
- `# SEAMS` — oversized-leaf evidence for `/sy:plan`.
- `# Decomposition` — replacement IDs and terminal reason.
- `# Ship retrospective` — human-readable shipped-vs-plan lessons.
- `# Claude Code usage` — standalone JSON usage log (`post-log`).
- `# Claude Code ship metrics` — standalone JSON outcome log (`post-log`).
- Epic decision logs ending in a `Plan checkpoint` footer.

## Loop mapping

- `/sy:plan` ↔ epic roadmap + direct executable children created in `backlog`, max the resolved `plan.max_active_tasks` cap active (resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`).
- `/sy:spec` ↔ task/bug + a new highest-version plan comment; the approved plan moves the task to `ready`.
- `/sy:ship` ↔ `in-progress` on build, `in-review` at a reviewable gated PR, `done` after merge;
  retrospective, standalone logs, and transcript live on the task.
- `/sy:spike` ↔ task under the selected experiment epic; `in-progress` during, `done` at verdict.
- dependencies ↔ `add-dependency` plus the closure semantics above.

## References: load only when needed

- `<tracker>/references/*` — adapter-specific cookbooks and setup.
