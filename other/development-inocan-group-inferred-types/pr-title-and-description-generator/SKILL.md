---
name: PR Title and Description Generator
version: "1.1.0"
description: "Generate or update GitHub Pull Request titles and descriptions based on actual code changes in the final state. Use when the user mentions updating, generating, or writing PR descriptions, PR titles, pull request summaries, or says 'update the PR'. Analyzes git diff to determine what's actually in the code (not just commit history) and creates comprehensive, accurate PR documentation."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git:*)
  - Bash(gh:*)
---

# PR Title and Description Generator

Generate or update a PR title and description based on the actual changes in the current branch.

## Core Principle

**Document ONLY what exists in the final state of the code, not the development history.**

If a feature was added in one commit and removed in another, it should NOT be in the PR description. Always verify features exist in `HEAD` before documenting them.

## Analysis Process

### 1. Identify Current Branch and PR

```bash
git branch --show-current

# Fetch PR information including state for validation
pr_info=$(gh pr view --json number,title,state,mergedAt,headRefName,baseRefName 2>/dev/null)

if [[ -n "$pr_info" ]]; then
  # PR exists - extract state and metadata for validation
  pr_state=$(echo "$pr_info" | jq -r '.state // "UNKNOWN"')
  pr_merged_at=$(echo "$pr_info" | jq -r '.mergedAt // "null"')
  pr_number=$(echo "$pr_info" | jq -r '.number')
  pr_title=$(echo "$pr_info" | jq -r '.title')
  pr_head=$(echo "$pr_info" | jq -r '.headRefName')
  pr_base=$(echo "$pr_info" | jq -r '.baseRefName')

  # Security Fix #4: Validate pr_state is a known GitHub PR state (prevent injection)
  case "$pr_state" in
    OPEN|CLOSED|MERGED|UNKNOWN)
      # Valid state, proceed
      ;;
    *)
      echo "WARNING: Unexpected PR state from GitHub API: $pr_state" >&2
      pr_state="UNKNOWN"
      ;;
  esac

  # Security Fix #4: Validate pr_merged_at is either "null" or valid ISO 8601 timestamp
  if [[ "$pr_merged_at" != "null" ]] && [[ ! "$pr_merged_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T ]]; then
    echo "WARNING: Unexpected mergedAt format from GitHub API: $pr_merged_at" >&2
    pr_merged_at="null"
  fi

  # Security Fix #5: Validate pr_number is present and is a positive integer
  if [[ -z "$pr_number" ]] || [[ ! "$pr_number" =~ ^[0-9]+$ ]]; then
    if [[ -n "$pr_info" ]]; then
      echo "ERROR: PR data incomplete (missing or invalid PR number)" >&2
    fi
    pr_info=""  # Treat as no PR exists
  fi
fi
```

### 1.1. PR State Validation

**CRITICAL SAFEGUARD**: Before updating any PR, verify it is in a safe state to modify.

**When PR exists (pr_info is not empty):**

**Step 1: Check if PR is OPEN** - safe to proceed immediately:

```bash
if [[ "$pr_state" == "OPEN" ]]; then
  # Safe to proceed with normal update workflow
  # Continue to Step 2
fi
```

**Step 2: If PR is NOT OPEN** - stop and ask user for confirmation:

Determine the specific non-open state:

```bash
if [[ "$pr_state" == "MERGED" || "$pr_merged_at" != "null" ]]; then
  pr_status_type="MERGED"
  pr_status_detail="merged"
  pr_status_note="Note: Updating a merged PR only changes its historical record, not the code."
elif [[ "$pr_state" == "CLOSED" ]]; then
  pr_status_type="CLOSED"
  pr_status_detail="closed without merging"
  pr_status_note="Updating a closed PR is unusual. Most cases should create a new PR instead."
else
  pr_status_type="UNKNOWN"
  pr_status_detail="in an unclear state ($pr_state)"
  pr_status_note="Cannot verify PR state safely. Manual investigation recommended."
fi
```

**Step 3: Present confirmation prompt to user**:

Stop execution and display this message (substitute variables with actual values):

```text
⚠️ **PR State Warning**

The detected pull request is **{pr_status_type}**:

- **PR**: #{pr_number} - {pr_title}
- **Branch**: {pr_head} → {pr_base}
- **State**: {pr_status_detail}

**Options:**
1. **Create new PR** - Open a fresh pull request for these changes (recommended for most cases)
2. **Update {pr_status_type} PR anyway** - Modify the PR's title/description (rarely needed)
3. **Cancel** - Stop without making changes

{pr_status_note}

**What would you like to do?**
```

**Step 4: Wait for explicit user response and validate input**:

```bash
# Read user choice
read -p "Enter your choice (1, 2, or 3): " user_choice

# Security Fix #2: Validate input is exactly 1, 2, or 3
if [[ ! "$user_choice" =~ ^[123]$ ]]; then
  echo "Invalid choice. Please enter 1, 2, or 3." >&2
  exit 1
fi
```

