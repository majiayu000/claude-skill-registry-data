---
name: consult-plan
description: Grill a proposed change, deviation, or new idea against a repo's existing plan (issues, board, roadmap, decisions), then record the outcome. Use to pitch an idea; update-progress calls it for handoff deviations.
argument-hint: "the idea, deviation, or innovation"
---

0. **Target repo** per [BOARD.md](../next/BOARD.md#target-repo): resolve `origin` (this skill needs it on GitHub), `-R <owner>/<repo>` on every `gh` call, and on a fork ask which repo to write to before any write.
1. **Baseline**, whatever exists: open issues, board state, roadmap doc, the decisions doc (found as in step 3) and the grill transcripts (`skilleddocs/grills/`, or `grills/` beside a tracked register) (cite decisions as `D<k>`, or `ADR <n>` in an ADR folder).
2. **Grill**: call the Skill tool with `"grilling"`, baseline as context. The question tree: does the idea fit, conflict with, or extend the plan, and what does the user want to happen?
3. **Record** once settled:
   - Append one row per decision to the repo's decisions doc: the one `AGENTS.md`/`CLAUDE.md` names; else an existing `docs/decisions.md`; else an ADR folder; else `skilleddocs/decisions.md` (same rule as `grill-docs`, which also gives the precedence when several files name one, the folder paths, the header and row format; an ADR folder gets one new ADR per decision, and marks an old ADR it reverses or narrows `Superseded by NNNN` / `Amended by NNNN`). Source: `consult-plan <local date>`, plus the issue or PR link when there is one. Untracked → exclude `skilleddocs/` per the `handoff-auto` skill's `TRACKING.md` (it also covers the `pip install .` hazard).
   - Idea **accepted** or changed: refines existing work → comment on that issue (the decision ids and a one-line outcome; an untracked register, e.g. on a fork, is unreadable to others: quote each decision's text instead of its id); needs its own work → open an issue and put it on the board at Todo ([BOARD.md](../next/BOARD.md)). No repo to write to (fork, both writes declined per BOARD.md's Target repo) → the decision row is the record: add the idea as a roadmap line if one exists, hand the user the issue title and body, and say so.
   - Idea **rejected**: the decision row is the record. Comment only if a related issue exists; never open an issue for a rejected idea.
