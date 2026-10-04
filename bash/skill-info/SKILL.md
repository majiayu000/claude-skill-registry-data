---
name: skill-info
description: "Show one skill in full — its team record or Library folder, versions, installs, health, and its eval report when it is a team skill — as Markdown boards from the terum-skills CLI. Use when the user names a skill and asks what it is, who installed it, how it scored, or what its receipt says."
metadata:
  managed-by: terum-skills
  short-description: "Show one skill's details and eval report"
---

Show one skill: the detail board, then its eval report when the skill is shared with the team.

Arguments: everything after the command (in Claude Code this arrives as "$ARGUMENTS"): the skill's name, a unique prefix of it, or nothing when the working directory is inside a Library skill folder; `--team <name>` is passed through.

## Command

    npx -y terum-skills@latest ls skill <name> --format md

Then, only when that board's **Next:** line offers `eval-report`, also run

    npx -y terum-skills@latest eval-report <name> --format md

and show both boards, detail first. A failure naming several candidates (`Ambiguous skill name …`) is a result: show it and ask which one.

## Before

Nothing to confirm: both commands only read.

## After

Show the boards verbatim; do not re-summarise unless asked. Offer the **Next:** line. `No skill named …` is a result, not something to retry: offer the list-skills skill so the user can find the name. An italic `_Resolved: …_` line says which folder or record answered a prefix or a bare invocation; keep it.

## Rules

- No TTY: never pipe `y`, never drive the CLI with `expect`, never add `--frames` to dodge a question. A question the CLI asks means the verb belongs in a terminal: say so and hand over the command.
- Never use the skill-file `` !`command` `` injection; run every command with your shell tool and read its output.
- Do not `cd`; run from the current working directory and pass absolute paths.
- Exit 1 is a result, not a retry: show the failure block, do not re-run, and do not claim earlier steps were rolled back.

## Sandbox

When `CODEX_SANDBOX_NETWORK_DISABLED=1` is set and the command starts with `npx`, add `--prefer-offline` after `npx` so a cached package resolves without the registry; if npx still reports a network error, ask the user to run the command in a terminal. In that sandbox the verbs that need the network — `sync`, `install`, `publish`, `invite`, `eval`, and `update`'s release probe — are handed to a terminal with the reason.
