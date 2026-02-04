---
name: fix-pr-feedback
description: |
  Address PR feedback with iterative refinement. MUST BE USED when fixing PR issues.
  Supports auto-detection (CI failures, code review) and manual triage (user reports bugs). Creates Beads issues for all problems, fixes systematically.
  Use when user says "fix the PR", "i noticed bugs", "ci failures", or "codex review found issues",
  or when user mentions CI failures, review comments, failing tests, PR iterations,
  bug fixes, feedback loops, or systematic issue resolution.
tags: [workflow, pr, beads, debugging, iteration]
allowed-tools:
  - Bash(bd:*)
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(make:*)
  - Read
  - Edit
  - mcp__serena__*
---

# Fix PR Feedback

Address PR feedback with automated discovery tracking and iterative fixes.

## Purpose

Handles the iterative refinement loop after PR creation:
- Read PR comments (human reviews, bot comments)
- Check CI status (failing tests, linting errors)
- Detect merge conflicts
- Create child Beads issues for each discovery
- Fix issues or ask user for guidance
- Commit fixes with proper Feature-Key trailers
- Push updates to same branch

**Philosophy:** Fast feedback → Track discoveries → Iterative fixes → Trust environments

## When to Use This Skill

**Trigger phrases:**
- "fix the PR"
- "address the feedback"
- "fix CI failures"
- "resolve code review comments"
- "handle PR issues"
- "update the PR"
- "respond to review"
- "i noticed bugs" (manual triage mode)
- "codex review found issues" (manual triage mode)

**Automatically invoked when:**
- User mentions PR number and "fix" or "address"
- User asks about failing checks
- User wants to respond to code review
- User provides numbered bug list (e.g., "1. X, 2. Y, 3. Z")

## Modes

This skill operates in two modes:

### Mode 1: Auto-Detection (Existing)

**Triggers:** "fix the PR", "fix CI failures", "address the feedback"

**Workflow:**
1. Automatically read CI logs via `gh pr view --json statusCheckRollup`
2. Automatically read PR comments via `gh pr view --json comments`
3. Automatically detect merge conflicts
4. Parse and categorize all discoveries
5. Create Beads issues for each
6. Present summary to user
7. Fix based on user approval

**Use when:** PR exists and you want AI to discover all issues automatically

### Mode 2: Manual Triage (NEW)

**Triggers:** "i noticed bugs: 1. X, 2. Y", "ci failures: 1. A, 2. B", "codex review found issues: 1. P, 2. Q"

**Workflow:**
1. Parse user's numbered bug list
2. Create Beads issue for each bug
3. **MANDATORY DISCUSSION:** Present all bugs with Beads IDs to user
4. Get user approval (fix all, fix specific ones, skip some)
5. Fix approved bugs systematically (one at a time)
6. **Auto-commit per bug** with Feature-Key trailer
7. Push all commits at end
8. Confirm completion to user

**Use when:** User already knows what bugs exist (from CI logs, code review, manual testing)

**Example user input formats:**
```
"i noticed bugs: 1. MCP type error, 2. permission denied, 3. obsolete test"
"ci failures: 1. labeler format, 2. PR metadata missing"
"codex review: 1. Update tests, 2. Add docs"
```

**Key difference:** Manual mode CREATES issues from user's list, then discusses. Auto mode DISCOVERS issues from PR/CI, then discusses.

## Workflow

### 1. Get PR Context

```bash
# Get current branch
git branch --show-current
# Extract FEATURE_KEY from feature-<KEY>

# Get PR number
gh pr view --json number,url,title -q '.number'
# Or user provides PR number explicitly
```

### 2. Set Beads Context

```bash
# Get parent feature issue
bd show <FEATURE_KEY>
```

### 3. Gather PR Feedback

**Mode 1 (Auto-Detection): Read CI/PR automatically**

**A. Check CI Status**
```bash
gh pr view <PR_NUMBER> --json statusCheckRollup -q '.statusCheckRollup'
```

Parse results:
- Failing checks (conclusion: failure, error)
- Pending checks (conclusion: pending)
- Passing checks (conclusion: success)

**B. Read PR Comments**
```bash
gh pr view <PR_NUMBER> --json comments -q '.comments[] | {author:.author.login, body:.body, createdAt:.createdAt}'
```

Filter for:
- Code review comments (human reviewers)
- Bot comments (Codex, Danger, etc.)
- Recent comments (last 24 hours)

**C. Check Merge Conflicts**
```bash
gh pr view <PR_NUMBER> --json mergeable -q '.mergeable'
```

**Mode 2 (Manual Triage): Parse user's bug list**

