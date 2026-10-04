---
name: ship-push-only
description: For advisory / team-owned repos where humans own PR review and merge. Implement → test → code review → push feature branch. Stop. Do NOT open a PR; do NOT merge; do NOT deploy. Notify the reviewer and hand off.
---

# Ship Push-Only

For repos where the team owns the PR/merge/deploy flow and Claude's role ends at "branch is pushed and clean." Common in advisory engagements where the project has many users in production and a team-owned review process. Pushing commits is fine; opening PRs and merging is not.

## Pipeline

### 1. Code Review (parallel background agents)

Same as `ship-auto` step 1 — Claude review + codex review in parallel. Fix BLOCKING findings. This catches issues before the human reviewer even sees the branch, which makes their review cheaper.

### 2. Definition of Done

Same as `ship-auto` step 2.

### 3. Push the branch

```bash
git push -u origin <branch>
```

That's it. **Do NOT** run `gh pr create`. **Do NOT** auto-open a PR.

### 4. Notify the reviewer

Surface to the user in a single message:
- Branch name + commit summary (one line per commit)
- Diff stats (`git diff --stat <base>...HEAD`)
- Local code review findings (if any non-blocking advisories surfaced — flag them so the human reviewer can confirm or dismiss)
- Test status (passing, list of test files)
- Suggested PR title + 2-3 bullet description, ready to paste — but **don't** open it

Then stop. The PR opening, review cycle, merge, and deploy are the human reviewer's call.

## What NOT to do

- Don't `gh pr create` — even with "draft" or "ready-for-review" status. The team's process owns this.
- Don't message the team directly. Hand off to the user; he relays.
- Don't run any deploy command, even ones the repo defines. Production deploys are the team's owned action.
- Don't pre-emptively address review feedback that hasn't been written yet. Wait for actual comments.

## D-class

Same gates as `ship-auto` apply for any operations that *do* run (e.g., the local code review, branch push to a non-default branch). Pushes to feature branches are fine; pushes to `main` / `master` are D-class.

## When team practice changes

If the team adopts a more automated flow later, the project's `CLAUDE.md` switches to `Ship skill: ship-auto` (or `ship-guarded`) and this skill is no longer invoked for that repo.
