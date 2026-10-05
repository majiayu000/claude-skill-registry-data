---
name: reasoning-lora
version: 1.0.0
description: Structured reasoning via sequential-thinking MCP. Forces explicit step-by-step analysis before coding for complex problems. Reduces rework on multi-step tasks.
---

# Sequential Thinking — Structured Reasoning

> **先想清楚再动手。复杂问题不跳步，每个 thought 一个判断。**

## Trigger

Any of → `mcp__sequential-thinking__sequentialthinking` first, then act:
1. Multi-step task (≥3 independent steps)
2. Uncertain approach (≥2 viable methods)
3. High-risk: delete, refactor, architecture, security
4. Complex diagnosis: unclear error, multiple possible root causes
5. User says "think", "analyze", "why"

## Template

```
thought: "Problem: [1 sentence]. Option A: [brief]. Option B: [brief]. Constraints: [list]."
thoughtNumber: 1
totalThoughts: 3
nextThoughtNeeded: true
# Adjust totalThoughts up if problem is more complex, down if simpler
```

## Principles

- One judgment per thought — don't pack multiple decisions
- Revise: wrong earlier thought → `isRevision: true`
- Branch: both directions worth exploring → `branchFromThought`
- Verify: final thought validates hypothesis → `needsMoreThoughts: false`
- Dynamic: more complex than expected → raise totalThoughts; simpler → lower

## Success Story
Without this skill: "Refactor the auth system" → jumped straight to code → 4 hours later realized wrong approach → rewrote everything.
With this skill: "Refactor the auth system" → 5 sequential thoughts → identified JWT-vs-session tradeoff → picked correct approach → 1 hour, first try.

## Integration
- **memory-lora**: Patterns found → stored for cross-session recall
- **delegation-lora**: "Need to search" → Explore agent. "Need review" → second-brain
- **second-brain**: Major reasoning decisions → Brain 2 validates approach
