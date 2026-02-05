---
name: jira-scripts
description: Use Jira scripts instead of Jira MCP for ticket operations. Read operations (jira-get-issue), write operations (jira-create-ticket, jira-comment-ticket, jira-update-ticket, jira-log-work, jira-link-tickets), and list operations (jira-list-tickets, jira-list-sprint). Use when reviewing code, creating tickets, commenting on tickets, updating tickets, logging work, linking tickets, listing tickets, or viewing sprint. Replaces ~30 MCP functions (40k tokens) with lightweight bash scripts.
---

# Jira Scripts Usage

**Purpose:** Perform Jira operations using lightweight bash scripts instead of heavy MCP tools.

**When to use:** When fetching ticket details, creating tickets, commenting on tickets, updating ticket fields, logging work, linking tickets, listing tickets, or viewing sprint issues.

---

## Core Principles

1. **Scripts over MCP** - 99.4% token savings (40k → 250 tokens)
2. **Credentials in files** - Uses `~/.claude/scripts/.jira-credentials` (gitignored)
3. **Clear error messages** - Scripts stop and show setup instructions if credentials missing
4. **Standard exit codes** - 0=success, 1=args, 2=not found, 3=API error, 4=creds missing

---

## Available Scripts

### Read Operations

#### jira-get-issue

**Fetch complete Jira issue details including description and acceptance criteria.**

**Usage:**
```bash
jira-get-issue <ticket-id>
```

**Examples:**
```bash
# Fetch ticket details
jira-get-issue INT-3877

# Use in Bash tool
result = Bash(command="~/.claude/scripts/jira-get-issue INT-3877")
if result.returncode == 0:
    ticket_content = result.stdout
else:
    ticket_content = None  # Ticket not found or error
```

**Output format:**
```markdown
# Issue: INT-4013

**Title:** Upgrade uv to 0.9.5
**Status:** Completed
**Type:** Task
**Priority:** Medium
**Assignee:** Mark Pellegrini

**Created:** 2025-10-23
**Updated:** 2025-10-27

**Labels:** None
**Components:** Build and dependencies
**Fix Versions:** VRM 6.22.0
**Story Points:** 5

## Description

[Full ticket description with formatting preserved]

## Acceptance Criteria

[Acceptance criteria if present]

## Developer Checklist

[Technical implementation details from customfield_11848 - shows data structures, API changes, migration notes]

## Test Plan

[Testing strategy and test cases from customfield_11003]

## Dev Complete Checklist

[Completion checklist from customfield_11340 if present]

## Development and Implementation Checklist

[Implementation checklist from customfield_11661 if present]

## Comments

### Comment by John Doe (2025-10-20)

[Comment body with formatting preserved]

---

### Comment by Jane Smith (2025-10-21)

[Another comment]

---

[All comments with full pagination - no limits]

## Related Issues

- Relates to: INT-1234 (Other ticket title)
- clones: PLAT-53 (Frontend ticket)

### Related Ticket Details

#### PLAT-53

**Status:** In Progress
**Summary:** (FE) Add the ability to see what notification was sent in the activity stream

**Description (preview):**
[First 500 chars of description]

**Developer Checklist (preview):**
[First 1000 chars of developer checklist]

**View:** https://fortressinfosec.atlassian.net/browse/PLAT-53

---

[Additional related tickets...]

---
**View in Jira:** https://fortressinfosec.atlassian.net/browse/INT-4013
```

**What's included:**
- **All custom checklists** - Developer Checklist, Test Plan, Dev Complete, Implementation Checklist
- **All comments** - Full pagination, no limits, ADF format parsed
- **Related ticket details (FULL)** - Fetches COMPLETE data for FE/BE pairs, clones, blocking tickets:
  - Each related ticket includes: Description, Acceptance Criteria, Developer Checklist, Test Plan, Comments
  - No recursion: Only fetches related tickets of the main ticket (not related-to-related)
  - Perfect for FE/BE coordination - see both tickets' checklists and requirements
