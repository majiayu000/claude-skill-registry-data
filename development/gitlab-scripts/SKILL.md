---
name: gitlab-scripts
description: Use GitLab scripts instead of GitLab MCP for both read and write operations. Read operations (gitlab-mr-comments, gitlab-list-mrs) for fetching MR data. Write operations (gitlab-create-mr, gitlab-comment-mr, gitlab-inline-comment, gitlab-update-mr) for creating/updating MRs and posting inline code comments. Use when reviewing code, creating MRs, commenting on MRs, adding inline code review comments, updating MR metadata, listing MRs, or working with GitLab merge requests. Replaces 82 MCP functions (80k tokens) with lightweight bash scripts.
---

# GitLab Scripts Usage

**Purpose:** Perform GitLab merge request operations (both read and write) using lightweight bash scripts instead of heavy MCP tools.

**When to use:** When fetching MR data, creating MRs, commenting on MRs, updating MR metadata, listing MRs, or reviewing code during workflows.

---

## Core Principles

1. **Scripts over MCP** - 99.75% token savings (80k → 200 tokens)
2. **Credentials in files** - Uses `~/.claude/scripts/.gitlab-credentials` (gitignored)
3. **Clear error messages** - Scripts stop and show setup instructions if credentials missing
4. **Standard exit codes** - 0=success, 1=args, 2=not found, 3=API error, 4=creds missing

---

## Available Scripts

### Read Operations

#### gitlab-mr-comments

**Fetch merge request discussions/comments for a ticket.**

**Usage:**
```bash
gitlab-mr-comments <ticket-id>
```

**Examples:**
```bash
# Fetch comments for a ticket
gitlab-mr-comments INT-3877

# Use in Bash tool
result = Bash(command="~/.claude/scripts/gitlab-mr-comments INT-3877")
if result.returncode == 0:
    comments = result.stdout
else:
    comments = None  # No comments or MR not found
```

**Output format:**
```markdown
📝 MR !3302 Comments (7 discussions):

## Comment by @reviewer - 2025-10-24
**Location:** src/api/auth.py:45
This needs validation for negative amounts
---

## Comment by @security - 2025-10-24
**Status:** ✅ Resolved
Looks good after fixes
---

**Summary:** 7 total discussions, 2 resolved, 5 unresolved
```

**Exit codes:**
- 0 = Success (comments fetched or no comments)
- 1 = No branch found for ticket
- 2 = No MR found for branch
- 3 = API error (network, auth failed)
- 4 = Credentials missing

---

#### gitlab-list-mrs

**List merge requests with optional filters.**

**Usage:**
```bash
gitlab-list-mrs [--state opened|closed|merged|all] [--author <username>] [--assignee <username>] [--labels <label1,label2>]
```

**Examples:**
```bash
# List all open MRs (default)
gitlab-list-mrs

# List merged MRs
gitlab-list-mrs --state merged

# List open MRs by author
gitlab-list-mrs --author rmurphy --state opened

# List MRs assigned to user with specific labels
gitlab-list-mrs --assignee alice --labels bug,urgent

# Use in Bash tool
result = Bash(command="~/.claude/scripts/gitlab-list-mrs --state opened")
if result.returncode == 0:
    mr_list = result.stdout
```

**Output format:**
```markdown
📋 Merge Requests (3 found):

## !1234: INT-3877: Add rate limiting to auth endpoints
**Status:** opened
**Author:** @rmurphy
**Assignee:** @alice
**Labels:** security, urgent
**Created:** 2025-10-20
**Updated:** 2025-10-24
**URL:** https://gitlab.com/project/merge_requests/1234
---

## !1235: INT-3878: Fix validation bug
**Status:** opened
**Author:** @bob
**Assignee:** Unassigned
**Labels:** None
**Created:** 2025-10-21
**Updated:** 2025-10-23
**URL:** https://gitlab.com/project/merge_requests/1235
---
```

**Exit codes:**
- 0 = Success (MRs listed or no MRs found)
- 1 = Usage error (invalid arguments)
- 3 = API error (network, auth failed)
- 4 = Credentials missing

