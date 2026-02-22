---
name: finish-task
description: "Complete a beads task - run checks, commit, push, close issue, cleanup worktree, generate session summary"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, Skill
---

# Finish Beads Task: $ARGUMENTS

You are completing work on beads task `$ARGUMENTS`. Follow this checklist precisely. **Work is NOT complete until git push succeeds.**

## 1. Verify Current State

```bash
bd show $ARGUMENTS
git status
git log --oneline -5
pwd
```

Confirm:
- Task is `in_progress`
- You're in the correct worktree
- All changes are visible

## 2. Verify Acceptance Criteria

**Philosophy: Bounded autonomy** — Verify the task achieved what it set out to do.

From the `bd show` output above, check for recorded acceptance criteria (in notes or description). Verify each is met:
```
Acceptance Criteria Check:
- [x] <criterion 1> — Implemented in <file>
- [x] <criterion 2> — Verified by <test>
- [x] Tests pass
```

If any criterion is NOT met, either:
1. Complete the missing work before proceeding
2. Create a follow-up task for deferred items and note the reason

## 3. Run Quality Gates

Run appropriate tests for the project:

```bash
# Python projects
uv run pytest

# Node projects
pnpm test

# Or project-specific
make run-checks
```

**If tests fail, STOP.** Fix the issues before proceeding. Do NOT close a task with failing tests.

## 4. Review and Update Documentation

Before committing, review whether documentation needs updates:

1. **README.md** - Does it reflect new features, commands, or setup steps?
2. **CLAUDE.md** - Any new patterns, commands, or guidelines for AI assistants?
3. **PROJECT_SPEC.md** - Implementation status, new decisions, or architecture changes?
4. **Inline docs** - Are new functions/classes documented?

Update any documentation that is now stale or incomplete due to your changes. Keep updates minimal and focused - only document what changed.

## 5. File Follow-up Issues

If there's remaining work, TODOs, or improvements discovered during implementation:

```bash
bd create "Follow-up: <description>"
```

Do this BEFORE closing the main task so nothing is lost.

## 6. Commit All Changes

```bash
git add -A
git status
```

Create a well-formatted commit:

```bash
git commit -m "$(cat <<'EOF'
feat(<scope>): <description>

<detailed explanation if needed>

Closes: $ARGUMENTS

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## 7. Sync Beads (Pre-Push)

Sync beads before pushing to pull any remote changes:

```bash
bd sync
```

## 8. Push to Remote

```bash
git push -u origin $(git branch --show-current)
```

**If push fails, resolve and retry.** Do NOT proceed until push succeeds.

## 9. Close the Task and Final Sync

```bash
bd close $ARGUMENTS --reason="Completed. See branch $(git branch --show-current)."
bd sync
```

**CRITICAL**: The final `bd sync` ensures the task closure is pushed to the remote. Without this, other agents won't see the task is complete.

## 10. Verify Everything is Synced

```bash
git status
bd show $ARGUMENTS
bd sync  # Run again to confirm no pending changes
```

Confirm:
- Git shows "Your branch is up to date with origin"
- Task status is `closed`
- `bd sync` shows "no changes" or "already up to date"

## 10.5. Frontend Evidence Prompt

Check if the PR includes frontend changes:

```bash
git diff main...HEAD --name-only | grep -E '\.(tsx|jsx|css|scss)$'
```

If frontend files are present, inform the user:

```
This PR includes frontend changes. Consider capturing screenshots for the PR:
  - Run the dev server and take desktop + mobile screenshots
  - Add them to the PR description or as GitHub comments
  - If spec/design images exist, compare visually
```

This is informational only — do not block on evidence capture.

## 11. Create Pull Request

Create a PR for the completed work:

```bash
gh pr create --title "feat(<scope>): <description>" --body "$(cat <<'EOF'
## Summary

<2-3 sentences describing what this PR accomplishes>

## Changes

- <bullet list of key changes>

## Task

Closes beads task `$ARGUMENTS`

## Test Plan

