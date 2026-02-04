---
name: sdd-pr
description: AI-powered PR creation after spec completion. Analyzes spec metadata, git diffs, commit history, and journal entries to generate comprehensive PR descriptions with user approval before creation.
---

# Spec-Driven Development: PR Creation Skill

## Overview

The `sdd-pr` skill creates professional, comprehensive pull requests by analyzing your completed specs and git history. Instead of manually writing PR descriptions, this skill uses AI to analyze all available context and generate detailed, well-structured PR descriptions that make code review more effective.

## When to Use This Skill

Use `Skill(sdd-toolkit:sdd-pr)` to:

- **After Spec Completion**: Create PRs when handed off from sdd-update
- **Comprehensive PRs**: Generate detailed PR descriptions that reviewers will appreciate
- **Save Time**: Automate the tedious task of writing thorough PR descriptions
- **Maintain Quality**: Ensure consistent, high-quality PR documentation

**When NOT to use:**
- For quick, trivial changes (just use gh CLI directly)
- When you need a very specific custom PR format
- For PRs that don't have an associated spec

## ⚠️ Long-Running Operations

**This skill may run operations that take up to 5 minutes. Be patient and wait for completion.**

### CRITICAL: Avoid BashOutput Spam
- **ALWAYS use foreground execution with 5-minute timeout:** `Bash(command="...", timeout=300000)`
- **WAIT for the command to complete** - this may take the full 5 minutes
- **NEVER use `run_in_background=True` for test suites, builds, or analysis**
- If you must use background (rare), **wait at least 60 seconds** between BashOutput checks
- **Maximum 3 BashOutput calls per background process** - then kill it or let it finish

### Why?
Polling BashOutput repeatedly creates spam and degrades user experience. Long operations should run in foreground with appropriate timeout, not in background with frequent polling.

### Example (CORRECT):
```
# Test suite that might take 5 minutes (timeout in milliseconds)
result = Bash(command="pytest src/", timeout=300000)  # Wait up to 5 minutes
# The command will block here until completion - this is correct behavior
```

### Example (WRONG):
```
# Don't use background + polling
bash_id = Bash(command="pytest", run_in_background=True)
output = BashOutput(bash_id)  # Creates spam!
```

## Core Philosophy

### From Template to Intelligence

Traditional PR creation uses static templates that miss important context. The sdd-pr skill:

1. **Analyzes Multiple Sources**
   - Spec metadata (what you planned)
   - Git diffs (what you actually changed)
   - Commit history (how it evolved)
   - Journal entries (why you made decisions)

2. **Generates Context-Aware Descriptions**
   - Explains the "why" not just the "what"
   - Highlights key decisions from journal entries
   - Provides technical depth from git diffs
   - Maintains professional tone and structure

3. **Requires User Approval**
   - Always shows draft before creation
   - User reviews and can request revisions
   - No PRs created without explicit confirmation

## Workflow

### Step 1: Invocation

The skill is typically invoked via handoff from sdd-update after spec completion:

```
Skill(sdd-toolkit:sdd-pr) "Create PR for spec my-feature-2025-11-03-001"
```

### Step 2: Context Gathering

The skill gathers context from multiple sources:

**Spec Metadata**
```json
{
  "title": "Add user authentication",
  "description": "Implement OAuth 2.0 authentication...",
  "objectives": ["Support GitHub and Google OAuth providers", ...]
}
```

**Completed Tasks**
- File paths modified
- Changes made in each file
- Task completion status

**Commit History**
- Commit messages and SHAs
- Task associations
- Development progression

**Journal Entries**
- Technical decisions
- Implementation notes
- Challenges overcome

**Git Diff**
- Actual code changes
- File-level summary if diff is large

### Step 3: AI Analysis

The agent analyzes all gathered context to:
- Understand the feature's purpose and scope
- Identify key changes and their impact
- Extract important decisions from journals
- Synthesize technical details from diffs

### Step 4: Draft Generation

The agent generates a comprehensive PR description following best practices:

```markdown
═══════════════════════════════════════════════════════════════════
Pull Request Draft
═══════════════════════════════════════════════════════════════════

Title: Add user authentication with OAuth 2.0

Branch: feat-auth → main

─────────────────────────────────────────────────────────────────────

## Summary

Adds user authentication using OAuth 2.0, supporting GitHub and Google
providers. Includes login/logout flows, session management, and profile access.

## What Changed

### Key Features
- OAuth 2.0 integration with GitHub and Google
- Secure session management with httpOnly cookies
- User profile endpoint with auth middleware

### Files Modified
- `src/auth/oauth.py`: OAuth provider implementation
- `src/auth/middleware.py`: Auth middleware
- `src/api/routes.py`: Login/logout/profile endpoints

## Technical Approach

Chose OAuth 2.0 over JWT-based auth for better security and simpler
implementation. OAuth handles token refresh automatically and provides
better user experience with provider-managed consent screens.

## Implementation Details

### Phase 1: OAuth Integration
- ✅ Implement OAuth provider classes
- ✅ Add callback URL handling
- ✅ Store tokens securely

### Phase 2: Session Management
- ✅ Create session middleware
- ✅ Implement logout functionality

## Testing

- Added 15 unit tests for OAuth providers
- Verified login/logout flows manually
- Tested with both GitHub and Google accounts

## Commits

- abc1234: task-1-1: Implement OAuth providers
- def5678: task-1-2: Add session middleware
- ghi9012: task-2-1: Create profile endpoint

─────────────────────────────────────────────────────────────────────
```

