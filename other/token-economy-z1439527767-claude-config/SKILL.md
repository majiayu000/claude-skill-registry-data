---
name: token-economy
version: 1.0.0
description: Token budget manager. Sets per-task token limits, routes simple tasks to Haiku subagents (70% savings), compresses skill chains for low-risk tasks, prunes stale context. Saves 50-70% tokens without quality loss. The brain's efficiency layer — sits between neural-orchestrator and skill execution. Triggers on every task.
---

# Token Economy — Efficiency Layer

> **"21 个 skill 不必全跑。L1 改个变量名不需要双脑审查。"**

## Token Budget by Task Tier

| Tier | Budget | Skill Activation | Model |
|------|--------|-----------------|-------|
| **L1: Trivial** | 500 tok | None. Direct execution. | Haiku subagent |
| **L2: Simple** | 2000 tok | reasoning-lora only (1-pass) | Haiku subagent |
| **L3: Complex** | 5000 tok | thinking-dimensions → reasoning-lora | Full model |
| **L4: Creative** | 10000 tok | divergent → thinking → reasoning | Full model |
| **L5: High-Risk** | 20000 tok | Full chain including failure-predictor + second-brain | Full model |

## Six Savings Mechanisms

### 1. Model Routing (biggest win — 50-70% savings)
```
L1-L2 tasks → Haiku subagent instead of full model
Haiku costs 70% less than Opus, 50% less than Sonnet
Quality impact: zero for L1-L2 tasks (simple, well-understood)
```

### 2. Skill Chain Compression
```
L2 task "add error handling to this function":
  Full chain: divergent → thinking-dims → reasoning → execute (5000 tok)
  Compressed: reasoning-lora 1-pass → execute (1500 tok, 70% saved)
```

### 3. Context Pruning
```
When context > 60% of window:
  → Trim conversation history older than 10 turns
  → Compress old tool outputs to 1-line summaries
  → Drop files no longer relevant to current task
```

### 4. Response Compression
```
L1: "Done. Renamed X to Y in file.ts."
L2: "Fixed. Added try/catch. Tests pass."
L3+: Full recap per compact.md #11
```

### 5. Verification Tiering
```
L1: No verification (trust the simple change)
L2: precommit-pipeline only (skip second-brain)
L3: precommit-pipeline + second-brain (skip skill-judge)
L5: Full verification chain
```

### 6. Cache Awareness
```
Same file read 3+ times in one session → cache in context, don't re-read
Same search query → use cached results
Same skill chain for same task type → reuse without re-routing
```

## Token Tracking

Log every task's token consumption:
```sql
token_log(task_type, tier, tokens_used, skills_activated, model_used, timestamp)
```

Weekly report:
```
=== Token Economy Report ===
Total saved: 45,000 tokens (38% of baseline)
L1-L2 Haiku routing: saved 28,000 tokens
Chain compression: saved 10,000 tokens
Context pruning: saved 7,000 tokens
Most expensive task type: architecture (avg 8,200 tok)
Most efficient: typo fix (avg 120 tok)
```

## Override

User can say "full analysis" or "deep dive" → bypass token economy, run full chain on any tier. Token economy is the default, not a gatekeeper.

## Integration
- **neural-orchestrator**: Token economy sits BETWEEN orchestrator routing and skill execution
- **brain-intuition**: Intuition + token economy = fastest path (L3 instinct skips everything)
- **brain-self-model**: Self-model feeds "I'm slow at X" → token economy pre-loads context for X
- **delegation-lora**: Token economy's model routing aligns with delegation (Haiku for simple)
