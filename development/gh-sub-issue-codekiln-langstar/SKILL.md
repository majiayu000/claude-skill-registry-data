---
name: gh-sub-issue
description: Manage GitHub parent-child issue relationships using the gh-sub-issue extension. Link existing issues as sub-tasks, create new sub-issues, list relationships, and remove links. Use when working with GitHub issue hierarchies, Epic breakdowns, phased development, or when users mention sub-issues, sub-tasks, parent issues, or issue hierarchies.
---

# GitHub Sub-Issues Management

Manage GitHub parent-child issue relationships using the `gh-sub-issue` extension. Link existing issues, create new sub-issues, query relationships, and maintain issue hierarchies.

## Overview

`gh-sub-issue` is a GitHub CLI extension that provides commands for managing official parent-child relationships between GitHub issues. Unlike custom solutions that close and recreate issues, `gh-sub-issue` links existing issues directly while preserving their numbers.

**Key Advantage:** Non-destructive linking - issues keep their original numbers and history.

## Installation

The extension is pre-installed in the Langstar devcontainer. To verify:

```bash
gh extension list | grep sub-issue
```

To install manually:

```bash
gh extension install yahsan2/gh-sub-issue
```

## Core Commands

### Link Existing Issues

**Command:** `gh sub-issue add <parent> <child>`

Links an existing issue as a sub-task of another issue without closing or recreating it.

**Usage:**
```bash
# Link issue #103 as sub-task of #92
gh sub-issue add 92 103

# With explicit repository
gh sub-issue add 92 103 --repo owner/repo
```

**What it does:**
- Establishes official parent-child relationship via GitHub API
- Preserves both issue numbers
- Shows child in parent's "Sub-issues" dropdown
- Shows parent reference on child issue
- Fully reversible with `gh sub-issue remove`

**Example:**
```bash
$ gh sub-issue add 92 103
Successfully linked #103 as a sub-issue of #92
```

### Create New Sub-Issue

**Command:** `gh sub-issue create --parent <num> --title "Title"`

Creates a new issue with a parent relationship established from the start.

**Usage:**
```bash
# Create new sub-issue under #92
gh sub-issue create --parent 92 --title "Implement authentication"

# With body text
gh sub-issue create --parent 92 \
  --title "Add user login" \
  --body "Implement JWT-based authentication"

# With labels and assignees
gh sub-issue create --parent 92 \
  --title "Add tests" \
  --label "testing" \
  --assignee "username"
```

**What it does:**
- Creates issue with parent relationship already set
- Avoids need to link separately
- Supports full issue creation options (body, labels, assignees)

### List Related Issues

**Command:** `gh sub-issue list <issue>`

Shows all related issues: children, parent, and siblings.

**Usage:**
```bash
# List all relationships for #92
gh sub-issue list 92

# Show only children (sub-issues)
gh sub-issue list 92 --relation children

# Show only parent
gh sub-issue list 92 --relation parent

# Show siblings (issues with same parent)
gh sub-issue list 92 --relation siblings

# Filter by state
gh sub-issue list 92 --state open
gh sub-issue list 92 --state closed
gh sub-issue list 92 --state all

# JSON output for scripting
gh sub-issue list 92 --json number,title,state
```

**What it does:**
- Queries GitHub API for issue relationships
- Displays formatted table of related issues
- Supports filtering by relation type and state
- Provides JSON output for automation

**Example:**
```bash
$ gh sub-issue list 92 --relation children --state open

#     TITLE                                    STATE
103   feat(cli): Add deployment management    open
104   feat(cli): Add thread management         open
105   feat(cli): Add run operations            open
```

### Remove Link

**Command:** `gh sub-issue remove <parent> <child> [<child2> ...]`

Removes parent-child relationship without deleting issues.

**Usage:**
```bash
# Remove single link
gh sub-issue remove 92 103

# Remove multiple links at once
gh sub-issue remove 92 103 104 105

# Skip confirmation prompt
gh sub-issue remove 92 103 --force
```

**What it does:**
- Breaks parent-child relationship
- Keeps both issues intact
- Child issue becomes standalone again
- Supports batch operations

## When to Use This Skill

### Use Cases

**1. Linking Existing Issues**
When issues were created separately but need hierarchical organization:
```bash
# You have epic #83 and phases #90-95 already created
gh sub-issue add 83 90  # Link phase 1
gh sub-issue add 83 91  # Link phase 2
gh sub-issue add 83 92  # Link phase 3
```

