---
name: git.commit.smart
description: Intelligently create git commits with proper formatting, conventional commit style, and Carbon ACX footer conventions.
---

# git.commit.smart

## Purpose

This skill automates the creation of high-quality git commits for Carbon ACX by:
- Analyzing staged changes to understand what changed and why
- Drafting commit messages following conventional commit format
- Matching existing repository commit style
- Including standardized Claude Code footer
- Handling pre-commit hook failures gracefully
- Ensuring no secrets or credentials are committed

## When to Use

**Trigger Patterns:**
- "Create a commit"
- "Commit these changes"
- "Make a commit with..."
- User has staged changes and needs to commit
- After completing a task that modified files

**Do NOT Use When:**
- No changes are staged (`git status` shows clean)
- User wants to review changes first (show diff instead)
- Creating a pull request (use `git.pr.create` skill instead)
- Amending existing commits (different workflow)

## Allowed Tools

- `bash` - Run git commands (status, diff, log, add, commit)
- `read_file` - Read modified files for context
- `grep` - Search for patterns in changes

**Access Level:** 2 (File Modification - can create commits)

**Tool Rationale:**
- `bash`: Required for all git operations
- `read_file`: Helps understand changes for better commit messages
- `grep`: Search commit history for style patterns

**Explicitly Denied:**
- No `--no-verify` flag (never skip hooks)
- No force operations
- No git config modifications
- No committing files in `.gitignore` patterns

## Expected I/O

**Input:**
- Type: Commit request (implicit or explicit)
- Context: Staged files ready to commit
- Optional: User-provided commit message hint or scope

**Example:**
```
"Commit the UX improvements to the dashboard"
"Create a commit for these changes"
"Commit with message: fix typo in README"
```

**Output:**
- Type: Git commit successfully created
- Format: Commit hash + message summary
- Includes:
  - Files committed (summary)
  - Commit message used
  - Commit hash
  - Next steps suggestion (push, create PR, run tests)

**Validation:**
- Commit message follows conventional format
- No secrets detected in changes
- Pre-commit hooks passed (or handled)
- Commit footer includes Claude Code attribution

## Dependencies

**Required:**
- Git repository (`.git` directory exists)
- Git configured with user.name and user.email
- Changes staged for commit (`git add` already run)

**Optional:**
- Pre-commit hooks installed
- `gh` CLI for GitHub integration (for suggesting PR creation)

## Workflow

### Step 1: Gather Context

Run in parallel:
```bash
git status
git diff --staged
git log --oneline -10
```

**Analysis:**
- What files are staged?
- What type of changes (features, fixes, docs, chores)?
- What's the commit message style in recent history?

### Step 2: Draft Commit Message

**Format:**
```
<type>(<scope>): <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Conventional Commit Types:**
- `feat` - New feature
- `fix` - Bug fix
- `chore` - Maintenance, dependencies, tooling
- `docs` - Documentation only
- `refactor` - Code restructuring without behavior change
- `test` - Adding or updating tests
- `style` - Formatting, whitespace, missing semicolons
- `perf` - Performance improvements

**Scope Examples:**
- `web` - Modern web app (apps/carbon-acx-web)
- `site` - Static React site
- `calc` - Derivation engine
- `data` - CSV data files
- `workers` - Cloudflare Workers
- `ci` - CI/CD workflows

**Subject Line:**
- Max 72 characters
- Imperative mood ("add feature" not "added feature")
- No period at end
- Lowercase after colon

**Body:**
- Explain WHY, not WHAT (what is in the diff)
- Wrap at 100 characters
- Use bullet points for multiple reasons
- Reference issues: `Closes #123`, `Relates to #456`

### Step 3: Create Commit

Use HEREDOC for message:
```bash
git commit -m "$(cat <<'EOF'
feat(web): add dark mode toggle to dashboard

Users requested ability to switch between light and dark themes
for extended analysis sessions. This adds a theme toggle in the
header that persists preference to localStorage.

Closes #42

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 4: Handle Pre-commit Hooks

**If hook fails:**

1. Read hook output
2. Determine failure type:
   - **Linter errors:** Fix automatically if possible, re-commit
   - **Formatter changes:** Files were modified by hook
   - **Test failures:** Report to user, cannot auto-fix

**If hook modified files:**

```bash
# Check if safe to amend
git log -1 --format='%an %ae'  # Verify we're the author
git status                      # Verify not pushed yet

# If both checks pass:
git add .
git commit --amend --no-edit
```

**If unsafe to amend:**
- Create NEW commit with hook fixes (never amend other developers' work)

### Step 5: Confirm Success

```bash
git log -1 --oneline
git status
```

**Report to user:**
- ✅ Commit created: `abc1234 feat(web): add dark mode toggle`
- Files committed: 3 files changed, 127 insertions(+), 45 deletions(-)
- Next steps: Run tests, push to remote, or create PR?

## Examples

### Example 1: Feature Commit

**User:** "Commit the new emission chart component"

**Claude Process:**
1. Run `git status`, `git diff --staged`, `git log -10`
2. Analyze changes: New React component in `apps/carbon-acx-web/src/components/`
3. Draft message:
   ```
   feat(web): add EmissionChart component for layer visualization

   Creates reusable chart component using Recharts to display
   emission data by layer. Includes responsive design, hover
   tooltips, and accessibility labels.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
