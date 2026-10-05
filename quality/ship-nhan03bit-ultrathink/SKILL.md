---
name: ship
description: Release orchestrator that drives code from development through testing, review, changelog generation, and deployment.
layer: orchestrator
category: orchestration
triggers:
  - "/ship"
  - "ship it"
  - "release this"
  - "deploy this"
  - "prepare a release"
  - "cut a release"
inputs:
  - Branch or commit range to ship
  - Optional version bump type (major, minor, patch)
  - Optional deployment target (production, staging, preview)
  - Optional release notes or highlights
outputs:
  - Test suite results (pass/fail report)
  - Code review summary
  - Generated changelog entry
  - Version bump applied
  - Git tag created
  - Pull request created (if applicable)
  - Deployment status
linksTo:
  - test
  - code-review
  - fix
  - debug
  - optimize
  - changelog-writer
  - commit-crafter
  - pr-writer
  - git-workflow
  - docs-writer
  - preview
linkedFrom:
  - cook
  - team
preferredNextSkills:
  - docs-writer
  - onboard
fallbackSkills:
  - test
  - code-review
riskLevel: high
memoryReadPolicy: full
memoryWritePolicy: always
sideEffects:
  - Runs test suite
  - May fix code issues found during review
  - Modifies version numbers in config files
  - Updates or creates CHANGELOG
  - Creates git tags
  - Creates git commits
  - Creates pull requests
  - May trigger deployments
---

# Ship

## Purpose

Ship is the release orchestrator. It takes code that's been developed and guides it through the final gauntlet: running the full test suite, performing a release-grade code review, generating the changelog, bumping the version, tagging, creating the PR, and optionally deploying. Ship is the quality gate between "code written" and "code in production."

Ship is deliberately cautious. It runs checks in a specific order, and any failure halts the pipeline with a clear report. It does not deploy broken code. It does not skip tests. It treats every release as a potential production incident waiting to happen and acts accordingly.

## Workflow

### Phase 1: Pre-flight Check
1. **Assess the release scope** -- Determine what's being shipped by examining the branch, commit range, or diff against the target branch.
2. **Invoke `git-workflow`** -- Verify the branch is clean, up to date with the base branch, and has no merge conflicts.
3. **Classify the release** -- Based on the changes, suggest a version bump:
   - **Patch**: Bug fixes, dependency updates, typo fixes
   - **Minor**: New features, non-breaking enhancements
   - **Major**: Breaking changes, API modifications, architecture shifts
4. **Present pre-flight report** -- Show the user what's being shipped, the suggested version, and any concerns. Get confirmation.

### Phase 2: Test
5. **Invoke `test`** -- Run the full test suite. This is not a quick spot-check; it's the full matrix:
   - Unit tests
   - Integration tests
   - End-to-end tests (if they exist)
   - Type checking
   - Linting
6. **Evaluate results** -- If any tests fail:
   - **Auto-fixable**: Invoke `fix` for straightforward failures (lint errors, type issues).
   - **Requires investigation**: Invoke `debug` for test failures that need root-cause analysis.
   - **Blocking**: If failures can't be resolved automatically, halt and report to user.
7. **Re-run tests** -- After fixes, run the suite again to confirm green.

### Phase 3: Review
8. **Invoke `code-review`** -- Perform a release-grade review of all changes:
   - Security: No secrets, no injection vectors, proper auth checks
   - Quality: No dead code, no TODO hacks, no console.logs
   - Performance: No obvious regressions, no N+1 queries
   - Completeness: No half-implemented features, no missing error handling
9. **Address review findings** -- Fix any issues rated as "must fix before release." Log "nice to have" items for follow-up.
10. **Invoke `optimize`** (if flagged) -- If the review identified performance concerns, run optimization.

### Phase 4: Changelog & Version
11. **Invoke `changelog-writer`** -- Generate a changelog entry from the commit history:
    - Group changes by category (Features, Bug Fixes, Breaking Changes, etc.)
    - Link to relevant PRs or issues
    - Highlight breaking changes prominently
12. **Bump version** -- Update version numbers in all relevant files (package.json, Cargo.toml, pyproject.toml, etc.).
13. **Invoke `commit-crafter`** -- Create a version bump commit.
14. **Invoke `git-workflow`** -- Create a git tag for the release.

