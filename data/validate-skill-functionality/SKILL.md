---
name: validate-skill-functionality
description: Load when user says "validate skill", "validate this skill", "review skill execution", "check skill", or "skill validation" at the end of executing a skill. Post-execution review workflow for validating that a skill worked correctly, documenting findings, and identifying issues.
---

# Validate Skill Functionality

**Purpose**: Systematic post-execution review to validate skill functionality and document findings.

**When to Use**: After a skill has completed its full execution workflow

## Workflow

Follow these steps to validate skill functionality:

### Step 1: Review Execution Context

- Identify which skill was just executed
- Review what the skill was supposed to accomplish
- Check the SKILL.md to understand expected behavior
- Review conversation history to identify all tool calls made during execution

### Step 2: Validate File Loading

**Check that all required files were loaded correctly:**

- Review all Read tool calls in the conversation
- Verify SKILL.md was loaded (for skill execution context)
- Check if skill references other files (references/, scripts/, assets/)
- Confirm referenced files were actually loaded when needed
- Look for "File not found" errors or truncated reads
- Verify file paths match expected locations

**Example checks:**
```
✅ SKILL.md loaded: Yes (line 1-88, complete)
✅ references/workflow.md loaded: Yes (when needed in Step 2)
❌ references/error-handling.md loaded: No (should have been loaded but wasn't)
✅ scripts/bulk-complete.py executed: Yes (correct parameters)
```

### Step 3: Validate Skill Nesting/Wrapping

**Check if skills correctly loaded nested skills:**

- Identify if the skill called other skills (e.g., execute-project calls create-skill)
- Verify nested skills were loaded using nexus-loader.py or explicit Read
- Confirm nested skill workflows were followed correctly
- Check that context was passed properly between skills
- Validate that nested skill outputs fed back correctly

**Example checks:**
```
Primary Skill: execute-project
  ✅ Loaded: Yes (via nexus-loader.py --skill execute-project)

  Nested Skill: create-skill
    ✅ Loaded: Yes (via nexus-loader.py --skill create-skill)
    ✅ SKILL.md read: Yes (complete)
    ✅ Workflow followed: Yes (all 7 steps)
    ✅ Context passed: Yes (user's workflow → create-skill)

  Nested Skill: close-session
    ✅ Loaded: Yes (auto-triggered)
    ✅ workflow.md loaded: Yes (as required)
    ✅ All 8 steps executed: Yes
```

### Step 4: Verify Expected Outputs

- Confirm the skill completed its workflow
- Check that outputs match expectations
- Verify all steps executed correctly
- Validate files were created/modified as expected

### Step 5: Check for Errors or Edge Cases

- Look for any errors or warnings during execution
- Identify edge cases or unexpected behavior
- Note any deviations from expected workflow
- Check for incomplete reads or missing context

### Step 6: Report Findings (≤5 lines)

Report to user verbally:
- ✅ What worked
- ❌ Issues found (if any)
- 💡 Recommendations (if any)

**NO documentation files** - Follow orchestrator.md ≤5 line rule
