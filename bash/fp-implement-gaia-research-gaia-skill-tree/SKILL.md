---
name: fp-implement
description: >-
  Phase 3 of the feature-pipeline suite. Use this after /fp-plan has received
  explicit user approval and printed the M2-plan stop hook — when you need to
  translate an approved numbered plan into committed, pushed code. Triggers on:
  "implement the plan", "start coding", "commit the plan", "write the code",
  "fp-implement", "Phase 3", "plan is approved let's code", "next step after
  plan", "execute the plan", "apply the plan", "make the changes". Reads
  planApproved and branch from state; refuses to run if approval hasn't been
  recorded. Commits one atomic change per plan step, pushes after each commit,
  handles obstacles cleanly, and hands off to /fp-review when done. Never
  squashes or skips steps — the one-commit-per-step rule keeps the review
  history readable and rollback surgical.
version: 3.0.0
---

# fp-implement  (Phase 3 — Implementation)

Translate the approved plan into commits, one step at a time. Each step is a
self-contained atomic commit pushed immediately — so if this turn is
interrupted, nothing is lost and the next run can pick up where it left off.

---

## Setup

```bash
STATE=".agents/skills/feature-pipeline/scripts/state.sh"
```

Check preconditions before touching any code. Skipping this check is how bad
state propagates — an unapproved plan being implemented defeats the whole
purpose of the approval gate in /fp-plan:

```bash
approved=$($STATE get planApproved)   # must be "true"
branch=$($STATE get branch)
pr=$($STATE get prNumber)
```

If `planApproved != true`, tell the user clearly and end the turn:

```
⚠ Plan not yet approved. Run /fp-plan first and wait for approval.
```

Checkout the branch so all commits land in the right place:

```bash
git checkout "$branch"
```

---

## Reading the plan

Fetch the approved plan from the PR body — this is the source of truth because
the user may have edited it during the approval step in /fp-plan:

```bash
gh pr view "$pr" --json body
```

If the fetch fails or the `## Plan` section is empty, ask the user to paste
the plan. Don't guess or reconstruct from memory.

---

## Implementation loop

Work through each numbered step in order. The one-step-one-commit discipline
matters: it keeps the diff reviewable, makes rollback surgical (`git revert`
on a single commit), and gives /fp-review clear commit messages to annotate.

For each step:

1. Implement the change in the relevant file(s). Read the file before editing
   so you don't clobber unrelated content.

2. Stage only the relevant hunks — don't sweep in unrelated changes:
   ```bash
   git add -p   # or git add <specific-files> when the step is clearly scoped
   ```

3. Commit with a conventional message so CI and reviewers can parse intent:
   ```bash
   git commit -m "<type>(<scope>): <description>"
   git push
   ```

4. Print one confirmation line:
   ```
     ✓ Step N committed: <short-hash>  <commit message>
   ```

### Handling obstacles

If a step hits an unexpected blocker (import error, schema conflict, test
failure that reveals a new problem not in the plan) — stop immediately. Partial
work committed half-done is harder to untangle than a clean stop with a note.

- Leave a `TODO` comment at the exact location explaining what's needed.
- Commit the partial work so nothing is lost:
  ```bash
  git commit -m "wip(<scope>): partial step N — <obstacle summary>"
  git push
  ```
- Record the blockage in state so the next run can see it:
  ```bash
  $STATE set ciStatus "blocked"
  ```
- Print what the obstacle is, what file/line is involved, and what additional
  information would unblock it. Then end your turn — don't attempt the next
  step while this one is unresolved.

---

## Phase completion

When all steps are committed and pushed, advance state so /fp-review knows to
start the sandbox pass:

```bash
$STATE set phase 4
```

Update the PR labels to reflect current status. `needs-plan` is no longer
accurate once code exists; `in-progress` signals the PR is ready for review:

```bash
# via GitHub MCP:
mcp__github__update_pull_request — remove "needs-plan", add "in-progress"
```

Print the M2 stop hook and end your turn. The stop hook is mandatory — it's
what tells the user which skill to run next and gives them a moment to scan
the commit list before review starts:

```
╔══ STOP HOOK M2 ══════════════════════════════════════════════════════════════╗
║  Implementation complete — <N> commits pushed to <branch>                    ║
║  Run /fp-review to start sandbox review.                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Constraints

- One commit per plan step — no squashing, no combining steps. Reviewers need
  to be able to understand each change in isolation.
- Never commit secrets, generated registry artifacts (`docs/graph/*`,
  `registry/gaia.json`), or files unrelated to the current step.
- Any registry mutations (`registry/nodes/`) must go through
  `gaia dev add` / `gaia dev merge` / `gaia dev split` — hand-edits skip
  timeline logging and break the audit trail.
- No force-pushes. If a commit needs to be undone, use `git revert`.
- End the turn after the stop hook. Sandbox review belongs to /fp-review.
