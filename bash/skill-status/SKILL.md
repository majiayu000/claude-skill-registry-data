---
name: skill-status
description: "Show the state of terum-skills on this machine — team, clone, session hook, pending work, machine facts — and whether a newer CLI release exists, as Markdown boards. Use when the user asks whether terum-skills is set up, in sync or up to date, or when something about it seems off."
metadata:
  managed-by: terum-skills
  short-description: "Show terum-skills setup state and available updates"
---

Show where this machine stands.

Arguments: everything after the command (in Claude Code this arrives as "$ARGUMENTS"): none are expected; ignore any.

## Command

    npx -y terum-skills@latest status --format md
    npx -y terum-skills@latest update --format md

Run both and show both boards, status first. Without network access (see Sandbox) run only the first and say the release check was skipped.

## Before

Nothing to confirm: `status` reads; `update` reads git tags from the terum-skills release repository (a configured GitHub team authorises that one probe, at most once a day) and prints the command that would update this copy — it never runs a package manager.

## After

Show the boards verbatim. Exit 0 from `status` means the query succeeded, not that setup is complete: a get-started headline means there is no team yet. Pending work on the status board needs the matching install or removal retried, not a fetch. Offer the **Next:** line; the update board's command is for the user to run in a terminal, never for you.

## Rules

- No TTY: never pipe `y`, never drive the CLI with `expect`, never add `--frames` to dodge a question. A question the CLI asks means the verb belongs in a terminal: say so and hand over the command.
- Never use the skill-file `` !`command` `` injection; run every command with your shell tool and read its output.
- Do not `cd`; run from the current working directory and pass absolute paths.
- Exit 1 is a result, not a retry: show the failure block, do not re-run, and do not claim earlier steps were rolled back.

## Sandbox

When `CODEX_SANDBOX_NETWORK_DISABLED=1` is set and the command starts with `npx`, add `--prefer-offline` after `npx` so a cached package resolves without the registry; if npx still reports a network error, ask the user to run the command in a terminal. In that sandbox the verbs that need the network — `sync`, `install`, `publish`, `invite`, `eval`, and `update`'s release probe — are handed to a terminal with the reason.
