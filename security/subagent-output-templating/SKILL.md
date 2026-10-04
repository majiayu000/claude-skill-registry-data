---
name: subagent-output-templating
description: Template for structured sub-agent output including YAML log format, task completion reports (WHY/WHAT/TRADE-OFFS/RISKS), and summary constraints. Use when defining how sub-agents should report results.
user-invocable: false
allowed-tools:
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Sub-Agent Output Templating

## Overview

This skill provides standardized templates for sub-agent OUTPUT formatting. It complements `subagent-prompting` (P0.1) which defines INPUT structure:

| Skill | Purpose |
|-------|---------|
| `subagent-prompting` | How to prompt sub-agents (GOAL/CONSTRAINTS/CONTEXT/OUTPUT) |
| `subagent-output-templating` | How sub-agents report results (logs, summaries, diagnostics) |

Use this skill when:
- Defining output requirements for sub-agent invocations
- Parsing sub-agent results in pipeline stages
- Ensuring consistent log formats across all agents

---

## Log File Format

### File Location

```
logs/{agent-name}-{YYYYMMDD-HHMMSS}.yaml
```

Example: `logs/bulwark-code-auditor-20260111-143022.yaml`

### YAML Schema

```yaml
# Required: Metadata block
metadata:
  agent: {agent-name}           # e.g., bulwark-code-auditor
  timestamp: {ISO-8601}         # e.g., 2026-01-11T14:30:22Z
  model: {model-used}           # sonnet, haiku, or opus
  task_id: {unique-identifier}  # For tracking across pipeline stages
  duration_ms: {execution-time} # Execution duration in milliseconds

# Required: Goal from the prompt (for traceability)
goal: "{GOAL from 4-part prompt}"

# Required: Completion report
completion:
  why:
    problem: "{What was broken/missing}"
    root_cause: "{Why it happened}"
    solution: "{What was implemented}"

  what:
    - file: {path}
      lines: "{range}"
      change: "{description}"

  trade_offs:
    gained:
      - "{benefit 1}"
    cost:
      - "{drawback 1}"

  risks:
    - risk: "{description}"
      mitigation: "{how addressed}"
      severity: {low|medium|high|critical}

  next_steps:
    - "{action item 1}"

# Required for code-writing agents (omit for read-only agents):
# Pipeline suggestions from implementer-quality.sh output
pipeline_suggestions:
  - pipeline: "{recommended pipeline name}"
    target_files:
      - "{file path}"
    reason: "{why this pipeline is recommended}"

# Required: Summary for main thread (100-300 tokens)
summary: |
  {Concise summary for main thread consumption}

# Required: Diagnostic output
diagnostics:
  model_requested: {model}
  model_actual: {model}
  context_type: {main|forked}
  parent_vars_accessible: {true|false}
  hooks_fired:
    - {hook-name}
  execution_time_ms: {duration}
  completion_status: {success|error|timeout}
```

---

## Task Completion Report (WHY/WHAT/TRADE-OFFS/RISKS)

Every sub-agent MUST conclude with this structured report. This enables explicit decision documentation rather than implicit code changes.

### WHY Section

Document the problem and solution rationale.

```yaml
why:
  problem: "Authentication bypass vulnerability in refresh token path"
  root_cause: "Token validation skips expiry check on refresh"
  solution: "Added isExpired() check to refresh token handler"
```

**Guidelines**:
- `problem`: What was broken, missing, or needs improvement
- `root_cause`: The underlying reason (not just symptoms)
- `solution`: What was done to address it

### WHAT Section

List all changes made with file locations.

```yaml
what:
  - file: src/auth/token.ts
    lines: "45-52"
    change: "Added isExpired() check before token refresh"
  - file: src/auth/token.test.ts
    lines: "120-145"
    change: "Added test for expired refresh token rejection"
```

**Guidelines**:
- One entry per file modified
- Include line ranges for precise location
- Describe the change, not the code

### TRADE-OFFS Section

Acknowledge explicit compromises made.

```yaml
trade_offs:
  gained:
    - "Security: Expired tokens now properly rejected"
    - "Compliance: Meets OWASP session management requirements"
  cost:
    - "Performance: Additional DB lookup on refresh (negligible)"
    - "Complexity: New error handling path for expired tokens"
```

**Guidelines**:
- Be honest about costs
- Quantify impact where possible
- Include both technical and business trade-offs

### RISKS Section

Document forward-looking concerns.

```yaml
risks:
  - risk: "Existing sessions with expired refresh tokens will fail"
    mitigation: "Grace period of 24h for migration"
    severity: medium
  - risk: "Grace period could be exploited"
    mitigation: "Monitor for unusual refresh patterns"
    severity: low
```

**Severity Levels**:
| Level | Definition |
|-------|------------|
| `low` | Unlikely or minor impact |
| `medium` | Possible impact, manageable |
| `high` | Likely impact, needs attention |
| `critical` | Must be addressed before deployment |

### NEXT STEPS Section

List follow-up actions for pipeline or human.

```yaml
next_steps:
  - "Monitor refresh failure rate for 24h"
  - "Remove grace period after migration window"
  - "Update documentation for new error codes"
```

**Guidelines**:
- Actionable items only
- Include owner if known (e.g., "DevOps: Update monitoring dashboard")
- Order by priority

---

## Summary Format for Main Thread

### Purpose

The summary is returned to the main thread for pipeline decision-making. It should enable the orchestrator to:
1. Understand key findings without reading full log
2. Decide next pipeline stage
3. Report status to user

### Token Budget

