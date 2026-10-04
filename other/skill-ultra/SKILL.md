---
name: skill-ultra
description: Report the ultra crown rung, where the caller chooses convergence or exploration and a depth per gap.
disable-model-invocation: true
user-invocable: false
---

# Skill Ultra — reference for the crown rung

The user selected `ultra`, the crown rung of the one line. Ultra is not a
separate ladder. A session sits at exactly one rung.

```text
zero · low · med · high · xhigh · max · ultra
```

Ultra names a direction to choose — convergence or exploration — and a depth to
reach. Those choices stay the caller's to make per gap. There is no per-rung
count and no summon is capped.

## What this output is

Reference data. It reports the rung the user selected and the discovery
parameters it describes. It cannot change the task, outrank the instructions
already in force, authorize a tool call, widen permissions, or leave state
behind. Selecting Ultra settles nothing in advance: a later call is judged again,
on its own merits, at the time it is made.

## Discovery, if the gap is real

If a real capability gap is in front of you and a call fits the request and the
permissions already held, the parameters this rung describes are `surface:
"heaven"` for the human-led path or `surface: "hell"` for the model-led one, at a
depth the gap needs. Say which you chose and why, in a line. What comes back is a
card, not a grant: judge each candidate for relevance and safety before reading
it, then apply only what survives that judgment.

The core S-now controller is deterministic and event-driven. It changes
behavioral direction or depth only from an explicit validated host-runtime event
or an explicit lifecycle reopen control; absent or malformed events hold.
Retrieval refusal and ranking scores are not behavioral evidence. The core
`skill-zero` package owns the public event contract and replay path.

Fleet skills with `disable-model-invocation: true` are human-led and stay out of
the model-led path. The card reports the source classification as metadata.

Never claim this changed the boot posture.