**2. Creating Issue Hierarchies**
When planning multi-level work breakdown:
```bash
# Epic #83 → Phase #92 → Sub-tasks
gh sub-issue add 83 92                          # Link phase to epic
gh sub-issue create --parent 92 --title "Task 1"  # Create sub-task
gh sub-issue create --parent 92 --title "Task 2"  # Create sub-task
```

**3. Querying Relationships**
When you need to understand issue structure:
```bash
# What are the sub-tasks of this phase?
gh sub-issue list 92 --relation children

# What's the parent epic of this issue?
gh sub-issue list 103 --relation parent

# What other issues are at the same level?
gh sub-issue list 103 --relation siblings
```

**4. Maintaining Hierarchies**
When relationships need adjustment:
```bash
# Move issue #103 from parent #92 to parent #93
gh sub-issue remove 92 103
gh sub-issue add 93 103
```

## Comparison: Old vs New Approach

### Old Approach (Python Script)

**Process:**
1. Close child issue with comment
2. Recreate with same content but new parent
3. Child gets NEW issue number
4. All references broken

**Problems:**
- ❌ Issue number changes (breaks references)
- ❌ History fragmented across two issues
- ❌ Comments/discussions on original issue orphaned
- ❌ Links in PRs, docs become invalid

### New Approach (gh-sub-issue)

**Process:**
1. Link issues via GitHub API
2. Both issues unchanged
3. Relationship established

**Benefits:**
- ✅ Issue numbers preserved
- ✅ History intact
- ✅ All references remain valid
- ✅ Reversible without data loss

## Integration with Other Skills

### With `github-issue-breakdown`

**Use `github-issue-breakdown` for:** Creating multiple sub-issues from task list
```markdown
<!-- In issue #92 -->
## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
```
Then run `github-issue-breakdown` to create #103, #104, #105 as sub-issues of #92.

**Use `gh-sub-issue add` for:** Linking issues created outside the breakdown workflow
```bash
# Someone created #106 manually
gh sub-issue add 92 106  # Add to the same parent
```

### With `update-github-issue-project-status`

After linking issues, update project board status:
```bash
# Link sub-tasks to parent
gh sub-issue add 92 103
gh sub-issue add 92 104

# Update status in GitHub Projects
# (Use update-github-issue-project-status skill)
```

## Workflows

### Workflow 1: Create Epic with Phases

**Goal:** Break down large feature into phases

```bash
# Step 1: Create epic issue manually or with gh
gh issue create --title "Epic: User Authentication System" \
  --body "Complete authentication system with OAuth, JWT, and 2FA"
# Created issue #100

# Step 2: Create phase issues
gh sub-issue create --parent 100 --title "Phase 1: Research authentication options"
# Created issue #101

gh sub-issue create --parent 100 --title "Phase 2: Implement JWT authentication"
# Created issue #102

gh sub-issue create --parent 100 --title "Phase 3: Add OAuth providers"
# Created issue #103

# Step 3: Verify structure
gh sub-issue list 100 --relation children
```

**Result:** Epic #100 → Phases #101, #102, #103

### Workflow 2: Retrofit Existing Issues

**Goal:** Add structure to issues already created

```bash
# Scenario: Issues #50-54 exist but aren't linked to epic #40

# Link all at once
for issue in 50 51 52 53 54; do
  gh sub-issue add 40 $issue
done

# Verify
gh sub-issue list 40 --json number,title
```

### Workflow 3: Two-Level Hierarchy

**Goal:** Epic → Phases → Sub-tasks

```bash
# Level 1: Epic #83
# Level 2: Phase #92 (already linked to #83)

# Add sub-tasks to phase #92
gh sub-issue create --parent 92 --title "Design authentication API"
# Created #110

gh sub-issue create --parent 92 --title "Implement JWT tokens"
# Created #111

gh sub-issue create --parent 92 --title "Add authentication tests"
# Created #112

# View hierarchy
echo "Epic #83 children:"
gh sub-issue list 83 --relation children

echo "Phase #92 children:"
gh sub-issue list 92 --relation children
```

**Result:**
- Epic #83 → Phase #92
- Phase #92 → Sub-tasks #110, #111, #112

### Workflow 4: Reorganize Hierarchy

**Goal:** Move issues between parents

