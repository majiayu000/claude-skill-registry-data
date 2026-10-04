---
name: issue
description: Implement a Linear issue end-to-end
argument-hint: <issue-id>
---

# Implement Linear Issue

Take a Linear issue and implement it completely using the full TDD workflow.

**YOU MUST NOT STOP UNTIL THE ISSUE IS FULLY RESOLVED.**

## Arguments

- `$ARGUMENTS` - Linear issue ID (e.g., `PLOT-123`)

## Phase 0: Issue Analysis (Parallel)

Launch THREE parallel agents simultaneously to gather all context at once:

**Agent 1 — Fetch Issue Details** (via Linear MCP):
- Title, description, labels, priority, assignee
- Parent issue (if sub-task)
- Related issues and comments
- Extract: what needs to be done, acceptance criteria, priority level, discussion context

**Agent 2 — Explore Codebase**:
- Use Glob and Grep to map the project structure
- Identify relevant source directories, test directories, and configuration files
- Find existing patterns, naming conventions, and architectural style
- Locate modules most likely to be affected based on common keywords from the issue ID prefix

**Agent 3 — Check Recent History**:
- `git log --oneline -20` for recent changes
- `git log --oneline --all --since='2 weeks ago'` for broader context
- Identify if anyone has worked on related areas recently
- Check for any in-flight branches that might conflict

### 0.1 Synthesize Results

Once all three agents complete, combine their outputs to form a unified understanding of:
- What the issue requires
- Where in the codebase the work will happen
- What recent changes might be relevant or conflicting

### 0.2 Update Issue Status

Move issue to "In Progress" state via Linear MCP.

### 0.3 Create Branch

```bash
ISSUE_ID='$ARGUMENTS'
BRANCH_SLUG=$(printf '%s' '<title from Linear>' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-40)
git checkout -b "${ISSUE_ID}-${BRANCH_SLUG}"
```

Paste the Linear title between the single quotes, writing each `'` in it as `'\''`.

### 0.4 Clarify If Needed

If the issue is ambiguous:
- Check comments for clarification
- Use `AskUserQuestion` to get missing details
- Add clarification as comment to Linear issue
- Do NOT proceed with assumptions

## Phase 1: Orchestrate

Invoke the **consolidation** skill, which loads the full orchestration cycle into your context. You become the conductor and dispatch each stage:

```
Skill(skill="skills:consolidation", args="## Task\n[issue title and description from Phase 0]\n\n## Acceptance criteria\n[from issue details]\n\n## Constraints\n- TDD: every subtask includes tests\n- Follow project conventions discovered in Phase 0\n\n## Working directory\n[cwd]")
```

The cycle runs planner → verifier → parallel architects → consolidator → reviewer → verifier in *your* context: you conduct it (the consolidation skill decides whether to delegate workstreams to `conductor` subagents).

## Phase 2: Finalize (PR)

After the cycle completes, prepare the PR in parallel with a final verification:

**Agent 1 — Verifier** (`subagent_type: "verifier"`): Post-verification — tests, lint, build.

**Agent 2 — PR Content**: Draft PR title, body, and summary from commits on the branch.

### 2.1 Create PR Linked to Issue

Title the PR `<type>(<scope>): <subject>`. The type is `fix` when the issue carries a bug label and `feat` otherwise; the scope names the area touched and is omitted for repo-wide changes; `<subject>` restates the Linear title from Phase 0 as a lowercase imperative (Linear "Login fails for expired sessions" → `fix(auth): handle expired sessions`).

Using the PR content prepared by Agent 2 (adjusted if fixes were needed):

```bash
gh pr create --title '<type>(<scope>): <subject>' --body-file - <<'EOF'
## Summary
Implements $ARGUMENTS

## Changes
- [list changes]

## Test Plan
- [x] Unit tests added
- [x] All tests pass
- [ ] Manual testing

Linear: $ARGUMENTS
EOF
```

Keep the heredoc delimiter quoted (`'EOF'`), so backticks and `$` in the body reach GitHub unchanged.

### 2.2 Update Linear Issue

Via Linear MCP:
1. Add comment with PR link
2. Update status to "In Review"
3. Link the PR to the issue

## Phase 3: Post-Merge

After PR is merged:
1. Move Linear issue to "Done"
2. Add final comment summarizing what was implemented

## Completion Criteria

- [ ] Issue requirements fully implemented
- [ ] All tests pass
- [ ] Code reviewed and issues fixed
- [ ] PR created and linked to issue
- [ ] Linear issue updated with progress
