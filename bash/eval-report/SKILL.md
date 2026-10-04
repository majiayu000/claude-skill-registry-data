---
name: eval-report
description: "Show a team skill's eval history — committed receipts per version and this machine's local runs — as a Markdown board from the terum-skills CLI, without fetching. Use when the user asks how a shared skill scored, which version passed, or what its receipts say."
metadata:
  managed-by: terum-skills
  short-description: "Show a team skill's eval receipts and local runs"
---

Show the eval history of one shared skill.

Arguments: everything after the command (in Claude Code this arrives as "$ARGUMENTS"): the skill's name (a unique prefix works, and nothing is needed inside a Library skill folder) and `--team <name>` when the user names a team, passed through.

## Command

    npx -y terum-skills@latest eval-report <skill> --format md

It reads the local team clone and this machine's run history; it never fetches. When the user wants the newest receipts, run the sync-skills skill first.

## Before

Nothing to confirm: the command only reads.

## After

Show the board verbatim. A skill that lives only in the Library (never published) has no team report: the failure says so — offer the eval skill instead. Offer the **Next:** line.

## Rules

- No TTY: never pipe `y`, never drive the CLI with `expect`, never add `--frames` to dodge a question. A question the CLI asks means the verb belongs in a terminal: say so and hand over the command.
- Never use the skill-file `` !`command` `` injection; run every command with your shell tool and read its output.
- Do not `cd`; run from the current working directory and pass absolute paths.
- Exit 1 is a result, not a retry: show the failure block, do not re-run, and do not claim earlier steps were rolled back.

## Sandbox

When `CODEX_SANDBOX_NETWORK_DISABLED=1` is set and the command starts with `npx`, add `--prefer-offline` after `npx` so a cached package resolves without the registry; if npx still reports a network error, ask the user to run the command in a terminal. In that sandbox the verbs that need the network — `sync`, `install`, `publish`, `invite`, `eval`, and `update`'s release probe — are handed to a terminal with the reason.
