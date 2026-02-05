---
name: git.pr.create
description: Create comprehensive pull requests with auto-generated summaries, test plans, and proper Carbon ACX formatting.
---

# git.pr.create

## Purpose

This skill automates pull request creation for Carbon ACX by:
- Analyzing complete branch history from base branch divergence
- Generating comprehensive PR summaries covering ALL commits (not just latest)
- Creating structured test plans
- Pushing branches if needed
- Using GitHub CLI to create PRs with proper formatting
- Applying appropriate labels and linking issues

## When to Use

**Trigger Patterns:**
- "Create a pull request"
- "Open a PR"
- "Make a PR for this branch"
- "Submit this for review"
- After completing feature/fix work on a branch

**Do NOT Use When:**
- Still working on feature (not ready for review)
- No commits on branch yet
- Branch has uncommitted changes (commit first)
- Creating a draft PR (different workflow - add `--draft` flag)

## Allowed Tools

- `bash` - Git and gh CLI commands
- `read_file` - Read modified files for context
- `grep` - Search codebase for related code

**Access Level:** 2 (Git operations - can push branches, create PRs)

**Tool Rationale:**
- `bash`: Required for git and gh commands
- `read_file`: Understand changes for better PR descriptions
- `grep`: Find related code for comprehensive context

**Explicitly Denied:**
- No force pushing
- No modifying code during PR creation
- No auto-merging PRs

## Expected I/O

**Input:**
- Type: PR creation request
- Context: Branch with commits ready for review
- Optional: User-provided PR title or description hints
- Optional: Base branch (defaults to main/master)

**Example:**
```
"Create a PR for this UX improvements branch"
"Open a pull request to main"
"Create PR: adds dark mode feature"
```

**Output:**
- Type: Pull request URL
- Format: GitHub PR link
- Includes:
  - PR number and title
  - Summary of changes (all commits)
  - Test plan checklist
  - Link to PR for review

**Validation:**
- PR body includes Summary section
- PR body includes Test Plan section
- PR includes Claude Code footer
- All commits pushed to remote
- PR successfully created on GitHub

## Dependencies

**Required:**
- Git repository with remote configured
- `gh` CLI installed and authenticated
- Branch with commits (different from base branch)
- GitHub repository accessible

**Optional:**
- CI/CD workflows (will run automatically on PR)
- Issue tracker for linking issues

## Workflow

### Step 1: Determine Base Branch

```bash
# Get current branch
git rev-parse --abbrev-ref HEAD

# Check if main or master exists
git rev-parse --verify main 2>/dev/null || git rev-parse --verify master 2>/dev/null
```

