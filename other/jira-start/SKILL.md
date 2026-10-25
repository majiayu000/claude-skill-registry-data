---
name: jira-start
description: Start work on a Jira ticket - read the story, plan, create a branch off main, implement, lint, and commit locally for the user to verify. Use when the user gives a Jira key (e.g. COG-123) and asks to work on / implement / pick up the ticket.
argument-hint: <JIRA-KEY> [extra instructions]
---

# Implement Jira ticket $ARGUMENTS

You are taking a Jira story from the board to a verified-ready local branch. **Do not push, open a PR, or move the ticket past "In Progress".** The user verifies first and then runs `/jira-pr`.

Jira helper: `.claude/scripts/jira.sh` (run `.claude/scripts/jira.sh` with no args for usage). If it fails with "not set", tell the user to copy `.claude/jira.env.example` to `.claude/jira.env` and fill it in, then stop.

## 1. Read and understand the ticket

1. `.claude/scripts/jira.sh get <KEY>` (KEY is the first word of the arguments; uppercase it). Also `get` the parent epic and any linked/blocking issues if they look relevant.
2. Work out: the problem, the user-facing behaviour wanted, the acceptance criteria, which roles are affected (`student` / `teacher` / `admin` / `superAdmin`), and whether it touches `client/`, `server/`, or both.
3. **Draft or vague stories:** if the ticket is missing information you cannot sensibly default (unclear behaviour, conflicting criteria, unknown data source), ask the user with AskUserQuestion — give concrete options grounded in the codebase. For small gaps, pick the conventional option and list it as an assumption. Never invent business rules silently.
4. If the status is already Done, or a branch for this key already exists (`git branch -a --list "*<KEY>*"`), stop and ask how to proceed.

## 2. Prepare the branch

1. `git status --porcelain` must be empty. If not, stop and ask — never stash or discard the user's work.
2. `git fetch origin && git switch main && git pull --ff-only origin main`.
3. Branch name from issue type: Bug → `fix/<KEY>-<slug>`, everything else → `feature/<KEY>-<slug>`. `<slug>` = 3–6 lowercase kebab words from the summary.
   `git switch -c <branch>`.
4. `.claude/scripts/jira.sh transition <KEY> progress` (warn and continue if the transition is unavailable).

## 3. Plan, then implement

1. Explore the affected code first. Follow `CLAUDE.md` strictly — in particular: routes ↔ controllers 1:1 by domain and mounted in `routes/v1/index.ts`; per-route middleware chains; `ApiError` + `next(error)`; client data flow page → hook → `lib/api.ts`; admin **and** super-admin page trees both updated; reuse sibling query-key shapes; don't rename misspelled paths.
2. For anything beyond a small change, write a short plan (files to touch, API shape, UI changes) and map each acceptance criterion to it before editing.
3. Implement. Keep the diff scoped to the ticket — no drive-by refactors.
4. New API routes → document in `docs/API.md`. New env vars → `docs/SETUP.md`.

## 4. Verify

There are no tests in this repo. Run whatever applies to what you changed and fix every error you introduced:
- `server/`: `npm run lint` (tsc --noEmit)
- `client/`: `npm run lint` and `npx tsc --noEmit`

Report pre-existing errors separately from ones you caused.

## 5. Commit locally

Commit with message `<KEY>: <summary>` plus a short body of what changed. Small logical commits are fine. Do not push.

## 6. Hand over for verification

End with:
- Ticket link and branch name
- What changed, grouped by server / client, with file links
- **Acceptance criteria checklist** — each criterion → how it is met, or ❌ / ⚠️ if not fully
- Assumptions made and open questions
- **How to verify manually**: exact pages/URLs, which role to log in as, API calls to try, edge cases
- Next step: "When it looks good, run `/jira-pr <KEY>`. To change something, just tell me."
