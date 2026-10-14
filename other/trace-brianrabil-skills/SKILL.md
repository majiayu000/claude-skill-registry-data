---
name: plan-mode-trace
description: Follow one value through the system end to end. Use when explaining how something works, debugging a data flow, or verifying that a path exists as described.
license: MIT
---

# Trace

Explain how something actually works by following one concrete instance end to end, not by summarizing the architecture.

1. Pick one concrete instance to follow — a single request, record, or message with a real identifier. A trace of a real instance beats a description of the general flow.
2. Follow it forward through every hop: entry point, validation, transformation, storage, and exit. Name the file, function, or service at each hop. Do not skip a hop because it seems obvious.
3. At each hop, record what changes and what is preserved. Note where the instance could be dropped, duplicated, or reordered.
4. Report the actual path as an ordered list of hops with the code or config that implements each. Flag any hop you inferred rather than read.

A trace is read-only. If the instance cannot be followed end to end, report the exact hop where the path breaks.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
