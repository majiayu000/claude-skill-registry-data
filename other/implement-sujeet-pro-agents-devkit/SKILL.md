---
name: implement
description: >-
  Implement, build, ship, or wire up a change in an existing repo. Polymorphic on input: a Jira
  URL/KEY-123, a GitHub issue URL or #N (fetched via the gh CLI), a Confluence/Slack link (fetched
  via MCP), or freeform "build the X" prose. Plans before it acts: gathers context, presents 2-4
  approaches with trade-offs, confirms, then writes the smallest correct change matching repo
  conventions, with tests for new behavior. Validates with the repo's own typecheck/lint/narrow tests
  at every checkpoint. Git via git directly (feature branch, never protected, never force, never merge);
  GitHub via the gh CLI only (PRs via gh pr create); clones SSH-only.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, WebFetch, Agent, Workflow
argument-hint: "<target> [--plan|--act] [-i|--interactive] [--deep]"
---

# implement — build a change in an existing repo

Polymorphic on the input. **Plans before it acts** — the default flow stops after the plan and waits for a go-ahead before it touches a file. Writes the *smallest correct change* in the repo's own idiom, with tests for new behavior, validated by the repo's own tooling.

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you implement (voice, discipline, edit format) | `persona.md` |
| The phased process + Workflow orchestration | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |
| Input routing (Jira / issue / doc / freeform) | `dispatch.md` |

## Quick start

1. **Read `dispatch.md`** and classify the input. Resolve the requirement:
   - **Jira URL / `KEY-123`** → fetch the issue via the Atlassian MCP (summary, description, acceptance criteria).
   - **GitHub issue URL / `#N`** → `gh issue view <url> --json title,body,labels,comments`. (GitHub access is always the `gh` CLI — assume `gh auth login` is done.)
   - **Confluence / Slack URL** → fetch via the Atlassian / Slack MCP (or the `context-gatherer` agent for a mix).
   - **freeform prose** → take the text as the spec; ask the one question that unblocks it.
2. **Read `persona.md`** — adopt the smallest-correct-change implementer stance.
3. **Run the workflow in `workflow.md`.** Gather context → present 2-4 approaches → **confirm the plan** → execute (fan out via the **Workflow tool** for multi-file work) → validate at every checkpoint → report.
4. **Validate** with the repo's own typecheck + lint + narrow tests after each checkpoint. A failing gate stops you (`rules.md`).

## Workflow is the default for real changes

"Always have a workflow." A change worth making gets the plan→act Workflow in `workflow.md`: gather → advise → **confirm** → execute → self-review → validate. For a multi-file change, fan out — spawn `implementer` to write the code, `test-engineer` to add tests, and `code-reviewer` / `security-auditor` to self-review the diff before you report. Skip the Workflow only for a one-file, single-concern edit — and say so.

## Modes

- **default (`--plan` then confirm then `--act`)** — gather, present approaches, write the plan, **stop and confirm**, then implement + validate + report. The plan→act gate is always on unless the user opts out.
- **`--plan`** — stop after the plan. Produce the approach menu and the file-level change list; touch nothing.
- **`--act`** — skip the confirm gate and implement the recommended approach directly (still validates, still gated on shared-state writes).
- **`-i`** — walk each fork with the user (scope, approach, test strategy) before proceeding; cap 3 questions.
- **`--deep`** — use a stronger reasoning profile; auto-select for cross-module, migration-shaped, or security-sensitive changes.
