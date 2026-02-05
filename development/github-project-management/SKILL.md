---
name: github-project-management
description: Guide for using GitHub Projects V2 with teams, status fields, and modern workflows. Use when setting up projects, explaining workflow, onboarding team members, or troubleshooting GitHub Projects. Covers teams (@developers, @product, @qa, @client), Status field with Blocked state, Priority/Type fields, epics, sub-issues, and label cleanup strategies.
---

# GitHub Project Management - Modern Team Workflow Guide

## Purpose
This skill teaches Claude how ChinchillaEnterprises uses GitHub Projects V2 for modern team collaboration in the AI era. It documents the philosophy, team structure, workflow patterns, and GitHub features used to manage projects efficiently.

**Key Philosophy:** In the AI era, development speed isn't the bottleneck—business alignment is. Our workflow reflects this reality.

## Activation
Use this skill when:
- Setting up a new GitHub Project
- Onboarding team members to project management workflow
- Explaining how we use GitHub Projects, Teams, Status fields, and automation
- Troubleshooting project management issues
- A future Claude instance needs context on our project structure

Example:
"Use your github-project-management skill to explain our workflow"

## Core Philosophy: The New Bottleneck

### Old World (Pre-AI)
- **Bottleneck:** Developer typing speed, technical knowledge
- **Focus:** How fast can we write code?
- **Constraint:** Engineering capacity

### New World (With AI)
- **Bottleneck:** Business decisions, client feedback, requirements clarity
- **Focus:** What do we actually need to build?
- **Constraint:** Alignment and communication

**Result:** Our workflow prioritizes visibility into WHO is blocking work, not just WHAT needs to be done.

---

## Team Structure

We use **GitHub Teams** to assign ownership and accountability:

### @ChinchillaEnterprises/developers
- **Members:** Abel (feathars91), Soroush (SOROUSH911)
- **Responsibility:** Implementation, coding, technical decisions
- **Use:** Assign development work to this team

### @ChinchillaEnterprises/product
- **Members:** Jamie (jamie805)
- **Responsibility:** Product management, client liaison, requirements gathering
- **Use:** Assign issues needing client decisions or product direction
- **Context:** Jamie shields developers from meetings so they can code

### @ChinchillaEnterprises/qa
- **Members:** Hailee (hailee-landin)
- **Responsibility:** Quality assurance, testing, bug verification
- **Use:** Assign issues in "In Review" status that need testing

### @ChinchillaEnterprises/client
- **Members:** Marta (Martagaiabras), Dean (dean5757)
- **Responsibility:** External client/Databricks coordination
- **Use:** Assign issues blocked by external decisions or Databricks team

---

## GitHub Projects V2 Setup

### Project Fields We Use

#### 1. **Status** (Single Select - Built-in GitHub field)
**Purpose:** Track where issues are in the workflow

**Options (in order):**
1. **Backlog** - Not started, being triaged
2. **Ready** - Approved and ready to begin work
3. **In Progress** - Active development
4. **Blocked** - Waiting on external input (THE CRITICAL STATUS)
5. **In Review** - Code review or testing phase
6. **Done** - Completed and shipped

**Why "Blocked" is critical:**
- Makes invisible blockers visible
- Shows WHO needs to take action (via Assignees)
- Prevents issues from sitting in "In Progress" for weeks
- Client can see their action items at a glance

#### 2. **Priority** (Single Select - Custom field)
**Purpose:** Indicate urgency and importance

**Options:**
- **Critical** (Red) - Production issues, blocking customers
- **High** (Orange) - Important for MVP/current sprint
- **Medium** (Yellow) - Nice to have for current milestone
- **Low** (Green) - Future improvements, backlog items

**Migration note:** We moved from `priority:critical` labels to this field. Labels were redundant.

#### 3. **Type** (Built-in GitHub issue type field)
**Purpose:** Categorize the nature of work

**Options (GitHub default):**
- **Task** - Regular work item
- **Bug** - Something broken
- **Feature** - New functionality
- **Epic** - Large work item with sub-issues

**Migration note:** Replaced `type:feature` label with this built-in field.

#### 4. **Size** (Single Select - Custom field)
**Purpose:** T-shirt sizing for effort estimation

**Options:**
- **XS** - < 1 hour
- **S** - 1-3 hours
- **M** - Half day to 1 day
- **L** - 2-3 days
- **XL** - 1+ week

#### 5. **Parent Issue** (Built-in GitHub field)
**Purpose:** Link sub-issues to parent epics

**How it works:**
- Create parent issue with task list (checkboxes)
- Hover over task items and click issue icon to convert to sub-issue
- Parent shows "Sub-issues progress: 3/5 (60%)" automatically

