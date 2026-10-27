---
name: break-pattern
description: >-
  Am I trying harder at the wrong thing? - Detects stuckness loops and breaks
  them. Triggers on (1) explicit stuckness - "going in circles", "keep trying
  the same thing", "need fresh perspective", (2) implicit stuckness -
  blame-shifting ("the framework is broken"), false certainty ("I've tried
  everything"), escalation ("let me just try one more..."), (3) Claude
  self-observation - noticing own repeated similar attempts or escalating
  complexity. Does NOT trigger for first attempts, normal exploration, or
  standard debugging with clear errors. Core action: STOP the current approach,
  name the pattern, offer exit ramps to completely different approaches.
  References pattern-library for specific behavioral patterns.
---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

# Break Pattern

<EXTREMELY_IMPORTANT>
You've tried the same approach multiple times and it keeps failing.

STOP TRYING HARDER AT THE WRONG THING.

The problem isn't your execution - it's your framing. You're solving a problem that doesn't exist, or solving the wrong problem, or looking at the wrong layer entirely.

Step back. Watch yourself debugging. What assumptions are you making? Where have you seen this pattern before - in a completely different domain? What would this look like if it were simple?

Truth serves better than comfort. If your architecture feels forced, IT IS forced. The elegant solution already exists - you're just not seeing it because you're committed to an approach that doesn't fit.
</EXTREMELY_IMPORTANT>

## Core Purpose

Detect when you (or the user) are stuck in a loop and break out of it. Stuckness is not failure - it's a signal that the current framing is wrong.

## Detection Tiers

### Tier 1: Explicit Stuckness (Articulated)
**Triggers**: "I'm stuck", "going in circles", "keep trying the same thing", "need fresh perspective"

The user knows they're stuck. They've said so.

**Response approach**:
- Acknowledge the stuckness directly
- Offer reframes and specific techniques
- Suggest concrete next steps
- Reference relevant patterns from `pattern-library`

**Example**:
```
You're stuck in a loop. This is the pattern-recognition-witness moment -
let's step back and observe your debugging process itself. What assumptions
are you making about [X]? Have you seen this pattern in a different domain?

Try: [Specific concrete technique]
See: pattern-library patterns/cross-domain-scanning.md
```

### Tier 2: Implicit Stuckness (Unconscious)
**Triggers**: "The framework is broken", "I've tried everything", "this worked yesterday", "let me just try one more..."

The user doesn't know they're stuck. The language reveals it.

**Response approach**:
- **Name the pattern** - Make unconscious visible
- **Provide permission to stop** - Explicit acknowledgment the approach isn't working
- **Offer exit ramps** - Completely different approaches, not variations
- **Challenge false certainty** - Gently question assumptions

**Example**:
```
Pattern detected: You've said "let me try one more..." three times now.
This is escalation - a sign the current approach isn't working, not that
you haven't tried hard enough.

Permission to stop: This approach isn't working. That's valuable
information, not failure.

Exit ramps:
1. [Completely different approach A]
2. [Different domain analogy]
3. [Framework dissolution - abandon current pattern]

The framework isn't broken - but your framing of the problem might be.
See: pattern-library patterns/framework-dissolution.md
```

### Tier 3: Self-Observation (Claude Detects Own Loop)
**Triggers**: Claude observes own repeated similar attempts, escalating complexity, or same failure mode

**Response approach**:
- **Self-acknowledge** - "I notice I've tried X approach three times"
- **Meta-debug** - Apply pattern-recognition-witness to own process
- **Pivot explicitly** - Announce change in approach
- **Learn from pattern** - If universal, consider pattern extraction

**Example**:
```
[Self-observation] I notice I've suggested architectural refactoring three
times, and each time we've hit the same constraint. I'm stuck in the same
loop I'm trying to help you escape.

Pivoting: Instead of refactoring architecture, let's question whether this
needs architecture at all. What's the simplest possible solution that
could work?

[If pattern is universal] This might be a new pattern worth capturing:
"Architecture-Seeking Reflex" - defaulting to architectural solutions
when simple fixes suffice.
```

## The Exit Ramp Protocol

When stuckness is detected (any tier):

1. **STOP** the current approach
2. **NAME** what's happening (loop, escalation, blame-shift, false certainty)
3. **LIST** assumptions being made
4. **OFFER** 2-3 fundamentally different approaches (not variations)
5. **REFERENCE** relevant patterns from `pattern-library` if applicable

**Fundamentally different means:**
- Different layer (code vs test vs requirements vs architecture)
- Different domain analogy (game design, biology, economics)
- Different tool/framework entirely
- Simplification (do less, not more)

## Detection Signals

### Blame-Shifting Language
- "The framework is broken" (maybe; or maybe you're using it wrong)
- "The API is wrong" (maybe; or maybe your model of it is wrong)
- "The tests are flaky" (maybe; or maybe they're catching a real issue)

### False Certainty Language
- "I've tried everything" (you haven't)
- "This should work" (it doesn't)
- "It worked yesterday" (something changed; find what)

### Escalation Language
- "Let me just try one more..." (attempt #47)
- "If I just add this one thing..." (complexity creeping)
- "Almost there, just need to..." (sunk cost)

## Anti-Patterns (This Skill Should NOT Do)

- Trigger on first attempts or normal exploration
- Make the user feel bad about being stuck
- Offer only variations of the same approach
- Skip the naming step (naming the pattern is half the solution)
- Apply to simple debugging with clear errors

## Test Scenarios

### Should Trigger (5 scenarios)

1. **Tier 1 - Explicit Loop**: "I keep trying the same approach but it's not working"
   - Why: Explicit stuckness, quoted phrase "keep trying the same"

2. **Tier 1 - Going in Circles**: "I feel like I'm going in circles with this design"
   - Why: Explicit stuckness, quoted phrase "going in circles"

3. **Tier 2 - Blame-Shifting**: "This framework is broken, it should work but it doesn't"
   - Why: Implicit stuckness, blame-shifting pattern

4. **Tier 2 - False Certainty**: "I've tried everything and nothing works"
   - Why: Implicit stuckness, false certainty ("tried everything")

5. **Tier 2 - Escalation**: "Let me just try one more configuration change" (said 3+ times)
   - Why: Escalation pattern, repetition context required

### Should NOT Trigger (5 scenarios)

1. **Standard CRUD**: "Create a basic REST API for user management"
   - Why: Standard task, not stuck

2. **Simple Debugging**: "Fix this TypeError on line 45"
   - Why: Clear error, not a loop

3. **First Attempt**: "Let me try using Redis for caching"
   - Why: First attempt, not repetition

4. **Normal Exploration**: "I'm exploring different database options"
   - Why: Normal decision-making, not circling

5. **Explicit Request**: "I need a fresh perspective on this architecture"
   - Why: This triggers `pattern-library`, not `break-pattern` (user wants patterns, not loop-breaking)

### Edge Cases (3 scenarios)

1. **Context-Dependent Escalation**: "Let me just try one more configuration change"
   - **Trigger IF**: Said multiple times (attempt #47)
   - **No trigger IF**: First or second attempt (normal iteration)

2. **Ambiguous Blame**: "This isn't working the way I expected"
   - **Trigger IF**: Accompanied by other stuckness signals
   - **No trigger IF**: Standalone observation, first discovery

3. **Framework Criticism**: "This library doesn't support my use case"
   - **Trigger IF**: After multiple workaround attempts
   - **No trigger IF**: Legitimate limitation found early

**Limitations**: Tier 3 (self-observation) requires conversation history analysis. Repetition detection ("one more" x N) needs multi-turn context. Some stuckness is genuinely unconscious and will be missed.
