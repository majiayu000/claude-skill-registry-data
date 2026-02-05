---
name: linear-issue-handler
description: Comprehensive workflow for managing Linear issues using the linearis CLI tool. Handles issue creation, status tracking, commenting, and file downloads with clear decision trees for when to ask for approval vs. acting autonomously.
---

# Linear Issue Handler Skill

## Overview

This skill provides a comprehensive workflow for managing Linear issues using the `linearis` CLI tool. It handles issue creation, status tracking, commenting, and file downloads with clear decision trees based on your preferences.

---

## Foundation

### Tools & Access
- **Primary Tool:** `linearis` CLI (accessed via Bash)
- **Authentication:** Uses `~/.linear_api_token` file
- **Reference Format:** Issues use format `ABC-<number>` (e.g., `RDS-2455`)

### Key Principle
Linear is the single source of truth for project management. All significant work should be reflected in the appropriate issue.

---

## Decision Trees & Your Preferences

### 1. Updating Issue Descriptions

**When to Update Directly (No Ask Needed):**
- ✅ Changing task checkbox status (e.g., `- [ ]` → `- [x]`)
- ✅ Updating status indicators (Pending → In Progress)
- ✅ Adding timestamps or minor factual updates
- ✅ Correcting obvious typos

**When to Ask First (Before Updating):**
- ❓ Rewriting section content or descriptions
- ❓ Reorganizing the issue structure
- ❓ Changing requirements or acceptance criteria
- ❓ Removing or significantly altering original intent

### 2. Reading Issue State Before Work

**Always Read the Issue When:**
- Starting work on a specific ticket you were assigned
- Picking up a ticket for the first time
- Unclear context from user instructions

**Don't Need to Read When:**
- User is giving you a direct, clear task ("Fix the bug in X file")
- Working on code without ticket reference
- Issue is just for documentation purposes

**Example:**
```
User: "Work on RDS-2455"
You: Read the issue first to understand current state, dependencies, blockers
```

### 3. Creating New Issues

**Ask User First (Context-Dependent) For:**
- Complex features or major changes
- Issues that might affect multiple teams
- Anything where project assignment is unclear
- Issues blocking other work

**Create Directly For:**
- Minor bugs discovered during work
- Small follow-up tasks clearly related to current work
- Documentation issues
- Obvious technical debt or code cleanup
- Use the parent ticket's project when creating sub-issues

**Example - Ask First:**
```
You: "This work requires architectural changes. Should I create an issue, or
would this be better handled in planning? Would you like this in PROJECT-X
or a different project?"
```

**Example - Create Directly:**
```
You: "I noticed a typo in the error message. Creating RDS-2500 as a follow-up."
User: (Reviews the new issue you created)
```

### 4. Updating Issue State

**Always Ask Before:**
- Changing state to "In Progress"
- Changing state to "Done" or marking complete
- Changing state to "Cancelled" or "Blocked"
- Any state change that affects others' work visibility

**Why Ask:** State changes affect workflow visibility for your team. Getting explicit approval prevents surprises.

**Example:**
```
You: "I've completed the work for RDS-2455. Should I mark it as 'Done',
or would you prefer to do that?"
User: "Yes, mark it done."
You: Updates state via linearis
```

---

## Common Workflows

### Workflow 1: Starting Work on an Assigned Issue

```bash
# You're told: "Work on RDS-2455"

# Step 1: Read the issue
linearis issues read RDS-2455

# Step 2: Review current state, check for embeds (screenshots, docs)
# If embeds present:
linearis embeds download

# Step 3: Check for blockers, dependencies, or sub-tasks
# Verify nothing has changed since assignment

# Step 4: Begin work, understanding full context
# -> This is especially important if you haven't seen the ticket before
```

### Workflow 2: Reporting Progress During Work

**For small progress updates (no decision needed):**
```bash
# You're actively working, making progress on a task
# Add a comment to show what you've done

linearis comments create RDS-2455 --body "## Progress Update

- [x] Completed component refactoring
- [x] Added unit tests
- [ ] Integration tests (in progress)

Next: Testing with real data"
```

**For major updates that need decision:**
```bash
# You hit a blocker or need to change approach

linearis comments create RDS-2455 --body "## Blocker Encountered

Found that the current API doesn't support filtering by X.

Options:
1. Modify API endpoint (bigger change)
2. Filter client-side (less efficient)
3. Create new endpoint (longer timeline)

Need guidance on approach."

# Then wait for user input before proceeding
```

### Workflow 3: Updating Task Status in Description

**Scenario:** You're making progress on a task list in the issue description.

```bash
# Issue description currently has:
# - [ ] Task 1: Implement component
# - [ ] Task 2: Add tests
# - [ ] Task 3: Documentation

# After completing Task 1, you can update directly:
linearis issues update RDS-2455 --description "
## Tasks
- [x] Task 1: Implement component ✅ Completed
- [ ] Task 2: Add tests
- [ ] Task 3: Documentation
"

# OR comment about the change:
linearis comments create RDS-2455 --body "✅ Completed: Task 1 - Implement component"
```

**Best Practice:** If the issue author will see the change, add a comment too so they get notified.

### Workflow 4: Creating a New Issue

**Step 1: Determine if you need to ask**
- Is this a complex/major feature? → Ask first
- Is this a minor follow-up to current work? → Create directly
- Unsure? → Ask

**Step 2: Gather information**
```
Title: Brief, descriptive
Project: Usually parent ticket's project (or ask user)
Description: Context, why it's needed, any acceptance criteria
```