| Complexity | Target Tokens | Use Case |
|------------|---------------|----------|
| Simple | 100-150 | Single finding, clear action |
| Moderate | 150-250 | Multiple findings, some nuance |
| Complex | 250-300 | Many findings, trade-off decisions |

### Summary Template

```
Found [N] [severity] issue(s): [brief description].
[Action taken / recommendation].
[Key risk or follow-up if any].
```

### Examples

**Simple (120 tokens)**:
```
Found 1 critical vulnerability: refresh tokens not validated for expiry.
Fixed by adding isExpired() check in token.ts:45-52. Added regression test.
Risk: existing sessions may fail during 24h migration window.
```

**Moderate (200 tokens)**:
```
Found 3 issues in authentication module:
- 1 critical: token expiry bypass (fixed)
- 1 medium: weak password hashing (fixed, migration needed)
- 1 low: verbose error messages (fixed)

All issues addressed with tests added. Migration script created for password re-hashing.
Next: run migration in staging, monitor for 48h before production.
```

### What to Include

- Finding count and severity
- Actions taken
- Key risks or blockers
- Recommended next steps

### What to Exclude

- Full reasoning or analysis
- Code snippets
- Verbose explanations
- Duplicate information from log

### Pipeline Suggestions in Summary (Code-Writing Agents)

Code-writing agents (e.g., bulwark-implementer) that invoke `implementer-quality.sh` and receive pipeline suggestions MUST include them in the summary with MANDATORY language. This ensures the orchestrator sees and acts on them per SA6.

```
MANDATORY FOLLOW-UP (SA6): Run the following pipeline(s):
  - {pipeline} on {target_files} ({reason})
Orchestrator MUST evaluate each suggestion and either execute or document deferral per SA6.
```

Read-only agents (reviewers, auditors) omit this section.

---

## Diagnostic Output

### Purpose

Enable automated behavioral testing without mocking. Diagnostics verify:
- Correct model was used
- Context isolation worked (for `context: fork` agents)
- Hooks fired as expected
- Execution completed successfully

### Location

```
logs/diagnostics/{agent-name}-{YYYYMMDD-HHMMSS}.yaml
```

### Format

```yaml
skill: subagent-output-templating
timestamp: 2026-01-11T14:30:22Z
diagnostics:
  model_requested: sonnet
  model_actual: sonnet
  context_type: forked      # main or forked
  parent_vars_accessible: false  # Should be false for forked
  hooks_fired:
    - Stop
  execution_time_ms: 4520
  completion_status: success  # success, error, timeout
notes: "Task completed successfully"
```

### Diagnostic Fields

| Field | Purpose | Values |
|-------|---------|--------|
| `model_requested` | Model specified in prompt | haiku, sonnet, opus |
| `model_actual` | Model that actually ran | haiku, sonnet, opus |
| `context_type` | Execution context | main, forked |
| `parent_vars_accessible` | Context isolation test | true, false |
| `hooks_fired` | Lifecycle hooks that executed | Array of hook names |
| `execution_time_ms` | Duration | Integer |
| `completion_status` | Final status | success, error, timeout |

---

## Quick Reference

### Minimal Log Template

```yaml
metadata:
  agent: {name}
  timestamp: {ISO-8601}
  model: sonnet
  task_id: "{id}"
  duration_ms: 0

goal: "{goal}"

completion:
  why:
    problem: "{problem}"
    root_cause: "{cause}"
    solution: "{solution}"
  what:
    - file: {path}
      lines: "{range}"
      change: "{description}"
  trade_offs:
    gained: ["{benefit}"]
    cost: ["{cost}"]
  risks:
    - risk: "{risk}"
      mitigation: "{mitigation}"
      severity: medium
  next_steps:
    - "{action}"

# Include for code-writing agents only (omit for read-only agents):
pipeline_suggestions:
  - pipeline: "{pipeline name}"
    target_files: ["{path}"]
    reason: "{reason}"

summary: |
  {100-300 token summary}

diagnostics:
  model_requested: sonnet
  model_actual: sonnet
  context_type: forked
  parent_vars_accessible: false
  hooks_fired: []
  execution_time_ms: 0
  completion_status: success
```

### Summary Checklist

```
[ ] Count and severity of findings stated
[ ] Actions taken described
[ ] Key risks mentioned
[ ] Next steps listed
[ ] Under 300 tokens
[ ] Pipeline suggestions with MANDATORY language (code-writing agents only)
```

### Output Location Checklist

```
[ ] Main log: logs/{agent}-{YYYYMMDD-HHMMSS}.yaml
[ ] Diagnostics: logs/diagnostics/{agent}-{YYYYMMDD-HHMMSS}.yaml
```

---

## Timestamp Formats

| Context | Placeholder | Format | Example |
|---------|-------------|--------|---------|
| **File paths** | `{YYYYMMDD-HHMMSS}` | Compact, filesystem-safe | `20260119-143022` |
| **YAML fields** | `{ISO-8601}` | Standard ISO format | `2026-01-19T14:30:22Z` |

**Why two formats?**
- File names: No colons (filesystem-safe on Windows), compact, lexically sortable
- YAML fields: Standard ISO-8601 for parsing and interoperability

**Important**: Always use `{YYYYMMDD-HHMMSS}` in file paths, never `{timestamp}` or `{ts}`.

---

## Related Skills

- **subagent-prompting** (P0.1): Defines INPUT structure (GOAL/CONSTRAINTS/CONTEXT/OUTPUT)
- **pipeline-templates** (P0.3): Pre-defined workflows that consume this output format

---

## References

For extended examples and edge cases, see `references/examples.md`.
