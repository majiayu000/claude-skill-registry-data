---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

> **On this platform.** This is pstack's `principle-guard-the-context-window` skill (MIT, Lauren Tan; the unmodified source is in `vendor/pstack`). Read [the platform map](../../docs/pstack-platform.md) (installed: `~/.local/share/dev-platform/current/docs/pstack-platform.md`) once per session: it says what the Cursor tools named here are on this machine, and which steps the guard hook leaves to the owner.

# Guard the Context Window

The context window is finite and non-renewable within a session. Every token should be worth its cost.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Isolate large payloads.** Route verbose outputs, screenshots, and large documents to subagents. The main context gets summaries, not raw data.
- **Keep frequently used content inline.** Templates and references used on every invocation belong in the skill file, not in separate files that cost a read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