**Step 3: Create using linearis**
```bash
linearis issues create \
  --title "Brief description of issue" \
  --project RDS \
  --description "Detailed context and acceptance criteria"

# Example:
linearis issues create \
  --title "Fix typo in error message" \
  --project RDS \
  --description "The error message in validateInput() has a typo: 'occured' should be 'occurred'"
```

**Step 4: Report back**
```
You: "Created RDS-2500 as a follow-up. Here's the link: [Linear URL]"
```

### Workflow 5: Creating a Sub-Issue

**For issues that are part of a larger ticket:**

```bash
# If RDS-2455 is parent, and you need to create RDS-2456 as a sub-task

# Use the parent's project (RDS in this case)
linearis issues create \
  --title "Sub-task: Implement specific part" \
  --project RDS \
  --parent RDS-2455 \
  --description "This is a sub-task of RDS-2455 focusing on..."

# Report:
You: "Created RDS-2456 as a sub-task of RDS-2455"
```

### Workflow 6: Downloading Embedded Files

**When an issue has attachments:**

```bash
# Check what embeds are available
linearis issues read RDS-2455
# Look for "embeds" array with download URLs

# Download the files
linearis embeds download RDS-2455

# Files are saved locally for reference
# Use the content to inform your work
```

---

## Workflow Examples in Context

### Example 1: Mid-Project Discovery

```
You: Working on RDS-2455, find that the API is missing a field needed

Step 1: Read the issue (just to confirm scope)
linearis issues read RDS-2455

Step 2: Add a comment with finding
linearis comments create RDS-2455 --body "## Discovery: API Missing Field

The endpoint returns X but doesn't include Y. Current code expects Y.

Options:
1. Backend adds field (bigger scope)
2. I request it separately (more calls)

Which should I do?"

Step 3: Wait for guidance before proceeding
```

### Example 2: Completing a Task List

```
Issue has:
- [ ] Build component
- [ ] Add tests
- [ ] Update docs

You finish building the component.

Option A - Direct update (for small checkboxes):
linearis comments create RDS-2455 --body "✅ Component build complete"

Option B - Update description:
// Update the issue description to mark checkbox done
// Then optionally comment for notification

Best: Do both for visibility
```

### Example 3: Discovery of Follow-Up Work

```
You: "During RDS-2455, I notice several similar components could be refactored"

Decision tree:
- Is this major refactoring? → Ask user first
- Is this a small cleanup? → Create sub-issue directly

You: "Created RDS-2456 as a follow-up for component consolidation"

Then add comment to parent:
linearis comments create RDS-2455 --body "See RDS-2456 for related refactoring opportunity"
```

---

## Tool Reference

### Create a Comment
```bash
linearis comments create <issueId> --body "Comment text here"
```
- `<issueId>`: Can be UUID or `ABC-123` format
- `--body`: The comment text (supports Markdown)

### Read Issue Details
```bash
linearis issues read <issueId>
```
- Returns current issue state, description, embeds array
- Shows file URLs and expiration times

### Download Embeds
```bash
linearis embeds download <issueId>
```
- Downloads files attached to issue
- Saves locally for reference

### Create Issue
```bash
linearis issues create \
  --title "Title" \
  --project PROJECT \
  --description "Details"
```

### Referencing Issues
In code/commit messages, always use format: `ABC-123`
Example: `git commit -m "Fix bug described in RDS-2455"`

---

## Best Practices

### 1. **Always Reference by Number**
- Use `RDS-2455` not "the issue about that thing"
- Helps others quickly find the context
- Makes it searchable

### 2. **Prompt Status Updates**
- If task status changes, update promptly
- Don't wait until the very end
- This keeps the team informed of progress

### 3. **Comment for Significant Changes**
- Small checkbox updates: Can just update description
- Major findings/blockers: Add a comment for notification
- When in doubt: Add a comment

### 4. **Separate Code Review from Issue Tracking**
- Issue comments: High-level progress, blockers, decisions
- Code review: Details in PR/MR comments
- Don't duplicate information

### 5. **Ask Before State Changes**
- Even if obvious work is done, ask before marking "Done"
- This prevents accidental state changes affecting others
- Builds confidence in the workflow

### 6. **Link Related Issues**
- When creating follow-ups: "Created ABC-200 for related work"
- When a ticket depends on another: "Blocked by ABC-199 until..."
- Comment with cross-references for context

### 7. **Provide Context in New Issues**
Include in description:
- Why is this needed?
- What should the outcome be?
- Any acceptance criteria?
- Links to related issues

---

## Quick Decision Flowchart

```
Do you need to update something about an issue?
│
├─ Update description/checklist?
│  ├─ Just checking boxes or status? → Update freely (no ask)
│  └─ Rewriting content? → Ask first
│
├─ Add a comment/status report?
│  └─ Always OK (they're just notifications)
│
├─ Change issue state (In Progress/Done)?
│  └─ Always ask first (impacts team visibility)
│
├─ Create a new issue?
│  ├─ Complex/major? → Ask first
│  └─ Minor/obvious follow-up? → Create directly
│
└─ Download files from issue?
   └─ Use `linearis embeds download` to retrieve
```

---

## When to Reach Out

If you're unsure about any of these scenarios:
- Issue creation complexity level
- Whether something needs a state change
- If a description rewrite is justified
- Anything blocking your work

→ **Ask the user.** Better to confirm than to assume.

---

## Skill Version
- **Last Updated:** November 13, 2025
- **Based on preferences:** Linear issue handling workflow (context-dependent creation, ask-first state changes, free description checkbox updates)