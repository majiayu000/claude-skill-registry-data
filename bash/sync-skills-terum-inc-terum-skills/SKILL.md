---
name: sync-skills
description: "Fetch the team's shared skills — reset each disposable team clone to origin/main — and show the outcome per team as a Markdown board from the terum-skills CLI. Use when the user wants the newest catalogue, receipts or roster before listing, searching or installing."
metadata:
  managed-by: terum-skills
  short-description: "Fetch the team's latest shared skills"
---

Refresh the local team clone.

Arguments: everything after the command (in Claude Code this arrives as "$ARGUMENTS"): `--team <name>` when the user names a team, passed through; nothing else is expected.

## Command

    npx -y terum-skills@latest sync --format md

Run it in the background when your shell tool can: a slow fetch takes a while. Never run `sync --hook` by hand; that is the session-start entry.

## Before

Say what it does in one sentence before running: it fetches and resets each disposable team clone to `origin/main`; it never uploads, places or edits the user's skill folders.

## After

Show the board verbatim. Disclose each team the board reports as not refreshed, with its reason. A team whose repository was recreated elsewhere is offered `team move` on the board: that verb asks a question, so hand it to a terminal.

## Rules

- No TTY: never pipe `y`, never drive the CLI with `expect`, never add `--frames` to dodge a question. A question the CLI asks means the verb belongs in a terminal: say so and hand over the command.
- Never use the skill-file `` !`command` `` injection; run every command with your shell tool and read its output.
- Do not `cd`; run from the current working directory and pass absolute paths.
- Exit 1 is a result, not a retry: show the failure block, do not re-run, and do not claim earlier steps were rolled back.

## Sandbox

When `CODEX_SANDBOX_NETWORK_DISABLED=1` is set and the command starts with `npx`, add `--prefer-offline` after `npx` so a cached package resolves without the registry; if npx still reports a network error, ask the user to run the command in a terminal. In that sandbox the verbs that need the network — `sync`, `install`, `publish`, `invite`, `eval`, and `update`'s release probe — are handed to a terminal with the reason.
