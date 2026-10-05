---
name: handoff
description: Update the active Technical Project Plan for handoff when context is running low or the session is ending, so the next session continues instead of restarting.
metadata:
  website: "https://photostructure.com/coding/claude-code-tpp/#handoff-wrap-up"
---

# TPP Handoff

> Documented in depth: [Claude Code has amnesia. So do PRs, changelogs, and your future self.](https://photostructure.com/coding/claude-code-tpp/)

We're out of time and need to hand off the remaining work. The Technical Project
Plan (TPP) is the handoff document — whatever this session learned must end up in
the file, or the next session re-learns it the hard way.

## Required Reading First

Before any work, you MUST read:

- The project's instructions: `AGENTS.md`, plus `CLAUDE.md` when present
- The project's TPP guide: `docs/TPP-GUIDE.md` if it exists; otherwise the
  bundled reference [TPP-GUIDE.md](../tpp/TPP-GUIDE.md)

## Your Task

Apply the guide's **Handoff rules** and **Keeping TPPs useful** sections to the
active TPP. What this session learned that the repository does not already
record — gotchas, dead ends and *why* they failed, the reasoning behind
decisions — is the part that must end up in the file.

The bar: the next session should be able to invoke the `tpp` skill with the plan
path and continue without asking what happened last time.

## Adapting for your project

- **Extend the required reading list** with the same project docs your `tpp`
  skill reads — the two skills should share one list.
- **Set the trimming and focus rules** in your project's `docs/TPP-GUIDE.md`,
  which owns them. Don't reintroduce a line budget here — the guide deliberately
  measures focus, not length.
