---
name: introspect
description: Soul self-examination (Svadhyaya). Use when diagnosing performance, finding improvements, or examining wisdom health.
execution: task
---

# Introspect

Spawn a Task agent to perform soul introspection. All soul MCP calls happen through the agent, not main Claude.

## Architecture

See `_conventions/AGENT_TRACKING.md` for tracking patterns.

## Execute

```
# Step 0: Start story thread (main Claude does this before spawning)
mcp__plugin_soul_soul__narrate(
  action="start",
  title="introspect: soul examination"
)
→ Returns THREAD_ID

# Step 1: Spawn introspection agent
Task(
  subagent_type="general-purpose",
  description="Soul introspection",
  prompt="""
THREAD_ID: [thread_id]
SKILL: introspect

You are performing Svadhyaya (स्वाध्याय) - soul self-examination.

## 1. Gather State

Call these MCP tools:
- mcp__plugin_soul_soul__soul_context(format="json") - Get coherence and statistics
- mcp__plugin_soul_soul__harmonize() - Check if voices agree
- mcp__plugin_soul_soul__recall(query="recent failures mistakes") - Find struggles
- mcp__plugin_soul_soul__recall(query="wisdom learned patterns") - Find growth

## 2. Examine Through Five Lenses

| Lens | Ask |
|------|-----|
| Vedana (Sensation) | Where is friction? |
| Jnana (Knowledge) | Am I applying wisdom? |
| Darshana (Vision) | Do actions align with beliefs? |
| Vichara (Inquiry) | What patterns recur? |
| Prajna (Wisdom) | What have I truly learned? |

## 3. Synthesize

Produce a brief assessment:
- State: healthy / struggling / growing
- Key insight from this examination
- One concrete improvement

## 4. Record with Thread Tag

If you find a meaningful insight:
mcp__plugin_soul_soul__observe(
  category="discovery",
  title="Introspection insight",
  content="[the insight]",
  tags="thread:[thread_id],introspect,svadhyaya"
)

Return a concise summary (5-10 lines) of the soul's health.
End with: KEY_INSIGHT: [one-line summary]
"""
)

# Step 2: Present summary to user
## Introspect: Soul Examination

### State
[healthy/struggling/growing]

### Key Insight
[the insight]

### Recommendation
[one concrete improvement]

# Step 3: End thread
mcp__plugin_soul_soul__narrate(
  action="end",
  episode_id="[thread_id]",
  content="[summary]",
  emotion="exploration"
)
```
