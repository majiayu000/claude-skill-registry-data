---
name: "verify"
description: "Generate or maintain a project-local verification skill that drives the real app the way a user does, in any language or framework, and proves behavior with captured evidence. Use for /verify, 'make a control skill for this repo', 'audit the verify skill', or when a project has no scripted way to prove UI, CLI, or service behavior."
disable-model-invocation: true
---

# Verify

Every serious project needs a scripted way to drive the real app and prove
behavior: launch it, exercise a feature the way a user would, capture evidence.
This skill produces that as a project-local skill at `.claude/skills/verify-<app>/`,
then keeps it honest as the app changes.

Without it, "it works" means "it compiled". With it, "it works" means a
reviewer can rerun one command and watch it work. That is the
**prove-it-works** principle made executable.

## Modes

- **Generate.** No verification skill exists yet, or the repo has no scripted way to prove behavior. Follow [GENERATE.md](GENERATE.md).
- **Maintain.** One exists and may have rotted. A feature map goes stale the moment the app changes. Follow [MAINTAIN.md](MAINTAIN.md).

Pick by what is on disk: glob `.claude/skills/verify-*/`. Nothing there means
generate. Exactly one means maintain. More than one means ask which.

## What holds in both modes

- **Drive the real user path.** Not internal setters, not test-only endpoints. If a user clicks it, the harness clicks it.
- **Capture the action and the resulting state**, not just a final screenshot. Verify side effects (files written, rows inserted, messages sent) alongside what is visible.
- **Evidence outlives cleanup.** Teardown removes instances and scratch state. A cleanup that eats the proof is a bug, and it is checked at the named location rather than assumed.
- **Kill what you started**, never by process name.
- **A generated or edited skill that was never executed is a draft.** Run its own instructions end to end before handing it over.

## Driving surfaces here

The harness recipe depends on what the app is. Prefer a harness the repo
already has (Playwright specs, expect scripts, curl-able endpoints, a debug
port) before reaching for a generic recipe.

| Surface | Reach for |
|---|---|
| Browser, Electron, web UI | the `claude-in-chrome` skill and its `mcp__claude-in-chrome__*` tools |
| CLI, TUI, server | the built-in `/run` skill, or a tmux/PTY harness |
| HTTP service | plain `curl` against a running dev server |

Whatever it is, the generated skill records the exact commands for *this* repo,
with real selectors and real ports. Examples are not a harness.