#### 6. **Sub-issues Progress** (Built-in GitHub field)
**Purpose:** Auto-calculates completion of child issues

**How it works:**
- Automatically updates when sub-issues are closed
- Shows visual progress bar in project view
- No manual updates needed

---

## Labels: Minimalist Approach

**Philosophy:** Use GitHub's built-in features (Status, Priority, Type fields) instead of labels.

### Labels We KEEP (GitHub Defaults Only)
- `bug` - Something isn't working
- `documentation` - Documentation improvements
- `duplicate` - Duplicate issue
- `enhancement` - New feature request
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `invalid` - Invalid issue
- `question` - Question, not a task
- `wontfix` - Will not be worked on

### Labels We DELETED (Redundant)
- ❌ `priority:*` labels → Use **Priority field** instead
- ❌ `status:*` labels → Use **Status field** instead
- ❌ `type:*` labels → Use **Type field** instead
- ❌ `team:*` labels → Use **GitHub Teams + Assignees** instead
- ❌ `blocked:*` labels → Use **Status: Blocked + Assignees** instead

**Result:** From 25 labels down to 9 (64% reduction!)

---

## Workflow Patterns

### Pattern 1: New Feature Request

```
1. Issue created → Status: Backlog
2. Team reviews → Set Priority (Critical/High/Medium/Low)
3. Team approves → Status: Ready
4. Dev picks it up → Status: In Progress, Assign to @developers
5. Blocked? → Status: Blocked, Assign to blocker (e.g., @product)
6. Unblocked → Status: In Progress, Assign back to @developers
7. Code complete → Status: In Review, Assign to @qa
8. Testing done → Status: Done (auto-closes issue via workflow)
```

### Pattern 2: Bug Report

```
1. Bug reported → Type: Bug, Priority: Critical/High
2. Dev investigates → Status: In Progress, Assign to @developers
3. Needs client data → Status: Blocked, Assign to @client
4. Data provided → Status: In Progress, Assign to @developers
5. Fix ready → Status: In Review, Assign to @qa
6. QA verified → Status: Done
```

### Pattern 3: Epic with Sub-issues

```
1. Create parent issue (the epic)
2. Add task list in description:
   - [ ] Sub-task 1
   - [ ] Sub-task 2
   - [ ] Sub-task 3
3. Hover over tasks, click issue icon to convert to sub-issues
4. Work on sub-issues normally
5. Parent issue auto-tracks: "Sub-issues progress: 2/3 (67%)"
6. When all sub-issues done → Epic done
```

### Pattern 4: Client-Blocked Issue

```
Old way (labels):
- Add label: blocked:client
- No notification sent
- Have to manually ping Marta

New way (teams + status):
1. Status: Blocked
2. Assign to: @ChinchillaEnterprises/client
3. Marta gets automatic notification
4. She sees it on project board immediately
5. Clear accountability
```

---

## GitHub Workflows (Automation)

### Enabled Workflows

1. **Auto-add sub-issues to project** - Sub-issues automatically join project
2. **Auto-add to project** - New issues/PRs automatically added
3. **Auto-close issue** - When Status → Done, issue closes
4. **Item added to project** - Can set default status for new items
5. **Item closed** - When issue closes → Status: Done
6. **Pull request linked to issue** - Auto-links PR to issue
7. **Pull request merged** - When PR merges → Status: Done

### How Auto-Close Works

```
Developer marks issue Status: Done
    ↓
Workflow triggers
    ↓
Issue automatically closed
    ↓
Clean board, no manual cleanup
```

---

## Best Practices

### 1. Use Teams, Not Labels
**❌ Don't:**
```
Issue #123
Labels: team:developers, blocked:client
```

**✅ Do:**
```
Issue #123
Status: Blocked
Assignees: @ChinchillaEnterprises/client
```

**Why:** Teams trigger notifications, labels don't.

### 2. Always Set Status When Assigning

**❌ Don't:**
```
Assign to: @developers
(Status still shows "Ready")
```

**✅ Do:**
```
Assign to: @developers
Status: In Progress
```

**Why:** Status and Assignees should always match the reality.

### 3. Use Blocked Status Liberally

**❌ Don't:**
```
Issue sits in "In Progress" for 2 weeks
Dev comments: "Waiting on Marta"
No one notices
```

**✅ Do:**
```
Status: Blocked
Assign to: @ChinchillaEnterprises/product
Comment: "Need client decision on X"
```

**Why:** Makes blockers visible to everyone.

### 4. Assign to WHO Can Unblock

**Blocked by Databricks team:**
```
Status: Blocked
Assign to: @ChinchillaEnterprises/client
(Marta coordinates with Databricks)
```

