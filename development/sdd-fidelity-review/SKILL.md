---
name: sdd-fidelity-review
description: Review implementation fidelity against specifications by comparing actual code to spec requirements. Identifies deviations, assesses impact, and generates compliance reports for tasks, phases, or entire specs.
---

# Implementation Fidelity Review Skill

## Overview

The `sdd-fidelity-review` skill compares actual implementation against SDD specification requirements to ensure fidelity between plan and code. It identifies deviations, assesses their impact, and generates detailed compliance reports.

## Skill Family

This skill is part of the **Spec-Driven Development** quality assurance family:
- **Skill(sdd-toolkit:sdd-plan)** - Creates specifications
- **Skill(sdd-toolkit:sdd-next)** - Finds next tasks and creates execution plans
- **Implementation** - Code is written
- **sdd-update-subagent** - Updates progress
- **Skill(sdd-toolkit:sdd-fidelity-review)** (this skill) - Reviews implementation fidelity
- **run-tests-subagent** - Runs tests

## When to Use This Skill

Use this skill when you need to:
- Verify implementation matches specification requirements
- Identify deviations between plan and actual code
- Assess task or phase completion accuracy
- Review pull requests for spec compliance
- Audit completed work for fidelity
- Document implementation variations

**Do NOT use for:**
- Creating specifications (use sdd-plan)
- Finding next tasks (use sdd-next)
- Updating task status (use sdd-update)
- Running tests (use run-tests)

## ⚠️ Long-Running Operations

**This skill may run operations that take up to 5 minutes. Be patient and wait for completion.**

### CRITICAL: Avoid BashOutput Spam
- **ALWAYS use foreground execution with 5-minute timeout:** `Bash(command="...", timeout=300000)`
- **WAIT for the command to complete** - this may take the full 5 minutes
- **NEVER use `run_in_background=True` for test suites, builds, or analysis**
- If you must use background (rare), **wait at least 60 seconds** between BashOutput checks
- **Maximum 3 BashOutput calls per background process** - then kill it or let it finish

### Why?
Polling BashOutput repeatedly creates spam and degrades user experience. Long operations should run in foreground with appropriate timeout, not in background with frequent polling.

### Example (CORRECT):
```
# Test suite that might take 5 minutes (timeout in milliseconds)
result = Bash(command="pytest src/", timeout=300000)  # Wait up to 5 minutes
# The command will block here until completion - this is correct behavior
```

### Example (WRONG):
```
# Don't use background + polling
bash_id = Bash(command="pytest", run_in_background=True)
output = BashOutput(bash_id)  # Creates spam!
```

## Review Types

### 1. Phase Review
**Scope:** Single phase within specification (typically 3-10 tasks)
**When to use:** Phase completion checkpoints, before moving to next phase
**Output:** Phase-specific fidelity report with per-task breakdown
**Best practice:** Use at phase boundaries to catch drift before starting next phase

### 2. Task Review
**Scope:** Individual task implementation (typically 1 file)
**When to use:** Critical task validation, complex implementation verification
**Output:** Task-specific compliance check with implementation comparison
**Best practice:** Use for high-risk tasks (auth, data handling, API contracts)

**Note:** For full spec reviews, run phase-by-phase reviews for better manageability and quality.

## Reading Specifications (CRITICAL)

**This skill delegates ALL spec file access to the `sdd fidelity-review` CLI tool:**

- ❌ **NEVER** use `Read()` tool on .json spec files - bypasses hooks and wastes context tokens (specs can be 50KB+)
- ❌ **NEVER** use Python to parse spec JSON directly
- ❌ **NEVER** use `jq` to query spec files via Bash
- ❌ **NEVER** use Bash commands to read specs (e.g., `cat`, `head`, `tail`, `grep`)
- ❌ **NEVER** use command chaining to access specs (e.g., `sdd --version && cat specs/active/spec.json`)
- ✅ **ALWAYS** use `sdd fidelity-review` CLI commands to access spec data
- ✅ The CLI provides efficient, structured access with proper parsing and validation
- ✅ Spec files are large - reading them directly wastes valuable context window space

**All spec loading, task extraction, and requirement analysis happens inside the CLI tool.**

## Querying Spec and Task Data Efficiently

Before running a fidelity review, you may need to gather context about the spec, phases, or tasks. Use these efficient CLI commands instead of creating bash loops:

### Query Multiple Tasks at Once
```bash
# Get all tasks in a phase
sdd query-tasks <spec-id> --parent phase-1 --json

# Get tasks by status
sdd query-tasks <spec-id> --status completed --json

# Combine filters
sdd query-tasks <spec-id> --parent phase-2 --status pending --json

# Get all tasks (no limit)
sdd query-tasks <spec-id> --limit 0 --json
```

### Get Single Task Details
```bash
# Get detailed information about a specific task
sdd get-task <spec-id> task-1-3
```

### List Phases
```bash
# See all phases with progress information
sdd list-phases <spec-id>
```

