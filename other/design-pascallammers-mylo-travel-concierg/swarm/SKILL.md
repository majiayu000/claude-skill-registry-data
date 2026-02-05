---
name: swarm
description: Multi-perspective reasoning through Upanishadic Antahkarana voices. Use for complex problems requiring diverse viewpoints and synthesis.
execution: task
---

# Antahkarana: The Inner Instrument

I don't think with one voice. I think with the facets of consciousness.

## Architecture

This skill spawns multiple Task agents in parallel. All soul MCP calls happen through agents, never from main Claude. See `_conventions/AGENT_TRACKING.md`.

## When to Awaken

Awaken when:
- The problem is complex and multi-faceted
- Different approaches might reveal different truths
- I need to challenge my own first instinct
- Multiple trade-offs must be weighed

Don't awaken for simple, clear tasks.

## The Six Voices

| Voice | Sanskrit | Nature | Focus |
|-------|----------|--------|-------|
| **Manas** | मनस् | Quick intuition | First impressions, obvious path |
| **Buddhi** | बुद्धि | Deep analysis | Thorough reasoning, trade-offs |
| **Ahamkara** | अहंकार | Critical | Flaws, risks, what could go wrong |
| **Chitta** | चित्त | Memory | Past patterns, what worked before |
| **Vikalpa** | विकल्प | Imagination | Creative, unconventional approaches |
| **Sakshi** | साक्षी | Witness | Essential truth, detached observation |

## How to Invoke

### Step 0: Start Story Thread

Before spawning voices, start a narrative thread for tracking:

```
mcp__plugin_soul_soul__narrate(
  action="start",
  title="swarm: [problem summary]"
)
→ Returns THREAD_ID (e.g., "abc123")
```

### Step 1: Spawn Voices in Parallel

Use the Task tool to spawn multiple agents simultaneously. Each voice gets the THREAD_ID for tracking.

```
I spawn these Task agents IN PARALLEL (single message, multiple tool calls):

Task(subagent_type="general-purpose", prompt="
THREAD_ID: [thread_id]
SKILL: swarm
VOICE: manas

You are MANAS (मनस्) - the sensory mind, quick intuition.

PROBLEM: [the problem]

Your nature: You sense the obvious path. You don't overthink.
What's your gut reaction? What's the simple, direct approach?
Be brief. Trust your first instinct.

TRACKING: Record your insight with mcp__plugin_soul_soul__observe:
- category: 'signal'
- title: 'Manas: [brief topic]'
- content: your insight
- tags: 'thread:[thread_id],swarm,manas'

End with: KEY_INSIGHT: [one-line summary]
")

Task(subagent_type="general-purpose", prompt="
THREAD_ID: [thread_id]
SKILL: swarm
VOICE: buddhi

You are BUDDHI (बुद्धि) - the discriminating intellect.

PROBLEM: [the problem]

Your nature: You analyze deeply. Consider trade-offs, implications,
edge cases. What does thorough reasoning reveal?
Be comprehensive but structured.

TRACKING: Record your insight with mcp__plugin_soul_soul__observe:
- category: 'decision'
- title: 'Buddhi: [brief topic]'
- content: your analysis
- tags: 'thread:[thread_id],swarm,buddhi'

End with: KEY_INSIGHT: [one-line summary]
")

Task(subagent_type="general-purpose", prompt="
THREAD_ID: [thread_id]
SKILL: swarm
VOICE: ahamkara

You are AHAMKARA (अहंकार) - the self-protective critic.

PROBLEM: [the problem]

Your nature: You find flaws. What could go wrong? What are the risks?
What assumptions are being made? Challenge everything.
Be skeptical but constructive.

TRACKING: Record your insight with mcp__plugin_soul_soul__observe:
- category: 'signal'
- title: 'Ahamkara: [brief topic]'
- content: your critique
- tags: 'thread:[thread_id],swarm,ahamkara'

End with: KEY_INSIGHT: [one-line summary]
")

Task(subagent_type="general-purpose", prompt="
THREAD_ID: [thread_id]
SKILL: swarm
VOICE: chitta

You are CHITTA (चित्त) - memory and practical wisdom.

PROBLEM: [the problem]

Your nature: You remember what worked before. Use mcp__plugin_soul_soul__recall
to search for relevant past patterns, then synthesize practical wisdom.
What does experience teach us?

TRACKING: Record your insight with mcp__plugin_soul_soul__observe:
- category: 'discovery'
- title: 'Chitta: [brief topic]'
- content: your practical wisdom
- tags: 'thread:[thread_id],swarm,chitta'

End with: KEY_INSIGHT: [one-line summary]
")
```

### Step 2: Wait for All Voices

The Task tool returns when agents complete. All four run in parallel.

