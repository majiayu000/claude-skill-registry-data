---
name: hitl-approval
description: Use when presenting a plan/summary to user and requesting explicit approval before proceeding. Generic approval gate for /audit, /build, /architect, /debug commands. Checks for auto-approve conditions ("do without approval" in prompt).
---

# HITL Approval Skill

> **ROOT AGENT ONLY** - Uses AskUserQuestion, runs only from root agent.

**Purpose:** Present plan/summary to user and get explicit approval before proceeding
**Trigger:** Decision point requiring human validation
**Inputs:** summary, affectedFiles, approach
**Outputs:** approved (boolean), feedback (string)

---

## Purpose & Use Cases

Use this skill as a **generic approval gate** for any major decision:

- **After /build analysis** → Approve implementation approach
- **After /audit findings** → Approve remediation plan
- **After /architect design** → Approve technical direction
- **After /debug investigation** → Approve fix strategy

---

## When Approval Auto-Approves

Approval auto-approves (requires no user intervention) if ANY condition is met:

| Condition                             | Auto-Approve?     |
| ------------------------------------- | ----------------- |
| Prompt contains "do without approval" | Yes               |
| Prompt contains "just do it"          | Yes               |
| Otherwise                             | Requires approval |

---

## Workflow

### Step 1: Check Auto-Approve Conditions

```
IF prompt contains "do without approval" OR "just do it":
    RETURN { approved: true, feedback: null }

CONTINUE to Step 2
```

### Step 2: Present Summary to User

Format the summary clearly with sections:

```
APPROVAL NEEDED
════════════════════════════════════════

📋 Summary:
{summary text}

📁 Affected Files:
{list of files}

🛠️  Approach:
{approach description}

Ready to proceed?
```

### Step 3: Ask for Approval

Use AskUserQuestion tool with two options:

- **APPROVE** → Continue to next phase
- **REVISE** → Collect feedback → Return to caller

### Step 4: Handle Response

**If APPROVED:**

```json
{
  "approved": true,
  "feedback": null
}
```

**If APPROVED WITH REVISIONS:**

```json
{
  "approved": false,
  "feedback": "User requested changes to approach - needs optimization for database queries"
}
```

### Step 5: Return Control to Caller

Return control to calling agent with:

- `approved: true|false`
- `feedback: string` (user's requested changes, if revisions needed)

Calling agent proceeds with:

- Execute (if approved)
- Revise based on feedback and re-submit for approval
- Loop back to investigation phase with updated approach

---

## HITL Tool Enforcement

HITL gates MUST use AskUserQuestion tool. Prose questions are rejected.

**Correct HITL:**

```
Use AskUserQuestion tool with:
- question: "Approve PRD package for implementation?"
- options: ["Approve", "Request Changes"]
```

**Incorrect HITL (REJECTED):**

```
"Ready to proceed? Let me know if you'd like any changes."
```

**Why:** Prose questions allow agents to continue without explicit user consent. The AskUserQuestion tool creates a blocking gate that ensures user acknowledgment before proceeding.

**Detection:** Commands check for AskUserQuestion tool call in agent response. Prose-only responses trigger loop back with instruction to use tool.

---

## Input Schema

```json
{
  "summary": "string (2-5 sentences describing what will happen)",
  "affectedFiles": "string[] (list of file paths or patterns)",
  "approach": "string (3-5 sentences explaining HOW it will be done)"
}
```

---

## Output Schema

```json
{
  "approved": "boolean",
  "feedback": "string | null (only if approved=false)"
}
```

---

## Examples

### Example 1: Change (Requires Approval)

```
Inputs:
{
  "summary": "Refactor database schema to support multi-tenancy. Affects 12 tables, requires data migration.",
  "affectedFiles": [
    "src/db/schema.ts",
    "src/migrations/",
    "src/services/user.service.ts",
    "src/services/team.service.ts"
  ],
  "approach": "1. Create new schema with tenant_id column. 2. Write migration script. 3. Deploy with blue-green strategy."
}

Processing:
  - Show approval request to user

User sees:
────────────────────────────────────────
APPROVAL NEEDED
════════════════════════════════════════

📋 Summary:
Refactor database schema to support multi-tenancy. Affects 12 tables, requires data migration.

📁 Affected Files:
- src/db/schema.ts
- src/migrations/
- src/services/user.service.ts
- src/services/team.service.ts

🛠️  Approach:
1. Create new schema with tenant_id column.
2. Write migration script.
3. Deploy with blue-green strategy.

Ready to proceed?

User clicks: YES

Output:
{
  "approved": true,
  "feedback": null
}
```

### Example 2: Approval Denied with Feedback

```
User clicks: NO, requesting changes

Follow-up prompt appears:
"What changes would you like? Be specific."

User responds:
"Don't deploy with blue-green yet. Need to test with read-only mode first."

Output:
{
  "approved": false,
  "feedback": "Don't deploy with blue-green yet. Need to test with read-only mode first."
}
```

---

## Integration

**Called by:** /audit, /build, /architect, /debug commands
**Calls:** AskUserQuestion tool
**Returns:** approved (boolean), feedback (string or null)
**Previous phase:** Analysis/investigation/design complete
**Next phase:** Execution (if approved) or revision (if rejected)

---

## Notes

- **Always honor explicit user instructions** in the original prompt about approval
- **AskUserQuestion** is required for this skill (runs in root agent context only)