### Step 5: User Review

The agent shows the draft and asks for user approval:

```
Agent: "Here's the PR description I've generated:

[shows full PR with title and body]

Would you like me to create this PR, or would you like me to revise it?"
```

### Step 6: PR Creation

Once approved, the agent invokes the creation command:

```bash
sdd create-pr spec-id --approve --title "PR Title" --description "$(cat <<'EOF'
[full PR body]
EOF
)"
```

The skill then:
1. Pushes branch to remote
2. Creates PR via `gh` CLI immediately (no additional confirmation)
3. Updates spec metadata with PR URL and number

## Context Sources

The skill analyzes four key sources:

### 1. Spec Metadata
High-level information about the feature/change:
- Title and description
- Objectives and success criteria
- Phase and task structure

### 2. Completed Tasks
Granular details about implementation:
- File paths modified
- Changes made in each file
- Task completion timestamps

### 3. Commit History
Development progression:
- Commit messages and SHAs
- Task-to-commit associations
- Chronological flow

### 4. Journal Entries
Decision logs and notes:
- Technical approach decisions
- Challenges and solutions
- Implementation rationale

**CLI Command:**
```bash
sdd get-journal <spec-id> [--task-id <task-id>]
```

### 5. Git Diff
Actual code changes:
- Full diff or file-level summary
- Code-level understanding
- Verification of changes

## PR Description Structure

The generated PR follows this structure:

### 1. Title (50-80 characters)
```
Add user authentication with OAuth 2.0
```
Action-oriented, specific, concise.

### 2. Summary (2-3 sentences)
High-level overview of what changed and why it matters.

### 3. What Changed
- **Key Features**: Bullet list of main features
- **Files Modified**: File-by-file change summary

### 4. Technical Approach
Explains key decisions and technical rationale from journal entries.

### 5. Implementation Details
Breakdown by phase with completed tasks.

### 6. Testing
Verification steps and test coverage.

### 7. Commits
Development history showing progression.

## Best Practices

### For Better PR Descriptions

1. **Write Detailed Journal Entries**
   The AI uses journal entries to explain technical decisions:
   ```bash
   sdd journal my-spec --content "Chose approach X because of Y..."
   ```

2. **Use Clear Commit Messages**
   Commit messages help explain the development flow:
   ```bash
   git commit -m "task-1-1: Implement OAuth provider classes"
   ```

3. **Review Before Approving**
   Always review the draft and ask for revisions if needed:
   ```
   "Can you emphasize the security aspects more?"
   ```

4. **Keep Specs Updated**
   Ensure spec metadata is current before completion:
   - All tasks marked completed
   - Journal entries added
   - Objectives reflect actual work

## Examples

### Example 1: Feature Addition

```bash
# Skill invoked after spec completion
Skill(sdd-toolkit:sdd-pr) "Create PR for oauth-feature-2025-11-03-001"

# Agent analyzes context and shows draft
# User reviews and approves
# PR created automatically
```

**Generated PR**: Comprehensive description with OAuth implementation details, security considerations, and testing approach.

### Example 2: Bug Fix

```bash
# Skill invoked for bug fix spec
Skill(sdd-toolkit:sdd-pr) "Create PR for memory-leak-fix-2025-11-03-002"

# Agent analyzes and shows draft
# PR explains root cause, fix approach, and verification
```

**Generated PR**: Detailed bug analysis with root cause from journal entries, fix implementation, and memory usage improvements.

### Example 3: Manual Invocation

```bash
# Invoke skill directly with prompt
Skill(sdd-toolkit:sdd-pr) "Create PR for spec refactor-api-2025-11-03-003"

# Agent gathers context, analyzes, and shows draft
# Review and approve
# PR created
```

## Troubleshooting

### "Spec missing git.branch_name metadata"

**Problem**: Spec doesn't have branch information

**Solution**: Ensure git integration is enabled when creating the spec. The spec must have branch metadata.

### "Branch push failed"

**Problem**: Git push errors

**Solution**:
```bash
# Check remote
git remote -v

# Check credentials
git push -u origin <branch-name>
```

### "Diff too large"

**Problem**: Git diff exceeds size limit

**Solution**: Skill automatically shows file-level summary instead of full diff when it's too large.
