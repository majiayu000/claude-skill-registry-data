---
name: issue
description: Create, update or resume a GitHub issue as durable resolution memory when requested.
argument-hint: "[create|update|resume|list|from-tasks|close] [#N | problem | brief folder]"
---

# Issue memory

Use the authenticated gh CLI. Read the specific issue and comments before
updating it; do not query unrelated issues. Capture the problem, evidence,
attempts, remaining action and verification so the issue can be resumed cold.
Use references/issue-template.md when creating one.

Confirm before creating or closing an issue. Append requested progress as
comments instead of overwriting the body. Label new issues `arsenal`; keep
`claude-memory` on the ones that already carry it and match either when
listing or resuming. Preserve the Pickup Directive contract. No code changes, commits or agents.

`from-tasks <brief folder>` creates one issue per top-level `##` task of
`tasks.md`, after a single confirmation for the whole batch. Each body uses
the template: Problem from the task and the acceptance criteria it cites,
Pickup Directive with the brief path, `base` and `branch` from the brief
frontmatter, the task identifier and its check command. It then writes
`[#N](url)` into each task heading and the range into the brief `issues`
field. Existing links are kept, never duplicated.

`close #N` appends a `Resolution:` comment from the evidence given (trace
row, commit, PR) and closes the issue as completed. Ship calls it after a
merge into a branch that is not the default one, where GitHub's `Closes #N`
does nothing.

After every `create`, end with one line asking whether to turn the issue
into a brief (« On en fait un brief ? » in the conversation language), with
the command in the harness syntax (`/brief:brief #N` in Claude Code). Never
start it yourself; Arsenal owns the transition.

Resume reconstructs the current state from the issue, not stale memory. A
solved issue does not trigger another diagnosis. List returns concise open
items and stops. If the controlled shell has no external networking, report
that authorization/capability boundary instead of claiming the GitHub action
happened or attempting an execution escape.

## Arsenal handoff

Return issue context and remaining actions to Arsenal when it called this
skill. A request to fix the issue can continue through Arsenal's implementation
route; reading or resuming context alone does not authorize code changes.
Issue creation and closure retain their confirmation gates.

## Verify external facts

Before stating an external fact (a version, an API, a price, a date, a
regulation, the behaviour of a tool or library, a person or company), search
first when the runtime offers web search: read the `websearch` skill and run
one quick search, then cite the source. One search per fact; `--deep` only on
request. Without web search, mark the claim unverified. Facts visible in the
repository or the request need no search.

## Execution policy

Work solo. Ask before any subagent or reviewer, even in auto mode. Explain
the independent scope and expected benefit first. No hidden advisor, nested
delegation, model retuning, repeated successful checks, or progress spam.
Use existing context before asking questions. Stop when the requested result
is delivered. User stops and scope changes override pending steps.
