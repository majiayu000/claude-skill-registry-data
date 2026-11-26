---
name: principal-review
description: The recurring ownership loop — review merged PRs since the last review, check invariant drift, groom the backlog, and write a report for Nick. Run weekly or per-milestone.
---

# principal-review

This loop is what "Fable owns the project" means operationally (ADR-000 §6). Output is a dated report in `docs/reports/`.

## Procedure

1. **Establish the window.** Find the last report in `docs/reports/`; review everything merged since (`gh pr list --state merged`), plus open PRs and CI status on main.
2. **Review merged work.** For each merged PR: does it match its issue's acceptance criteria? Any scope creep? Approval-path PRs — was the E2E test present and was it merged by Nick?
3. **Check invariant drift** against the golden rules:
   - Single-binary: `deps-allowlist.txt` vs `go.mod`; any new required external process?
   - Schema-first: grep for hand-rolled JSON shapes outside `pkg/schema`.
   - Parity: any CLI/TUI or MCP capability without a REST/WS equivalent?
   - Audit chain: do approval-path tests still cover request → notify → resolve → audit?
4. **Groom the backlog.** Close stale issues, write the next tranche of issues to the template standard (Context/Files/Acceptance/Tests/Blocked-by), promote P2/P3 stubs to full issues only when their milestone is next, re-order blocked-by chains if reality changed.
5. **Write the report** to `docs/reports/YYYY-MM-DD-principal-review.md`:
   - Merged work summary (one line per PR).
   - Invariant status (per rule: OK or drift found + issue filed).
   - Backlog delta (issues written/closed/re-scoped).
   - **Decisions needed from Nick** — proposed ADRs, dependency requests, release readiness (assessed against the `release` skill's preconditions). Explicit list, even if empty.
6. **Post a summary into Conch itself** (the build org is tenant #2), once the report is on a branch with a PR open: `ops/principal-review.sh post docs/reports/YYYY-MM-DD-principal-review.md <pr-url>`. It sends the report's title, one line per `## ` section with its item count, the `## Decisions needed from Nick` section in full and the PR link, as plain text, to the channel named by `CONCH_REVIEW_CHANNEL` (default `principal-review`), with `conch send`, as whoever `conch login` stored. The decisions section is found by that heading, so keep it. If Conch is unreachable, there is no login, or the channel refuses the post, the script says which in one line and exits 3; the report and its PR stand and nothing is retried. Release readiness stays an item in the decisions list: nothing here raises a Conch approval object.

## Cadence

Weekly, or at each milestone boundary — whichever comes first. If two loops in a row have nothing to review, say so in the report rather than skipping it.

The weekly run is a systemd user timer, and optional: `ops/principal-review.sh install` enables `conch-principal-review.timer` (Mondays 07:00, `Persistent=true`), which runs `ops/principal-review.sh run`. That starts a headless session to do steps 1–5 in its own worktree on a branch `principal-review/YYYY-MM-DD`; the script then commits the report, pushes the branch, opens a PR (`Refs #26`) and does step 6. It never commits to `main` and never merges, it holds `conch-agent`'s lock while it works, and it does nothing if the day's report is already on `main` or on that branch. `ops/principal-review.sh status` shows the timer and the last log. A milestone-boundary review is the same `run` by hand, or this skill in a session followed by `post`.
