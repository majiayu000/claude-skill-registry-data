---
name: branch-finishing
description: Apply when closing out a feature branch — pre-merge checklist, rebase, CI verification, cleanup, and post-merge steps.
license: MIT
version: 1.0.0
tokens_target: 1400
triggers:
  - finish branch
  - pre-merge checklist
  - branch cleanup
loads_after:
  - git-conventions
supersedes: []
---

# Sub-Skill: Branch Finishing

**Purpose:** Ensures every feature branch is cleanly rebased, reviewed, and merged without introducing regressions or leaving stale local state behind.

---

## Rules

### Pre-Merge Preparation

1. **Rebase before merge.** Always rebase onto the target branch immediately before requesting merge to catch regressions introduced since the branch was cut. Reference: ERR-2026-024
2. **Resolve conflicts locally.** Before pushing a rebase, resolve every conflict locally and run the full test suite; never push a branch with unresolved markers.
3. **CI green before review.** Ensure all CI checks pass on the latest push before requesting a human review; do not ask reviewers to look at a red branch.
4. **Self-review diff.** Before opening a PR, run `git diff main...HEAD` and read every changed line; catch debug prints, commented-out code, and accidental file inclusions yourself first.

### Commit Hygiene

5. **Squash fixup commits.** Before merge, squash or fixup any `wip:`, `fixup!`, or `tmp:` commits so the branch history is clean; use `git rebase -i` to consolidate.
6. **Issue closing keywords.** Use `Closes #NNN` or `Fixes #NNN` in the PR body so the linked issue auto-closes on merge; never leave issues open manually after a successful merge.
7. **Changelog update.** After any user-visible change, add an entry to `CHANGELOG.md` (or the project's equivalent) before marking the PR ready for review.
8. **Version bump.** If the project uses semantic versioning, bump the version in the appropriate manifest file as part of the branch before merge, not as a follow-up commit.

### Draft → Ready Transition

9. **Draft until CI passes.** Keep the PR in draft state until all CI checks are green and the self-review is complete; convert to ready-for-review only when the branch is genuinely merge-ready.
10. **Remove draft status explicitly.** Use `gh pr ready <number>` to convert from draft; do not rely on reviewers noticing a draft PR that was silently updated.

### Post-Merge Cleanup

11. **Delete remote branch after merge.** After a successful merge, delete the remote branch with `git push origin --delete <branch>` or enable auto-delete in repository settings; stale remote branches pollute the branch list.
12. **Delete local branch after merge.** After confirming the remote merge, delete the local tracking branch with `git branch -d <branch>` to keep the local workspace clean.
13. **Post-merge verification.** After merge, pull `main` locally and run the test suite once to confirm the integrated state is green; do not assume CI on the PR branch is sufficient.

### Conflict Resolution

14. **Prefer rebase over merge commits.** Avoid merge commits on feature branches; use `git rebase` to maintain a linear history unless the team explicitly requires merge commits.

---

## See also

- `skills/git-conventions/SKILL.md`
- `skills/review-deployment/SKILL.md`