```
User: "i noticed bugs: 1. MCP type error, 2. permission denied, 3. CI labeler format"

Parse numbered list:
bugs = [
  {num: 1, description: "MCP type error"},
  {num: 2, description: "permission denied"},
  {num: 3, description: "CI labeler format"}
]
```

### 4. Categorize Discoveries

**Group feedback by type:**

**Type: CI Failure**
- Pattern: statusCheckRollup shows failures
- Priority: 1 (blocks merge)
- Example: "Tests failing: test_github_projects_lookup"

**Type: Code Review Comment**
- Pattern: Human review with requested changes
- Priority: 1-2 (depends on severity)
- Example: "Codex: Tests reference deleted file"

**Type: Merge Conflict**
- Pattern: mergeable = false
- Priority: 0 (critical, blocks everything)
- Example: "Merge conflict in .beads/issues.jsonl"

**Type: Bot Suggestion**
- Pattern: Bot comment with improvement suggestion
- Priority: 2-3 (non-blocking)
- Example: "Danger: Add tests for new feature"

### 5. Create Child Beads Issues

For each discovery, create child issue:

```bash
# Create child issue linked to parent
bd create "Bug: <short-description>" \
  --type bug \
  --priority 1 \
  --description "<full-context>" \
  --design "<how-to-fix>"

# Link to parent (creates discovered-from dependency)
bd dep add <child-id> <parent-id> --type discovered-from
```

**Issue type rules:**
- CI failure → bug
- Code review comment → bug or task
- Merge conflict → bug (P0)
- Bot suggestion → chore or task
- Manual user report → bug (trust user classification)

**Priority rules:**
- Merge conflict → P0 (critical)
- Failing checks → P1 (high)
- Review comments → P1-P2
- Bot suggestions → P2-P3
- Manual reports → P1 (default, user can adjust)

### 6. Present Discoveries to User (MANDATORY)

**This phase is REQUIRED for both modes. Never skip discussion.**

```
📋 Created 3 Beads issues for PR #155:

1. ❌ bd-abc (Bug, P1): Test suite failing
   - tests reference deleted github_projects.py
   - Auto-fixable: YES (simple import update)

2. 🤖 bd-def (Bug, P1): Update tests for removed helper
   - FileNotFoundError in test_github_projects_lookup
   - Auto-fixable: YES (delete obsolete test)

3. ⚠️ bd-ghi (Task, P2): Add documentation for new skill
   - New skill needs usage examples
   - Auto-fixable: MAYBE (need to know what to document)

Which would you like me to fix?
a) Fix all auto-fixable issues (1, 2)
b) Fix specific ones (specify numbers)
c) I'll handle some myself (tell me which to skip)
```

**Options:**
- User: "fix all" → AI attempts all fixes
- User: "fix #1 and #2" → AI fixes specific issues
- User: "I'll fix #2" → AI skips that issue
- User: "just fix the auto-fixable ones" → AI fixes only bd-abc, bd-def

**Why mandatory discussion:**
- User may want to fix some issues themselves
- User may have context AI doesn't (architectural decisions)
- User may want to prioritize differently
- Transparency: user sees all issues before code changes

### 7. Fix Issues (if AI-fixable)

**Determine fixability:**

```javascript
function canAutoFix(discovery) {
  // AI can fix:
  if (discovery.type === "deleted_file_reference") return true;
  if (discovery.type === "import_error") return true;
  if (discovery.type === "lint_error") return true;
  if (discovery.type === "simple_test_fix") return true;

  // AI should ask:
  if (discovery.type === "architectural_change") return false;
  if (discovery.type === "breaking_api_change") return false;
  if (discovery.type === "security_issue") return false;

  // Default: ask
  return false;
}
```

**Fix workflow:**

For each fixable issue (iterate systematically):

```bash
# 1. Read relevant files with Serena
mcp__serena__find_symbol(name_path=<symbol>)
mcp__serena__get_symbols_overview(relative_path=<file>)

# 2. Make fixes with Serena
mcp__serena__replace_symbol_body(...)
mcp__serena__insert_after_symbol(...)

# 3. Verify fix (optional, <5s)
make lint-fast

# 4. Close child issue BEFORE commit
bd close ${childIssue.id} --reason "Fixed"

# 5. Force flush to JSONL (don't wait for debounce)
bd sync --flush-only

# 6. AUTO-COMMIT with child Feature-Key (inline, not "commit my work")
git add -A
git commit -m "fix: <issue-description>

Closes ${childIssue.id}

Feature-Key: ${childIssue.id}
Parent-Feature: ${parentIssue.id}
Discovery-Type: pr-review
PR-Number: ${prNumber}"

# 6. Move to next issue
# Repeat steps 1-5 for each approved bug
```

**Key: One commit per bug, close issue immediately after commit**

