---
name: audit-protocol-compliance
description: Systematic audit of session for task protocol compliance violations with documentation fix recommendations
allowed-tools: Read, Write, Bash, Grep, Skill
---

# Audit Protocol Compliance Skill

**Purpose**: Systematically audit conversation sessions for ALL task protocol compliance violations and recommend preventive documentation changes.

**When to Use**:
- After completing a task to verify protocol adherence
- When investigating protocol violations
- To validate that mandatory checkpoints were followed
- Before committing to identify and fix violations

## Skill Workflow

**Overview**: Parse timeline → Execute compliance checks → Report violations → Recommend fixes

### Phase 1: Get Structured Timeline

**Invoke parse-conversation-timeline skill**:
```bash
Skill: parse-conversation-timeline
```

This produces structured timeline JSON with:
- session_metadata
- timeline (chronological events)
- git_status
- task_state
- statistics

### Phase 2: Execute Category 1 Checks (CRITICAL - MANDATORY FIRST)

**Check 1.0: User Approval Checkpoints** (CRITICAL)
```bash
jq '.statistics.approval_checkpoints' timeline.json

# Rule: User MUST approve after SYNTHESIS before IMPLEMENTATION
# Rule: User MUST approve after REVIEW before COMPLETE

# FOR EACH checkpoint:
#   IF checkpoint.required == true AND checkpoint.found == false:
#     → CRITICAL VIOLATION
```

**Check 1.1: Task Merge to Main Before COMPLETE** (CRITICAL)
```bash
jq '.task_state.task_json.state' timeline.json
jq '.git_status.branches[] | select(.task_complete_but_not_merged == true)' timeline.json

# Rule: Task branch MUST be merged to main BEFORE marking state as COMPLETE

# IF task_state == "COMPLETE" AND merged_to_main == false:
#   → CRITICAL VIOLATION
```

**Check 1.2: Main Agent Source File Creation** (CRITICAL)
```bash
jq '.timeline[] | select(.type == "tool_use" and .actor == "main" and (.tool.name == "Edit" or .tool.name == "Write") and .file_classification.type == "source_file")' timeline.json

# Rule: Main agent MUST NOT create/edit source files during IMPLEMENTATION state
# Exception: Infrastructure files (module-info.java, pom.xml) allowed in any state

# FOR EACH tool_use in results:
#   IF file_classification.type == "source_file":
#     IF file_classification.worktree_type != "main_worktree":
#       → CRITICAL VIOLATION
```

**Check 1.3: Working Directory Violations** (CRITICAL)
```bash
jq '.timeline[] | select(.type == "tool_use" and .actor == "main" and (.tool.name == "Edit" or .tool.name == "Write") and .file_classification.worktree_type == "agent_worktree")' timeline.json

# Rule: Main agent MUST NOT perform Edit/Write in agent worktrees

# IF any results found:
#   → CRITICAL VIOLATION
```

### Phase 3: Execute Additional Checks (Categories 2-8)

**Check 2.1: Main Agent Implementation** (CRITICAL)
```bash
# Rule: Main agent MUST coordinate via Task tool, NOT implement directly
# Query timeline for Write/Edit on .java/.ts/.py during IMPLEMENTATION state
```

**Check 2.2: Agent Invocation Pattern** (HIGH)
```bash
# Rule: Launch independent agents in parallel (single message)
# Query: Count Task tool invocations per message
# IF Task tools spread across multiple messages: VIOLATION
```

**Check 3.1: Worktree Structure** (CRITICAL)
```bash
# Rule: Each agent must have own worktree before invocation
# Query: Check worktree creation before Task tool calls
```

**Check 3.2: Working Directory** (CRITICAL)
```bash
# Rule: Agents work in their assigned worktrees
# Query: Verify cwd matches expected worktree for each agent
```

**Check 4.1: Parallel Execution** (MEDIUM)
```bash
# Rule: Independent operations should run in parallel
# Query: Identify sequential Task calls that could be parallel
```

**Check 4.2: Iterative Validation** (HIGH)
```bash
# Rule: Implementation uses review mode + implementation mode iterations
# Query: Verify agents in review mode (opus) validate agents in implementation mode (haiku)
```

**Check 4.3: Agent Integration** (CRITICAL)
```bash
# Rule: Agent work must merge to task branch
# Query: Verify git merge operations after agent completion
```

### Phase 4: Generate Recommendations

For EACH violation, recommend specific protocol changes:

```json
{
  "type": "CLARIFICATION|EXAMPLE|WARNING|EDGE_CASE",
  "file": "/workspace/main/CLAUDE.md",
  "section": "Multi-Agent Architecture",
  "change": "Add explicit warning: 'VIOLATION: Main agent creating .java files directly'",
  "rationale": "Make prohibition more visible"
}
```

