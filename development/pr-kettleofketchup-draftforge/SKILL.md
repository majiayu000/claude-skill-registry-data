---
name: pr
description: DraftForge PR lifecycle workflow. Use when the user runs /pr, opens or pushes a pull request, or asks to monitor CI checks and Copilot review on a branch. Creates the PR (or reuses an existing one), polls GitHub Actions and Copilot up to ~15 min, then analyses CI failures and Copilot comments and reports findings grouped by file and skill.
---

# /pr — PR lifecycle workflow

## Purpose

Drive a PR from "branch pushed" to "actionable review summary" without the user babysitting it. The skill:

1. Resolves PR state (open existing or create new).
2. Requests Copilot as a reviewer if missing.
3. Polls GitHub Actions checks and the Copilot review (up to 15 min).
4. Pulls CI failure logs and Copilot inline comments.
5. Categorises findings by file → matched `.github/instructions/*.instructions.md` → canonical skill, then surfaces them to the user with concrete next steps.

## When to trigger

- User types `/pr`.
- User says "open a PR" / "create a PR" / "spin up a PR" on the current branch.
- User says "watch CI" / "monitor checks" / "wait for Copilot" on a branch with an open PR.
- A push has just happened and the user is asking what's next.

Do **not** trigger automatically just because a branch has uncommitted work — confirm first.

## Workflow

### Phase 1 — Resolve state

```bash
branch=$(git branch --show-current)
pr_json=$(gh pr view --json number,state,headRefName,baseRefName,url,reviewRequests,reviews 2>/dev/null || echo "")
```

- If `pr_json` is empty → no PR yet → go to Phase 2 (create).
- If PR exists and is `OPEN` → go to Phase 3 (request Copilot if absent, then monitor).
- If PR is `MERGED` / `CLOSED` → report and stop; ask whether to open a new one.

Before creating, verify the branch is pushed (`git rev-parse --abbrev-ref --symbolic-full-name @{upstream}` succeeds) and is ahead of `main`.

### Phase 2 — Create the PR (if missing)

Pre-fill title/body from commits when the branch has 1–3 commits; otherwise prompt the user once for a title. Always use a HEREDOC body with `## Summary` and `## Test plan` sections, per repo convention. Full patterns and the exact `gh pr create` invocation: [references/creating-the-pr.md](references/creating-the-pr.md).

### Phase 3 — Request Copilot reviewer (idempotent)

```bash
PR=$(gh pr view --json number -q .number)
# Skip if Copilot is already in reviewRequests OR has already reviewed
need_copilot=$(gh pr view $PR --json reviewRequests,reviews \
  --jq '(.reviewRequests + .reviews) | any(.login // .author.login | tostring | test("copilot"; "i")) | not')
if [ "$need_copilot" = "true" ]; then
  gh pr edit $PR --add-reviewer @copilot
fi
```

The exact bot login varies (`copilot-pull-request-reviewer[bot]` / `Copilot`). The case-insensitive `test("copilot"; "i")` match is intentional — don't hardcode an exact login.

### Phase 4 — Monitor checks and Copilot review

Poll every 30 s, max 30 iterations = 15 min. Break early when **both** are done. Full polling pattern, jq queries, and "is Copilot done?" heuristics: [references/monitoring-ci-and-copilot.md](references/monitoring-ci-and-copilot.md).

While polling, narrate progress in **single-line updates** ("iter 4/30: 3 checks running, copilot pending"). Do NOT print large JSON blobs to the user — those go to logs.

If the 15 min budget exhausts:
- If checks are still running: report which jobs and proceed to analysis with what completed.
- If Copilot is still pending: report and analyse CI-only; tell the user they can re-run `/pr` later to pick up the Copilot review.

### Phase 5 — Analyse and report

Two analyses run in parallel; one merged report:

1. **CI failures** — `gh run view <id> --log-failed` for each failed run, extract the error lines (look for `FAIL`, `Error`, `Traceback`, `assert`, lines ending with `:[0-9]+:` for compiler errors). Cap at 10 lines per failed step.
2. **Copilot inline comments** — `gh api repos/{owner}/{repo}/pulls/{N}/comments` → for each comment, match the `path` against every `.github/instructions/*.instructions.md` `applyTo` glob and tag it with the matched skill(s).

Output format and severity heuristics: [references/analyzing-results.md](references/analyzing-results.md).

## What this skill does NOT do

- Does not push for the user (assumes branch is already pushed; tells the user to push if not).
- Does not fix the issues Copilot raises — only surfaces them with the canonical-skill pointer so the user / next skill invocation can act.
- Does not enable automatic Copilot review at the repo level — that's a one-time UI step (Settings → Rules → Rulesets).
- Does not stream raw `gh run view --log-failed` output into the chat — extracts just the error lines.

## References

- [creating-the-pr.md](references/creating-the-pr.md) — `gh pr create` patterns, title/body autofill, push-check
- [monitoring-ci-and-copilot.md](references/monitoring-ci-and-copilot.md) — polling loop, jq queries, "done" heuristics
- [analyzing-results.md](references/analyzing-results.md) — CI log extraction, Copilot-comment → skill matching, output format
