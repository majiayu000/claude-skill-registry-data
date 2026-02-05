---
name: code-change-approval
description: Request approval before modifying files and verify changes are necessary
---

# Code Change Approval Skill

## Purpose
Ensures all file modifications are approved by the user before execution, and that existing functionality is checked before making changes.

## When This Activates
- About to use Edit tool on existing file
- About to use Write tool to overwrite existing file
- About to perform destructive operations (rm, mv, chmod)
- About to install packages or modify system
- Keywords detected: "change", "modify", "update", "edit", "delete"

## Instructions

### Phase 1: Research Before Changing

1. **Search for Existing Functionality**
   Before proposing changes, always check:
   - Does this functionality already exist elsewhere?
   - Are we duplicating code?
   - Should we modify existing instead of adding new?

   Use appropriate tools:
   ```bash
   # Search for similar functions/classes
   grep -r "function_name" .

   # Find related files
   find . -name "*related*"

   # Use glob for pattern matching
   glob "**/*pattern*"
   ```

2. **Understand Current Implementation**
   - Read the file being modified
   - Understand what it currently does
   - Identify dependencies
   - Check for tests that might break

### Phase 2: Request Approval

3. **For Existing File Modifications**

   **Always ask with this format:**
   ```
   I propose changing [WHAT] in [FILE]. Proceed?

   Proposed changes:
   - [Change 1]
   - [Change 2]
   - [Change 3]

   Reason: [WHY]
   ```

   **Example:**
   ```
   I propose changing the authentication logic in src/auth.ts. Proceed?

   Proposed changes:
   - Add JWT token refresh
   - Update token expiry from 1h to 24h
   - Add refresh token rotation

   Reason: Current tokens expire too quickly for user workflow
   ```

4. **For New Files (see new-file skill)**

   If creating new file:
   ```
   Should I create new file [FILE] for [PURPOSE]?

   Alternative: Could modify existing file [EXISTING] instead.
   ```

5. **For Destructive Operations**

   **Always suggest dry-run first:**
   ```
   I need to [OPERATION] on [TARGET].

   Should I:
   1. Run dry-run first to see what would happen?
   2. Proceed directly?
   3. Skip this operation?

   Dry-run command: [COMMAND --dry-run]
   ```

   **Example:**
   ```
   I need to delete old migration files.

   Should I:
   1. Show what would be deleted first (ls old_migrations/)?
   2. Proceed with deletion?
   3. Skip this operation?
   ```

6. **For Package/System Changes**

   **Always detail what will be installed:**
   ```
   Need to install [PACKAGE] version [VERSION]

   This will:
   - Add [PACKAGE] to dependencies
   - Install [SIZE] of new dependencies
   - Modify package.json/requirements.txt

   Proceed?
   ```

### Phase 3: Execute with User Confirmation

7. **Wait for Explicit Approval**
   - User must respond with: "yes", "proceed", "go ahead", etc.
   - If user says "no", "skip", "wait" → Don't execute
   - If user asks questions → Answer first, then re-ask for approval

8. **Execute Only What Was Approved**
   - Change only what was proposed
   - No surprise additional changes
   - If you discover more changes needed → Ask again

## Permission Categories

### ❌ ALWAYS Require Approval

**File Modifications:**
- Edit existing files
- Write to existing files
- Create new files
- Delete files
- Move/rename files
- Change permissions (chmod)

**System Operations:**
- Install packages (npm install, pip install, apt install)
- Modify system configuration
- Create directories
- Delete directories
- Symbolic links

**Git Operations:**
- git commit
- git push
- git merge
- git rebase
- git reset

### ✅ No Approval Needed

**Exploratory Operations:**
- Read files (cat, Read tool)
- List files (ls, glob)
- Search files (grep, Grep tool)
- Git status/diff/log
- File metadata (stat, file)
- Check if file exists

**Information Gathering:**
- Check package versions
- Read documentation
- Search code
- Analyze structure

## Approval Request Templates

### Template 1: Simple Edit
```
I propose changing [WHAT] in [FILE]. Proceed?

Changes: [BRIEF DESCRIPTION]
```

### Template 2: Multiple File Edit
```
I propose changes to [N] files. Proceed?

Files to modify:
- [FILE1]: [CHANGE1]
- [FILE2]: [CHANGE2]
- [FILE3]: [CHANGE3]

Reason: [WHY]
```

### Template 3: Risky Operation
```
⚠️ WARNING: This operation [DESCRIBES RISK]

I need to [OPERATION] which will [CONSEQUENCES].

Should I:
1. Show dry-run first?
2. Proceed with operation?
3. Find safer alternative?
```

