---
name: sflow-jira-board
description: List Jira Software boards and show all Stories in active or future sprints while explicitly excluding the backlog. Use only on explicit request.
disable-model-invocation: true
argument-hint: "[BOARD-ID] [--project KEY] [--state active,future]"

---

# Jira board Stories without backlog

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Use Singularity Flow's direct Jira Software REST client. Do not use Jira MCP tools and do not construct a backlog query.

1. Check the connection with `singularity-flow jira status --json` when it has not already been checked.
2. If no board ID was supplied, run:

   `singularity-flow jira boards [--project <KEY>] --json`

3. If exactly one board matches, use it. If multiple boards match, use `ask_user` to let the user select the exact board. Never infer a board from a similar name.
4. Run:

   `singularity-flow jira board <BOARD-ID> --state active,future --type Story --json`

5. Group the result by sprint and show sprint name/state, Story key, summary, status, assignee, and priority.
6. Always say `Backlog excluded`. The command enumerates active and future sprints and reads their issues; it does not call the Jira backlog endpoint.
7. Keep the user-supplied sprint states if they explicitly request `active`, `future`, or `closed`. Do not introduce `closed` by default.

This skill is read-only. Never request or display a Jira token, PAT, password, or authorization header.