- **Full ADF parsing** - All text content extracted from Atlassian Document Format

**Example:** Fetching PLAT-54 returns:
- PLAT-54 full data (343 lines)
- PLAT-53 full data (FE pair) with its own Developer Checklist, Test Plan, Comments
- 4 other related tickets with full data
- Total: ~1100 lines of comprehensive context

**Exit codes:**
- 0 = Success (ticket fetched)
- 1 = Missing ticket argument
- 2 = Ticket not found (404)
- 3 = API error (auth failed, network issue)
- 4 = Credentials missing

---

### Write Operations

#### jira-create-ticket

**Create a new Jira ticket with project, type, summary, and optional description.**

**Usage:**
```bash
jira-create-ticket <project-key> <issue-type> <summary> [description]
```

**Examples:**
```bash
# Create Task with description
jira-create-ticket INT Task "Add rate limiting" "Implement rate limiting on auth endpoints"

# Create Bug without description
jira-create-ticket INT Bug "Fix login error"

# Use in Bash tool
result = Bash(command='jira-create-ticket INT Task "Add logging" "Add structured logging to API"')
if result.returncode == 0:
    # Parse created ticket key from output
    ticket_key = extract_ticket_key(result.stdout)
else:
    # Handle error
    echo(f"Failed to create ticket: {result.stderr}")
```

**Common issue types:**
- Task
- Bug
- Story
- Epic
- Sub-task

**Output format:**
```
✓ Created ticket: INT-1234

**View in Jira:** https://fortressinfosec.atlassian.net/browse/INT-1234
**Issue ID:** 12345
```

**Exit codes:**
- 0 = Success (ticket created)
- 1 = Missing required arguments
- 2 = Project not found or invalid issue type
- 3 = API error (auth failed, permission denied)
- 4 = Credentials missing

---

#### jira-comment-ticket

**Add a comment to an existing Jira ticket.**

**Usage:**
```bash
jira-comment-ticket <ticket-id> <comment-text>
```

**Examples:**
```bash
# Add simple comment
jira-comment-ticket INT-3877 "Work completed and tested"

# Add detailed comment
jira-comment-ticket INT-3877 "Implemented rate limiting with 100 req/min threshold. All tests passing."

# Use in Bash tool
result = Bash(command='jira-comment-ticket INT-3877 "Code review complete - ready for merge"')
if result.returncode == 0:
    echo("Comment added successfully")
```

**Output format:**
```
✓ Comment added to INT-3877

**Comment ID:** 67890
**Author:** John Doe
**Created:** 2025-10-27T14:30:00.000-0400
**View in Jira:** https://fortressinfosec.atlassian.net/browse/INT-3877
```

**Exit codes:**
- 0 = Success (comment added)
- 1 = Missing required arguments
- 2 = Ticket not found
- 3 = API error (auth failed, permission denied)
- 4 = Credentials missing

---

#### jira-update-ticket

**Update fields on an existing Jira ticket (description, assignee, status, priority, labels).**

**Usage:**
```bash
jira-update-ticket <ticket-id> [--description <desc>] [--assignee <email>] [--status <status>] [--priority <priority>] [--labels <label1,label2>]
```

**Examples:**
```bash
# Update description and priority
jira-update-ticket INT-3877 --description "Updated requirements" --priority High

# Transition status and assign
jira-update-ticket INT-3877 --status "In Progress" --assignee "user@fortressinfosec.com"

# Update labels
jira-update-ticket INT-3877 --labels "backend,api,security"

# Multiple fields
jira-update-ticket INT-3877 --description "Final version" --status "Done" --priority Medium

# Use in Bash tool
result = Bash(command='jira-update-ticket INT-3877 --status "In Progress"')
if result.returncode == 0:
    echo("Ticket status updated")
```