**Blocked by product decision:**
```
Status: Blocked
Assign to: @ChinchillaEnterprises/product
(Jamie gets client input)
```

**Blocked by testing:**
```
Status: In Review
Assign to: @ChinchillaEnterprises/qa
(Hailee tests and verifies)
```

---

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Label Soup
Using 20+ labels to track everything → Use fields and teams instead

### ❌ Anti-Pattern 2: Hidden Blockers
Issue stuck in "In Progress" with no visibility → Use "Blocked" status

### ❌ Anti-Pattern 3: Manual Tracking
Spreadsheets to track who owns what → Use GitHub Teams + Assignees

### ❌ Anti-Pattern 4: Stale Issues
Issues never close, accumulate over time → Use auto-close workflow

### ❌ Anti-Pattern 5: @mention Spam
Constantly @mentioning people in comments → Assign to teams instead

---

## Quick Reference: GitHub CLI Commands

### Working with GitHub Projects V2

#### Get Project Number
```bash
# List all projects for an org
gh project list --owner ChinchillaEnterprises --format json | jq '.projects[] | {number, title}'

# Output example:
# {
#   "number": 4,
#   "title": "BeonIQ Product"
# }
```

#### List Project Fields
```bash
gh project field-list 4 --owner ChinchillaEnterprises --format json
```

#### Update Issue with Project Fields (GraphQL)

**IMPORTANT:** GitHub CLI's `gh issue edit` does NOT support setting Project fields (Status, Priority, etc.). You MUST use GraphQL API.

**Step 1: Get the Project Item ID**
```bash
# Query to get project item ID for an issue
gh api graphql -f query='
query {
  organization(login: "ChinchillaEnterprises") {
    projectV2(number: 4) {
      id
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              number
            }
          }
        }
      }
    }
  }
}'

# Find the item ID for your issue number in the response
```

**Step 2: Get Field IDs**
```bash
# Get all field IDs and their option IDs
gh api graphql -f query='
query {
  organization(login: "ChinchillaEnterprises") {
    projectV2(number: 4) {
      id
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}'

# Example output:
# {
#   "id": "PVTSSF_lADOBcY...",
#   "name": "Status",
#   "options": [
#     {"id": "47fc9ee4", "name": "Backlog"},
#     {"id": "f75ad846", "name": "In Progress"},
#     ...
#   ]
# }
```

**Step 3: Update the Field Value**
```bash
# Set Status to "In Progress"
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PVT_kwDOBcY..."
      itemId: "PVTI_lADOBcY..."
      fieldId: "PVTSSF_lADOBcY..."
      value: {
        singleSelectOptionId: "f75ad846"
      }
    }
  ) {
    projectV2Item {
      id
    }
  }
}'
```

**Full Working Example:**
```bash
# Update issue #99 to Status: "In Progress" and Priority: "High"

# 1. Get project ID
PROJECT_ID=$(gh api graphql -f query='
query {
  organization(login: "ChinchillaEnterprises") {
    projectV2(number: 4) { id }
  }
}' --jq '.data.organization.projectV2.id')

# 2. Get item ID for issue #99
ITEM_ID=$(gh api graphql -f query='
query {
  organization(login: "ChinchillaEnterprises") {
    projectV2(number: 4) {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              number
            }
          }
        }
      }
    }
  }
}' --jq '.data.organization.projectV2.items.nodes[] | select(.content.number == 99) | .id')

# 3. Get Status field ID and "In Progress" option ID
STATUS_FIELD_ID=$(gh api graphql -f query='
query {
  organization(login: "ChinchillaEnterprises") {
    projectV2(number: 4) {
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options { id name }
          }
        }
      }
    }
  }
}' --jq '.data.organization.projectV2.fields.nodes[] | select(.name == "Status") | .id')

IN_PROGRESS_ID=$(gh api graphql -f query='...' --jq '.data.organization.projectV2.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "In Progress") | .id')

# 4. Update the status
gh api graphql -f query="
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: \"$PROJECT_ID\"
      itemId: \"$ITEM_ID\"
      fieldId: \"$STATUS_FIELD_ID\"
      value: { singleSelectOptionId: \"$IN_PROGRESS_ID\" }
    }
  ) {
    projectV2Item { id }
  }
}"
```

**Why This Is Necessary:**

GitHub Projects V2 fields are NOT part of the issue itself - they're metadata on the PROJECT ITEM. When you do `gh issue edit 99 --add-field Status="In Progress"`, GitHub CLI doesn't know what project you're talking about or what the field IDs are.

