---
name: verify-requirements-complete
description: Verify all stakeholder requirement reports exist and are valid before synthesis
allowed-tools: Bash, Read
---

# Verify Requirements Complete Skill

**Purpose**: Validate that all 3 stakeholder requirement reports (architect, tester, formatter) exist and are valid before proceeding to SYNTHESIS phase.

**Performance**: Prevents synthesis errors, ensures complete requirements gathered

## When to Use This Skill

### ✅ Use verify-requirements-complete When:

- All stakeholder agents reported completion
- Before transitioning to SYNTHESIS phase
- Before invoking synthesize-plan skill
- Want to ensure requirements phase complete

### ❌ Do NOT Use When:

- Agents still working in REQUIREMENTS phase
- Already in SYNTHESIS phase
- Requirements already verified
- Task not in REQUIREMENTS phase

## What This Skill Does

### 1. Checks Report Files Exist

```bash
# Verifies all 3 files present:
/workspace/tasks/{task}/{task}-architect-requirements.md
/workspace/tasks/{task}/{task}-tester-requirements.md
/workspace/tasks/{task}/{task}-formatter-requirements.md
```

### 2. Validates Report Content

```bash
# For each report:
- Non-empty content
- Contains required sections
- Proper markdown format
- Actual analysis (not placeholder)
```

### 3. Checks Agent Status

```bash
# Verifies agent status.json files:
- All agents show "completed" status
- No agents in "failed" state
- Timestamps reasonable
```

### 4. Reports Results

```bash
# Clear output:
✅ architect-requirements.md: Valid (2,345 bytes, 5 sections)
✅ tester-requirements.md: Valid (1,867 bytes, 4 sections)
✅ formatter-requirements.md: Valid (1,234 bytes, 3 sections)

All requirements complete. Ready for SYNTHESIS.
```

## Usage

### Basic Verification

```bash
# Check if requirements complete
TASK_NAME="implement-formatter-api"

/workspace/main/.claude/scripts/verify-requirements-complete.sh \
  --task "$TASK_NAME"
```

### With Detailed Output

```bash
# Get detailed validation results
TASK_NAME="implement-formatter-api"

/workspace/main/.claude/scripts/verify-requirements-complete.sh \
  --task "$TASK_NAME" \
  --verbose true
```

## Validation Checks

### File Existence Check

```bash
# All 3 reports must exist:
- architect-requirements.md
- tester-requirements.md
- formatter-requirements.md

# If any missing:
❌ FAILED: Missing reports: tester-requirements.md
```

### Content Validation

**Non-Empty**:
```bash
# File must have content (>100 bytes minimum)
if [ $(wc -c < report.md) -lt 100 ]; then
  echo "❌ Report too small (likely placeholder)"
fi
```

**Required Sections** (Architecture):
```markdown
# Must contain:
- ## Dependencies / Integration Points
- ## Design Patterns / Architecture
- ## API Design (if applicable)
```

**Required Sections** (Tester):
```markdown
# Must contain:
- ## Test Coverage
- ## Test Strategy
- ## Edge Cases
```

**Required Sections** (Formatter):
```markdown
# Must contain:
- ## Documentation Requirements
- ## Code Style Standards
```

### Agent Status Check

```bash
# Check status.json for each agent
STATUS=$(jq -r '.status' agents/{agent}/status.json)

# Valid statuses:
✅ "completed" - Agent finished successfully
❌ "failed" - Agent encountered errors
❌ "in_progress" - Agent still working
❌ "not_started" - Agent never invoked
```

## Workflow Integration

### Pre-Synthesis Validation

```markdown
REQUIREMENTS phase: Agents working
  ↓
All agents report completion
  ↓
[verify-requirements-complete skill] ← THIS SKILL
  ↓
Check all reports exist
  ↓
Validate report content
  ↓
Check agent status
  ↓
If ALL PASS:
  ✅ Ready for SYNTHESIS
  → Invoke synthesize-plan skill

If ANY FAIL:
  ❌ Not ready for SYNTHESIS
  → Fix missing/invalid reports
  → Re-invoke failed agents
```

## Output Format

Script returns JSON:

```json
{
  "status": "success",
  "message": "All requirements complete and valid",
  "task_name": "implement-formatter-api",
  "reports": {
    "architect": {
      "exists": true,
      "valid": true,
      "size_bytes": 2345,
      "sections": 5
    },
    "tester": {
      "exists": true,
      "valid": true,
      "size_bytes": 1867,
      "sections": 4
    },
    "formatter": {
      "exists": true,
      "valid": true,
      "size_bytes": 1234,
      "sections": 3
    }
  },
  "agent_status": {
    "architect": "completed",
    "tester": "completed",
    "formatter": "completed"
  },
  "ready_for_synthesis": true,
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

**Or if validation fails**:

```json
{
  "status": "failed",
  "message": "Requirements incomplete",
  "task_name": "implement-formatter-api",
  "missing_reports": ["tester-requirements.md"],
  "invalid_reports": [],
  "failed_agents": ["tester"],
  "ready_for_synthesis": false,
  "errors": [
    "tester-requirements.md does not exist",
    "tester agent status: failed"
  ],
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Common Failure Scenarios

### Scenario 1: Missing Report

```bash
❌ tester-requirements.md not found

Cause: Agent failed to create output file
Fix: Re-invoke tester agent with explicit output path
```

### Scenario 2: Empty Report

```bash
❌ formatter-requirements.md is empty (0 bytes)

Cause: Agent created file but wrote no content
Fix: Re-invoke formatter agent, check for errors
```

### Scenario 3: Placeholder Content

```bash
❌ architect-requirements.md contains placeholder

Content: "TODO: Add requirements here"

Cause: Agent didn't complete analysis
Fix: Re-invoke architect agent with clear requirements
```

### Scenario 4: Agent Failed

```bash
❌ tester agent status: failed

Cause: Agent encountered error during execution
Fix: Check agent error log, fix issue, re-invoke
```

### Scenario 5: Missing Sections

```bash
❌ tester-requirements.md missing required sections

Missing: "Edge Cases" section

Cause: Agent provided incomplete analysis
Fix: Re-invoke with emphasis on complete sections
```

## Recovery Actions

### Missing Report

```bash
# Re-invoke missing agent
AGENT="tester"
TASK="implement-formatter-api"

# Invoke via Task tool with output requirement
Task tool: tester
  prompt: "Write requirements to /workspace/tasks/$TASK/$TASK-tester-requirements.md"
```

### Invalid Content

```bash
# Re-invoke agent with stronger requirements
Task tool: architect
  prompt: "CRITICAL: Write complete analysis to requirements file.
  Must include all sections: Dependencies, Design Patterns, API Design.
  File must be >500 bytes with actual content."
```

### Failed Agent

```bash
# Check error logs
cat /workspace/tasks/{task}/agents/{agent}/error.log

# Fix underlying issue (missing dependencies, etc.)
# Re-invoke agent
```

## Safety Features

### Precondition Validation

- ✅ Verifies task exists
- ✅ Checks task in REQUIREMENTS phase
- ✅ Confirms task directory accessible

### Comprehensive Checks

- ✅ File existence for all 3 reports
- ✅ Content validation (non-empty, sections)
- ✅ Agent status verification
- ✅ Format validation (markdown)

### Clear Error Reporting

- ✅ Lists specific missing reports
- ✅ Identifies invalid reports
- ✅ Reports failed agents
- ✅ Provides recovery actions

## Related Skills

- **gather-requirements**: Creates reports that this skill verifies
- **synthesize-plan**: Consumes verified reports
- **state-transition**: May use this for REQUIREMENTS → SYNTHESIS validation

## Troubleshooting

### False Positive: Report Valid But Flagged

```bash
# Report exists but validation incorrectly fails
# Possible causes:
1. Different file naming (check exact filename)
2. Report in wrong directory (check path)
3. Validation regex too strict (adjust)

# Manual verification:
ls -la /workspace/tasks/{task}/*-requirements.md
cat /workspace/tasks/{task}/{task}-architect-requirements.md
```

### Agent Completed But No Report

```bash
# Agent status shows "completed" but file missing
# Possible causes:
1. Agent wrote to wrong path
2. Agent didn't include Write tool call
3. File permissions issue

# Find where agent wrote:
find /workspace/tasks/{task} -name "*requirements*"

# If found in wrong location, move it:
mv {wrong-path} {correct-path}
```

### Report Exists But Content Invalid

```bash
# File exists but doesn't pass validation
# Check:
1. File size: wc -c {report}
2. Sections present: grep "^##" {report}
3. Actual content: head -50 {report}

# If truly invalid, re-invoke agent
```

## Validation Criteria Summary

### Architect Requirements

✅ **VALID**:
- File exists at correct path
- Size > 500 bytes
- Contains sections: Dependencies, Design Patterns, API Design
- Agent status: completed

❌ **INVALID**:
- File missing or empty
- Placeholder content only
- Missing required sections
- Agent status: failed or in_progress

### Tester Requirements

✅ **VALID**:
- File exists at correct path
- Size > 400 bytes
- Contains sections: Test Coverage, Test Strategy, Edge Cases
- Agent status: completed

❌ **INVALID**:
- File missing or empty
- Generic content (not task-specific)
- Missing test strategy
- Agent status: failed or in_progress

### Formatter Requirements

✅ **VALID**:
- File exists at correct path
- Size > 300 bytes
- Contains sections: Documentation Requirements, Code Style
- Agent status: completed

❌ **INVALID**:
- File missing or empty
- Just references to style-guide.md (no task specifics)
- Missing documentation requirements
- Agent status: failed or in_progress

## Implementation Notes

The verify-requirements-complete script performs:

1. **Precondition Phase**
   - Check task exists
   - Verify task directory accessible
   - Confirm task in REQUIREMENTS phase

2. **File Check Phase**
   - Look for all 3 report files
   - Check file existence
   - Verify file readable

3. **Content Validation Phase**
   - Check file size (not empty/placeholder)
   - Validate markdown structure
   - Check for required sections
   - Verify actual content present

4. **Agent Status Phase**
   - Read agent status.json files
   - Check completion status
   - Verify no failures
   - Validate timestamps

5. **Aggregation Phase**
   - Combine all validation results
   - Determine overall status
   - List specific failures
   - Provide recovery actions

6. **Reporting Phase**
   - Return JSON with detailed results
   - Report ready_for_synthesis boolean
   - List missing/invalid reports
   - Provide next steps
