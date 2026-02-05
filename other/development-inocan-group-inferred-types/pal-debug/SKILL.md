---
name: pal-debug
description: Systematic debugging and root cause analysis using PAL MCP. Use for complex bugs, mysterious errors, race conditions, memory leaks, and integration problems. Triggers on debugging requests, error investigation, or when stuck on difficult issues.
---

# PAL Debug - Root Cause Analysis

Systematic debugging with hypothesis testing and expert validation through the PAL MCP server.

## When to Use

- Complex bugs that aren't obvious
- Mysterious errors with unclear causes
- Race conditions or timing issues
- Memory leaks or performance problems
- Integration failures between systems
- When you've tried basic debugging and are stuck

## Quick Start

Use the `mcp__pal__debug` tool for multi-step investigation:

```python
# Step 1: Start investigation
result = mcp__pal__debug(
    step="Investigating: API returns 500 on concurrent requests",
    step_number=1,
    total_steps=3,
    next_step_required=True,
    findings="Initial investigation - gathering context",
    hypothesis="Unknown - needs investigation",
    confidence="exploring",
    relevant_files=["/path/to/api/handler.py"]
)

# Step 2+: Continue with continuation_id
result = mcp__pal__debug(
    step="Found evidence in logs showing connection pool exhaustion",
    step_number=2,
    total_steps=3,
    next_step_required=True,
    findings="Connection pool limit reached under load",
    hypothesis="Database connection pool too small for concurrent requests",
    confidence="high",
    continuation_id=result["continuation_id"]
)
```

## Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `step` | string | Current investigation narrative |
| `step_number` | int | Current step (starts at 1) |
| `total_steps` | int | Estimated total steps needed |
| `next_step_required` | bool | True if more investigation needed |
| `findings` | string | Evidence and discoveries |

## Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `hypothesis` | string | Current root cause theory |
| `confidence` | enum | exploring/low/medium/high/very_high/almost_certain/certain |
| `relevant_files` | list | Absolute paths to relevant files |
| `files_checked` | list | All files examined |
| `issues_found` | list | Issues with severity levels |
| `continuation_id` | string | Continue previous session |
| `model` | string | Override model (default: openai/gpt-5) |
| `thinking_mode` | enum | minimal/low/medium/high/max |

## Confidence Levels

- `exploring` - Just starting, no theory yet
- `low` - Early hypothesis, little evidence
- `medium` - Some supporting evidence
- `high` - Strong evidence for theory
- `very_high` - Very confident, need verification
- `almost_certain` - Nearly confirmed
- `certain` - 100% confirmed (skips external validation)

## Workflow Pattern

```
Step 1: State the problem and initial direction
        ↓
Step 2: Gather evidence, form hypothesis
        ↓
Step 3: Test hypothesis, refine or pivot
        ↓
Step N: Confirm root cause, propose fix
```

## Example: Database Connection Issue

```python
# Start
mcp__pal__debug(
    step="API returning 500 errors under load. Starting investigation.",
    step_number=1,
    total_steps=4,
    next_step_required=True,
    findings="Errors correlate with high traffic periods",
    hypothesis="Resource exhaustion under load",
    confidence="exploring",
    relevant_files=[
        "/app/api/routes.py",
        "/app/db/connection.py"
    ]
)
```

## Best Practices

1. **Start broad, narrow down** - Don't assume the cause upfront
2. **Document everything** - Track files checked, even dead ends
3. **Update hypothesis** - Revise as new evidence emerges
4. **Use continuation_id** - Preserve context across steps
5. **Set realistic steps** - Adjust total_steps as complexity reveals itself
