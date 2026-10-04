---
name: fix-issue
description: Pick up an open GitHub issue in this repo and ship a fix as a PR. Reads the issue body (assumes the create-issue format), branches from latest main, implements the change, runs `make test`, pushes, and opens a PR that closes the issue. Use when the user asks to fix/work/pick up an issue or invokes /fix-issue.
---

# fix-issue

Take a single issue from open to PR. The issue is the source of truth — read it, plan against it, verify against its acceptance criteria. Issues filed by [create-issue](../create-issue/SKILL.md) follow a known shape: Summary / Context / Current Behavior / Expected Behavior / Acceptance Criteria / (optional) Notes.

## When to Use

- User asks to "fix issue #N", "pick up the latest issue", "work on issue X"
- User invokes `/fix-issue` with or without a number
- User asks what's available — list open `claude-ready` issues

## Arguments

- `/fix-issue 42` — fix that specific issue
- `/fix-issue` (no arg) — list open `claude-ready` issues and ask which to pick up
- `/fix-issue list` — same as no-arg

Never pick an issue on your own without showing the user the candidate first.

## Instructions

### Step 1: Resolve the target issue

If given a number, fetch it:

```bash
gh issue view <N> --json number,title,body,labels,state,url
```

If no number, list candidates:

```bash
gh issue list --state open --label claude-ready --json number,title,labels --limit 20
```

Show the list and ask which one. If the chosen issue is closed, stop and ask.

### Step 2: Read context

Parse the issue body against the [create-issue](../create-issue/SKILL.md) template (Summary / Context / Current Behavior / Expected Behavior / Acceptance Criteria). If the format is off, work from what's there — don't refuse to proceed, but flag the gap to the user.

Read [CLAUDE.md](../../../CLAUDE.md) for project conventions (Python 3.12 + FastAPI + SQLModel + `typer` CLI under `src/job_applier/`; SvelteKit + Svelte 5 runes + TypeScript under `web/src/`; pytest + vitest, `make test`; ruff lint via `make lint`; migrations as `_ensure_*_columns()` in `models/db.py` — no alembic; mutations via SvelteKit form actions; `web/src/lib/api.ts` must stay browser-safe; LLM never called server-side; no LinkedIn/Indeed scraping; feature branch + PR workflow).

Read the files named in **Context**. If the issue doesn't name files, grep/find them from the description before guessing (`grep -rn` across `src/job_applier/` and `web/src/`).

### Step 3: Plan and confirm

Output to the user:

- 1–2 sentences restating what the issue asks for
- Files you intend to touch (Python under `src/job_applier/`, frontend under `web/src/`, tests under `tests/` and/or `web/src/**`)
- Test plan — which existing tests cover this area, which new test(s) you'll add (pytest for backend, vitest for frontend)
- Any ambiguity in the issue you want resolved before coding

Wait for go-ahead. This step exists because issue bodies are often terse and one round of clarification saves a wrong-direction PR.

### Step 4: Branch from latest main

```bash
git status --short                  # must be clean
git fetch origin main
git checkout main && git pull --ff-only origin main
git checkout -b fix/issue-<N>-<short-slug>
```

If the working tree is dirty, stop and ask. Never auto-stash.

### Step 5: Implement + test

- Write the fix in scope of the acceptance criteria.
- Add or update tests. Backend tests go in `tests/test_<module>.py` (reuse the `make_raw` factory from `conftest.py` for `RawJob` setup; use `@pytest.mark.parametrize` for table-driven cases). Frontend tests go colocated as `web/src/lib/*.test.ts` or under `web/src/lib/__tests__/` (use `@testing-library/svelte`). New modules / endpoints / source adapters need tests (project rule).
- If the change adds a `SQLModel` field, also add a matching idempotent `_ensure_*_columns()` helper in `src/job_applier/models/db.py` and wire it into `init_db()` — fresh and returning DBs both need to land on the same schema.
- Run `make test` (which runs both `make test-api` pytest and `make test-web` vitest). If backend changed, also run `make lint`. If frontend changed, also run `cd web && npm run check`.
- Iterate until green. Don't push a red branch.

### Step 6: Commit, push, open PR

Match recent commit-message style (`git log --oneline -10`) — short, imperative, no trailing period.

```bash
git push -u origin HEAD

gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<1–3 bullets on what changed>

## Test Plan
- [x] make test (passes locally)
- [ ] <any manual verification the user should do>

Closes #<N>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

The `Closes #<N>` line auto-closes the issue when the PR merges.

### Step 7: Report

Return the PR URL. One line.

## Guardrails

- **One issue per invocation.** Don't bundle fixes for multiple issues into a single PR even if they look related — open separate PRs and let the user merge in the order they prefer.
- **Stay in scope.** The acceptance criteria define done. If you spot adjacent bugs while reading the code, mention them at the end of the PR body (for a follow-up issue) but do not fix them in this PR.
- **Never push to main directly.** Always feature branch → PR.
- **Never close the issue manually.** Let the PR close it on merge.
- **Hard project rules to never violate while fixing:**
  - No `anthropic` SDK / `ANTHROPIC_API_KEY` / server-side LLM calls. Scoring and drafting only happen via `.claude/commands/` slash commands.
  - No LinkedIn / Indeed scraping in source adapters.
  - No `print()` in `src/job_applier/` library code (use `typer.echo` in CLI, logging elsewhere); no `console.log` in committed frontend code.
  - No raw client `fetch` for mutations — use SvelteKit form actions in `+page.server.ts`.
  - `web/src/lib/api.ts` must stay browser-safe (no `$env/dynamic/private`, no `node:`/`fs` imports).
