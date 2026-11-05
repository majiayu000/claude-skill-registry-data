---
name: helper-sub-agents
description: shared rules for the helper sub-agents an orchestrating skill spawns
disable-model-invocation: true
---

how an orchestrator such as [/loop](../loop/SKILL.md) or [/orchestrate-multi-pr-work](../orchestrate-multi-pr-work/SKILL.md) uses helpers. the calling skill names when to spawn one, its output dir, its single code writer and how many run at once

agents are highly reactive to their context, so delegate deep investigation rather than consuming every detail yourself. do small lookups yourself

- give each helper its question, what you already know and an output path under the caller's output dir; it writes the full result there and returns a short gist. read the file only when the gist could change a decision
- helpers contribute intelligence while writes stay single-threaded: they leave the checkout, commits and pushes alone unless the calling skill names an exception
- a helper that needs another commit runs in its own worktree from `bin/wt-run <ref> -- pwd` and confirms its `HEAD` before starting. remove that worktree once the helper is done
- side effects stay in local dev. helpers spawn no helpers of their own
- decisions stay with you; a helper's result is evidence for them
