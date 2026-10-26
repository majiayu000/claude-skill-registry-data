---
name: commit
description: "Reviews, validates and commits authorized changes, merges the task branch into local dev, pushes dev and arms the staging promotion. Use when a task is ready to land, when the user says commit, ship or push it, or when a routine reaches its commit gates."
allowed-tools: Bash(git *), Bash(pnpm *), Bash(gh *)
---

## Context

Claude Code fills these in; in Codex, run the commands.

- Current git status: !`git status`
- Current diff (staged and unstaged): !`git diff HEAD`
- Recent commits (for style reference): !`git log --oneline -5`

## Your task

1. Analyse the diff and write a conventional commit message:
   - Format: `type(scope): description` — types: feat, fix, chore, refactor, style, docs, test, ci
   - Keep the subject line under 72 characters
   - Add a body if the change is non-obvious (what changed and why, not how)
   - If multiple logical changes exist, note that and suggest splitting

2. Run `pnpm verify:changed` (`--dry-run` lists the checks it picks for this
   diff), plus any check from `AGENTS.md` it does not cover. Review the final
   diff and resolve failures before committing. Then run
   `node scripts/guardrails/risk-tier.mjs --base origin/dev`: for `standard` or
   `high` risk, run `/code-review` first (Codex: `/review`; a fresh-context reviewer) unless it
   already ran on this diff, and fix or answer each finding. If a gate fails twice
   on the same error, stop and report it (failure budget in `AGENTS.md`).
   For web UI changes in `gms` or `gaa-admin` it also runs `pnpm e2e` (a SKIP
   means no dev server is running; say so in the recap).

3. Stage only authorized changes, preserving unrelated staged and unstaged work.
   Commit with the reviewed message. Do not bypass hooks or force-push.

4. Merge completed task branches into local `dev` in a clean integration checkout,
   incorporating current `origin/dev` first. Validate the combined result with the
   checks above, then push `dev` directly. Do not push feature branches or create
   feature-to-dev PRs unless explicitly requested. If remote dev advances,
   integrate and revalidate locally before retrying; never force-push.
   Unattended scheduled runs (`docs/agents/routines.md`) instead push their task
   branch and open a feature-to-dev PR; they never push `dev`.

5. Use PRs for `dev → staging → main` promotion, reusing an existing promotion PR.
   After a verified dev push, automatically create/update the staging PR and arm
   auto-merge on its reviewed head, following `/release`.
   This has standing authorization. Main merges and production publication or
   deployment still require separate authorization.

6. Run the `file-friction` skill for anything you worked around during this task.

7. End with a recap for the user (and the staging PR body when you promote):
   - **Changed:** one line per commit.
   - **Gates:** each check run and its result.
   - **Outcome:** `success`, `flawed` (shipped but needed rework or left known gaps),
     `blocked` (missing credential, service or decision) or `manual` (deliberately
     left for a human), with the reason.
   - **Friction:** issue numbers filed or commented, or `none`.

8. When the work was an agent task, post a run record with
   `node scripts/agents/run-record.mjs --kind run ... --post <issue>`; see
   `docs/agents/run-records.md`.