**Available options:**
- `--description <text>` - Update ticket description
- `--assignee <email>` - Assign to user by email
- `--status <status>` - Transition to new status (e.g., "In Progress", "Done")
- `--priority <priority>` - Set priority (e.g., "High", "Medium", "Low")
- `--labels <label1,label2>` - Set labels (comma-separated)

**Output format:**
```
✓ Updated ticket fields: INT-3877
✓ Transitioned status to: In Progress

**Updated ticket:** INT-3877
**View in Jira:** https://fortressinfosec.atlassian.net/browse/INT-3877
```

**Exit codes:**
- 0 = Success (ticket updated)
- 1 = Missing ticket ID or invalid option
- 2 = Ticket not found
- 3 = API error (invalid status transition, permission denied, invalid field value)
- 4 = Credentials missing

**Note:** Status transitions must be valid for the ticket's current state. Script automatically determines the correct transition ID.

---

#### jira-log-work

**Log time spent on a Jira ticket with optional comment.**

**Usage:**
```bash
jira-log-work <ticket-id> <time-spent> [comment]
```

**Examples:**
```bash
# Log 2 hours 30 minutes with comment
jira-log-work INT-3877 "2h 30m" "Implemented rate limiting logic"

# Log 1 day 4 hours without comment
jira-log-work INT-3877 "1d 4h"

# Log 30 minutes
jira-log-work INT-3877 "30m" "Code review"

# Use in Bash tool
result = Bash(command='jira-log-work INT-3877 "3h" "Implemented feature and tests"')
if result.returncode == 0:
    echo("Work logged successfully")
```

**Time format (Jira duration format):**
- Units: `w` (weeks), `d` (days), `h` (hours), `m` (minutes)
- Examples: `2h`, `1d 4h`, `30m`, `1w 2d 3h 30m`

**Output format:**
```
✓ Work logged on INT-3877

**Worklog ID:** 23456
**Time Spent:** 2h 30m (9000s)
**Author:** John Doe
**Created:** 2025-10-27T14:30:00.000-0400
**View in Jira:** https://fortressinfosec.atlassian.net/browse/INT-3877
```

**Exit codes:**
- 0 = Success (work logged)
- 1 = Missing required arguments
- 2 = Ticket not found
- 3 = API error (invalid time format, permission denied)
- 4 = Credentials missing

---

#### jira-link-tickets

**Create a link between two Jira tickets with specified relationship type.**

**Usage:**
```bash
jira-link-tickets <source-ticket-id> <link-type> <target-ticket-id>
```

**Examples:**
```bash
# Create blocking relationship
jira-link-tickets INT-3877 "Blocks" INT-3878

# Create relates-to relationship
jira-link-tickets INT-3877 "Relates to" INT-3900

# Create duplicate relationship
jira-link-tickets INT-3877 "Duplicates" INT-3999

# Use in Bash tool
result = Bash(command='jira-link-tickets INT-3877 "Blocks" INT-3878')
if result.returncode == 0:
    echo("Tickets linked successfully")
```

**Common link types (case-sensitive):**
- `"Blocks"` / `"is blocked by"`
- `"Relates to"`
- `"Duplicates"` / `"is duplicated by"`
- `"Clones"` / `"is cloned by"`
- `"Causes"` / `"is caused by"`

**Output format:**
```
✓ Linked tickets: INT-3877 Blocks INT-3878

**View in Jira:**
  - https://fortressinfosec.atlassian.net/browse/INT-3877
  - https://fortressinfosec.atlassian.net/browse/INT-3878
```

**Exit codes:**
- 0 = Success (tickets linked)
- 1 = Missing required arguments
- 2 = One or both tickets not found
- 3 = API error (invalid link type, permission denied)
- 4 = Credentials missing

---

### List Operations

#### jira-list-tickets

**List Jira tickets with optional filters (project, status, assignee, type) or custom JQL.**

**Usage:**
```bash
jira-list-tickets [--project <key>] [--status <status>] [--assignee <email>] [--type <issue-type>] [--jql <custom-jql>]
```

