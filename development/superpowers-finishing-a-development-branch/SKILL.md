---
name: superpowers-finishing-a-development-branch
description: 'Use when all tasks in a plan are complete — run the full ship pipeline
  from code to merged PR: detect base branch, verify clean working tree, merge base
  with conflict gate, run tests with hard gate on current-branch failures, audit coverage
  for diff gaps, verify all plan items addressed, run pre-landing code review, auto-decide
  MICRO/PATCH version bumps, generate and format changelog, update TODOs, bisect-friendly
  commit, push with upstream tracking, create PR with review evidence checklist, and
  optional documentation sync. Purpose: Replace the fragmented pick-an-option finishing
  flow with a single disciplined pipeline where no step is skipped and no PR ships
  without passing every gate. Key capabilities: hard gates that stop the pipeline
  rather than skip failing steps; plan completion audit that reports NOT DONE items
  and refuses to ship incomplete work; per-item coverage audit (happy path, nil/null,
  error, empty state); changelog generated from git log and prepended in keep-a-changelog
  format; version auto-decision (MICRO/PATCH auto-bumped, MINOR/MAJOR asked); review
  readiness dashboard showing all gates before final verdict. Also for: landing single-commit
  hotfixes; shipping cleanup or refactor branches; promoting experimental branches
  to production-ready; managing the terminal step of any subagent-driven workflow.'
---

# Ship — Finish and Publish

**Core principle:** Never skip tests or reviews. Completeness first.

This skill replaces the old "4 options" flow with a full automated pipeline that ends with a PR.

---