### 8. Push Updates (After All Fixes)

```bash
# Push all commits at once
git push

# PR auto-updates, CI re-runs automatically
```

**Note:** Push ONCE at the end, not after each commit. This allows:
- Batched CI runs (faster feedback)
- Atomic PR update (all fixes together)
- Easy rollback if needed (revert all commits, force-push)

### 9. Confirm to User

```
✅ Fixed 2 of 3 issues in 2 commits:
   ✅ bd-abc (CI Failure): Closed
   ✅ bd-def (Codex Review): Closed
   ⏭️ bd-ghi (Danger Bot): Skipped (needs human input)

📤 Pushed to feature-GUARD_SKILL_ACTIVATION
🔄 PR #156 updated, CI re-running

Next steps:
- Wait for CI results (~2min)
- If CI passes → Ready to merge
- If CI fails → Say "fix the PR" again to iterate
```

### 10. Iteration Loop (Manual)

**User triggers next iteration if needed:**

```
CI re-runs → New failures appear
User: "fix the PR"
AI: [Reads new CI output, creates new child issues, repeats workflow]
```

**OR user checks manually:**

```
User: "check CI status"
AI: [Shows current check results]
User: "fix the PR" (if failures exist)
```

**No automatic polling** - user controls when to iterate. This follows V3 philosophy: trust environments, manual triggers.

## Integration Points

### With Beads
- **Creates child issues** for each discovery
- **Links via discovered-from** (deps=[parent.id])
- **Tracks in hierarchy** (bd-pso → bd-pso.1, bd-pso.2, ...)
- **Closes on fix** with commit reference

### With sync-feature-branch
- **Reuses commit logic** for Feature-Key trailers
- **Same branch** (iterative refinement)
- **Auto-close child** after successful commit

### With create-pull-request
- **Same PR** (updates, not new PR)
- **PR body unchanged** (GitHub shows commit history)
- **CI re-runs** automatically on push

