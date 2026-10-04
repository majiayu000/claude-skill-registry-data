---
name: search-skills
description: "Search the team's shared skills by name, description or category, optionally narrowed by author or project, and show the matches as a Markdown board from the terum-skills CLI. Use when the user asks whether the team has a skill for something or wants to find one by keyword."
metadata:
  managed-by: terum-skills
  short-description: "Search the team's shared skills"
---

Find skills in the team Marketplace.

Arguments: everything after the command (in Claude Code this arrives as "$ARGUMENTS"): the search term, then any of `--category <c>`, `--author <a>`, `--project <p>`, passed through unchanged. Search covers every configured team. Ask for a term when none is given.

## Command

    npx -y terum-skills@latest search <term> [--category <c>] [--author <a>] [--project <p>] --format md

Quote a term that contains spaces.

## Before

Nothing to confirm: the command only reads the local team clone. When the user wants the newest catalogue, run the sync-skills skill first.

## After

Show the board verbatim. `No skills found.` is a result: say so and offer a broader term or the list-skills skill. Offer the **Next:** line (the skill-info skill for a match; installing goes through the terum-skills skill, which confirms the destination first).

## Rules

- No TTY: never pipe `y`, never drive the CLI with `expect`, never add `--frames` to dodge a question. A question the CLI asks means the verb belongs in a terminal: say so and hand over the command.
- Never use the skill-file `` !`command` `` injection; run every command with your shell tool and read its output.
- Do not `cd`; run from the current working directory and pass absolute paths.
- Exit 1 is a result, not a retry: show the failure block, do not re-run, and do not claim earlier steps were rolled back.

## Sandbox

When `CODEX_SANDBOX_NETWORK_DISABLED=1` is set and the command starts with `npx`, add `--prefer-offline` after `npx` so a cached package resolves without the registry; if npx still reports a network error, ask the user to run the command in a terminal. In that sandbox the verbs that need the network — `sync`, `install`, `publish`, `invite`, `eval`, and `update`'s release probe — are handed to a terminal with the reason.
