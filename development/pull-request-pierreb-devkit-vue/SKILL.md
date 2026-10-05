---
name: pull-request
description: >
  Use this whenever the user asks to "open a PR", "ship this", "create the
  pull request", "make a PR", or once a Vue feature/fix is verified and ready
  to push. Full lifecycle: branch → commit (commitizen) → issue → draft PR →
  CI → ready → autonomous monitor loop (fix comments, resolve threads,
  iterate until CI green + zero unresolved threads). `--perfect` adds a
  CodeRabbit convergence loop on top. Never works on `main`/`master`, never
  uses `--no-verify`.
---

# Pull Request Skill

Manage the full lifecycle of a pull request: branch → commit → issue → PR (draft) → CI → ready → monitor → iterate.

**Golden rules**
- Never commit or push without an explicit user request (exception: the monitoring loop in section 6 is an autonomous workflow — once the user starts it, commits/pushes within the loop are implicitly authorized)
- Never work directly on `main` / `master`
- Never use `--no-verify`

## 1. Branch

Create a dedicated branch before any work:

```bash
git switch -c type/short-description   # e.g. feat/user-auth, fix/login-crash
```

Types: `feat`, `fix`, `docs`, `test`, `ci`, `build`, `style`, `refactor`, `perf`, `chore`.

## 2. Commit (on demand only)

Use commitizen — never write commit messages manually:

```bash
npm run commit
```

> **In the monitor loop (section 6)**, commitizen is interactive and cannot run autonomously.
> Use `git commit -m` directly with a conventional commit message instead:
> ```bash
> git commit -m "fix(scope): description of fixes applied in this pass"
> ```

## 3. Verify before PR

Run `/verify` and fix all failures before opening the PR. **Never lower coverage thresholds** — add tests instead.

## 4. Issue

Search for an existing issue first:

```bash
gh issue list --search "<topic>" --state open
```

- **Issue found** → note the number, use `Closes #N` in the PR body
- **No issue found** → create one via CLI:

```bash
gh label list   # pick the right label first

gh issue create \
  --title "type(scope): short description" \
  --body "## Problem
<describe the problem>

## Expected behaviour
<what should happen>" \
  --label "Fix"
```

Label priority: use repo labels from `gh label list` first. Fallback mapping from commit type:
`feat→Feat`, `fix→Fix`, `docs→Docs`, `test→Tests`, `ci→CI`, `build→Build`,
`style→Style`, `refactor→Refactor`, `perf→Perf`, `chore→Chore`.

## 5. PR creation

Open as **draft** first — CI runs immediately; some review bots (e.g. CodeRabbit) only trigger on ready PRs:

```bash
gh pr create --draft \
  --title "type(scope): description" \
  --body "$(cat <<'EOF'
<filled template>
EOF
)" \
  --label "Feat" \
  --assignee "@me"
```

PR title must follow `type(scope): description` (conventional commits). Link the issue with `Closes #N` in the body.

**Fill every required section of `.github/pull_request_template.md`:**
- Narrative sections (Summary, Why, Scope): write real content, no placeholders
- Checkbox sections (Validation, Guardrails): check each box that applies (`- [x]`), leave unchecked only what genuinely does not apply
- Follow any instructions in the template (e.g. "Delete this section if not applicable")

Once **draft CI passes**, convert to ready **immediately, before anything else**:

```bash
gh pr ready <number>
```

> **Ordering invariant (hard requirement):** CodeRabbit never reviews a draft PR. Flipping to ready is a mandatory prerequisite for entering — or continuing — any wait on CodeRabbit/review threads. Do it the moment draft CI is green, BEFORE starting section 6. Waiting on CodeRabbit while the PR is still draft is a guaranteed silent deadlock (observed 2026-07-16, issue #4450).
>
> Some bots (e.g. CodeRabbit) trigger on ready, not on CI completion. After converting, do a **preliminary review pass** before entering the main loop:
>
> ```bash
> sleep 180
> # Read feedback (see 6b) — fix any actionable comments and push before entering the loop
> ```
>
> If actionable comments exist: fix, `/verify`, commit, push, then enter the loop at step 6a.
> If none: enter the loop at step 6a directly.

## 6. Monitor loop (autonomous)

The PR must already be ready (see §5) before this loop starts — CodeRabbit
never reviews a draft, so entering this loop while still draft deadlocks.

After `gh pr ready`, run an autonomous polling loop until either CI is green
with zero unresolved threads for 3 consecutive passes (~9 min) or the safety
limit (10 iterations) trips.

```bash
OWNER=$(gh repo view --json owner -q .owner.login)
REPO=$(gh repo view --json name -q .name)
PR=<number>
```

Per pass:
0. **Draft guard** (belt-and-braces) → if still `isDraft: true` and CI is
   green, `gh pr ready "$PR"` immediately — covers a loop that started
   pre-flip, or a rebase/force-push that reverted the PR to draft
1. Wait CI → fix + /verify + commit + push if red, else continue
2. Check mergeable — `CONFLICTING` stops, `UNKNOWN` retries
3. Grace `sleep 180` + adaptive recheck of pending review checks
4. Read **only unresolved threads** (see `references/monitoring.md`)
5. Actionable → batch-fix in one commit, /verify, push, reply with SHA,
   resolve via GraphQL. Never resolve silently — reply is audit trail.
6. Non-actionable → reply explaining why, resolve, continue
7. Zero unresolved 3 passes in a row + CI green + branch protection
   `APPROVED`+`MERGEABLE` → STOP ✓

Downstream projects: classify stack-level vs downstream comments via the
`devkit-vue` remote and open issues upstream for stack-level findings.

**Full procedure (commands, classification rules, stop condition matrix):**
see `references/monitor-loop.md`. Load when running the loop.

## 7. Perfect mode (`--perfect`)

When invoked with `--perfect`, run an outer convergence loop after the standard monitor loop (section 6) completes:

```text
REPEAT:
  1. Wait for CodeRabbit          → CodeRabbit auto-triggers on every push. Poll for up to 5 min.
                                    ONLY if no review appears after 5 min, post:
                                    `@coderabbitai full review` as PR comment, then wait (see monitoring.md)
  2. Run monitor loop (section 6) → fix all comments, resolve all threads, CI green
  3. Run diff audit               → audit `git diff master...HEAD` for security, logic bugs,
                                    data integrity, API design, performance issues
  4. If audit has findings        → fix all, commit, push, GOTO 1
  5. If 0 CodeRabbit comments AND 0 audit findings → run cleanup (step 6), then STOP ✓
  6. Cleanup outdated threads     → list all threads with isOutdated==true that have NO reply
                                    explaining the fix. For each, reply with the SHA and a brief
                                    explanation of how/why it was addressed, then resolve if not
                                    already resolved.
```

**Safety limit:** 5 outer iterations max — report to user if still not converged.

**Important:** In section 6c, you MUST reply to every thread before resolving it. Never resolve a thread silently — the reply serves as audit trail.

## 8. Conflict resolution

```bash
BASE_REF=$(gh pr view "$PR" --json baseRefName -q .baseRefName)
git fetch origin "$BASE_REF" && git rebase "origin/$BASE_REF"
# Resolve conflicts, then: git add <files> && git rebase --continue
git push --force-with-lease origin HEAD
```

After force-push, restart from 6a.
