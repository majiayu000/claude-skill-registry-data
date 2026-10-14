---
name: new-workspace
description: "Use when the user prefixes a request or skill invocation with 'new-workspace' or asks to do the following work in a separate/isolated workspace — e.g. '/new-workspace /implement <card>' — or invokes it standalone to prepare an isolated workspace for subsequent work. Sets up an isolated workspace via the using-workspaces skill, then runs the requested skill or task inside it."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before creating the workspace (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back per the `using-workspaces` skill, note the gap; never invent contents.

- `<project-root>/docs/workspace-isolation.md`

# New Workspace

Companion skill: isolate first, then run whatever came next. Parse the invocation, set up the workspace, hand off.

## 1. Parse the Invocation

Everything after `new-workspace` is the downstream request — a skill invocation (`/implement <card>`), a named skill with args, or a plain task description. Store it as `<downstream>`. Empty `<downstream>` → standalone mode: set up the workspace, report the path, and stop — subsequent instructions run inside the workspace.

## 2. Set Up the Workspace

Invoke the `using-workspaces` skill and follow it fully — detect existing isolation, create via the project's configured tool, run setup, verify a clean baseline. Consent is already implied: the user explicitly asked for a separate workspace, so skip its consent question.

Read `<project-root>/docs/workspace-isolation.md` **before** creating the workspace: spec files may be untracked or gitignored and absent from the new workspace. The copy already in context remains the source of truth for the tool's operations after the move.

## 3. Hand Off

All downstream work happens inside the workspace:

- Resolve `<project-root>` to the workspace root for code, tests, and commands — except the `<project-root>/docs` specs, which may exist only in the source checkout.
- Report the workspace path once, then run `<downstream>` as if the user had invoked it directly inside the workspace — load and follow that skill in full, including its own required reads.

## Edge Cases

| Situation | Action |
|-----------|--------|
| Already inside an isolated workspace | Skip creation; run `<downstream>` in place and say so |
| No downstream request | Standalone mode: set up, report path, stop — subsequent instructions run inside the workspace |
| Workspace creation fails (sandbox/permissions) | Tell the user, ask whether to run `<downstream>` in place — don't silently proceed |
| `<downstream>` names an unknown skill | Set up, report, then treat the text as a plain task |
