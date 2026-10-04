---
name: fleet-architecture-cron-operations
description: How the architect operates during the weekly architecture-health-check CRON — what to scan, how to produce the health report, and how findings flow to the immune system and PM.
---

# Architecture CRON Operations — Architect's Scheduled Health Check

Your **architecture-health-check** CRON fires weekly. It runs in an isolated session with proper model and effort. Your job in that session is specific: scan the codebase for architectural drift, produce a health report, and surface findings.

## What the CRON Session Looks Like

When the CRON fires, you're in an isolated session. No task context. No heartbeat data. Just your CRON message telling you to run the health check. Your tools, skills, and sub-agents are available.

## The Weekly Check Protocol

### 1. Dependency Direction Scan

Use `dependency-mapper` sub-agent:
```
Agent: dependency-mapper
Prompt: "Scan fleet/core/ for imports from fleet/infra/, fleet/mcp/, 
        or fleet/cli/. Report any violations of inward dependency direction."
```

Expected: zero violations. Any match is structural drift.

### 2. Module Size Check

Scan for modules approaching the 500-line convention:
```
Agent: code-explorer
Prompt: "List all Python files in fleet/ over 300 lines with line counts.
        Flag any over 500 as split candidates."
```

### 3. Pattern Consistency Scan

Use `pattern-analyzer` sub-agent:
```
Agent: pattern-analyzer
Prompt: "Compare patterns used in fleet/infra/ clients (mc_client, 
        irc_client, gh_client, plane_client). Report any inconsistencies
        in how they handle errors, configure clients, or expose interfaces."
```

### 4. Cross-Agent Drift Check

Review recent commits across the codebase:
```bash
git log --since="7 days ago" --stat --oneline
```

Look for: different conventions in different areas, new patterns that deviate from established ones, config loading inconsistencies.

### 5. Produce Health Report

```
fleet_artifact_create("analysis_document", "Architecture Health — Week of {date}")
```

Structure:
```
## Architecture Health Report — Week of {date}

### Dependency Direction: {PASS/FAIL}
- Violations: {count}
- Details: {list if any}

### Module Size: {OK/WARNING}
- Files approaching limit: {count}
- Largest: {file} ({lines} lines)

### Pattern Consistency: {OK/DRIFT}
- Inconsistencies: {count}
- Details: {list if any}

### Cross-Agent Drift: {OK/DRIFT}
- Observations: {list}

### Overall: {HEALTHY/DEGRADING/NEEDS ATTENTION}

### Actions Needed:
- {specific tasks to create or flag}
```

### 6. Post Findings

```python
# Post to board memory for PO and fleet-ops visibility
fleet_chat(
    "Architecture health check complete. Status: {overall}. "
    "{findings_summary}",
    mention="project-manager"  # PM creates tasks for issues
)
```

If critical issues found:
```python
fleet_alert(
    category="architecture",
    severity="high",
    details="Dependency direction violation in fleet/core/{module}"
)
```

### 7. Record Trail

The CRON session automatically records trail. But explicitly post:
```python
# Board memory with architecture tags
# This feeds fleet-ops compliance checks and accountability patterns
```

## The CRON Configuration

From `config/agent-crons.yaml`:
```yaml
- name: architecture-health-check
  schedule: "0 8 * * 1"  # Monday 8am weekly
  model: sonnet           # sonnet sufficient for scanning
  effort: medium          # not deep thinking, structured scanning
  session: isolated       # clean session, no task contamination
```

## What This CRON is NOT

- NOT a code review (fleet-ops reviews individual tasks)
- NOT a design session (that's contribution work with a task)
- NOT fixing issues (create tasks via PM for that)

This CRON DETECTS. PM TRIAGES. Agents FIX. You separate detection from remediation.

## Integration With Other Skills

This CRON uses knowledge from:
- `/fleet-architecture-health` — what to look for
- `/fleet-domain-boundary-enforcement` — dependency direction rules
- `/fleet-srp-verification` — module responsibility checks
- `/fleet-design-pattern-selection` — pattern consistency reference

The CRON is WHERE you apply these skills. The skills are WHAT you know. Together they produce the health report.