---

### Write Operations

#### gitlab-create-mr

**Create a new merge request.**

**IMPORTANT:** Title format MUST be `"<jira-ticket>: <description>"` (e.g., `"INT-3877: Add rate limiting"`)

**Usage:**
```bash
gitlab-create-mr <source-branch> <target-branch> <title> [description]
```

**Examples:**
```bash
# Create MR with title only
gitlab-create-mr INT-3877-auth develop "INT-3877: Add rate limiting to auth endpoints"

# Create MR with title and description
gitlab-create-mr INT-3877-auth develop "INT-3877: Add rate limiting to auth endpoints" "Implements rate limiting using Redis for distributed tracking. Limits: 100 req/min per user."

# Use in Bash tool
result = Bash(command='~/.claude/scripts/gitlab-create-mr INT-3877-auth develop "INT-3877: Add rate limiting" "Full implementation..."')
if result.returncode == 0:
    echo("✅ MR created successfully")
    mr_url = extract_url_from(result.stdout)
else:
    echo(f"❌ Failed to create MR: {result.stderr}")
```

**Output format:**
```
✅ Merge request created successfully!

MR !1234: INT-3877: Add rate limiting to auth endpoints
URL: https://gitlab.com/project/merge_requests/1234

Source: INT-3877-auth → Target: develop
```

**Exit codes:**
- 0 = Success (MR created)
- 1 = Usage error (missing required arguments)
- 2 = Branch not found
- 3 = API error (conflict, permissions, network, auth failed)
- 4 = Credentials missing

**Common errors:**
- Exit 3 with "already exists": MR already created for this branch
- Exit 2: Source or target branch doesn't exist
- Exit 3 with "403": No permission to create MRs

---

#### gitlab-comment-mr

**Add a comment to an existing merge request.**

**Usage:**
```bash
gitlab-comment-mr <mr-iid> <comment-text>
```

**Examples:**
```bash
# Add approval comment
gitlab-comment-mr 1234 "LGTM, approved"

# Add review comment with details
gitlab-comment-mr 1234 "Please add validation for negative amounts in src/api/auth.py:45"

# Use in Bash tool
result = Bash(command='~/.claude/scripts/gitlab-comment-mr 1234 "Review complete. All tests passing."')
if result.returncode == 0:
    echo("✅ Comment added successfully")
else:
    echo(f"❌ Failed to add comment: {result.stderr}")
```

**Output format:**
```
✅ Comment added to MR !1234

Comment ID: 987654
Author: @rmurphy
Created: 2025-10-24

Comment text:
LGTM, approved
```

**Exit codes:**
- 0 = Success (comment added)
- 1 = Usage error (missing required arguments)
- 2 = MR not found
- 3 = API error (permissions, network, auth failed)
- 4 = Credentials missing

**Common errors:**
- Exit 2: MR IID doesn't exist
- Exit 3 with "403": No permission to comment on this MR

---

#### gitlab-inline-comment

**Add inline comment to specific code line in merge request (for code review).**

**Usage:**
```bash
gitlab-inline-comment <ticket-or-mr-iid> <file-path> <line-number> <comment-text>
```

**Examples:**
```bash
# Using ticket ID (finds MR automatically)
gitlab-inline-comment INT-3877 src/auth.py 45 "Missing validation for negative amounts"

# Using MR IID directly
gitlab-inline-comment 1234 src/auth.py 45 "Missing validation for negative amounts"

# Add inline review comment
gitlab-inline-comment INT-4000 fisio/common/write_manager.py 401 "ReplaceOne should be included in this check for AR enrollment"

# Use in Bash tool
result = Bash(command='~/.claude/scripts/gitlab-inline-comment INT-3877 src/auth.py 45 "Add null check here"')
if result.returncode == 0:
    echo("✅ Inline comment added")
else:
    echo(f"❌ Failed to add inline comment: {result.stderr}")
```

