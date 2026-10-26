---
name: next
description: Show the next work-session task from a repo's GitHub kanban board. Use when starting a work session or asking what to work on next.
disallowed-tools: Edit, Write, NotebookEdit
---

Read-only. Board lookup and status labels: [BOARD.md](BOARD.md).

0. **Target repo** per [BOARD.md](BOARD.md#target-repo): resolve `origin` (this skill needs it on GitHub) and pass `-R <owner>/<repo>` on every `gh` call below. Read-only, so no fork question; on a fork, say which repo's board and CI you read.
1. **Find the board** per BOARD.md.

2. **Red default branch first.** Workflow names: `gh workflow list -R <owner>/<repo> --json name -q '.[].name'`. Per workflow on the default branch, check the latest *completed* run (`gh run list -R <owner>/<repo> --branch <default> --status completed --limit 1 --workflow <name> --json conclusion,url`). Any `failure` is priority #1. `cancelled`/`timed_out` is worth a mention, not a priority.

3. **Candidates.**
   - Projects v2: items in In Review first, tagged "awaiting verification"; then items in Todo/Ready. Empty list → cross-check `gh issue list -R <owner>/<repo> --state open --json number,title,projectItems` before calling the board empty.
   - Labels: `status:in-review` first, tagged "awaiting verification"; then `status:todo`.
   - Roadmap doc: open linked issues in doc order; gated items last.

   Skip any issue labelled `wayfinder:*` (planning tickets, worked only via `/wayfinder`), and, with several boards, any In Progress or In Review on another of this repo's boards (`gh issue list -R <owner>/<repo> --state open --json number,projectItems`).

   Labels used: `priority:*` (ordering), `size:*` (size). Groups stay in that order (In Review, then Todo); within each, order by priority label (`p0` > `p1` > …, `critical` > `high` > `medium` > `low`), else roadmap order, else oldest first. A repo's `CLAUDE.md`/`AGENTS.md` overrides any of this.

4. **Present** the top 1–3: number, title, size label (or "unestimated"), suggested model (fast for narrow, well-specified work; strong for ambiguous or design-heavy). "go" picks the top one. Picking doesn't claim the card; whoever creates the branch moves it.