### Phase 5: Ship
15. **Invoke `pr-writer`** -- Create a pull request with:
    - Release summary
    - Changelog excerpt
    - Test results summary
    - Migration notes (if any)
16. **Invoke `preview`** (if available) -- Generate a preview deployment for final visual verification.
17. **Deploy** (if authorized) -- Trigger deployment to the specified target:
    - Staging first, then production (if the pipeline supports it)
    - Or directly to production if the user confirms
18. **Post-ship report** -- Summarize what was shipped, the version, and any follow-up items.

## Quality Gates

Each gate must pass before proceeding to the next phase.

| Gate | Criteria | On Failure |
|------|----------|------------|
| Branch health | Clean, no conflicts, up to date | Fix branch issues first |
| Test suite | All tests pass | Fix failures or halt |
| Type check | No type errors | Fix type errors |
| Lint | No lint errors | Auto-fix or halt |
| Code review | No critical findings | Fix critical issues |
| Security scan | No vulnerabilities | Fix or document exceptions |
| Changelog | Generated and accurate | Edit manually if needed |
| Version bump | Applied correctly | Fix version files |

## Usage

Use Ship when code is ready to release. Ship is the final quality gate and should be invoked after `cook` or `team` has completed the development work.

**Best for:**
- Releasing a new version of a package or application
- Deploying features to production
- Creating release candidates for testing
- Cutting a release after a sprint

**Not ideal for:**
- Development work (use `cook` first)
- Hotfixes (use `cook` with expedited flow, then `ship` with `--hotfix` mindset)
- Initial project setup (use `bootstrap`)

## Examples

### Example 1: Standard release
```
User: /ship Release the current feature branch to production

Ship workflow:
1. git-workflow -> Check branch health, find 12 commits since last release
2. Pre-flight -> Suggest minor version bump (new features, no breaking changes)
3. test -> Run full suite: 247 tests pass, 0 fail
4. code-review -> Review all 12 commits, find 1 console.log to remove
5. fix -> Remove console.log, re-test
6. changelog-writer -> Generate entry with 3 features, 2 bug fixes
7. Version bump -> 1.3.0 -> 1.4.0
8. commit-crafter -> "chore: bump version to 1.4.0"
9. git-workflow -> Create tag v1.4.0
10. pr-writer -> Create release PR
11. Deploy -> Push to staging, verify, push to production
```

### Example 2: Hotfix release
```
User: /ship Ship this bugfix to production ASAP

Ship workflow:
1. git-workflow -> Verify hotfix branch from production
2. Pre-flight -> Suggest patch bump
3. test -> Run full suite (expedited: focus on affected areas)
4. code-review -> Focused review on the fix only
5. changelog-writer -> "Bug Fixes: Fix critical auth bypass in /api/auth"
6. Version bump -> 2.1.3 -> 2.1.4
7. commit-crafter + git-workflow -> Commit, tag v2.1.4
8. pr-writer -> Create hotfix PR with urgency flag
9. Deploy -> Directly to production after confirmation
```

### Example 3: Pre-release
```
User: /ship Create a beta release for testing

Ship workflow:
1. git-workflow -> Check branch health
2. Pre-flight -> Suggest 2.0.0-beta.1 (breaking changes detected)
3. test -> Run full suite
4. code-review -> Full review with focus on breaking changes
5. changelog-writer -> Highlight all breaking changes with migration guides
6. Version bump -> 2.0.0-beta.1
7. commit-crafter + git-workflow -> Commit, tag v2.0.0-beta.1
8. pr-writer -> Create PR labeled as pre-release
9. preview -> Deploy to preview/staging environment only
```

## Guardrails

- **Never skip tests.** Every release runs the full test suite. No exceptions.
- **Never ship with critical review findings.** Fix them or don't ship.
- **Always generate a changelog.** Every release must be documented.
- **Always tag releases.** Git tags are the source of truth for versions.
- **Confirm before deploying to production.** Always get explicit user confirmation for production deployments.
- **Keep the release atomic.** Don't mix unrelated changes into a release.
- **Document breaking changes.** If the release has breaking changes, they must be prominently documented with migration instructions.
