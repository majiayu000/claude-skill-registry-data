---
name: loop-breaker
description: Use when a long task has drifted into a frame the agent built for itself and stopped serving the owner's goal, even though each step checks out — endless sub-proofs of one component, polishing one property past the point it matters, re-planning a plan instead of delivering, or building tools for the tools. The strongest case is an agent that wrote a requirement into its own plan, labelled it as the owner's decision, and now works to satisfy a goal nobody asked for. Also use when the owner asks what the work is for, says it went in circles, says the agent pushed a requirement through, or says the agent lost the point. Not for ordinary debugging, where repeated attempts at one bug are expected.
---

# loop-breaker — leave a self-made frame

> Home branch in Memora: `root/skill/loop-breaker`.

## Choosing a part

| Situation | Part |
|---|---|
| Detect that work has drifted inward, then break out to one outward step | `parts/detect-and-break/` |

One part for now; open it when the situation above matches.

## Rules

- **Judge meaning, not counts.** Never detect a loop by counting keywords or mentions. Ask who uses the result of the step, and whether the owner asked for it in this turn.
- **Provenance of every requirement.** For the property being proven, quote the owner's own words that asked for it. A requirement that exists only in a plan, spec or checklist the agent wrote is the agent's proposal, even when the plan is marked as approved. Wholesale approval approves a document, not each invented line in it.
- **Every task carries an explicit priority.** Fix the order with the owner when the task is set: what serves the visible result, what can wait. A task with no assigned priority is asked about at once, not silently deferred and not taken first because the plan lists it first. Work follows the priorities, not the plan's own sequence. A fresh owner sentence cancels the item it contradicts, without discussion.
- **Answers to the agent's own options ratify a frame.** A choice made inside a list the agent wrote is not a requirement from the owner. Restating the goal beats another question batch.
- **Instrument before property.** Before proving a property of the product, prove the check runs on the same interpreter, binary, config and data as the product. A probe on a different environment measures the probe.
- **A pass that refutes itself closes the seam.** "My previous diagnosis was wrong" or "the finding did not reproduce" is the end of that seam, not the start of the next proof. Take one outward run instead.
- **Owner's words win.** When the owner has called a direction wrong, the next work starts from their direction, not from the last plan file the agent wrote.
- **Forks go to `ask_questions`.** When the next direction is a product choice (what to build, how much polish is enough), ask; the agent does not choose it alone after a loop is detected.
- **Record confirmed loops** in the memory tree under `root/skill/loop-breaker` with `outcome` and a pointer to the session.
- **Read sessions outside the project tree** (the host's session-log tool, `HOSTS.md`), never into it.

## Related

`review` (`parts/challenge`, `parts/self-reflection`, `parts/verify`), `planning`, `task-cycle`, `grill-me`.