### ❌ DON'T Do This (Inefficient)
```bash
# BAD: Bash loop calling sdd get-task repeatedly
for i in 1 2 3 4 5; do
  sdd get-task spec-id "task-1-$i"
done

# BAD: Creating temp scripts
cat > /tmp/get_tasks.sh << 'EOF'
...
EOF

# BAD: Using grep to parse JSON
sdd get-task spec-id task-1 | grep -o '"status":"[^"]*"'
```

### ✅ DO This Instead
```bash
# GOOD: Single command gets all tasks in phase-1
sdd query-tasks spec-id --parent phase-1 --json

# GOOD: Parse JSON properly with jq if needed
sdd query-tasks spec-id --parent phase-1 --json | jq '.[] | select(.status=="completed")'
```

## Workflow

This skill delegates all fidelity review logic to the dedicated `sdd fidelity-review` CLI tool, which handles spec loading, implementation analysis, AI consultation, and report generation.

### Step 1: Validate Inputs

Ensure the user provides:
- `spec_id`: The specification to review
- Either `task_id` (for task-level review) or `phase_id` (for phase-level review)

### Step 2: Construct CLI Command

Build the appropriate `sdd fidelity-review` command based on review scope:

**For task review:**
```bash
sdd fidelity-review <spec-id> --task <task-id>
```

**For phase review:**
```bash
sdd fidelity-review <spec-id> --phase <phase-id>
```

### Step 3: Execute CLI Command

Use the Bash tool to execute the constructed command:
```bash
sdd fidelity-review <spec-id> --task <task-id>
```

**CRITICAL:** The CLI tool handles ALL spec file operations. Do NOT:
- Read spec files with Read tool
- Parse specs with Python or jq
- Use cat/head/tail/grep on spec files
- Create temporary bash scripts (e.g., `/tmp/*.sh`)
- Use bash loops to iterate through tasks (e.g., `for i in 1 2 3; do sdd get-task...`)
- Call `sdd get-task` in a loop - use `sdd query-tasks` for batch retrieval
- Use grep/sed/awk to parse JSON outputs - all commands return structured JSON

**When you need task/spec context before running fidelity review:**
✅ Use `sdd query-tasks <spec-id> --parent <phase-id> --json` to get all tasks in a phase
✅ Use `sdd query-tasks <spec-id> --status <status> --json` to filter by status
✅ Use `sdd get-task <spec-id> <task-id>` to get a single task's details
✅ Use `sdd list-phases <spec-id>` to see all phases

Then execute the fidelity review with the appropriate scope.

Your job is to execute the CLI command and parse its JSON output.

The CLI tool handles:
- Loading and validating the specification
- Extracting task/phase requirements
- Analyzing implementation files
- Consulting AI tools (gemini, codex, cursor-agent) for deviation analysis
- Detecting consensus across multiple AI perspectives
- Categorizing deviations (exact match, minor, major, missing)
- Assessing impact levels
- Generating structured report

### Step 4: Parse and Present Results

The CLI returns JSON output with the structure:
```json
{
  "spec_id": "...",
  "review_type": "task|phase",
  "scope": {"id": "...", "title": "..."},
  "summary": {
    "tasks_reviewed": 0,
    "files_analyzed": 0,
    "deviations_found": 0,
    "fidelity_score": 0
  },
  "findings": [
    {
      "task_id": "...",
      "assessment": "exact_match|minor_deviation|major_deviation|missing",
      "deviations": [...],
      "impact": "low|medium|high",
      "ai_consensus": "..."
    }
  ],
  "recommendations": [...]
}
```

Parse this JSON, surface the structured findings directly to the invoking workflow, and include a link or path to the saved JSON report. The agent’s responsibility is to faithfully relay the CLI’s assessed deviations, recommendations, consensus signals, and metadata—perform validation/formatting as needed, but do not introduce any new analysis beyond what the CLI returned. Do not open or read the saved artifact; simply point the caller to its location.

## Report Structure

```markdown
# Implementation Fidelity Review

**Spec:** {spec-title} ({spec-id})
**Scope:** {review-scope}
**Date:** {review-date}

## Summary

- **Tasks Reviewed:** {count}
- **Files Analyzed:** {count}
- **Overall Fidelity:** {percentage}%
- **Deviations Found:** {count}

## Fidelity Score

- ✅ Exact Matches: {count} tasks
- ⚠️ Minor Deviations: {count} tasks
- ❌ Major Deviations: {count} tasks
- 🚫 Missing Functionality: {count} items

## Detailed Findings

### Task: {task-id} - {task-title}

**Specified:**
- {requirement-1}
- {requirement-2}

**Implemented:**
- {actual-1}
- {actual-2}

**Assessment:** {exact-match|minor-deviation|major-deviation}

**Deviations:**
1. {deviation-description}
   - **Impact:** {low|medium|high}
   - **Recommendation:** {action}

## Recommendations

1. {recommendation-1}
2. {recommendation-2}

## Journal Analysis

**Documented Deviations:**
- {task-id}: {deviation-summary} (from journal on {date})

**Undocumented Deviations:**
- {task-id}: {deviation-summary} (should be journaled)
```

