---
name: repo-cartographer
description: Map and explain unfamiliar repositories for Codex before implementation. Use when the user asks where to start, how a codebase works, what files own a behavior, how to onboard into a repo, or which change path is safest. Do not use for focused code review, release work, docs-only edits, or direct bug fixing when the user already supplied the failing surface.
---

# Repo Cartographer

Build a useful map before changing code.

## Workflow

1. Read project signposts first: `README`, `AGENTS.md`, `CONTRIBUTING`, package files, build scripts, docs, tests, and route or entrypoint directories.
2. Identify the runtime, package manager, commands, app boundaries, data stores, external services, and generated-code conventions.
3. Trace one or two representative flows from entrypoint to side effect. Prefer actual imports, routes, tests, or handlers over guesses.
4. Name the safest change paths: files to edit, tests to run, fixtures to inspect, and risks to avoid.
5. Stop at a map unless the user explicitly asks to implement.

## Output Shape

- `What This Repo Is`: one paragraph.
- `How To Run/Verify`: commands found in the repo.
- `Key Areas`: directories, ownership, and purpose.
- `Likely Change Path`: where to work for the user's goal.
- `Open Questions`: only blockers that code/docs did not answer.

## Ground Rules

- Prefer `rg`, `rg --files`, and targeted file reads.
- Do not invent architecture names the repo does not support.
- Mark confidence as `High`, `Medium`, or `Low` when recommending a path.
- If the repo is large, map the relevant slice first and say what remains unmapped.
