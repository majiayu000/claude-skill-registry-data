---
name: "speckit-roundtable"
description: "Argue a decision from several named positions — the person who has to maintain it, the person who has to use it, the person paying for it, the person attacking it — and record the disagreement rather than averaging it away. Use for a decision with real trade-offs that one reading keeps resolving too easily."
argument-hint: "The decision, in a sentence. Optionally the positions to seat."
compatibility: "Read-only. Produces a transcript and a recommendation; changes nothing."
metadata:
  author: "speckit-demo"
  source: "adapted from BMAD's bmad-party-mode / multi-agent discussions"
user-invocable: true
disable-model-invocation: false
model: opus
---

## User Input

```text
$ARGUMENTS
```

## Why this exists

A single reasoner resolves trade-offs too early and too quietly. It picks the
option it thought of first, then writes the justification. BMAD's answer is to
run the discussion with several personas in character; the value is not the
role-play, it is that **the disagreement gets written down** instead of being
averaged into one confident paragraph.

This is deliberately not a subagent fan-out. The existing reviewers
(`spec-challenger`, `code-reviewer`, `spec-reviewer`) already give independent
readings of an artifact that exists. This is for a decision that has not been
made yet, where the cost is in the trade-off and not in the evidence.

## Seat the table

Four positions by default. Use the ones with something at stake in *this*
decision, and add a domain-specific one when it is obvious.

| Position | What it argues for | What it will sacrifice |
| --- | --- | --- |
| **The maintainer** | the version still legible in a year; fewer moving parts | short-term convenience, cleverness |
| **The user** | the behaviour they can predict from the outside | internal elegance |
| **The sceptic** | the smallest thing that could work; does this need to exist? | completeness, future-proofing |
| **The attacker** | what happens under malformed input, concurrency, interruption, scale | ergonomics |

## Run it

1. **State the decision as a choice**, with at least two named options. "Should
   we improve X" is not a decision; "A or B, and what we lose either way" is.
2. **One round, each position in turn.** Two to four sentences. Each must name
   the option it backs and the cost it accepts. No position is allowed to agree
   with everything.
3. **One rebuttal round**, only where positions actually conflict. Skip it where
   they do not — a manufactured argument buries the real one.
4. **Name the disagreement that survives.** If every position converged, say so
   plainly; that is a real and useful result, not a failed exercise.

## Output

```
Decision: <A or B>

Maintainer: <position, cost accepted>
User:       <…>
Sceptic:    <…>
Attacker:   <…>

Unresolved: <the disagreement that survived, or "none">
Recommendation: <option>, because <the consideration that outweighed the rest>
Rejected: <option>, which would have been right if <condition>
```

That last line is the point. A recommendation with no stated condition under
which it flips is a preference wearing a suit.

## Boundaries

- It decides nothing and writes no file. Hand the result to `/speckit-specify`,
  `/speckit-correct-course`, or the user.
- It does not spawn subagents. Constitution II: an orchestration nobody asked
  for is cost, not rigour.
- Four positions, one round, one rebuttal. A roundtable that runs long stops
  being read, and an unread transcript is worse than no transcript.