4. Execute commit
5. Report success with hash

### Example 2: Fix Commit

**User:** "Commit the bug fix"

**Claude Process:**
1. Analyze staged changes: Fix in `calc/derive.py` line 245
2. Read recent commits for style
3. Draft message:
   ```
   fix(calc): correct emission factor calculation for aviation layer

   Previous calculation was using wrong unit conversion factor
   (kg instead of tCO2e). This fixes the multiplier to match the
   emission_factors.csv schema.

   Fixes #128

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
4. Execute commit
5. Suggest running `pytest tests/` to verify fix

### Example 3: Chore Commit with Pre-commit Hook

**User:** "Commit the dependency updates"

**Claude Process:**
1. Analyze: `package.json` and `pnpm-lock.yaml` modified
2. Draft message:
   ```
   chore(deps): update React and TypeScript dependencies

   - React 18.2.0 → 18.3.1 (security patch)
   - TypeScript 5.5.3 → 5.5.4 (bug fixes)

   All tests pass with updated versions.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
3. Execute `git commit`
4. **Pre-commit hook runs and fails:** ESLint finds unused imports
5. Read hook output, identify issue
6. Run `pnpm run lint --fix` to auto-fix
7. Check authorship: matches current user ✅
8. Check pushed: branch is ahead, not pushed ✅
9. Amend commit:
   ```bash
   git add .
   git commit --amend --no-edit
   ```
10. Report: "Commit created (with pre-commit lint fixes applied)"

### Example 4: Documentation Commit

**User:** "Commit the README updates"

**Claude Process:**
1. Analyze: Only `README.md` changed
2. Draft message:
   ```
   docs: update installation instructions for pnpm workspaces

   Clarifies the difference between running commands from repo
   root vs within app directory. Adds troubleshooting section
   for common pnpm workspace issues.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
3. Execute commit
4. Suggest: "Documentation updated. Ready to push or create PR?"

### Example 5: Multi-file Refactor

**User:** "Commit these refactoring changes"

**Claude Process:**
1. Analyze: 8 files changed across `apps/carbon-acx-web/src/`
2. Identify pattern: Moving components to new directory structure
3. Draft message:
   ```
   refactor(web): reorganize components into feature-based folders

   Restructures components from flat directory to feature-based
   organization:
   - charts/ - All visualization components
   - forms/ - Activity and data entry forms
   - layout/ - Headers, footers, navigation

   No functional changes, only file moves and import updates.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
4. Execute commit
5. Suggest: "Run `pnpm test` to verify imports still resolve correctly"

## Limitations

**Scope Limitations:**
- Cannot commit unstaged changes (user must `git add` first)
- Cannot resolve merge conflicts (different skill)
- Cannot amend commits by other authors (safety constraint)
- Cannot skip pre-commit hooks without user approval

**Known Edge Cases:**
- Empty commits (no changes staged) → Report error, suggest `git add`
- Detached HEAD state → Warn user, suggest checking out branch
- Merge in progress → Warn, suggest completing or aborting merge first
- Untracked files only → Remind to `git add` files first

**Performance Constraints:**
- Very large diffs (1000+ files) may take 10-20 seconds to analyze
- Binary files can't be analyzed for context (rely on filenames)

**Security Boundaries:**
- Scans for common secret patterns (.env, credentials, API keys)
- Rejects commits with potential secrets (warns user)
- Cannot detect all possible credential formats
- User must manually review sensitive changes

## Validation Criteria

**Success Metrics:**
- ✅ Commit message follows conventional commit format
- ✅ Commit includes Claude Code footer
- ✅ Type and scope appropriate for changes
- ✅ Subject line ≤72 characters
- ✅ Body explains WHY (not just WHAT)
- ✅ No secrets detected in commit
- ✅ Pre-commit hooks passed or handled
- ✅ User informed of success and next steps

**Failure Modes:**
- ❌ No staged changes → Ask user to `git add` files
- ❌ Secret detected → Reject commit, warn user
- ❌ Pre-commit hook failed → Report error, suggest fixes
- ❌ Commit type unclear → Ask user for clarification
- ❌ Git not configured → Report error, suggest `git config`

**Recovery:**
- If uncertain about commit type: Ask user
- If hook fails repeatedly: Show error, ask user to investigate
- If secret detected: Explain pattern matched, ask user to confirm false positive
- If commit message unclear: Draft and ask user to review before committing

## Related Skills

**Composes With:**
- `git.pr.create` - After committing, create pull request
- `git.branch.manage` - Create branch before committing
- `schema.linter` - Validate data files before committing changes

**Dependencies:**
- None - foundational skill

**Alternative Skills:**
- For PRs: `git.pr.create`
- For releases: `git.release.prep`

## Maintenance

**Owner:** Workspace Team (shared skill)
**Review Cycle:** Monthly
**Last Updated:** 2025-10-24
**Version:** 1.0.0

**Maintenance Notes:**
- Update conventional commit types if Carbon ACX adds new categories
- Adjust secret detection patterns as new credential types emerge
- Review pre-commit hook handling as repo hooks evolve
- Keep commit message examples synchronized with actual repo style