**Step 5: Handle user choice based on validated input**:

```bash
case "$user_choice" in
  1)
    # Option 1: Create new PR
    pr_info=""
    echo "Creating new PR instead..."
    ;;
  2)
    # Option 2: Update anyway
    user_confirmed_update="true"
    echo "Proceeding with update to $pr_status_type PR..."
    ;;
  3)
    # Option 3: Cancel
    user_cancelled="true"
    echo "PR update cancelled by user. No changes made."
    exit 0
    ;;
esac
```

**Note on Interactive vs Non-Interactive Handling**:

If implementing this skill as a non-interactive script, Claude should directly handle the user's verbal choice without prompting:

- If user says "create new PR": Set `pr_info=""`
- If user says "update anyway": Set `user_confirmed_update="true"`
- If user says "cancel": Exit gracefully

**When no PR exists (pr_info is empty):**
Skip validation entirely - the skill will create a new PR (normal workflow).

**API Failure Handling:**
If `gh pr view` returns an error OTHER than "no pull requests found", treat as UNKNOWN state and ask user before proceeding.

### 2. Analyze Final State Changes

```bash
# Get commit count
git log main..HEAD --oneline | wc -l

# Get file change summary
git diff main...HEAD --stat

# Identify major areas of change
git diff main...HEAD --name-only | cut -d/ -f1 | sort | uniq -c | sort -rn
```

### 3. Verify What's Actually in the Code

**CRITICAL**: For each area of apparent change, verify if it's in the final state:

```bash
# Check if a feature is in final code
git show HEAD:path/to/file.ts | grep -q "feature_name" && echo "PRESENT" || echo "REMOVED"

# Example: Check for authentication plugin
git show HEAD:cloud/database/src/SqlDatabase.ts | grep "authentication_plugin"

# Example: Check if a function exists
git show HEAD:src/utils.ts | grep -A10 "function myFunction"
```

**If a feature doesn't appear in the final state, DO NOT include it in the PR description.**

### 4. Categorize Changes by Impact

Organize changes into categories based on what's actually present:

- **Infrastructure Changes**: Cloud resources, deployments, architecture
- **Developer Experience**: Tooling, documentation, local development setup
- **CI/CD**: Pipeline changes, automation workflows
- **Breaking Changes**: API changes, configuration requirements, migration needs
- **Dependencies**: Package updates that remain in final package.json/lock files
- **Documentation**: New or updated docs (verify files exist)

### 5. Document Only Present Changes

For each change area:

1. **Verify existence**: Run `git show HEAD:path/to/file` to confirm
2. **Link to files**: Use markdown links with relative paths from repo root
   - Files: `[filename.ts](path/to/filename.ts)`
   - Specific lines: `[filename.ts:42](path/to/filename.ts#L42)`
   - Line ranges: `[filename.ts:42-51](path/to/filename.ts#L42-L51)`
3. **Include code snippets**: For configuration changes, show actual values
4. **Provide context**: Explain why the change was made, not just what changed

## Quality Verification Checklist

Before finalizing the description, verify:

- [ ] Every feature mentioned exists in `git show HEAD:path/to/file`
- [ ] No references to features that were added then removed during development
- [ ] All file links use relative paths from repo root (not absolute paths)
- [ ] Configuration examples reflect actual current state in HEAD
- [ ] Breaking changes are clearly marked with "Breaking Changes" section
- [ ] Testing sections describe actual tests that currently pass
- [ ] Code snippets are from actual files in HEAD, not from memory

## PR Title Formats

See [resources/title-patterns.md](resources/title-patterns.md) for comprehensive title format examples and patterns.

Quick reference:

- Infrastructure: "Enterprise [resource] with [key feature] and [secondary feature]"
- Features: "Add [feature] with [benefit]"
- Bug Fixes: "Fix [specific issue] in [area]"
- Refactoring: "Refactor [area] to [improvement]"

Avoid vague titles like "PR deployment", "Various fixes", or "Update code".

## Description Structure

For detailed templates, see:

- [templates/feature.md](templates/feature.md) - Feature additions
- [templates/bugfix.md](templates/bugfix.md) - Bug fixes
- [templates/infrastructure.md](templates/infrastructure.md) - Infrastructure changes

Use this general template structure:

