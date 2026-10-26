---
name: session-handoff
description: End an implementation session that started from a GitHub issue — writes the handoff, records progress against the issue, moves the card.
argument-hint: "issue number(s) or URL(s)"
---

1. Call the Skill tool with `"handoff-auto"`, passing the argument. Keep the path it prints.
2. Append `## Board status` to that document: issues touched; complete / partial / blocked; deviations from the issue; new ideas not in the issue.
3. Move each issue's card ([BOARD.md](../next/BOARD.md); its Target repo section first: on a fork, ask before writing): already closed by a merged PR → leave it, note it under `## Board status`; complete → In Review; partial or blocked → stays In Progress, plus an issue comment saying why if blocked. **Complete** = the issue's done-when is met; list any deviations under `## Board status` but don't change the done-when. Projects board with no In Review option → leave the card In Progress, note it in the handoff, and point at [IN-REVIEW-OPTION.md](../kanban-setup/IN-REVIEW-OPTION.md).
   Under a guarded agent (`implementer`/`manager`: read-only `gh`), gh writes (card moves, comments) belong to the caller: skip them and list them under `## Board status` as manual steps.
4. Print the handoff path as the last line.

A repo's `CLAUDE.md`/`AGENTS.md` may prescribe filename or required sections; follow it. Commit the handoff or not per the `handoff-auto` skill's `TRACKING.md`.