## Step 0: Detect Base Branch

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
CURRENT_BRANCH=$(git branch --show-current)
echo "Base: ${BASE_BRANCH:-main}"
echo "Feature: $CURRENT_BRANCH"
```

---

## Step 1: Verify Clean Working Tree

```bash
git status --porcelain
```

If dirty:
- Offer to stash: `git stash push -m "wip: ship pipeline $(date)"`
- Or commit as WIP: `git commit -m "WIP: ship pipeline $(date)" --allow-empty`

Proceed only with a clean tree.

---

## Step 2: Merge Base

```bash
git fetch origin "$BASE_BRANCH" --quiet 2>/dev/null || true
echo "Merging base into feature branch..."
git merge "origin/$BASE_BRANCH" --no-edit
```

If merge conflicts → STOP. Report conflicts. Do not proceed.

---

## Step 3: Run Tests

Run the project's test suite:

```bash
# Run the test command (adjust to project)
npm test 2>&1 || pytest 2>&1 || bun test 2>&1 || cargo test 2>&1 || true
```

**If tests fail:**
1. First check: are failures in the current branch? → Fix them
2. Second check: are failures pre-existing on base? → Report but don't block
3. If unclear → STOP. Do not ship with failing tests.

**Hard gate:** If the current branch has failing tests, fix them before proceeding.

---

## Step 4: Coverage Audit

Trace every code path in the diff and map user flows:

```bash
git fetch origin "$BASE_BRANCH" --quiet 2>/dev/null || true
BASE_SHA=$(git rev-parse "origin/$BASE_BRANCH")
HEAD_SHA=$(git rev-parse HEAD)
git diff "$BASE_SHA..$HEAD_SHA" --stat
```

1. **Codepath tracing** — For each changed function, trace: happy path, nil/null, error, empty state
2. **User flow mapping** — Map changed code to user-facing flows it affects
3. **Gap identification** — Which paths have no test?
4. **Gap remediation** — Write tests for critical gaps now, or flag informational gaps

---

## Step 5: Plan Completion Audit

Read the implementation plan (if one exists):

```bash
ls docs/superpowers/plans/*.md 2>/dev/null | head -5
cat docs/superpowers/plans/*.md 2>/dev/null | head -200 || echo "No plan found"
```

Check if all plan items are addressed in the diff:

| Plan Item | Status |
|-----------|--------|
| [item 1] | DONE / NOT DONE / PARTIAL |
| [item 2] | DONE / NOT DONE / PARTIAL |

**If any NOT DONE items exist:** STOP and report. Do not ship incomplete work.

---

## Step 6: Pre-Landing Review

Run `superpowers-requesting-code-review` against the diff. If it finds CRITICAL issues, fix them first.

---

## Step 7: Version Bump

Auto-detect bump type:

```bash
echo "Changes since last version tag:"
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo "origin/$BASE_BRANCH")..HEAD --format="%s" | head -20
```

| Type | Trigger |
|------|---------|
| **MICRO** | Docs, comments, typos, formatting |
| **PATCH** | Bug fixes, minor improvements |
| **MINOR** | New features, breaking changes |
| **MAJOR** | Breaking changes, API redesign |

Auto-decide MICRO and PATCH. Ask the user for MINOR and MAJOR.

```bash
# Auto-bump MICRO/PATCH
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Current version: $CURRENT_VERSION"
echo "Suggested bump: [MICRO/PATCH] — [reason]"
```

---

## Step 8: CHANGELOG

Generate changelog from commit history since last version:

```bash
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo "origin/$BASE_BRANCH")..HEAD --format="%s"
```

Categorize commits into:
- **Added** — New features
- **Changed** — Changes to existing functionality
- **Fixed** — Bug fixes
- **Improved** — Performance, refactoring, quality
- **Docs** — Documentation

If CHANGELOG.md exists, prepend new entries. Format:

```markdown
## [VERSION] — YYYY-MM-DD

### Added
- [feature description] — #[PR]

### Fixed
- [fix description] — #[PR]
```

---

## Step 9: TODOs Update

```bash
cat TODOS.md 2>/dev/null || echo "No TODOs.md found"
```

- Mark completed TODOs as done
- Remove TODOs that are no longer relevant
- Flag TODOs that reference code that no longer exists

---

## Step 10: Commit

Split into bisectable logical chunks:

```bash
git add -p
echo "Files staged:"
git diff --cached --stat
```

Commit message format:
```bash
git commit -m "[type]: [brief description]

[Longer description if needed]

Reviewed with: superpowers-requesting-code-review"
```

For multiple commits: commit related changes together, unrelated changes separately.

---

## Step 11: Push

```bash
git push -u origin "$CURRENT_BRANCH"
```

---

## Step 12: Create PR

```bash
echo "Creating PR from $CURRENT_BRANCH to $BASE_BRANCH..."

gh pr create \
  --base "$BASE_BRANCH" \
  --head "$CURRENT_BRANCH" \
  --title "[VERSION] — [summary]" \
  --body "$(cat <<'EOF'
## What changed
[auto-generated from changelog]

## Review evidence
- [x] Tests pass
- [x] Coverage audit complete
- [x] Plan items addressed
- [x] Code review passed

## TODOs updated
[yes/no — checked]

## Checklist
- [ ] Approved
- [ ] CI green
- [ ] Ready to merge

---
_Shipped with superpowers_
EOF
)"
```

---

## Step 13: Review Readiness Dashboard

Before presenting the final summary, confirm all gates:

```
REVIEW READINESS DASHBOARD
══════════════════════════════════════════
Test results:         [PASS / FAIL] · [N] failures
Coverage audit:        [COMPLETE / INCOMPLETE] · [N] gaps
Plan completion:       [DONE / N items pending]
Code review:           [PASSED / N issues] · [N] critical
TODOs updated:         [YES / NO]
Version bumped:        [VERSION]
CHANGELOG updated:     [YES / NO]
PR created:            [URL]
══════════════════════════════════════════
VERDICT: [READY TO MERGE / BLOCKED — see above]
```

---

## Step 14: Document Sync (optional)

If the project has documentation that references the changed code:
- Update README if API/behavior changed
- Update ARCHITECTURE.md if structure changed
- Update inline code examples
- Commit docs changes separately

---

## Key Rules

- **Never skip tests** — hard gate, no exceptions
- **Never merge with failing tests** in the current branch
- **Never skip the review** — critical issues must be fixed
- **Never ship incomplete work** — plan audit gates shipping
- **Auto-decide MICRO/PATCH** — only ask for MINOR/MAJOR

---

## When to Stop

Stop and ask for user input when:
- Tests fail in current branch
- Merge conflicts exist
- Critical review issues found
- Plan items are NOT DONE
- MINOR or MAJOR version bump needed
- More than 3 AUTO-FIX items needed (batch for approval)

---

## Integration

- **Called by:** `superpowers-subagent-driven-development` (final step)
- **Calls:** `superpowers-requesting-code-review` (Step 6)
- **Pairs with:** `superpowers-using-git-worktrees` for isolated ship pipeline
