---
name: linear-agent
description: Intelligent, conversational interface for managing Linear workspace operations (issues, projects, teams, reporting)
allowed-tools: "*"
---

# Linear Agent Skill

## Purpose

Intelligent, conversational interface for managing Linear workspace operations. This skill provides comprehensive issue management, project planning, team coordination, and reporting capabilities through natural language interaction.

**Core Capabilities:**
- **Issue Management**: Create, retrieve, update, and search issues with smart defaults
- **Project Planning**: Bulk operations for epics, milestones, and feature sets
- **Team Coordination**: Assign work, track progress, manage workloads
- **Reporting**: Generate team summaries, sprint reports, and activity metrics
- **Templates**: Pre-configured patterns for bugs, features, and tasks

## Architecture

This skill wraps the MCP Linear tools and provides helper utilities that add:
- Retry logic and error handling
- Smart defaults and validation
- Template-based issue creation
- Batch operations
- Natural language → Linear API translation

**⚡ OPTIMIZED: All helper scripts have been upgraded for reliability and clarity!**
See `helpers/README.md` for detailed documentation and examples.

**Helper Scripts:**
- `linear_client.py`: Unified API client with retry logic ✅ **Fixed auth header**
- `query_issues.py`: Advanced querying and filtering ✅ **Simplified & reliable**
- `get_issue.py`: Retrieve specific issue by identifier ✅ **NEW**
- `update_issue.py`: Issue updates with validation ✅ **State lookup + comments**
- `create_issue.py`: Template-based issue creation
- `bulk_operations.py`: Batch create/update operations
- `reporting.py`: Team and sprint reports
- `test_api.py`: API connectivity testing ✅ **NEW**

**Templates:**
- `bug_report.yaml`: Bug issue template
- `feature_request.yaml`: Feature request template
- `task.yaml`: Generic task template

## Workflows

### Workflow 1: Create Issue

**Trigger**: User wants to create a new Linear issue

**Steps:**

1. **Understand Requirements**
   - Extract issue details from user's natural language request
   - Identify: title, description, type (bug/feature/task), priority, labels
   - Ask clarifying questions if needed

2. **Select Team**
   - If team not specified, list available teams using `linear_client.py`
   - Ask user to select team or infer from context

3. **Choose Template (Optional)**
   - For bugs: Use `bug_report.yaml` template
   - For features: Use `feature_request.yaml` template
   - For tasks: Use `task.yaml` template
   - For simple issues: Skip template

4. **Populate Fields**
   - If using template, gather template variables
   - Apply smart defaults:
     - Priority: 3 (Normal) unless specified
     - Labels: Infer from issue type and content
     - Estimate: Leave empty unless specified

5. **Create Issue**
   - Use `helpers/create_issue.py` with gathered information
   - Example:
     ```bash
     python helpers/create_issue.py \
       --team "Backend Team" \
       --title "Fix authentication timeout" \
       --description "Users report 30s timeout on login" \
       --labels "bug,p1" \
       --priority 2 \
       --verbose
     ```

6. **Return Results**
   - Show created issue ID, title, and URL
   - Confirm status and next steps

**Example Interaction:**
```
User: "Create a bug issue for authentication timeout in the backend team"
Skill: "I'll create a bug issue for the Backend Team. Let me gather some details:
  - What steps reproduce the issue?
  - What's the expected vs actual behavior?
  - What environment (OS, version)?"
User: "Login page → 30s timeout. Should login in <3s. Chrome on Mac."
Skill: *Creates issue using bug template with details*
Result: "✅ Created ISS-456: [BUG] Authentication timeout - https://linear.app/..."
```

---

### Workflow 2: Query & Retrieve Issues

**Trigger**: User wants to find or list issues with specific criteria

**Steps:**

1. **Parse Query**
   - Extract filters: team, state, assignee, priority, labels, keywords
   - Identify search mode: list all, filter by criteria, search by keyword

2. **Execute Query**
   - Use `helpers/query_issues.py` with parsed filters
   - Example:
     ```bash
     python helpers/query_issues.py \
       --team "Backend Team" \
       --state "In Progress" \
       --labels "bug" \
       --verbose
     ```