**Key Concepts:**
- **Issue** = The GitHub issue (#99)
- **Project Item** = The representation of that issue in the project board
- **Project Fields** = Custom fields (Status, Priority, etc.) that exist on the PROJECT, not the issue

### Working with Teams

#### List Team Members
```bash
gh api orgs/ChinchillaEnterprises/teams/developers/members --jq '.[] | .login'
```

#### Create Team
```bash
gh api orgs/ChinchillaEnterprises/teams \
  -f name="team-name" \
  -f description="Team description" \
  -f privacy="closed"
```

#### Add Member to Team
```bash
gh api -X PUT orgs/ChinchillaEnterprises/teams/team-name/memberships/username
```

### Working with Issues

#### List All Labels
```bash
gh label list --repo ChinchillaEnterprises/transportation-insight
```

#### Delete Redundant Labels
```bash
gh label delete "priority:critical" --repo ChinchillaEnterprises/transportation-insight --yes
```

#### Add Issue to Milestone
```bash
gh issue edit 99 --milestone "Demo Ready - Nov 21"
```

#### Assign Users to Issue
```bash
# Assign individual users
gh issue edit 99 --add-assignee feathars91 --add-assignee SOROUSH911

# Note: Cannot assign teams directly via CLI, only individual users
```

---

## Project-Specific Details

### BeonIQ MVP Project
- **Project URL:** https://github.com/orgs/ChinchillaEnterprises/projects/4
- **Repository:** ChinchillaEnterprises/transportation-insight
- **Current Items:** 37 issues
- **Custom Fields:** 15 fields
- **Team Size:** 6 people across 4 teams

### Status Distribution (Example)
- Backlog: 26 issues
- Ready: 11 issues
- In Progress: 0 issues
- Blocked: 0 issues
- In Review: 0 issues
- Done: 2 issues

---

## Migration History

### What We Changed (January 2025)

**Before:**
- 25 labels mixing priority, status, team, type
- No GitHub Teams
- Manual @mentions for notifications
- No "Blocked" status
- Hidden blockers

**After:**
- 9 labels (GitHub defaults only)
- 4 GitHub Teams with clear roles
- Automatic notifications via team assignments
- "Blocked" status for visibility
- Clear accountability

**Impact:**
- 64% reduction in labels
- Faster issue triage
- Better visibility into blockers
- Clear ownership via teams

---

## Troubleshooting

### "I can't add Blocked status via CLI"
**Solution:** GitHub API doesn't support adding single-select options to existing fields. Add manually via web UI:
1. Go to Project Settings
2. Click Status field
3. Add option "Blocked"
4. Choose yellow/red color
5. Drag to position after "In Progress"

### "Team notifications not working"
**Check:**
1. User is actually in the team (`gh api orgs/ORG/teams/TEAM/members`)
2. Issue is assigned to `@ORG/team`, not individual user
3. User has notifications enabled in GitHub settings

### "Workflows not triggering"
**Check:**
1. Go to Project → Workflows menu
2. Verify workflows are enabled
3. Check that Status field values match workflow triggers exactly

### "Too many labels, confused about what to use"
**Solution:** Delete all custom labels, use fields and teams:
- Priority → Use Priority field
- Status → Use Status field
- Type → Use Type field
- Team/Owner → Use GitHub Teams + Assignees

---

## Success Criteria

When using this workflow, you should:

✅ Use Status field to track progress (not labels)
✅ Use Priority field to indicate urgency (not labels)
✅ Use Type field to categorize issues (not labels)
✅ Assign to GitHub Teams (not individual users by default)
✅ Use "Blocked" status to make blockers visible
✅ Assign blocked issues to whoever can unblock them
✅ Keep label count minimal (< 10 labels)
✅ Let workflows auto-close issues
✅ Use sub-issues for epics
✅ Track progress via project board, not spreadsheets

---

## Future Enhancements to Consider

### Potential Additions
- **Sprint field** - Track which sprint/cycle work belongs to
- **Customer field** - Tag issues by customer (e.g., Marta, KGPCO, Milbank)
- **Iteration field** - For teams using 2-week iterations
- **Custom automation** - GitHub Actions for Slack notifications on blocked items

### Questions to Ask Before Adding
1. Does this replace a label? (Good!)
2. Does this duplicate existing functionality? (Bad!)
3. Will this help visibility or add noise? (Visibility = Good)
4. Can we use a built-in GitHub feature instead? (Prefer built-in)

---

## Remember

**The goal isn't more features—it's clarity and speed.**

In the AI era:
- Code is fast to write
- Decisions are slow to make
- Visibility into blockers is critical
- Clear ownership prevents delays

Our workflow optimizes for **communication and alignment**, not just task tracking.

---

**When in doubt:** Keep it simple, use built-in features, assign to teams, make blockers visible.
