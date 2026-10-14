---
name: batch-subagents
description: Use many CLI agent workers for fixed highly parallel tasks.
---

# batch-subagents

Prompts/tasks should be pogramatically generatable from few dependant variables such as:
 - each agent reviews one file in a directory (1 variable)
 - for each concept and chapter in a text book, the agent identifies all other related concepts (2 variables)
 - For each edge in a knowledge graph an agent reviews its validity (1 variable)

Use the `cross-provider-subagent` skill for cli worker instructions

## Batch

Turn the independent work into jobs with stable labels. Through
exactly one parent-visible shell call, `xargs -0 -n 1 -P "$parallelism"` pool.
Construct and assess those

Keep each label, absolute workspace, and complete prompt as literal data in its
numbered job directory.

GNU `xargs` treats child exit 255 as a stop signal. Have each per-job wrapper
record the worker's real status and result under its job directory, then return
zero to `xargs` so every job can launch. Emit every stable label with its result
or visible failure, and return nonzero if the pool or any worker failed.