3. **Format Results**
   - For small result sets (<10): Show full details
   - For larger sets: Show summary table with ID, title, state, priority
   - Offer to export as CSV/JSON if many results

4. **Follow-up Actions**
   - Ask if user wants to update any of the found issues
   - Offer to generate report from results

**Example Interaction:**
```
User: "Show me all in-progress bugs for the backend team"
Skill: *Executes query with filters*
Result: "Found 8 in-progress bugs:
  ISS-123: Login timeout
  ISS-124: API rate limit error
  ...
  Would you like to update any of these?"
```

---

### Workflow 3: Update Issue

**Trigger**: User wants to modify an existing issue

**Steps:**

1. **Identify Issue**
   - Get issue ID from user (e.g., "ISS-123")
   - OR find issue by title/description if ID not provided

2. **Fetch Current State**
   - Retrieve current issue using `linear_client.py`
   - Show current values for fields being updated

3. **Determine Updates**
   - Extract fields to update from user request
   - Supported: title, description, priority, state, assignee, labels, estimate

4. **Apply Updates**
   - Use `helpers/update_issue.py` with changes
   - Example:
     ```bash
     python helpers/update_issue.py \
       --issue-id ISS-123 \
       --state "In Progress" \
       --assignee "user_abc123" \
       --comment "Starting work on this" \
       --verbose
     ```

5. **Confirm Changes**
   - Show before/after snapshot
   - Display updated issue URL

**Example Interaction:**
```
User: "Move ISS-123 to In Progress and assign to me"
Skill: *Fetches current state, applies updates*
Result: "✅ Updated ISS-123:
  State: Backlog → In Progress
  Assignee: Unassigned → John Doe
  Added comment explaining changes"
```

---

### Workflow 4: Bulk Operations

**Trigger**: User wants to create/update multiple issues at once

**Steps:**

1. **Understand Scope**
   - Determine operation type: create or update
   - Identify source: YAML file, CSV, or manual list

2. **Prepare Batch File** (if needed)
   - If user provides data directly, create temporary batch file
   - Format:
     ```yaml
     team: "Backend Team"
     issues:
       - title: "Issue 1"
         description: "Description 1"
         labels: ["bug", "p1"]
       - title: "Issue 2"
         priority: 2
     ```

3. **Validate Batch**
   - Check all required fields present
   - Warn about missing optional fields
   - Confirm with user before executing

4. **Execute Batch**
   - Use `helpers/bulk_operations.py`
   - Show progress for each issue
   - Example:
     ```bash
     python helpers/bulk_operations.py \
       --action create \
       --input batch.yaml \
       --verbose
     ```

5. **Report Results**
   - Summary: X/Y issues created/updated successfully
   - List any failures with error messages
   - Offer to save results to file

**Example Interaction:**
```
User: "Create issues from roadmap.yaml"
Skill: *Loads file, validates, executes batch*
Result: "✅ Created 25/25 issues successfully:
  - 10 features
  - 8 tasks
  - 7 bugs
  All issues added to Q1 Roadmap project"
```

---

### Workflow 5: Generate Report

**Trigger**: User wants team/sprint metrics or status summary

**Steps:**

1. **Determine Report Type**
   - **Team Summary**: Overall team metrics (by state, priority, assignee)
   - **Sprint Report**: Activity over time period (created, completed, velocity)

2. **Set Parameters**
   - Team name
   - Time period (for sprint reports)
   - Output format (markdown or JSON)

3. **Generate Report**
   - Use `helpers/reporting.py`
   - Example:
     ```bash
     python helpers/reporting.py \
       --team "Backend Team" \
       --report sprint \
       --period 7 \
       --format markdown
     ```

4. **Format Output**
   - Display report in readable format
   - Highlight key metrics
   - Offer to save to file

**Example Interaction:**
```
User: "Show me the backend team's sprint summary for the last week"
Skill: *Generates sprint report*
Result: "# Sprint Report: Backend Team

Period: Last 7 days

Activity:
- Issues Created: 12
- Issues Completed: 8
- Velocity: 8 issues/week

By State:
- In Progress: 15
- Done: 42
- Backlog: 23

Would you like me to save this report?"
```

---

## Helper Script Usage