### With Serena
- **Smart code search** to find issues
- **Symbol-aware edits** for fixes
- **Token-efficient** (doesn't read entire files)

## Discovery Patterns

### Pattern: Deleted File Reference

**Detect:**
```
CI output: "FileNotFoundError: scripts/lib/github_projects.py"
```

**Fix:**
```
1. Find references: mcp__serena__search_for_pattern("github_projects.py")
2. For each reference:
   - Read context: mcp__serena__get_symbols_overview
   - Replace call: mcp__serena__replace_symbol_body
   - Update imports: mcp__serena__insert_after_symbol
```

### Pattern: Test Failure

**Detect:**
```
CI output: "FAILED tests/test_foo.py::test_bar - AssertionError"
```

**Fix:**
```
1. Read test: mcp__serena__find_symbol("test_bar", relative_path="tests/test_foo.py")
2. Analyze failure reason
3. If simple assertion mismatch → fix expected value
4. If logic error → ask user for guidance
```

### Pattern: Lint Error

**Detect:**
```
CI output: "E501 line too long (92 > 88 characters)"
```

**Fix:**
```
1. Read file at line number
2. Reformat with black/prettier (or manually)
3. Commit lint fix
```

### Pattern: Merge Conflict

**Detect:**
```
gh pr view: mergeable = false
```

**Fix:**
```
1. Fetch latest: git fetch origin master
2. Attempt rebase: git rebase origin/master
3. If conflicts:
   - Ask user to resolve manually
   - Provide guidance on conflict resolution
4. If clean: git push --force-with-lease
```

## Best Practices

1. **Create issues first** - Track before fixing
2. **Fix one at a time** - Easier to verify
3. **Auto-fix simple issues** - Lint, imports, obvious bugs
4. **Ask for complex issues** - Architecture, security, breaking changes
5. **Close child on success** - Keep Beads clean
6. **Push after each fix** - CI validates incrementally
7. **Check CI between fixes** - Don't stack failures

## What This Skill Does

✅ Read PR feedback (comments, CI, conflicts)
✅ Create child Beads issues for discoveries
✅ Fix simple/obvious issues automatically
✅ Ask user for complex issues
✅ Commit with proper Feature-Key trailers
✅ Push updates to same branch
✅ Close child issues on success

## What This Skill DOESN'T Do

❌ Create new PRs (fixes go to existing PR)
❌ Force merge (respects required checks)
❌ Fix architectural issues without asking
❌ Run full test suite locally (CI does this)
❌ Wait for CI to pass (pushes immediately)
❌ Delete child issues (closes, preserves history)

## Anti-Patterns

❌ Fixing without creating child issues
❌ Creating new branch for fixes
❌ Closing parent issue before PR merges
❌ Auto-fixing security issues without review
❌ Batching multiple fixes in one commit
❌ Not linking child issues to parent

## Safety Guardrails

**Before auto-fixing:**
- Check issue complexity (simple vs architectural)
- Check affected files (tests vs core logic)
- Check change size (lines modified)

**Auto-fix allowed:**
- <50 lines changed
- Non-protected paths
- Tests, docs, lint fixes
- Import/reference updates

**Require user approval:**
- >50 lines changed
- Protected paths (.claude/hooks, migrations, workflows)
- Core business logic
- API contract changes
- Security-related code

**Never auto-fix:**
- Merge conflicts (too risky)
- Breaking API changes
- Database migrations
- Authentication/authorization logic

## Example Scenarios

### Scenario 1: Simple Test Fix

```
User: "fix the PR"

AI reads PR #155:
- CI failure: test_github_projects_lookup references deleted file
- Fixable: Yes (simple import update)

AI:
1. Creates bd-pso.1 (Bug: Update tests for removed helper)
2. Uses Serena to update test imports
3. Commits: "fix: Update tests to use Beads commands"
4. Pushes to branch
5. Closes bd-pso.1
6. Confirms: "✅ Fixed CI failure, PR updated"
```

### Scenario 2: Complex Architectural Change

```
User: "fix the PR"

AI reads PR #155:
- Codex: "This approach doesn't scale for large datasets"
- Not fixable: Requires architectural decision

AI:
1. Creates bd-pso.2 (Task: Optimize for large datasets)
2. Asks user: "This requires architectural changes. Options:
   a) Add pagination
   b) Use streaming
   c) Keep current approach with docs
   Which approach?"
3. User chooses option
4. AI implements or creates plan
```

### Scenario 3: Multiple Issues

```
User: "fix the PR"

AI reads PR #155:
- CI failure: Lint errors (15 lines)
- Codex: Test coverage suggestion
- Danger: Missing docs

AI:
1. Creates 3 child issues: bd-abc, bd-def, bd-ghi
2. Shows summary with auto-fixability analysis
3. Asks: "Fix all, or one at a time?"
4. User: "fix all"
5. AI fixes lint (auto-commit), adds tests (asks first, commits), adds docs (auto-commit)
6. 3 commits created with different Feature-Keys
7. All 3 child issues closed
8. Pushes all commits
9. Confirms: "✅ All issues resolved, CI re-running"
```

### Scenario 4: Manual Triage (NEW)

```
User: "i noticed bugs: 1. MCP type error, 2. permission denied, 3. obsolete test, 4. CI labeler, 5. CI metadata"

AI:
1. Parses 5 bugs from numbered list
2. Creates 5 Beads issues: bd-l76, bd-m89, bd-njn, bd-2qv.1, bd-2qv.2
3. Links all to parent (discovered-from)
4. **MANDATORY DISCUSSION:**
   📋 Created 5 Beads issues for PR #156:
   1. bd-l76 (Bug, P1): MCP type error → Auto-fixable: YES (doc update)
   2. bd-m89 (Bug, P1): permission denied → Auto-fixable: YES (chmod +x)
   3. bd-njn (Bug, P1): obsolete test → Auto-fixable: YES (delete file)
   4. bd-2qv.1 (Bug, P1): CI labeler → Auto-fixable: YES (YAML format)
   5. bd-2qv.2 (Bug, P1): CI metadata → Auto-fixable: YES (PR body)

   Which should I fix?
5. User: "fix all"
6. AI fixes systematically:
   - bd-l76: Update AGENTS.md (commit, close)
   - bd-m89: chmod +x script (commit, close)
   - bd-njn: Delete test file (commit, close)
   - bd-2qv.1: Fix labeler.yml (commit, close)
   - bd-2qv.2: Update PR body (commit, close)
7. Pushes 5 commits
8. Confirms: "✅ Fixed all 5 bugs, PR updated, CI re-running"
```

## Future Enhancements

1. **Auto-invoke after PR creation** - PostPRCreate hook
2. **CI status monitoring** - Periodic checks for failures
3. **Smart retry logic** - Re-run failed checks if transient
4. **Conflict resolution hints** - AI-suggested merge strategies
5. **Bulk operations** - Fix all simple issues at once
6. **Learning mode** - Track which auto-fixes succeed/fail

---

**Last Updated:** 2025-01-13
**Related Skills:** create-pull-request, sync-feature-branch, beads-workflow
**Helper Scripts:** scripts/bd-link-pr
**References:**
- PR workflow: AGENTS.md
- Beads integration: .claude/skills/beads-workflow/SKILL.md

**Changelog:**
- 2025-01-13: Added manual triage mode for user-reported bugs, mandatory discussion phase, auto-commit per bug, CLI-first pattern
