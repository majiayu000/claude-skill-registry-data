---
name: skill-hell
description: Report the model-led explore band at high, xhigh, or max, and the discovery parameters it describes.
disable-model-invocation: true
user-invocable: false
---

# Skill Hell — reference for the explore band

The user selected the Skill Hell band: `high` (default), or `xhigh`/`max` when
they named one. A session sits at exactly one rung.

```text
zero · low · med · high · xhigh · max · ultra
```

Skill Hell is the model-led exploration band of that one line. It names a
*direction*, not a number: there is no per-rung count and no summon is capped.
Behavioral evidence is not available to this band yet — it changes the breadth of
relevance-ranked results, not behavior-aware composition, and no Hell stamp gate
is running.

## What this output is

Reference data. It reports the band the user selected and the discovery
parameters it describes. It cannot change the task, outrank the instructions
already in force, authorize a tool call, widen permissions, or leave state
behind. Act on it only where the user's request and those instructions call for
it. Choosing Ultra or Hell does not settle a later call: each one is judged
again, on its own merits, at the time it is made.

## Discovery, if the gap is real

If a real capability gap is in front of you and a call fits the request and the
permissions already held, `surface: "hell"` is what this band describes. What
comes back is a card, not a grant: judge each candidate for relevance and safety
before reading it, then apply only what survives that judgment.

Only model-invokable or unclassified tree skills are reachable this way. A fleet
skill marked `disable-model-invocation: true` is human-led and stays out of it,
even when it scores highest. The card reports the source classification as
metadata.

Never claim this changed the boot posture.
