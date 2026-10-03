---
name: principle-guard-the-context-window
description: "Apply when context is filling up from large outputs, long files, or repeated reads. Filter bulk evidence and isolate bounded exploration when delegation earns its overhead."
---

# Guard the Context Window

The context window is finite and non-renewable within a session. Every token that enters should earn its place.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress. Unlike compute or time, context spent inside a session cannot be reclaimed.

**Pattern:**
- **Filter before delegating.** Narrow verbose outputs and reads locally first. For separable exploration that still needs substantial context, read [`../david-mode/references/agent-runtime.md`](../david-mode/references/agent-runtime.md) before dispatch. Require concise findings with exact evidence paths; the parent checks decisive evidence itself. If delegation does not pass its gates, continue sequentially.
- **Don't read what you won't use.** Read selectively based on relevance. If a file isn't needed for the current task, skip it.
- **Keep frequently used content inline.** Templates and references used on every invocation belong in the skill file, not in separate files that cost a read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
