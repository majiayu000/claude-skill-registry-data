---
name: tour
description: "A hands-on, 10-minute walkthrough that shows the user how every part of their job-search workspace works (files, board, outbox, interview room, pages, safety switches), using real actions rather than descriptions. Use when the user types /tour, says they're confused about how things work, or right after /start."
---

# tour (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/tour/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/tour/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Skip "First, check the panels". Stops 3–5 use the chat versions: stop 3 → the `pipeline` skill, on the practice row only (have the user say "I applied to Practice Co today", then show that row in `jobs/tracker.csv`; with real jobs and no practice row, just show the board and explain), and name the other chat boards in one sentence: "show my contacts" (`$contacts`), "job inbox" (`$job-inbox`), and "apply kit" (`$apply-kit`) while filling in a form; stop 4 → the `outbox` skill (list, read, copy, discard the practice draft); stop 5 → a one-question chat mock interview (see the `mock-interview` skill's Codex notes).
- Stop 2: there is no due-alerts pop-up in Codex; `$today` is where due items show.
- Stop 6: publishing pages as links is a Claude feature; open the file instead (built-in browser or double-click).
- Stop 7: in Codex, profile changes are confirmed in chat ("OK to save?") rather than by a popup.
- Stop 8: the commands to remember are `$today` and `$menu`; their board is "show my board"; mention `history/activity.md` shows what either app changed.