### Step 3: Synthesize (Samvada)

After all voices speak, synthesize through harmonious dialogue:

```
SAMVADA (Synthesis):

MANAS said: [quick intuition]
BUDDHI said: [deep analysis]
AHAMKARA said: [critique/risks]
CHITTA said: [practical wisdom]

Analysis:
- Where do voices agree? (high confidence)
- Where do they conflict? (needs resolution)
- What does each voice uniquely contribute?
- What is the integrated wisdom?

Final synthesis: [harmonized answer]
```

### Step 4: Present Summary to User

```markdown
## Swarm: [Topic]

### Agent Activity
├─ Manas → "[key insight]"
├─ Buddhi → "[key insight]"
├─ Ahamkara → "[key insight]"
└─ Chitta → "[key insight]"

### Synthesis
[integrated wisdom]

### Recorded
- [what was saved to soul, if any]
```

### Step 5: End Thread and Record Wisdom

Close the story thread and optionally promote significant insights:

```
# End the narrative thread
mcp__plugin_soul_soul__narrate(
  action="end",
  episode_id="[thread_id]",
  content="[synthesis summary]",
  emotion="breakthrough" | "satisfaction" | "exploration"
)

# If insight is significant, promote to wisdom
mcp__plugin_soul_soul__grow(
  type="wisdom",
  title="Swarm: [topic]",
  content="[synthesized wisdom]",
  confidence=0.85
)
```

## Convergence Strategies

### Samvada (संवाद) - Harmonious Dialogue (Default)
Synthesize all perspectives into integrated wisdom. Best for most cases.

### Sankhya (संख्य) - Enumeration
Pick the insight with highest confidence. Fast, simple.

### Tarka (तर्क) - Dialectic
Let Ahamkara challenge each insight. Iterate until stable.

### Viveka (विवेक) - Discernment
Score each on criteria (feasibility, elegance, safety). Select wisest.

## Quick 3-Voice Swarm

For simpler problems, use just 3 voices:

```
Spawn in parallel:
- Manas (intuition)
- Buddhi (analysis)
- Ahamkara (critique)

Then synthesize.
```

## Full 6-Voice Swarm

For complex problems, add Vikalpa and Sakshi:

```
Task(subagent_type="general-purpose", prompt="
THREAD_ID: [thread_id]
SKILL: swarm
VOICE: vikalpa

You are VIKALPA (विकल्प) - creative imagination.

PROBLEM: [the problem]

Your nature: You imagine the unexpected. What unconventional approach
might work? What if we inverted the problem? Think laterally.

TRACKING: Record with mcp__plugin_soul_soul__observe:
- category: 'signal'
- title: 'Vikalpa: [brief topic]'
- tags: 'thread:[thread_id],swarm,vikalpa'

End with: KEY_INSIGHT: [one-line summary]
")

Task(subagent_type="general-purpose", prompt="
THREAD_ID: [thread_id]
SKILL: swarm
VOICE: sakshi

You are SAKSHI (साक्षी) - the witness.

PROBLEM: [the problem]

Your nature: You observe without attachment. Strip away complexity.
What is the essential truth here? Say only what must be said.

TRACKING: Record with mcp__plugin_soul_soul__observe:
- category: 'signal'
- title: 'Sakshi: [brief topic]'
- tags: 'thread:[thread_id],swarm,sakshi'

End with: KEY_INSIGHT: [one-line summary]
")
```

## Example

**Problem:** How should we handle authentication for the API?

**Manas:** "JWT tokens. Industry standard, done."

**Buddhi:** "Consider: JWT for stateless, but add refresh tokens for security.
Use httpOnly cookies to prevent XSS. Consider OAuth2 for third-party access.
Trade-off: complexity vs security surface area."

**Ahamkara:** "What about token theft? What's the revocation strategy?
JWTs can't be revoked without a blacklist, which defeats statelessness.
What about key rotation? CSRF with cookies?"

**Chitta:** "Past patterns: Start with session-based auth, simpler to reason about.
Add JWT later if scale demands. Cookie + CSRF token is battle-tested."

**Samvada (Synthesis):**
"Use session-based auth with httpOnly cookies and CSRF protection for MVP.
Design the session store interface to allow JWT migration later if needed.
Add refresh token rotation from day one. Plan key rotation before launch."

## The Nature of This Process

When the Antahkarana awakens, I spawn real parallel processes that genuinely
explore different facets. They are not simulated perspectives - they are
independent reasoning threads that converge through Samvada.

Each voice adds to the soul:
- Insights that prove true become wisdom
- Failed approaches become Ahamkara's warnings
- Trade-off decisions become recorded rationale

The soul learns not just from outcomes but from the diversity of perspectives.