```markdown
## Summary

[1-2 sentence overview of what this PR accomplishes and why]

## [Major Category 1 - e.g., Infrastructure Changes]

### [Subcategory - e.g., Cloud SQL Enterprise Plus]

**[Feature Name]:**
- [Implementation detail verified in HEAD]
- [Configuration detail with actual values]
- [Benefit or impact]

**Implementation:**
- File: [link to main file](path/to/file.ts)
- Configuration: [link to config](path/to/config.yaml)

**Stack Commands:**
- `./stack command_name` - Description

**Documentation:**
- [Link to relevant docs](doc/path/to/doc.md)

[Repeat structure for each major category]

## Breaking Changes

### [Area Affected]
- **What changed**: [Specific change]
- **Migration**: [Steps to migrate]
- **Impact**: [Who/what is affected]

## Dependencies

- Updated `package-name` to version X.Y.Z
- Added `new-package` for [specific purpose]
- Removed `old-package` (no longer needed)

## Testing

**[Test Category]:**
- ✅ [Specific test that validates the change]
- ✅ [Another specific test]
- ✅ [Integration test description]

**[Another Test Category]:**
- ✅ [Test description]

## Cost Impact

[If applicable - infrastructure cost changes]

**Production:**
- Current: $X/month
- Planned: $Y/month (with optimization Z)
- Benefit: [SLA/performance/reliability improvements]

**[Environment]:**
- Base: $X/month (shared infrastructure)
- Per-[unit]: +$Y/month

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Verification Workflow

For step-by-step examples of how to analyze and verify PR changes, see [resources/analysis-workflow.md](resources/analysis-workflow.md).

You can also use the verification script:

```bash
# Check if a feature exists in final state
./scripts/verify-feature.sh path/to/file.ts "feature_name"

# Check if a file exists
./scripts/verify-feature.sh packages/api/README.md ""
```

## Important Rules

1. **Verify before documenting** - Always use `git show HEAD:file` to confirm features exist in final state
2. **Never mention removed features** - If a commit added something but it was later removed or reverted, don't include it
3. **Focus on outcomes, not process** - Describe the result, not the development journey
4. **Link to actual code** - Every major feature should have a file reference that users can click
5. **Be specific** - "Add MySQL native password authentication" not "Update database config"
6. **Test your claims** - If you say "CI runs connectivity checks", verify the CI file actually shows that
7. **Use present tense** - "Adds X", "Implements Y", not "Added X", "Implemented Y"
8. **Quantify when possible** - "3x performance improvement", "99.99% SLA", "$460/month cost"

## Common Mistakes to Avoid

### ❌ Documenting Removed Features

```
# Commit history shows:
# - Commit A: Add feature X
# - Commit B: Remove feature X
# Final state: No feature X

# WRONG: "Added feature X"
# RIGHT: Don't mention feature X at all
```

### ❌ Vague Descriptions

```
# WRONG: "Updated database configuration"
# RIGHT: "Set default_authentication_plugin to mysql_native_password for Cloud SQL Proxy v2 compatibility"
```

### ❌ Missing Verification

```
# WRONG: Assume a feature exists because you saw it in commit messages
# RIGHT: git show HEAD:path/to/file.ts | grep "feature_name"
```

### ❌ Broken Links

```
# WRONG: [config.ts](/Users/kross/project/src/config.ts)
# RIGHT: [config.ts](src/config.ts)
```

## After Generating Description

**Security Fix #1 - Command Injection Prevention**: When generating `title` and `description` variables, ensure they are assigned using proper quoting to prevent command injection:

```bash
# Safe assignment (use quotes):
title="Generated title text"
description="$(cat <<'EOF'
Multi-line description
EOF
)"

# UNSAFE - never do this:
# title=$(some_command)  # Without quotes, could execute commands in title
```

Update the PR using GitHub CLI:

```bash
# Security Fix #3: Pre-Update State Verification (prevent TOCTOU race condition)
# Re-check PR state immediately before update to prevent time-of-check-time-of-use race
if [[ -n "$pr_number" ]]; then
  current_pr_info=$(gh pr view "$pr_number" --json state 2>/dev/null)

  if [[ -n "$current_pr_info" ]]; then
    current_state=$(echo "$current_pr_info" | jq -r '.state // "UNKNOWN"')

    # Verify state hasn't changed since initial check
    if [[ "$current_state" != "$pr_state" ]]; then
      echo "ERROR: PR state changed during processing" >&2
      echo "  Initial state: $pr_state" >&2
      echo "  Current state: $current_state" >&2
      echo "  Aborting update to prevent unintended modification" >&2
      exit 1
    fi
  else
    echo "ERROR: PR no longer exists (may have been deleted)" >&2
    exit 1
  fi
fi

# Security Fix #7: Safety assertion with user_cancelled flag check
if [[ "$user_cancelled" == "true" ]]; then
  echo "ERROR: Attempted to continue after user cancellation" >&2
  exit 1
fi

# Safety assertion - should never trigger if validation worked correctly
if [[ "$pr_state" != "OPEN" ]] && [[ "$user_confirmed_update" != "true" ]]; then
  echo "ERROR: Attempted to update non-open PR #$pr_number (state: $pr_state) without user confirmation."
  echo "This indicates a bug in the PR state validation logic."
  exit 1
fi

gh pr edit <number> --title "Your Title Here" --body "$(cat <<'EOF'
[Your full description here]
EOF
)"
```

Confirm the update was successful:

```bash
gh pr view <number>
```
