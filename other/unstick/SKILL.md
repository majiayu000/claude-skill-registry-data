---
description: When you're stuck on a problem - get unstuck fast
argument-hint: "[what you're stuck on]"
allowed-tools:
  - Read
  - Agent
  - Grep
  - Glob
  - WebSearch
---

Break through a block. Uses the Unsticker agent for root-cause analysis and fresh approaches.

## Steps

### Step 1: Capture the stuck state

If the user described what they're stuck on, use that. Otherwise, infer from:
- Current memory.md → Now
- Recent daily note entries
- Last few tool calls in context

Articulate the block in one sentence: "I'm stuck on [X] because [Y]."

### Step 2: Classify the block

| Type | Signals | Approach |
|------|---------|----------|
| **Knowledge gap** | "I don't know how to..." | Search docs, read source, check knowledge-base |
| **Decision paralysis** | "I can't decide between..." | List tradeoffs, pick the reversible option |
| **Circular debugging** | Same error 3+ times | Step back, restate the problem, try opposite approach |
| **Scope confusion** | "This is bigger than I thought" | Yak-shave check — are you solving the right problem? |
| **Environmental** | Build/deploy/config issues | Check logs, verify prerequisites, try clean state |

### Step 3: Deploy the Unsticker

Spawn the unsticker agent:

```
Agent(unsticker): I'm stuck on [problem].

What I've tried: [list attempts]
Error/symptom: [what's happening]
Expected: [what should happen]

Break this down. What am I missing?
```

### Step 4: Execute the suggestion

Take the unsticker's top recommendation and try it immediately.
Don't deliberate — act. The fastest way out of stuck is through.

### Step 5: Log the resolution

If resolved, add to daily note:
```markdown
### Unstick — HH:MM
- **Block:** [what was stuck]
- **Root cause:** [why]
- **Fix:** [what worked]
```

If the fix reveals a pattern, nominate to knowledge-nominations.md.
