---
name: team-roles
description: Runs multi-role engineering work with the repo's role briefs (planner, architect, api-engineer, web-engineer, qa-engineer, code-reviewer, security-reviewer) in Claude Code or Codex. Use when a task spans planning, API, web and tests, when the user says "use the planner", "get a review" or "split this by role", or when a change needs a fresh-context review before commit.
---

# Team roles

The role briefs are plain Markdown in `.claude/agents/<role>.md`, identical for both tools. Each lists the tools the role needs; stay inside that list.

## Pick the roles

| Need | Role |
| --- | --- |
| Vague request, no acceptance criteria | `planner` |
| Schema, API contract or multi-layer design | `architect` |
| FastAPI code under `apps/api/fastapi` | `api-engineer` |
| Next.js code under `apps/web` or `packages/ui` | `web-engineer` |
| Tests from acceptance criteria, or a regression test | `qa-engineer` |
| Review of a finished diff | `code-reviewer` |
| Auth, permissions, public routes, CI or dependency changes | `security-reviewer` |

Use only the roles the task needs. A small fix needs one role or none.

## Run a role

1. Write a brief: the task, the files, the acceptance criteria and what is out of scope. A role sees only its brief.
2. Start the role with a clean context:
   - **Claude Code:** delegate to the subagent with the role's name.
   - **Codex:** open a new task or session, tell it to read `.claude/agents/<role>.md` and follow it, then give it the brief.
3. Read the role's result. It must list the commands it ran with pass or fail, the files changed and known risks. Send it back if any of those is missing.

## Order

`planner` → `architect` (if the design is open) → `qa-engineer` → `api-engineer` → `web-engineer` → `code-reviewer` (+ `security-reviewer`) → `/commit`.

API work goes before web work, because web types come from the generated client.

## Rules

- A reviewer is never the session that wrote the change. If the author was Codex, reviewing in Claude Code (or the reverse) is better still.
- Read-only roles (`planner`, `architect`, both reviewers) edit nothing, whichever tool runs them.
- The PR gets a second, automatic review: the `AI review` comment from `.github/workflows/ai-review.yml`. Treat its findings as claims to check.
- Finish with `pnpm verify:changed`; roles do not replace the gates in `AGENTS.md`.