**Examples:**
```bash
# List all INT project tickets (default if no filters)
jira-list-tickets

# List tickets by status and assignee
jira-list-tickets --status "In Progress" --assignee "rmurphy@fortressinfosec.com"

# List tasks in INT project
jira-list-tickets --project INT --type Task

# Use custom JQL query
jira-list-tickets --jql "project = INT AND status = 'In Progress' AND priority = High"

# Use in Bash tool
result = Bash(command='jira-list-tickets --status "In Progress"')
if result.returncode == 0:
    tickets_markdown = result.stdout
```

**Available filters:**
- `--project <key>` - Filter by project key (e.g., INT, AIM)
- `--status <status>` - Filter by status (e.g., "In Progress", "Done")
- `--assignee <email>` - Filter by assignee email
- `--type <type>` - Filter by issue type (e.g., Task, Bug, Story)
- `--jql <query>` - Use custom JQL query (overrides other filters)

**Output format:**
```markdown
📋 Jira Tickets (15 found):

## INT-3877: Add rate limiting
**Status:** In Progress
**Type:** Task
**Priority:** High
**Assignee:** John Doe
**Created:** 2025-10-20
**Updated:** 2025-10-27
**URL:** https://fortressinfosec.atlassian.net/browse/INT-3877
---

[... more tickets ...]

**JQL Query:** `project = "INT" AND status = "In Progress" ORDER BY updated DESC`
```

**Exit codes:**
- 0 = Success (tickets listed, even if 0 results)
- 1 = Invalid option or usage error
- 3 = API error (invalid JQL, permission denied)
- 4 = Credentials missing

**Note:** Results ordered by updated date (most recent first), limited to 50 tickets.

---

#### jira-list-sprint

**Show issues in the current active sprint for a board.**

**Usage:**
```bash
jira-list-sprint [board-id]
```

**Examples:**
```bash
# Use default board (from JIRA_DEFAULT_BOARD_ID in credentials)
jira-list-sprint

# Use specific board ID
jira-list-sprint 18

# Use in Bash tool
result = Bash(command='jira-list-sprint 18')
if result.returncode == 0:
    sprint_issues = result.stdout
```

**Output format:**
```markdown
🏃 Active Sprint: Sprint 42 (2025-10-14 to 2025-10-27)

## Sprint Tickets (12 found):

### INT-3877: Add rate limiting
**Status:** In Progress
**Type:** Task
**Assignee:** John Doe
**Story Points:** 5
---

[... more tickets ...]

**Summary:**
- In Progress: 5
- To Do: 4
- Done: 3

**Total Issues:** 12
**Sprint ID:** 456
**Board ID:** 18
```

**Exit codes:**
- 0 = Success (sprint issues listed, even if 0 results)
- 1 = Missing board ID and no default configured
- 3 = API error (board not found, permission denied)
- 4 = Credentials missing

**Note:** If no board-id provided, uses `JIRA_DEFAULT_BOARD_ID` from `.jira-credentials`. The INT board ID is 18.

---

## Integration Patterns

### Pattern 1: Fetch with Fallback (Recommended)

```python
# Try to fetch ticket, fall back gracefully if unavailable
result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")

if result.returncode == 0:
    ticket_content = result.stdout
    # Ticket available - use for requirements mapping
elif result.returncode == 4:
    # Credentials not configured
    echo("⚠️ Jira credentials not configured - skipping requirements check")
    ticket_content = None
else:
    # Ticket not found or other error
    ticket_content = None
```

**When:** PR review workflows where ticket context is optional

### Pattern 2: Required Ticket

```python
# Require ticket - fail if not available
result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")

if result.returncode != 0:
    echo(f"❌ Failed to fetch ticket {ticket}: {result.stderr}")
    exit(1)

ticket_content = result.stdout
# Process ticket requirements...
```

**When:** Ticket requirements are critical to workflow

### Pattern 3: Requirements Mapping

