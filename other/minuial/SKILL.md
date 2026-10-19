---
name: minuial
description: Use when the user runs /minuial. The morning-start ritual — boots (or reuses) the standing Henneth window, serves the situation board, raises the Galadriel plan mirror when the project already has a plans folder, refreshes the board (tickets + metis growth), then computes the /este adherence pulse, printing all URLs. Read-only against your repos; the one call that lights every dashboard before the day's work begins.
purpose: The morning-start ritual that lights every dashboard — Henneth, board, plan mirror, adherence pulse.
user_invocable: true
stage: watch
composes: henneth:dispatch, board:dispatch, galadriel:dispatch, este:dispatch
---

# Minuial — the Dawn-Twilight

In the reckoning of the Elves, Minuial named the hour before sunrise — the first
stirring of light before the day proper. So this skill: the one call that lights
every window before the day's work begins.

## Workflow

Five skills, one after another, no gate between them — this composes existing
read-only skills. The one branch is step 3, which runs only when the project
already carries a plans folder.

### 1. Henneth

Invoke `/henneth` through the Skill tool. Boots the standing artifact window if it
is not already running, reuses it if it is.

### 2. Board — serve

Invoke `/board` through the Skill tool (bare, no arguments). Lays the board page,
boots or reuses its server, prints the URL.

### 3. Galadriel — the plan mirror

Run this step only when the project already has a plans folder. Check
`docs/plans/` in the current project. If it is absent, print one line — no plans
folder, the Mirror stays dark — and go on to step 4. Do not create one: seeding a
repo is `/galadriel`'s own behavior on a direct call, and the morning ritual does
not take that branch.

When the folder exists, invoke `/galadriel` through the Skill tool. It renders the
mirror and boots or reuses the standing server.

This step stands **before** the board refresh. The board's galadriel link records
whatever URL exists at the moment `board-galadriel.sh` runs, so a mirror raised
after the refresh leaves that link hidden until the next one.

### 4. Board — refresh

Invoke `/board refresh --stability-scrape` through the Skill tool. Re-fetches
every seated ticket and the metis growth numbers. `board.sh refresh` already runs
the growth hook (`board-growth.sh` → `appgrowth.py`, the same query `/growth`
runs standalone) as part of its own sweep — a separate `/growth` call would only
repeat the same BigQuery pull, so Minuial does not make one.

The `--stability-scrape` flag also sweeps the Stability tile's bound apps and
names any BigQuery can't answer. Minuial does not chase those into `/beleg`'s
console-scrape flow itself — that is a separate, Chrome-driven action with its
own time cost, not the quick "light every dashboard" character of this ritual.
A named app just carries the note it already would; report it in step 6 and let
the human decide whether `~/.claude/hooks/board.sh stability-write` is worth
running this morning (`skills/board/SKILL.md`, *The console-scrape fallback*).

### 5. Estë

Invoke `/este` through the Skill tool. Computes the adherence pulse, appends the
run to history, and renders its own dashboard into the Henneth window already
booted in step 1.

### 6. Report

Print the URLs — Henneth's window, the Board's, and the Mirror's when step 3 ran
— and let `/board refresh`'s and `/este`'s own output stand for what each pulled
or computed. When step 3 was skipped, say so in one line rather than omitting it
silently. Nothing further to report; nothing was forged or posted.

## Notes

- **Read-only against your repos.** Henneth boots a server, Board serves and
  refreshes from Jira/YouTrack and BigQuery, Estë reads transcripts, Galadriel
  renders into `~/.claude/galadriel/`. Minuial opens no PR, posts no comment,
  changes no ticket. The one write that could reach a project tree —
  `/galadriel` seeding `docs/plans/example.md` where no plans folder stands — is
  deliberately not taken here; step 3 skips instead.
- **No seated tickets is not an error.** If the board carries no ticket channels
  yet, `/board refresh`'s ticket loop is simply empty — the growth pull still
  runs. Seat one first with `/board add <KEY> [--active]` to have it on the
  morning board.