**Default base:** `main` (or `master` if main doesn't exist)
**User can override:** "Create PR to develop branch"

### Step 2: Analyze Complete Branch History

Run in parallel:
```bash
# All commits on this branch (from divergence point)
git log main...HEAD --oneline

# Full diff from base
git diff main...HEAD --stat

# Current status
git status

# Check remote tracking
git rev-parse --abbrev-ref @{upstream}
```

**CRITICAL:** Must analyze ALL commits in branch, not just the latest one!

**Analysis:**
- How many commits?
- What types (feat, fix, chore, docs)?
- Which files/components affected?
- Any breaking changes?
- Related issues mentioned in commits?

### Step 3: Draft PR Title

**Format:** `<type>(<scope>): <concise description>`

**Examples:**
- `feat(web): add dark mode toggle to dashboard`
- `fix(calc): correct aviation emission factor calculation`
- `chore(deps): update React and TypeScript dependencies`
- `refactor(web): reorganize components into feature folders`

**Rules:**
- Max 72 characters
- Imperative mood
- Lowercase after colon
- Summarizes PRIMARY change (if multiple types, use most significant)

### Step 4: Draft PR Body

**Template:**
```markdown
## Summary
- **Change 1:** Brief description with context
- **Change 2:** Another key change
- **Change 3:** Additional important detail
(Continue for all significant changes)

## Test Plan
- [ ] Specific test action 1
- [ ] Verification step 2
- [ ] Final check 3
(Comprehensive checklist based on changes)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Summary Section:**
- Bullet points, 3-10 items typically
- Each bullet explains WHAT changed and WHY
- Group related commits together
- Highlight breaking changes prominently
- Include performance/security implications
- Reference file paths for context

**Test Plan Section:**
- Checkbox format `- [ ] Task`
- Specific, actionable tests
- Cover all affected functionality
- Include edge cases if relevant
- Manual testing steps
- Automated test commands where applicable

**Examples of Good Summaries:**
```markdown
## Summary
- **Dark mode support:** Adds theme toggle in header with localStorage persistence, allowing users to switch between light/dark themes
- **Accessibility improvements:** All theme colors now meet WCAG AA contrast ratios, tested with axe-core
- **Component updates:** Updated 12 components to support theme variables instead of hardcoded colors
- **Documentation:** Added theme customization guide to docs/THEMING.md
```

**Examples of Good Test Plans:**
```markdown
## Test Plan
- [ ] Toggle theme in header - verify colors switch immediately
- [ ] Refresh page - verify theme preference persists
- [ ] Test all chart components in both themes
- [ ] Run accessibility audit: `pnpm run a11y-check`
- [ ] Verify contrast ratios with browser DevTools
- [ ] Test on mobile viewport (theme toggle should be accessible)
- [ ] Run full test suite: `pnpm test`
```

### Step 5: Push Branch (if needed)

```bash
# Check if branch tracks remote
git rev-parse --abbrev-ref @{upstream} 2>/dev/null

# If no upstream, push with -u flag
git push -u origin $(git rev-parse --abbrev-ref HEAD)

# If already tracking, just push
git push
```

### Step 6: Create PR via GitHub CLI

Use HEREDOC for proper formatting:

```bash
gh pr create \
  --base main \
  --title "feat(web): add dark mode toggle to dashboard" \
  --body "$(cat <<'EOF'
## Summary
- **Dark mode support:** Adds theme toggle in header with localStorage persistence
- **Accessibility improvements:** All theme colors meet WCAG AA contrast ratios
- **Component updates:** Updated 12 components to support theme variables

## Test Plan
- [ ] Toggle theme in header - verify colors switch
- [ ] Refresh page - verify theme persists
- [ ] Run accessibility audit: `pnpm run a11y-check`
- [ ] Run full test suite: `pnpm test`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Optional flags:**
- `--label "ai-generated"` - If AI wrote significant code
- `--draft` - If user wants draft PR
- `--assignee @me` - Auto-assign to current user

### Step 7: Link Issues (if mentioned in commits)

Check commits for issue references:
```bash
git log main...HEAD --oneline | grep -E "#[0-9]+"
```

If found, include in PR body:
- `Closes #123` - Will auto-close issue when merged
- `Fixes #456` - Same as Closes
- `Relates to #789` - Links without closing

### Step 8: Report Success

**Output to user:**
```
✅ Pull Request Created

PR #42: feat(web): add dark mode toggle to dashboard
URL: https://github.com/owner/carbon-acx/pull/42

Summary: 5 commits, 12 files changed
- feat(web): dark mode support
- test(web): add theme switching tests
- docs: update theming guide
- fix(web): contrast ratio adjustments
- chore: update dependencies

Next Steps:
- Review the PR description
- Request reviewers if needed
- Monitor CI/CD checks
- Address any feedback
```

## Examples

### Example 1: Feature PR

**User:** "Create a PR for the emission chart component"

**Claude Process:**
1. Get current branch: `feat/emission-chart-component`
2. Analyze commits:
   ```
   git log main...HEAD --oneline
   a1b2c3d feat(web): add EmissionChart component
   d4e5f6g test(web): add EmissionChart tests
   g7h8i9j docs: update component documentation
   ```
3. Analyze diff: 4 files changed (component, test, story, docs)
4. Draft PR:
   - **Title:** `feat(web): add EmissionChart component for layer visualization`
   - **Summary:**
     - New reusable chart component using Recharts
     - Displays emission data by layer with tooltips
     - Responsive design and accessibility labels
     - Includes Storybook stories and unit tests
   - **Test Plan:**
     - Test chart renders with sample data
     - Verify responsive behavior on mobile
     - Check accessibility with screen reader
     - Run test suite: `pnpm test`
5. Push branch: `git push -u origin feat/emission-chart-component`
6. Create PR: `gh pr create ...`
7. Return URL: `https://github.com/owner/carbon-acx/pull/123`

### Example 2: Bug Fix PR

**User:** "Open a PR for the aviation calculation fix"

**Claude Process:**
1. Branch: `fix/aviation-emission-factor`
2. Commits:
   ```
   fix(calc): correct aviation emission factor multiplier
   test(calc): add regression test for aviation calculations
   ```
3. Analyze: `calc/derive.py` modified (1 line), `tests/test_aviation.py` added
4. Draft PR:
   - **Title:** `fix(calc): correct aviation emission factor calculation`
   - **Summary:**
     - Fixed unit conversion error (was using kg, should be tCO2e)
     - Added regression test to prevent future errors
     - Verified against reference data from ICAO
   - **Test Plan:**
     - Run full test suite: `pytest tests/`
     - Verify aviation emissions match expected values
     - Check all other layers unaffected
     - Rebuild dataset: `make build`
5. Check commits for issue refs: Found `Fixes #128`
6. Create PR with issue link
7. Apply `bug` label if available

### Example 3: Multi-Commit Refactor PR

**User:** "Create PR for component reorganization"

**Claude Process:**
1. Branch: `refactor/component-structure`
2. Analyze 8 commits:
   ```
   refactor(web): create charts/ directory
   refactor(web): move chart components to charts/
   refactor(web): create forms/ directory
   refactor(web): move form components to forms/
   refactor(web): create layout/ directory
   refactor(web): move layout components
   refactor(web): update all imports
   test(web): verify all imports resolve
   ```
3. Diff: 45 files changed (mostly moves + import updates)
4. Draft PR:
   - **Title:** `refactor(web): reorganize components into feature-based structure`
   - **Summary:**
     - Restructured flat component directory into feature folders
     - Groups: charts/, forms/, layout/, shared/
     - Updated all imports across codebase
     - No functional changes - only organization
     - Improves discoverability and maintainability
   - **Test Plan:**
     - Build succeeds: `pnpm build`
     - All tests pass: `pnpm test`
     - Dev server runs: `pnpm dev`
     - No broken imports in browser console
     - Verify Storybook still works: `pnpm storybook`
5. Create PR
6. Suggest reviewers familiar with web app

### Example 4: Dependency Update PR

**User:** "Make a PR for the dependency updates"

**Claude Process:**
1. Branch: `chore/update-dependencies`
2. Commits:
   ```
   chore(deps): update React to 18.3.1
   chore(deps): update TypeScript to 5.5.4
   chore(deps): update Vite to 5.4.0
   test: verify all tests pass with new versions
   ```
3. Files: `package.json`, `pnpm-lock.yaml`
4. Draft PR:
   - **Title:** `chore(deps): update React, TypeScript, and Vite`
   - **Summary:**
     - React 18.2.0 → 18.3.1 (security patch for XSS vulnerability)
     - TypeScript 5.5.3 → 5.5.4 (bug fixes for type inference)
     - Vite 5.3.5 → 5.4.0 (HMR performance improvements)
     - All tests passing with updated versions
     - No breaking changes
   - **Test Plan:**
     - Full test suite: `pnpm test`
     - Type checking: `pnpm type-check`
     - Build production: `pnpm build`
     - Dev server: `pnpm dev` (verify HMR works)
     - Check bundle size: `pnpm run analyze`
5. Add changelog notes about security fix
6. Create PR with `dependencies` label

## Limitations

**Scope Limitations:**
- Cannot create PRs without commits on branch
- Cannot auto-merge PRs (requires human approval)
- Cannot request specific reviewers (user must do manually or we can add flag)
- Cannot create cross-repository PRs

**Known Edge Cases:**
- Branch has uncommitted changes → Warn user to commit first
- Branch not pushed to remote → Automatically push with `-u`
- Base branch has conflicts → Report conflict, suggest rebase
- No `gh` CLI installed → Report error with install instructions
- GitHub authentication expired → Report error, suggest `gh auth login`

**Performance Constraints:**
- Very large PRs (100+ commits) may take 30+ seconds to analyze
- Branches with binary files show limited context
- Cross-fork PRs require additional permissions

**Security Boundaries:**
- Does not modify code during PR creation
- Does not auto-merge
- Does not bypass branch protection rules
- Respects repository permissions

## Validation Criteria

**Success Metrics:**
- ✅ PR title follows conventional commit format
- ✅ PR body includes Summary section with 3+ bullet points
- ✅ PR body includes Test Plan with checkboxes
- ✅ PR includes Claude Code footer
- ✅ All commits analyzed (not just latest)
- ✅ Branch successfully pushed to remote
- ✅ PR created on GitHub
- ✅ User receives PR URL
- ✅ Related issues linked if mentioned in commits

**Failure Modes:**
- ❌ No commits on branch → Report error, suggest making commits
- ❌ `gh` not installed → Provide installation instructions
- ❌ Not authenticated → Suggest `gh auth login`
- ❌ Branch name conflicts with existing PR → Report, suggest closing old PR
- ❌ Network error → Retry once, then report to user

**Recovery:**
- If push fails: Check for force-push protection, suggest pull first
- If `gh pr create` fails: Show error, suggest manual creation with drafted text
- If unclear what changed: Ask user to describe PR purpose
- If too many commits: Group by type in summary

## Related Skills

**Composes With:**
- `git.commit.smart` - Create commits before making PR
- `git.branch.manage` - Create/manage branch before PR
- `carbon.data.qa` - Understand data changes for better PR context

**Dependencies:**
- Git configured with remotes
- `gh` CLI installed and authenticated

**Alternative Skills:**
- For commits: `git.commit.smart`
- For releases: `git.release.prep`

## Maintenance

**Owner:** Workspace Team (shared skill)
**Review Cycle:** Monthly
**Last Updated:** 2025-10-24
**Version:** 1.0.0

**Maintenance Notes:**
- Update PR template as Carbon ACX conventions evolve
- Adjust label assignment logic if repo adds new labels
- Keep test plan examples current with actual testing practices
- Review `gh` CLI flags as GitHub adds new PR features