```python
# Fetch ticket and extract requirements for code review
result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")

if result.returncode == 0:
    ticket_content = result.stdout

    # Parse requirements sections
    requirements = extract_section(ticket_content, "## Description")
    acceptance_criteria = extract_section(ticket_content, "## Acceptance Criteria")

    # Use in review
    Task(investigator, f"""
    Verify code implements these requirements:

    {requirements}

    Acceptance Criteria:
    {acceptance_criteria}

    Check: Are all requirements implemented? Are acceptance criteria met?
    """)
```

**When:** Mapping ticket requirements to code changes

---

## Credentials Setup

**File:** `~/.claude/scripts/.jira-credentials`

**The script handles credentials automatically:**
- If file missing: Shows setup instructions and exits with code 4
- If file incomplete: Shows which vars are missing and exits with code 4
- File is gitignored (pattern: `scripts/*-credentials`)

**Credentials are set directly in file** (not sourced from environment):

```bash
ATLASSIAN_API_TOKEN="your-token-here"
ATLASSIAN_SITE_NAME="fortressinfosec"
ATLASSIAN_USER_EMAIL="your.email@fortressinfosec.com"
JIRA_DEFAULT_BOARD_ID="18"  # Optional: Default board for jira-list-sprint (INT board)
```

These match the Jira MCP credentials and use the same PAT token with Basic Auth.

**Note:** `JIRA_DEFAULT_BOARD_ID` is optional and used by `jira-list-sprint` when no board-id argument is provided.

---

## Error Handling

### Missing Credentials (Exit 4)

**Script output:**
```
❌ ATLASSIAN_API_TOKEN not set

❌ Jira credentials not found or incomplete.

STOP: This script requires Jira API credentials to be configured.

The script uses the same credentials as the Jira MCP. Make sure these
environment variables are set:
[Instructions...]
```

**Your action:** Stop execution, tell user credentials need configuration.

### Ticket Not Found (Exit 2)

**Script output:**
```
❌ Ticket not found: INT-9999
```

**Your action:** Ticket might be invalid, in different project, or inaccessible. Not critical for review workflows.

### API Error (Exit 3)

**Script output:**
```
❌ Jira API error (HTTP 401)
Error: Authentication failed
```

**Your action:** Credentials are wrong or expired. Tell user to check credentials file.

---

## Common Scenarios

### Scenario 1: PR Review with Requirements Check

```python
# Phase: Context Gathering

# Fetch ticket (optional - may not exist)
ticket_result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")
ticket_content = ticket_result.stdout if ticket_result.returncode == 0 else None

# Fetch MR comments (optional)
mr_result = Bash(command=f"~/.claude/scripts/gitlab-mr-comments {ticket}")
mr_comments = mr_result.stdout if mr_result.returncode == 0 else None

# Git analysis (always works)
git_diff = Bash(command="git diff origin/develop...HEAD")

# Review with available context
# If ticket_content exists, agents can map requirements
# If not, review focuses on code quality only
```

**Why:** Ticket and MR comments are optional context - review continues without them.

### Scenario 2: Requirements Coverage Report

```python
# Generate report mapping ticket requirements to code

ticket_result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")

if ticket_result.returncode == 0:
    ticket_content = ticket_result.stdout

    Task(investigator, f"""
    Create requirements coverage report.

    TICKET: {ticket_content}
    CODE CHANGES: [changed files list]

    For each requirement in ticket description or acceptance criteria:
    1. Is it implemented? (file:line)
    2. Is it tested? (test file:line)
    3. Any gaps?

    Return: Requirements coverage matrix
    """)
else:
    echo("⚠️ Ticket not found - skipping requirements coverage")
```

**Why:** Requirements mapping only makes sense if ticket is available.

### Scenario 3: Extract Acceptance Criteria

