---
name: distill
description: Distill content with 5-level granularity, showing quality loss estimation before execution
argument-hint: <path|type> [level]
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# /distill - Content Distillation

Reduce content size while preserving critical information. Shows quality loss estimation before execution.

**Out of scope**: Conversation context (use built-in `/compact`)

## Granularity Levels

| Level | Name | Target Reduction | Preserves | May Remove |
|-------|------|------------------|-----------|------------|
| 1 | `essence` | 85-95% | Identity only | Everything except core purpose |
| 2 | `summary` | 70-80% | + Behavior | Reasoning, examples, context |
| 3 | `condensed` | 45-60% | + Reasoning | Verbose examples, redundant explanations |
| 4 | `detailed` | 25-40% | + Context | Redundant phrasing, verbose wording |
| 5 | `minimal` | 10-20% | All facts, rules, examples, structure | Filler words, redundant phrasing, excessive formatting |

## Criticality Heuristics

Priority order for preservation (highest → lowest):

| Content Type | Criticality Order |
|--------------|-------------------|
| policy | Rules > Priority > Rationale > Examples > Detection |
| code | Signatures > Logic > Types > Comments > Formatting |
| memory | Facts > Decisions > Reasoning > Timestamps > Verbose |
| artifacts | Requirements > Criteria > Rationale > Background > Examples |
| default | Critical > Important > Helpful > Context > Lossy |


## Workflow

### 1. Run Estimation Script

```bash
.claude/skills/distill/scripts/estimate_distill.py "$FILE" [content_type]
```

### 2. Present Results & Confirm

```
/distill global/policy/RULES.md

Tokens: ~4364

| Level        | After | Reduction | Critical Loss |
|--------------|-------|-----------|---------------|
| 1. essence   | ~654  | 85%       | ~35%          |
| 2. summary   | ~1527 | 65%       | ~15%          |
| 3. condensed | ~2400 | 45%       | ~5%           |
| 4. detailed  | ~3273 | 25%       | ~2%           |
| 5. minimal   | ~3709 | 15%       | ~0%           |
----------------------------------------------------

Select level [1-5/cancel]:
```

### 3. Execute Distillation

Remove ONLY what "May Remove" permits for selected level.

**Self-check**: If removing content not in "May Remove" column → STOP, wrong level.

### 4. Verify & Report

After writing, measure actual tokens:

```bash
.claude/skills/distill/scripts/estimate_distill.py "$FILE" [content_type]
```

Report (compare against initial estimation, not generic range):
```
Before: 4434 tokens → Estimated: 2858 tokens (35% reduction)
Actual: 2621 tokens (41%) | Variance: +6%
```

If variance >10%, warn and offer git restore.

### 5. Output Location

- **Git-versioned files**: Replace original (git tracks history)
- **Serena memories**: Archive old as `<name>_archived_<timestamp>`, write new

## Anti-Patterns

- Distilling without estimation first
- Removing content not permitted by level's "May Remove"
- Not verifying actual vs target reduction
- Skipping user confirmation
