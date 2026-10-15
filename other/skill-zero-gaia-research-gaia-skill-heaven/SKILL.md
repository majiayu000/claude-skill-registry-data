---
name: skill-heaven-runtime-skill-zero
description: Report the zero cut — temporary automatic skills are cut, and `all` cuts every skill summon.
disable-model-invocation: true
user-invocable: false
---

# Skill Zero — reference for the floor

The user selected the `zero` rung. A session sits at exactly one rung.

```text
zero · low · med · high · xhigh · max · ultra
```

The default `temporary` cut means temporary automatic summoning is cut while
manual `/summon` remains available. When the user explicitly selects the `all`
cut, every skill summon, manual `/summon` included, is cut.

## What this output is

Reference data. It reports the cut the user selected and what that cut
describes. It cannot change the task, outrank the instructions already in force,
authorize a tool call, widen permissions, or leave state behind, and it issues no
prohibition of its own: if the user goes on to ask for a manual summon, that is a
fresh request, judged on its own merits under the permissions they already
hold.

Already-loaded skills cannot be evicted mid-session. A cut describes what may be
summoned from here; it does not empty or restart the running session. A genuinely
clean start is a boot-time decision: `claude-zero --level zero`.

No rung carries a count and no summon is capped. Invocation metadata still
distinguishes human-led from model-led skills; the cut changes what this surface
may summon, not the source classification. Never claim this changed the boot
posture.