```python
# Parse acceptance criteria for checklist

ticket_result = Bash(command=f"~/.claude/scripts/jira-get-issue {ticket}")

if ticket_result.returncode == 0:
    # Extract acceptance criteria section
    if "## Acceptance Criteria" in ticket_result.stdout:
        criteria_section = extract_between(
            ticket_result.stdout,
            "## Acceptance Criteria",
            "## Related Issues"
        )

        # Convert to checklist for verification
        checklist = parse_criteria_to_checklist(criteria_section)
    else:
        checklist = []
```

**Why:** Structured parsing of ticket data for automated verification.

---

## Comparison: Script vs MCP

| Aspect | Jira MCP | jira-scripts |
|--------|----------|--------------|
| **Functions** | ~30 | 1 |
| **Token Cost** | ~40,000 | ~250 |
| **Setup** | MCP server config | One credentials file |
| **Maintenance** | Auto-generated, external | One bash script, local |
| **Customization** | None (auto-generated) | Full control over output |
| **Performance** | Slower (tool loading) | Faster (direct curl) |

**Token savings:** 39,750 tokens per conversation (99.4%)

---

## Quick Reference

| Operation | Script | Usage Example |
|-----------|--------|---------------|
| **Fetch ticket** | `jira-get-issue` | `jira-get-issue INT-3877` |
| **Create ticket** | `jira-create-ticket` | `jira-create-ticket INT Task "Summary" "Description"` |
| **Add comment** | `jira-comment-ticket` | `jira-comment-ticket INT-3877 "Comment text"` |
| **Update ticket** | `jira-update-ticket` | `jira-update-ticket INT-3877 --status "In Progress"` |
| **Log work** | `jira-log-work` | `jira-log-work INT-3877 "2h 30m" "Work description"` |
| **Link tickets** | `jira-link-tickets` | `jira-link-tickets INT-3877 "Blocks" INT-3878` |
| **List tickets** | `jira-list-tickets` | `jira-list-tickets --status "In Progress"` |
| **List sprint** | `jira-list-sprint` | `jira-list-sprint 18` |

**Check exit codes:**
```python
result = Bash(command="jira-get-issue INT-3877")
if result.returncode == 0:
    # Success - use result.stdout
elif result.returncode == 4:
    # Credentials missing - tell user to configure
elif result.returncode == 2:
    # Ticket/resource not found
else:
    # API error (3) or usage error (1)
```

**Credentials file location:**
```
~/.claude/scripts/.jira-credentials
```

**Common exit codes:**
- 0 = Success
- 1 = Usage error (missing/invalid arguments)
- 2 = Not found (ticket, project, board)
- 3 = API error (auth failed, permission denied, invalid operation)
- 4 = Credentials missing/incomplete

---

## When NOT to Use Scripts

**Use Jira MCP instead when:**
- Need **bulk operations** (updating 50+ tickets at once)
- Need **advanced JQL queries** with complex aggregations
- Need **custom field manipulation** beyond standard fields
- Need **attachment management** (upload/download files)
- Need **webhook/automation management**
- Need >10 different specialized Jira operations in one workflow

**Scripts now cover most common operations:** Read (get-issue), Write (create-ticket, comment-ticket, update-ticket, log-work, link-tickets), and List (list-tickets, list-sprint) operations are all supported.

---

## Summary

**What:** Lightweight bash scripts replace heavy Jira MCP for common operations
**When:** Fetching ticket details, creating tickets, commenting, updating, logging work, linking tickets, listing tickets/sprints
**Why:** 99.4% token savings (40k → 250)
**How:** Use Bash tool to call appropriate jira-* script

**Available scripts:**
- **Read:** `jira-get-issue` (fetch ticket details)
- **Write:** `jira-create-ticket`, `jira-comment-ticket`, `jira-update-ticket`, `jira-log-work`, `jira-link-tickets`
- **List:** `jira-list-tickets`, `jira-list-sprint`

**Remember:** Scripts are optional tools. If credentials aren't configured, workflows continue without Jira context. Don't block on missing optional data.