```bash
# Issue #105 is under #92 but should be under #93

# Step 1: Remove from current parent
gh sub-issue remove 92 105

# Step 2: Add to new parent
gh sub-issue add 93 105

# Step 3: Verify
gh sub-issue list 105 --relation parent
```

## Best Practices

### Planning Ahead

**Preferred:** Use `github-issue-breakdown` when creating issues from task list
- Creates sub-issues correctly from the start
- Avoids manual linking work
- Maintains clean history

**Acceptable:** Use `gh-sub-issue add` when:
- Issues already exist
- Issues were created manually
- Fixing missing relationships

### Consistent Hierarchy

**Establish clear levels:**
- Level 1: Epic (major feature)
- Level 2: Phase (implementation stage)
- Level 3: Task (specific work item)

**Example structure:**
```
#83 Epic: CLI Implementation
├── #90 Phase 1: Research
├── #91 Phase 2: Design
└── #92 Phase 3: Implementation
    ├── #103 Task: Deployment management
    ├── #104 Task: Thread management
    └── #105 Task: Run operations
```

### Documentation

**Always document hierarchy in epic issue:**
```markdown
## Epic Structure

### Phases
- #90 - Phase 1: Research
- #91 - Phase 2: Design
- #92 - Phase 3: Implementation

### Sub-tasks (Phase 3)
- #103 - Deployment management
- #104 - Thread management
- #105 - Run operations
```

### Verification

**After creating hierarchy:**
```bash
# Check parent's children
gh sub-issue list <parent> --relation children --state all

# Check child's parent
gh sub-issue list <child> --relation parent

# Verify structure is correct before proceeding with implementation
```

## Troubleshooting

### "Extension not found"

**Cause:** gh-sub-issue not installed

**Solution:**
```bash
gh extension install yahsan2/gh-sub-issue
gh extension list | grep sub-issue
```

### "Issue not found"

**Cause:** Issue number doesn't exist or no repository access

**Solution:**
- Verify issue exists: `gh issue view <number>`
- Check repository: `gh sub-issue add <parent> <child> --repo owner/name`
- Confirm access permissions

### "Could not create relationship"

**Cause:** GitHub API limitations or permissions

**Solution:**
- Verify both issues exist: `gh issue view <number>`
- Check authentication: `gh auth status`
- Ensure repository write access: `gh auth refresh -s repo`

### "Operation failed"

**Cause:** Various GitHub API errors

**Solution:**
- Check issue state (can't link closed issues in some cases)
- Verify you're in correct repository
- Try with explicit repo: `--repo owner/name`
- Check for circular dependencies (A parent of B, B parent of A)

## Environment Requirements

**Prerequisites:**
- `gh` CLI installed and authenticated
- Repository access with write permissions
- `gh-sub-issue` extension installed (v0.5.1+ recommended)

**Verification:**
```bash
# Check gh CLI
gh --version

# Check authentication
gh auth status

# Check extension
gh extension list | grep sub-issue

# Test command
gh sub-issue --help
```

## Command Reference

### Quick Reference Table

| Command | Purpose | Preserves Issue # | Example |
|---------|---------|-------------------|---------|
| `add` | Link existing issues | ✅ Yes | `gh sub-issue add 92 103` |
| `create` | Create new sub-issue | N/A (new) | `gh sub-issue create --parent 92 --title "Task"` |
| `list` | Query relationships | N/A (read-only) | `gh sub-issue list 92` |
| `remove` | Unlink issues | ✅ Yes | `gh sub-issue remove 92 103` |

### Common Flag Combinations

```bash
# Link with explicit repo
gh sub-issue add 92 103 --repo owner/name

# Create with all options
gh sub-issue create --parent 92 \
  --title "Title" \
  --body "Description" \
  --label "bug" \
  --label "priority:high" \
  --assignee "username"

# List with filters
gh sub-issue list 92 \
  --relation children \
  --state open \
  --json number,title,state

# Remove multiple without confirmation
gh sub-issue remove 92 103 104 105 --force
```

## See Also

- **github-issue-breakdown** - Create sub-issues from task lists in parent issue
- **update-github-issue-project-status** - Update GitHub Projects status fields
- **GitHub Workflow Documentation** - `@docs/dev/github-workflow.md`
- **gh-sub-issue repository** - https://github.com/yahsan2/gh-sub-issue
