---
name: okr-review
description: Quarterly OKR review with key results scoring, progress tracking, and next quarter planning
auto_trigger: true
trigger_keywords:
  - okr review
  - review okrs
  - quarterly objectives
  - key results
  - okr progress
  - objective review
  - q1 review
  - q2 review
  - q3 review
  - q4 review
  - quarter review
  - score okrs
allowed-tools: Task, Read, Edit, mcp__flywheel__search_notes, mcp__flywheel__get_section_content, mcp__flywheel__get_note_metadata
---

# OKR Review

Run a quarterly OKR (Objectives and Key Results) review with progress tracking, scoring, and next quarter planning.

## Trigger Detection

Activate when user:
- Wants to review OKR progress
- Needs to score key results
- Is doing quarterly planning
- Asks about goal progress

## Examples

- "Review my Q1 OKRs"
- "Score my key results"
- "How am I doing on my objectives?"
- "Quarterly OKR review"
- "Review OKRs for 2026-Q1"

## Process

1. **Determine Quarter**
   - If quarter specified (e.g., "Q1", "2026-Q1"), use it
   - Otherwise, use current quarter

2. **Delegate to Agent**
   ```
   Task(
       subagent_type="okr-review-agent",
       description="Review OKRs",
       prompt="Review OKRs for [quarter]. Score key results and plan next quarter."
   )
   ```

3. **Present Results**
   - Objective scores (0-1.0)
   - Key result progress
   - Next quarter recommendations

## OKR Scoring Guide

| Score | Meaning |
|-------|---------|
| 0.0-0.3 | Failed to make real progress |
| 0.4-0.6 | Made progress but fell short |
| 0.7-1.0 | Delivered (1.0 = exceeded) |

**Note**: 0.7 is considered success in OKR methodology. Consistently hitting 1.0 means goals weren't ambitious enough.

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | N/A | Agent handles |
| 2. File Exists Check | N/A | Agent validates |
| 3. Chain Validation | N/A | Single delegation |
| 4. Mutation Confirm | N/A | Agent confirms |
| 5. MCP Health | N/A | Agent checks |
| 6. Post Validation | N/A | Agent verifies |