- [x] All tests passing (<count> tests)
- [ ] Manual verification (if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## 11a. Code Review and Auto-Fix

Run automated code review on the PR using parallel specialized reviewers:

```
/multi-review
```

The multi-review will:
- Launch 3-5 specialized review agents in parallel (simplicity, patterns, security, performance, architecture)
- Select relevant reviewers based on change types
- Aggregate findings by severity (Critical > Important > Suggestion)
- Filter to high-confidence (≥80%) issues
- Offer auto-fix for fixable issues

### If Issues Found

For each Critical or Important issue:

1. **Review the finding** - Note the file, line, and reviewer that flagged it
2. **Implement fix** - Make the minimal change to address the issue
3. **Verify** - Ensure the fix doesn't introduce new problems

After fixing all issues:

```bash
# Run tests to verify fixes
uv run pytest  # or pnpm test / make run-checks

# Commit the fixes
git add -A
git commit -m "$(cat <<'EOF'
fix: address code review findings

- <brief list of issues fixed>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push updates
git push
```

Re-run review if significant changes were made:

```
/multi-review
```

**Iteration limit:** Maximum 3 review cycles. If issues persist after 3 attempts:
- List remaining unresolved issues
- Ask user: "Code review found issues I couldn't automatically resolve: <list>. Proceed with merge anyway, or address manually?"

### If No Issues Found

Proceed directly to merge decision.

### Merge Decision

After code review passes (or user approves despite issues):

"PR created: <URL>. Code review [passed / fixed N issues / has N unresolved issues]. Would you like me to merge it and clean up the worktree?"

If user approves, proceed to step 12. If user declines, leave the PR open for manual review and skip to step 13.

## 12. Merge PR and Cleanup

```bash
BRANCH_NAME=$(git branch --show-current)
MAIN_REPO=$(git worktree list | head -1 | awk '{print $1}')

cd "$MAIN_REPO"

# Merge PR and clean up branch
gh pr merge --squash --delete-branch

# Pull the merged changes
git pull
```

If `gh pr merge` fails with "already merged", just delete the branch manually:
```bash
git branch -d "$BRANCH_NAME" 2>/dev/null || true
git push origin --delete "$BRANCH_NAME" 2>/dev/null || true
```

Worktree cleanup is handled automatically by Claude Code when the session exits (native worktrees auto-remove when clean).

## 13. Re-Read Original Task Spec

**CRITICAL**: Before writing the session summary, re-read the original task specification to accurately identify divergences:

```bash
bd show $ARGUMENTS
```

Save this output mentally - you'll compare it against your implementation when writing the SPEC DIVERGENCES section. Don't rely on memory; divergences are easy to miss without explicit comparison.

## 14. Session Summary

**IMPORTANT**: Output a detailed session summary for orchestrating agents. This summary will be consumed by a coordinating agent to track progress across multiple parallel work sessions. Be verbose and thorough.

Use this exact format:

```
===============================================
SESSION SUMMARY: <Task Title>
===============================================

TASK OVERVIEW
-------------
ID: $ARGUMENTS
Title: <title from bd show>
Status: Closed
Priority: <P1/P2/P3 from bd show>
Type: <feature/task/bug from bd show>

INTENT & SCOPE
--------------
What this task set out to accomplish:
<2-3 sentences explaining the goal of this task in plain language. What problem does it solve? Why was it needed?>

IMPLEMENTATION SUMMARY
----------------------
<Narrative description of what was built. Write 3-5 sentences explaining the approach taken, key design decisions, and how the pieces fit together. An orchestrating agent should be able to understand the work without reading the code.>

FILES CREATED
-------------
<For each new file, include path and brief description>

1. <path/to/file.py>
   Purpose: <what this file does>
   Key components: <main classes/functions>
   Lines: <approximate line count>

2. <path/to/file.py>
   ...

FILES MODIFIED
--------------
<For each modified file, explain what changed and why>

1. <path/to/file.py>
   Changes: <what was added/changed>
   Reason: <why this change was needed>

2. <path/to/file.py>
   ...

TESTS
-----
New tests added: <count>
Total tests now passing: <count>
Test file(s): <path(s)>

Key test coverage:
- <what scenarios are tested>
- <what edge cases are covered>

DOCUMENTATION UPDATED
---------------------
<List each doc file updated with a brief note on what changed, or "None required">

GIT ACTIVITY
------------
Branch: <branch-name>
Commits: <count>
PR: <URL or "Not created">
Merged to: <target branch>
Model: <opus|sonnet|inherited>

BEADS STATUS
------------
Task closed: Yes
Reason: <close reason>
Synced to remote: Yes

SPEC DIVERGENCES
----------------
Compare your implementation against the original task description from `bd show`. Document ANY differences between what was specified and what was actually built. Be explicit and thorough - the orchestrator relies on this to keep the task board accurate.

Format each divergence as:

**Divergence N: <brief title>**
- Specified: <what the task description said to do>
- Implemented: <what was actually built>
- Reason: <why the change was necessary - technical constraint, better approach discovered, dependency issue, etc.>
- Impact: <what downstream tasks or specs need updating>

If implementation matched spec exactly, state: "None - implementation matches specification."

Examples of divergences to document:
- Different file structure than specified
- Added/removed features from original scope
- Changed API contracts or schemas
- Used different libraries or approaches
- Deferred functionality to follow-up tasks
- Discovered requirements that weren't in the spec

FOLLOW-UP ISSUES CREATED
------------------------
<List any new beads issues created during this session, or "None">

DEPENDENCIES UNBLOCKED
----------------------
The following tasks were blocked by this task and can now proceed:
<List each task ID and title, or "None">

ARCHITECTURAL NOTES
-------------------
<Any important technical decisions, patterns established, or constraints discovered that future work should be aware of. This helps maintain consistency across parallel agent sessions.>

HANDOFF CONTEXT
---------------
<What should the next agent or session know? Include:
- Any gotchas or things that didn't work as expected
- Assumptions made that might need revisiting
- Suggested next steps if continuing related work
- Dependencies on external systems or APIs
- Performance considerations if any>

LEARNINGS CAPTURED
------------------
<Path to auto-compound doc if written, or "None — clean implementation">

===============================================
END SESSION SUMMARY
===============================================
```

This format ensures orchestrating agents have full context to coordinate parallel work and make informed decisions about task assignment.

## 14.5. Auto-Compound Learnings

Check the session summary you just wrote for compoundable knowledge. Look for:
- SPEC DIVERGENCES that reveal gotchas or unexpected behavior
- ARCHITECTURAL NOTES with patterns future workers should know
- HANDOFF CONTEXT with gotchas or "things that didn't work as expected"
- Bug fixes where the root cause was non-obvious

**If meaningful learnings are present** (not trivial — skip for clean implementations with no surprises):

1. Determine the category from the learning content:
   - Runtime surprise or unexpected behavior → `runtime-errors/`
   - Build/config gotcha → `build-errors/`
   - Performance discovery → `performance/`
   - Database/migration insight → `database/`
   - Integration issue → `integration/`
   - Workflow/tooling insight → `workflow/`

2. Write a lightweight solution document:

   ```bash
   PROJECT_ROOT=$(git worktree list | grep '\[main\]' | awk '{print $1}')
   if [ -z "$PROJECT_ROOT" ]; then
     PROJECT_ROOT=$(git rev-parse --show-toplevel)
   fi
   mkdir -p "$PROJECT_ROOT/docs/solutions/<category>"
   ```

   Document format:
   ```markdown
   ---
   scope: project
   module: <affected module>
   date: <YYYY-MM-DD>
   problem_type: <from category>
   severity: <medium|high>
   tags: [<relevant keywords>]
   source: auto-compound
   task_id: $ARGUMENTS
   ---

   # <Descriptive Title>

   ## Symptom
   <What went wrong or was unexpected>

   ## Root Cause
   <Why it happened>

   ## Solution
   <What fixed it or the pattern to follow>

   ## Prevention
   <How to avoid this in future>
   ```

3. Write to `$PROJECT_ROOT/docs/solutions/<category>/<symptom-slug>-<module>-<date>.md`

**If no meaningful learnings** (clean implementation, spec matched, no gotchas):
Skip silently — not every task produces learnings.

**Important**: This is fire-and-forget. Do NOT ask the user about scope (always project-specific) or present decision menus. The `source: auto-compound` tag in frontmatter distinguishes these from rich `/compound` documents.

## 15. Persist Summary to Disk

Write the summary to a file so orchestrating agents can read it directly from disk.

```bash
# Get project root (handles worktrees correctly - use main repo if in worktree)
PROJECT_ROOT=$(git worktree list | grep '\[main\]' | awk '{print $1}')
if [ -z "$PROJECT_ROOT" ]; then
  PROJECT_ROOT=$(git rev-parse --show-toplevel)
fi

# Create directory if needed
mkdir -p "$PROJECT_ROOT/docs/session_summaries"

# Add to .gitignore if not present
if ! grep -q "^docs/session_summaries/$" "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
  echo "docs/session_summaries/" >> "$PROJECT_ROOT/.gitignore"
fi

# Generate filename with timestamp
TIMESTAMP=$(date +%y%m%d-%H%M%S)
SUMMARY_FILE="$PROJECT_ROOT/docs/session_summaries/$ARGUMENTS_${TIMESTAMP}.txt"
```

Write the summary content using a heredoc:

```bash
cat > "$SUMMARY_FILE" <<'SUMMARY_EOF'
<paste the full session summary content here>
SUMMARY_EOF

echo "Summary written to: $SUMMARY_FILE"
```

**Important:** The summary file allows orchestrators to asynchronously review completed work without needing the worker session to remain active.

## 16. Copy to Clipboard (Optional)

Use AskUserQuestion to offer copying the summary to clipboard:

**Question:** "Copy session summary to clipboard?"
- **Options:** "Yes, copy to clipboard" / "No, skip"
- **Header:** "Clipboard"

If the user selects "Yes, copy to clipboard":

```bash
cat "$SUMMARY_FILE" | pbcopy
echo "Summary copied to clipboard"
```

This avoids clipboard conflicts when multiple worker sessions complete simultaneously.

## 17. Notify Orchestrator

**IMPORTANT**: If you documented any SPEC DIVERGENCES, the orchestrator needs to reconcile the beads task board with the implementation reality.

Output this message to the user:

```
===============================================
TASK COMPLETE: $ARGUMENTS

Summary ready for orchestrator.
Divergences documented: <Yes/None>

Next step: Paste this summary into the orchestrator session
and run `/reconcile-summary` to update affected tasks.
===============================================
```

If the SPEC DIVERGENCES section was "None - implementation matches specification", you can simplify to:

```
===============================================
TASK COMPLETE: $ARGUMENTS

No spec divergences - implementation matched specification.
Summary available at: <path to summary file>
===============================================
```