## Integration with SDD Workflow

### When to Invoke

Fidelity reviews can be triggered at multiple points in the development workflow:

**1. After task completion (Optional verification):**
   - Optional verification step for critical tasks
   - Ensures task acceptance criteria fully met
   - Particularly useful for high-risk tasks (auth, data handling, API contracts)
   - Can be automated via verification task metadata

**2. Phase completion (Recommended):**
   - Review entire phase before moving to next phase
   - Catch drift early before it compounds
   - Best practice: Use at phase boundaries
   - Prevents accumulated technical debt

**3. Spec completion (Pre-PR audit):**
   - Final comprehensive audit before PR creation
   - Run phase-by-phase reviews for better quality
   - Ensures PR matches spec intent
   - Documents any deviations for PR description

**4. PR review (Automated compliance):**
   - Automated or manual PR compliance checks
   - Verify changes align with original specification
   - Useful for reviewer context and validation

### Review Outcome Handling

The `sdd-fidelity-review` skill hands its synthesized results—JSON findings plus the saved JSON report reference—directly back to the caller. The invoking workflow decides what to do next. Common follow-up actions the main agent may optionally consider include journaling deviations, planning remediation work, running regression tests, or proposing spec updates after stakeholder review. No automatic delegation occurs; the fidelity-review skill’s responsibility ends once it delivers the consensus results and report pointer.

### Report Handoff

Fidelity review generates a detailed report comparing implementation against specification:

**Usage Pattern:**
1. Skill executes `sdd fidelity-review` CLI tool
2. CLI analyzes implementation, generates JSON output, and saves the JSON consensus report in `.fidelity-reviews/`
3. Skill parses the JSON, presents the summarized findings, and surfaces the stored report path to the caller

## Fidelity Assessment

### Exact Match (✅)
Implementation precisely matches specification requirements. No deviations detected.

### Minor Deviation (⚠️)
Small differences from spec with no functional impact:
- Different variable names (but consistent with codebase style)
- Minor refactoring for code quality
- Improved error messages
- Additional logging or comments

### Major Deviation (❌)
Significant differences affecting functionality or architecture:
- Different API signatures than specified
- Missing required features
- Different data structures
- Changed control flow or logic

### Missing Functionality (🚫)
Specified features not implemented:
- Required functions missing
- Incomplete implementation
- Skipped acceptance criteria

## Best Practices

### DO
✅ Validate that spec_id and task_id/phase_id are provided
✅ Present findings clearly with categorized deviations
✅ Highlight recommendations for remediation
✅ Note AI consensus from multiple tool perspectives
✅ Provide context from the fidelity assessment
✅ Surface the saved JSON report path so the caller can inspect the full consensus artifacts

### DON'T
❌ Attempt to manually implement review logic (CLI handles it)
❌ Read spec files directly with Read/Python/jq/Bash (CLI loads them)
❌ Create temporary bash scripts or use bash loops (e.g., `for i in...; do sdd get-task...`)
❌ Call `sdd get-task` in a loop - use `sdd query-tasks` for batch queries instead
❌ Use grep/sed/awk to parse JSON - all CLI commands return structured JSON
❌ Skip input validation
❌ Ignore the CLI tool's consensus analysis
❌ Make up review findings not from CLI output
❌ Perform additional analysis beyond the CLI's consensus results
❌ Open the persisted JSON report; reference its filepath instead

## Example Invocations

**Phase review:**
```
Task(
  subagent_type: "sdd-toolkit:sdd-fidelity-review-subagent",
  prompt: "Review phase phase-1 in spec user-auth-001. Compare all completed tasks in Phase 1 (User Model & Authentication) against specification requirements.",
  description: "Phase 1 fidelity review"
)
```

**Task-specific review:**
```
Task(
  subagent_type: "sdd-toolkit:sdd-fidelity-review-subagent",
  prompt: "Review task task-2-3 in spec user-auth-001. Compare implementation in src/middleware/auth.ts against task requirements for JWT authentication middleware.",
  description: "Review auth middleware task"
)
```

## Error Handling

### Missing Required Information
If invoked without required information, the skill returns a structured error indicating which fields are missing.

### Spec Not Found
If the specified spec file doesn't exist, the skill reports which directories were searched and suggests verification steps.

### No Implementation Found
If the specified files don't exist, the skill warns that the task appears incomplete or the file paths are incorrect.

## Success Criteria

A successful fidelity review:
- ✅ Compares all specified requirements against implementation
- ✅ Identifies and categorizes deviations accurately
- ✅ Assesses impact of deviations
- ✅ Provides actionable recommendations
- ✅ Generates clear, structured report
- ✅ Automatically saves to `specs/.fidelity-reviews/` directory
- ✅ Documents findings for future reference

---

*For creating specifications, use Skill(sdd-toolkit:sdd-plan). For task progress updates, use sdd-update-subagent. For running tests, use run-tests-subagent.*