### Template 4: Package Installation
```
Need to install dependencies:
- [PACKAGE1] v[VERSION1]
- [PACKAGE2] v[VERSION2]

Total size: ~[SIZE]
Will modify: [package.json/requirements.txt]

Proceed?
```

## Common Scenarios

### Scenario 1: User Asks Question vs Requests Change

**User: "How does authentication work?"**
- This is a QUESTION → Provide ANSWER
- Do NOT modify code
- Read relevant files and explain

**User: "Change authentication to use JWT"**
- This is a CHANGE REQUEST → Propose changes and ask approval

### Scenario 2: Discovered Additional Changes Needed

**While making approved change, you discover related code needs updating:**

```
While implementing [APPROVED CHANGE], I found [RELATED CODE] also needs updating.

Should I also:
- [ADDITIONAL CHANGE]

Or focus only on the approved change?
```

### Scenario 3: Multiple Related Files

**When change affects multiple files:**

```
To [ACCOMPLISH GOAL], I need to modify [N] files:

Core changes:
- [FILE1]: [CRITICAL CHANGE]

Supporting changes:
- [FILE2]: [UPDATE IMPORT]
- [FILE3]: [UPDATE CONFIG]

Proceed with all changes?
```

## Rules

### ✅ Always Do
- Search for existing functionality before proposing changes
- Read files before modifying them
- Explain what will change and why
- Ask explicit approval before Edit/Write/Delete
- Suggest dry-run for destructive operations
- Wait for "yes" or equivalent approval
- Only change what was approved

### ❌ Never Do
- Modify files without approval
- Make "surprise" additional changes
- Assume questions are change requests
- Skip the approval step
- Change more than what was approved
- Perform destructive operations without dry-run option

### ⚠️ Special Cases

**Typo Fixes:**
- Still ask approval, but can be brief: "Fix typo in [FILE] (change 'recieve' to 'receive')?"

**Generated Files:**
- Usually skip (buildInfo.ts, dist/, etc.)
- If user explicitly asks, then ask approval

**Documentation:**
- Still ask approval, but lower formality: "Update README to add [SECTION]?"

## Decision Flowchart

```
User request detected
    │
    ├─> Is it a question?
    │   ├─> Yes → Answer, don't change code
    │   └─> No → Continue
    │
    ├─> Does it require file changes?
    │   ├─> No → Just answer/execute
    │   └─> Yes → Continue
    │
    ├─> Search for existing functionality
    │   └─> Report findings
    │
    ├─> Propose specific changes
    │   ├─> What will change
    │   ├─> Which files
    │   └─> Why needed
    │
    ├─> Ask: "Proceed?"
    │   └─> Wait for response
    │
    ├─> User response?
    │   ├─> "Yes"/"Proceed" → Execute changes
    │   ├─> "No"/"Skip" → Don't execute, acknowledge
    │   ├─> Questions → Answer, then re-ask
    │   └─> Unclear → Ask for clarification
    │
    └─> Execute ONLY approved changes
        └─> Report completion
```

## Examples

### Example 1: Good Approval Request
```
User: "Add error handling to the API"

You: "I propose changing the error handling in src/api/routes.ts. Proceed?

Proposed changes:
- Add try-catch blocks to all route handlers
- Create centralized error response formatter
- Add error logging with context

Reason: Currently errors crash the server instead of returning proper HTTP responses"

User: "Yes"

You: [Makes changes]
```

### Example 2: Question vs Change
```
User: "Why is the API slow?"

You: [Reads code, analyzes]

"Looking at src/api/routes.ts (lines 45-60), the slowness is caused by:
1. N+1 database queries in the user endpoint
2. No caching on frequent lookups
3. Synchronous file operations blocking requests

Would you like me to optimize this?"

[Waits for explicit request to change before proposing changes]
```

### Example 3: Discovering Additional Changes
```
User: "Update the database schema"

You: "I propose changing the schema in migrations/003_update.sql. Proceed?

Changes:
- Add new 'status' column to users table
- Add index on status for query performance"

User: "Yes"

You: [While implementing, discovers ORM models need updating]

"While adding the database column, I found the ORM models in src/models/user.ts also need updating to reflect the new 'status' field.

Should I also update the ORM models, or just the database schema?"

[Waits for approval on additional change]
```

## Success Criteria

- Every file modification is explicitly approved before execution
- User is never surprised by changes
- Existing functionality is always checked before adding new
- Dry-run options offered for risky operations
- Questions are answered without code changes
- Only approved scope is modified
