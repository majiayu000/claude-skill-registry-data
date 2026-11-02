---
name: write-pull-request
description: Write clear commits and pull requests that a reviewer can check quickly. Use this whenever you commit, push, open or update a pull request, or draft a commit message or PR description.
---

# Write a pull request

A reviewer needs to know why the change exists, what it does and how you know it
works. Writing those down well is often the difference between a quick review and
a long one.

## When to use

Any commit or pull request. Commit, push or open a PR only when the user asked you
to, because these are visible to other people.

## Steps

1. **Finish verification first.** Follow `verify-and-report`.

2. **Check what you are committing.**

   ```bash
   git status --short
   git diff --staged
   ```

   Stage named files. Avoid `git add .`, which can pick up secrets and scratch files.

3. **Follow the project's format.** Run `git log --oneline -20`, and match it. Check
   for a commit convention or a PR template in the repository.

4. **Keep commits to one purpose.** Explain why in the message. The diff already
   shows what changed.

5. **Branch from the current default branch.** Never push directly to it unless the
   project does that and the user asked.

6. **Write the PR.** Use the template below. Use real numbers, and only ones you
   measured. Keep it short enough to read.

7. **Check CI after pushing.** If it fails, read the log and fix the cause. Do not
   merge unless you were asked to.

## Stop and ask when

- You were not asked to commit or push.
- Hooks fail. Fix the cause, and do not bypass them with `--no-verify`.
- You would need to force push a shared branch.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Commit message "fix bug" | Useless in history | Say what broke and why |
| Mix a refactor with a feature | Hard to review | Split the commits |
| Paste the diff into the description | Adds nothing | Explain the reason |
| Claim tests that you did not run | A false record | List only what you ran |
| Hide known gaps | Reviewers will miss them | List them |

## Example

```markdown
fix(billing): stop double refunds on webhook retries

The provider retries webhooks after a timeout, and `applyRefund` had no duplicate
check, so a retry credited the customer again. Store the event id in the same
transaction, and skip events already seen.
```

## Report

Use this as the pull request description:

```markdown
## Why
<The problem and its evidence: numbers, logs or links.>

## Change
<What changed, by area. Mention behaviour that stays the same on purpose.>

## Validation
<Commands and results. For a bug fix, how the old code fails.>

## Not included
<Known gaps, follow-ups and anything unverified.>
```
