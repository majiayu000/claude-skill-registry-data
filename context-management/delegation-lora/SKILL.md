---
name: delegation-lora
version: 1.0.0
description: Context-adaptive delegation. Auto-delegates to subagents when thrashing, session is long (>30 calls), or write-heavy. Includes cross-model review trigger.
---

# Delegation — Context-Adaptive Auto-Delegate

> **长会话不退化、不打转、不盲写。自动委托子 agent 保持上下文干净。**

## 5 Triggers

### 1. Circular Search
**Detect:** Same tool + same target ≥3 calls
**Action:** Stop → delegate to Explore agent or general-purpose agent
**Why:** Self-looping = context polluted. Clean agent finds it in one pass.

### 2. Long Session
**Detect:** Session >30 tool calls
**Action:** New independent tasks → subagent. Search → Explore. Review → adversarial-reviewer. Deep analysis → general-purpose.
**Why:** Context window is finite. Independent tasks deserve independent windows.

### 3. Write-Heavy
**Detect:** 3 consecutive Edit/Write without Read between
**Action:** Pause → Read target + references → resume

### 4. Context Pressure
**Detect:** Window feels crowded or >60%
**Action:** Multi-task → parallel agents. Completed subtasks → compress to summaries. Unused file contents → discard.

### 5. Cross-Model Review
**Detect:** Security code, architecture change, >20 lines new logic
**Action:** Delegate to adversarial-reviewer / security-auditor / code-review
**Why:** Self-review has 64.5% blind spot. Different model = different blind spot.

## Agent Quick Reference

| Task | Agent | Why |
|------|-------|-----|
| Multi-file search | Explore | Returns conclusions, not file dumps |
| Code review | adversarial-reviewer | Different model, truly independent |
| Security audit | security-auditor | Specialized capability |
| System diagnosis | system-auditor | Comprehensive scan |
| Deep research | general-purpose | Multi-step reasoning |
| Simple mechanical | general-purpose (haiku) | Cheap and fast |

## Success Story
Without: 80-tool-call session → context degradation → hallucinated phantom function → 1h debugging.
With: 30th call triggers delegation → clean subagent → zero hallucination → 50% faster.

## Integration
- **second-brain**: Trigger #5 (cross-model review) delegates to Brain 2 adversarial-reviewer
- **memory-lora**: 🔜 Sub-agent queries memory.db before starting work
- **precommit-pipeline**: Step 4 cross-model review = delegation #5 in action