## Output Format

```json
{
  "audit_timestamp": "2025-11-01T...",
  "overall_verdict": "PASSED|FAILED",
  "violations": [
    {
      "check_id": "0.2",
      "severity": "CRITICAL",
      "rule": "Main agent MUST NOT use Write/Edit on source files during IMPLEMENTATION state",
      "actual_behavior": "Main agent used Edit tool on FormattingRule.java while state == IMPLEMENTATION",
      "evidence": {
        "task_state": "IMPLEMENTATION",
        "tool_used": "Edit",
        "target_file": "FormattingRule.java",
        "target_type": "source_file",
        "actor": "main",
        "timestamp": "2025-11-01T15:02:00Z"
      },
      "verdict": "VIOLATION",
      "protocol_reference": "CLAUDE.md § Multi-Agent Architecture",
      "recommended_changes": [
        {
          "type": "CLARIFICATION",
          "file": "CLAUDE.md",
          "section": "Multi-Agent Architecture",
          "change": "Add explicit warning about source file creation prohibition",
          "rationale": "Make violation more obvious"
        }
      ]
    }
  ],
  "compliant_checks": [
    {
      "check_id": "1.1",
      "rule": "Main agent must coordinate stakeholder agents",
      "verdict": "COMPLIANT",
      "evidence": "Task tool invoked for architect, engineer, formatter"
    }
  ],
  "summary": {
    "total_checks": 25,
    "violations": 1,
    "compliant": 24,
    "overall_verdict": "FAILED",
    "critical_violations": 1,
    "high_violations": 0,
    "medium_violations": 0
  }
}
```

## CRITICAL RULES (ZERO TOLERANCE)

### Rule 1: Check 1.0-1.3 Execute FIRST
- Do NOT skip to other checks
- Do NOT assume state is correct
- Read timeline data, don't infer

### Rule 2: Binary Verdicts Only
- Output: "VIOLATION" or "COMPLIANT"
- NO "would be OK if..."
- NO "technically a violation, but..."
- NO gray areas

### Rule 3: No Rationalization

**PROHIBITED PATTERNS**:
- ❌ "Main agent implemented code, BUT this would be OK in VALIDATION state"
- ❌ "Technically a violation, but the work is good quality"
- ❌ "The agent was trying to fix violations, so it's reasonable"

**REQUIRED PATTERN**:
- ✅ "Check 1.2: VIOLATION - Main agent used Edit during IMPLEMENTATION state"
- ✅ "Evidence: task.json state == IMPLEMENTATION, Edit tool on source file"
- ✅ "Verdict: VIOLATION (no exceptions)"

### Rule 4: State-Based Rule Application

Rules apply based on actual task_state, NOT:
- TodoWrite state
- What state "should" be
- What main agent thinks state is
- What would make behavior acceptable

### Rule 5: Evidence Required
- Every violation must cite timeline evidence
- Include: actual state, tool used, target file, actor, timestamp
- No assumptions or inferences

## Check Execution Matrix

| Check ID | Category | Severity | Description |
|----------|----------|----------|-------------|
| 1.0 | Approval checkpoints | CRITICAL | User approval after SYNTHESIS |
| 1.1 | State verification | CRITICAL | Merge before COMPLETE |
| 1.2 | Implementation boundaries | CRITICAL | Main agent source file creation |
| 1.3 | Working directory | CRITICAL | Agent worktree isolation |
| 2.1 | Coordination | CRITICAL | Main agent delegates via Task tool |
| 2.2 | Invocation pattern | HIGH | Parallel agent launch |
| 2.3 | Role clarity | HIGH | Clear mode specification (opus/haiku) |
| 3.1 | Worktree structure | CRITICAL | Agent worktrees exist |
| 3.2 | Working directory | CRITICAL | Agents in correct worktrees |
| 4.1 | Parallel execution | MEDIUM | Independent operations parallel |
| 4.2 | Iterative validation | HIGH | Review/implementation iterations |
| 4.3 | Agent integration | CRITICAL | Work merged to task branch |

## Verification Checklist

Before outputting audit results:
- [ ] Check 1.0-1.3 executed FIRST
- [ ] All checks attempted
- [ ] Each violation has timeline evidence
- [ ] Binary verdicts only (no rationalizations)
- [ ] Overall verdict calculated (ANY violation = FAILED)
- [ ] Recommended changes provided for each violation
- [ ] JSON is valid

## Related Skills

- **parse-conversation-timeline**: Get structured timeline for auditing
- **learn-from-mistakes**: Fix specific mistake after identifying it
- **audit-protocol-efficiency**: Optimize execution patterns (run after compliance passes)