### Create Issue
```bash
cd /home/user/writing_ecosystem/.claude/skills/linear-agent

# Simple issue
python helpers/create_issue.py \
  --team "Backend Team" \
  --title "Add rate limiting"

# With template
python helpers/create_issue.py \
  --team "Backend" \
  --template bug_report \
  --var short_description="Login timeout" \
  --var detailed_description="Users report 30s timeout" \
  --var expected="Login within 3s" \
  --var actual="30s timeout"
```

### Update Issue
```bash
# Change status
python helpers/update_issue.py \
  --issue-id ISS-123 \
  --state "In Progress" \
  --comment "Starting work"

# Update multiple fields
python helpers/update_issue.py \
  --issue-id ISS-124 \
  --priority 1 \
  --assignee "user_xyz" \
  --labels "urgent,bug"
```

### Query Issues
```bash
# Filter by team and state
python helpers/query_issues.py \
  --team "Backend Team" \
  --state "In Progress"

# Search by keyword
python helpers/query_issues.py \
  --search "authentication" \
  --limit 20

# Export to CSV
python helpers/query_issues.py \
  --team "Backend" \
  --output issues.csv \
  --format csv
```

### Bulk Operations
```bash
# Create from YAML
python helpers/bulk_operations.py \
  --action create \
  --input batch.yaml

# Update from JSON
python helpers/bulk_operations.py \
  --action update \
  --input updates.json
```

### Reporting
```bash
# Team summary
python helpers/reporting.py \
  --team "Backend Team" \
  --report summary

# Sprint report
python helpers/reporting.py \
  --team "Backend" \
  --report sprint \
  --period 7 \
  --output sprint_report.md
```

---

## Environment Setup

**Required Environment Variables:**
```bash
LINEAR_API_KEY=lin_api_...  # Your Linear API key
```

**Optional:**
```bash
LINEAR_WORKSPACE_ID=...     # Default workspace (if multiple)
```

**Get API Key:**
1. Go to Linear Settings → API
2. Create new personal API key
3. Set as environment variable

---

## Templates

### Bug Report Template Variables
- `short_description`: Brief bug summary
- `detailed_description`: Detailed explanation
- `steps`: Steps to reproduce
- `expected`: Expected behavior
- `actual`: Actual behavior
- `os`: Operating system
- `version`: Software version

### Feature Request Template Variables
- `short_description`: Brief feature summary
- `problem`: Problem statement
- `solution`: Proposed solution
- `alternatives`: Alternative approaches
- `success_criteria`: Definition of done

### Task Template Variables
- `short_description`: Task title
- `detailed_description`: Task details
- `acceptance_criteria`: Completion criteria

---

## Best Practices

### Creating Issues
1. **Use templates** for bugs and features (ensures consistency)
2. **Set priority** based on urgency and impact
3. **Add labels** for categorization and filtering
4. **Include estimates** to track effort
5. **Assign to team members** with capacity

### Updating Issues
1. **Add comments** when making significant changes
2. **Validate state transitions** (don't skip states)
3. **Update estimates** as work progresses
4. **Keep descriptions current** with new information

### Bulk Operations
1. **Validate batch files** before executing
2. **Use dry-run mode** for large batches
3. **Monitor progress** during execution
4. **Save results** for audit trail

### Reporting
1. **Generate weekly sprint reports** for team visibility
2. **Track velocity trends** over time
3. **Monitor workload distribution** to prevent burnout
4. **Review label usage** to ensure proper categorization

---

## Troubleshooting

### "Team not found"
- Verify team name matches exactly (case-sensitive)
- List all teams: `python helpers/linear_client.py`

### "Label not found"
- Check label exists for that team
- List labels: Use Linear client to query labels

### "Rate limit exceeded"
- Client automatically throttles at 1400 requests/hour
- Wait for rate limit window to reset
- Consider batching operations

### Authentication errors
- Verify LINEAR_API_KEY is set correctly
- Check API key hasn't expired
- Ensure key has necessary permissions

---

## Reference Documentation

See `reference/` directory for:
- `linear_api_schema.md`: GraphQL schema reference
- `field_mappings.md`: Field mapping guide

See `learnings/` directory for:
- `pitfalls.md`: Common mistakes and how to avoid them