**Output format:**
```
✅ Inline comment added to MR !1234

Discussion ID: d987654
Note ID: n123456
Author: @rmurphy
Created: 2025-10-27
Location: src/auth.py:45

Comment text:
Missing validation for negative amounts
```

**Exit codes:**
- 0 = Success (inline comment added)
- 1 = Usage error (missing arguments, invalid line number)
- 2 = MR or branch not found
- 3 = API error (line doesn't exist in diff, invalid position, permissions, network, auth failed)
- 4 = Credentials missing

**Common errors:**
- Exit 3 with "400 Bad Request": Line number doesn't exist in the diff or file wasn't modified in the MR
- Exit 2: Ticket branch or MR not found
- Exit 3 with "403": No permission to comment on this MR

**Important notes:**
- Inline comments only work on **lines that were modified** in the MR
- For general comments (not tied to code), use `gitlab-comment-mr` instead
- Line numbers refer to the **new file** (after changes), not the old file

---

#### gitlab-update-mr

**Update merge request metadata (title, description, assignee, labels).**

**Usage:**
```bash
gitlab-update-mr <mr-iid> [--title <title>] [--description <desc>] [--assignee <username>] [--labels <label1,label2>]
```

**Examples:**
```bash
# Update title only
gitlab-update-mr 1234 --title "INT-3877: Updated title"

# Update multiple fields
gitlab-update-mr 1234 --assignee alice --labels "bug,urgent"

# Update description
gitlab-update-mr 1234 --description "Updated implementation with performance improvements"

# Update all fields at once
gitlab-update-mr 1234 --title "New title" --assignee bob --labels "feature,ready" --description "Complete rewrite"

# Use in Bash tool
result = Bash(command='~/.claude/scripts/gitlab-update-mr 1234 --labels "reviewed,approved"')
if result.returncode == 0:
    echo("✅ MR updated successfully")
else:
    echo(f"❌ Failed to update MR: {result.stderr}")
```

**Output format:**
```
✅ Merge request !1234 updated successfully!

Title: INT-3877: Add rate limiting to auth endpoints
URL: https://gitlab.com/project/merge_requests/1234
Assignee: alice
Labels: bug, urgent

Updated fields:
  - Assignee
  - Labels
```

**Exit codes:**
- 0 = Success (MR updated)
- 1 = Usage error (missing required arguments or no update fields provided)
- 2 = MR or user not found
- 3 = API error (permissions, network, auth failed)
- 4 = Credentials missing

**Common errors:**
- Exit 1: No update flags provided (must provide at least one of --title, --description, --assignee, --labels)
- Exit 2: Assignee username doesn't exist
- Exit 3 with "403": No permission to update this MR

---

## Integration Patterns

### Pattern 1: Fetch with Fallback (Recommended)

```python
# Try to fetch MR comments, fall back gracefully if unavailable
result = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}")

if result.returncode == 0:
    mr_comments = result.stdout
    # Comments available - use in review
elif result.returncode == 4:
    # Credentials not configured
    echo("⚠️ GitLab credentials not configured - skipping MR comments")
    mr_comments = None
else:
    # MR not found or other error
    mr_comments = None
```

**When:** PR review workflows, optional comment fetching

### Pattern 2: Required Comments

```python
# Require comments - fail if not available
result = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}")

if result.returncode != 0:
    echo(f"❌ Failed to fetch MR comments: {result.stderr}")
    exit(1)

mr_comments = result.stdout
# Process comments...
```

**When:** Comment analysis is critical to workflow

### Pattern 3: Check Before Use

```python
# Check if credentials are configured before attempting
creds_file = Path("~/.claude/scripts/.gitlab-credentials").expanduser()

if not creds_file.exists():
    echo("⚠️ GitLab scripts not configured - skipping MR comment fetch")
    mr_comments = None
else:
    result = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}")
    mr_comments = result.stdout if result.returncode == 0 else None
```

**When:** Want to avoid unnecessary script execution

---

## Credentials Setup

**File:** `~/.claude/scripts/.gitlab-credentials`

**The script handles credentials automatically:**
- If file missing: Shows setup instructions and exits with code 4
- If file incomplete: Shows which vars are missing and exits with code 4
- File is gitignored (pattern: `scripts/*-credentials`)

**Manual setup (if needed):**

```bash
# File format
GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxx"
GITLAB_API_URL="https://gitlab.com/api/v4"
GITLAB_PROJECT_ID="29007973"
```

**Get your token:**
1. Go to: https://gitlab.com/-/profile/personal_access_tokens
2. Create token with `api` scope
3. Copy the token (starts with `glpat-`)

**Find project ID:**
- On your project's GitLab page
- Look under the project name (e.g., "Project ID: 29007973")

---

## Error Handling

### Missing Credentials (Exit 4)

**Script output:**
```
❌ GitLab credentials not found or incomplete.

STOP: This script requires GitLab API credentials to be configured.

Please create the file: ~/.claude/scripts/.gitlab-credentials

With the following content:
    GITLAB_PERSONAL_ACCESS_TOKEN="your-token-here"
    GITLAB_API_URL="https://gitlab.com/api/v4"
    GITLAB_PROJECT_ID="your-project-id"

[Instructions for getting each value]
```

**Your action:** Stop execution, tell user to configure credentials.

### No Branch Found (Exit 1)

**Script output:**
```
⚠️ No branch found for ticket: INT-9999
```

**Your action:** Ticket might be invalid, merged, or not in git. Ask user to verify ticket ID.

### No MR Found (Exit 2)

**Script output:**
```
⚠️ No MR found for branch: INT-3877-fix-auth
```

**Your action:** MR might not exist or is not accessible. Not a critical error for review workflows.

### API Error (Exit 3)

**Script output:**
```
❌ GitLab API error: 401 Unauthorized
```

**Your action:** Credentials are wrong or expired. Tell user to regenerate API token.

---

## Common Scenarios

### Scenario 1: PR Review Workflow

```python
# Phase: Context Gathering (parallel operations)

# Fetch MR comments (optional - may not exist)
mr_result = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}")
mr_comments = mr_result.stdout if mr_result.returncode == 0 else None

# Fetch Jira ticket (optional - may not exist)
jira_result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")
ticket_content = jira_result.stdout if jira_result.returncode == 0 else None

# Git analysis (always works - local)
git_diff = Bash(command="git diff origin/develop...origin/INT-3877")

# Continue with review using available data
```

**Why:** MR comments and Jira ticket are optional context - review continues without them.

### Scenario 2: Agent Delegation

```python
# Pass MR comments to agent as context

mr_comments = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}").stdout

Task(investigator, f"""
Analyze code changes in {worktree_path}.

EXISTING MR COMMENTS:
{mr_comments or "No existing comments"}

Check if concerns raised in MR comments were addressed in the code.
""")
```

**Why:** Agents need context about existing feedback.

### Scenario 3: Checking for Previous Review

```python
# See if MR has been reviewed before attempting automated review

mr_result = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}")

if mr_result.returncode == 0:
    comment_count = mr_result.stdout.count("## Comment by")

    if comment_count > 10:
        echo(f"⚠️ MR has {comment_count} existing comments - may already be reviewed")
        # Proceed differently or ask user
```

**Why:** Avoid duplicate work on heavily-commented MRs.

### Scenario 4: Create MR After Implementation

```python
# After completing implementation, create MR automatically

branch_name = "INT-3877-auth"
target_branch = "develop"
title = "INT-3877: Add rate limiting to auth endpoints"
description = """
Implements rate limiting for authentication endpoints.

Changes:
- Added Redis-based rate limiter
- Configured limits: 100 req/min per user
- Added unit and integration tests

Fixes INT-3877
"""

result = Bash(command=f'~/.claude/scripts/gitlab-create-mr {branch_name} {target_branch} "{title}" "{description}"')

if result.returncode == 0:
    echo("✅ MR created successfully")
    # Extract MR URL from stdout for user
elif result.returncode == 3 and "already exists" in result.stderr:
    echo("⚠️ MR already exists for this branch")
else:
    echo(f"❌ Failed to create MR: {result.stderr}")
```

**Why:** Automate MR creation after implementation completion.

### Scenario 5: Add Review Comments Programmatically

```python
# After code review analysis, add comments to MR

mr_iid = "1234"
findings = [
    "LGTM overall. Minor suggestions below.",
    "Consider adding validation for negative amounts in src/api/auth.py:45",
    "Performance: Batch Redis operations for better throughput"
]

for comment in findings:
    result = Bash(command=f'~/.claude/scripts/gitlab-comment-mr {mr_iid} "{comment}"')
    if result.returncode != 0:
        echo(f"⚠️ Failed to add comment: {result.stderr}")
```

**Why:** Automate posting review findings to MR.

### Scenario 6: Update MR After Changes

```python
# After addressing review comments, update MR metadata

mr_iid = "1234"
new_labels = "reviewed,ready-for-merge"

result = Bash(command=f'~/.claude/scripts/gitlab-update-mr {mr_iid} --labels "{new_labels}"')

if result.returncode == 0:
    echo("✅ MR updated - marked as ready for merge")
else:
    echo(f"❌ Failed to update MR: {result.stderr}")
```

**Why:** Update MR status after review process completion.

---

## Comparison: Script vs MCP

| Aspect | GitLab MCP | gitlab-scripts |
|--------|------------|----------------|
| **Functions** | 82 | 5 (covers common MR workflows) |
| **Token Cost** | ~80,000 | ~1,000 |
| **Setup** | MCP server config | One credentials file |
| **Maintenance** | Auto-generated, external | 5 bash scripts, local |
| **Customization** | None (auto-generated) | Full control over output |
| **Performance** | Slower (tool loading) | Faster (direct curl) |
| **Operations** | All GitLab operations | MR-focused (read + write) |

**Token savings:** 79,000 tokens per conversation (98.75%)

---

## Quick Reference

**Read operations:**
```bash
gitlab-mr-comments <ticket-id>                    # Fetch MR discussions
gitlab-list-mrs [--state X] [--author Y]          # List MRs with filters
```

**Write operations:**
```bash
gitlab-create-mr <source> <target> <title> [desc]     # Create MR (title format: "TICKET: desc")
gitlab-comment-mr <mr-iid> <comment-text>             # Add general comment
gitlab-inline-comment <ticket> <file> <line> <text>   # Add inline code comment
gitlab-update-mr <mr-iid> [--title X] [--labels Y]    # Update metadata
```

**Check exit code:**
```python
result = Bash(command="gitlab-mr-comments INT-3877")
if result.returncode == 0:
    # Success
elif result.returncode == 4:
    # Credentials missing - tell user
else:
    # Error - check result.stderr
```

**Credentials file location:**
```
~/.claude/scripts/.gitlab-credentials
```

**Documentation:**
```
~/.claude/scripts/README.md  # Complete script documentation
```

---

## When NOT to Use Scripts

**Use GitLab MCP instead when:**
- Need to **manage pipelines** (trigger, cancel, retry)
- Need to **manage repository settings** (branches, tags, webhooks)
- Need to **manage issues** (create, update, close)
- Need to **post threaded discussions** with file:line references
- Need >10 different GitLab operations in one workflow

**Scripts cover common MR workflows:** Read MR data (comments, list), write MR data (create, comment, update metadata).

---

## Summary

**What:** Lightweight bash scripts replace heavy GitLab MCP for common MR workflows
**When:** Reading MR data (comments, lists) or writing MR data (create, comment, update)
**Why:** 98.75% token savings (80k → 1k)
**How:** Use Bash tool to call `gitlab-[operation] <args>`

**Available operations:**
- **Read**: `gitlab-mr-comments`, `gitlab-list-mrs`
- **Write**: `gitlab-create-mr`, `gitlab-comment-mr`, `gitlab-inline-comment`, `gitlab-update-mr`

**Remember:** Scripts are optional tools. If credentials aren't configured, workflows continue without GitLab operations. Don't block on missing optional data.
