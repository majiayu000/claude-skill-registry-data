---
name: list-skills
description: "List the skills on this machine (your Library) and the skills your team shares (the Marketplace) as Markdown boards from the terum-skills CLI. Use when the user asks what skills they have, what the team shares, what is installed, edited, untracked or missing an eval, or wants an overview of their terum-skills state."
metadata:
  managed-by: terum-skills
  short-description: "List your local skills and the team's shared skills"
---

Show the user's skills as boards. The terum-skills CLI renders them with `--format md`; the board it prints is the answer.

Arguments: everything after the command (in Claude Code this arrives as "$ARGUMENTS"). `--local` shows only your Library, `--team` only the team Marketplace, and `--team <name>` names a configured team (passed through unchanged); with no arguments show both.

## Command

Run with your shell tool, from the current working directory:

    npx -y terum-skills@latest ls --local --format md
    npx -y terum-skills@latest ls --format md

With `--local`, run only the first; with `--team`, only the second; with `--team <name>`, only the second with `--team <name>` appended. Add `--rows all` to either when the user asks for every row.

## Before

Nothing to confirm: both commands only read this machine and the local team clone.

## After

Show each board verbatim as the answer; do not re-summarise unless asked. The board's **Next:** line holds the follow-ups to offer. On a machine with no team the second command fails: the board carries a `> ❌ No team is configured on this machine.` block with the two get-started lines and exits 1. That is a result — say in one sentence that there is no team yet and show the Library board from the first command. If a board carries a **Notes** or `> ❌` failure block naming a hand-off, say plainly "run this in a terminal" and give the command.

## Rules

- No TTY: never pipe `y`, never drive the CLI with `expect`, never add `--frames` to dodge a question. A question the CLI asks means the verb belongs in a terminal: say so and hand over the command.
- Never use the skill-file `` !`command` `` injection; run every command with your shell tool and read its output.
- Do not `cd`; run from the current working directory and pass absolute paths.
- Exit 1 is a result, not a retry: show the failure block, do not re-run, and do not claim earlier steps were rolled back.

## Sandbox

When `CODEX_SANDBOX_NETWORK_DISABLED=1` is set and the command starts with `npx`, add `--prefer-offline` after `npx` so a cached package resolves without the registry; if npx still reports a network error, ask the user to run the command in a terminal. In that sandbox the verbs that need the network — `sync`, `install`, `publish`, `invite`, `eval`, and `update`'s release probe — are handed to a terminal with the reason.
