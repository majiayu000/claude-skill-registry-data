---
name: plan-mode-to-checklist
description: Index a body of work and fan out subagents to build a checklist from it. Use when a set of docs, plans, or artifacts must be turned into a checklist of everything to verify, do, or publish.
license: MIT
---

# To Checklist

Index the work, then fan out. A checklist built from an index is complete; a checklist
built from memory is a guess.

1. Read the body of work — the docs, plans, artifacts, or a directory to index. If the
   work is scattered, gather it into one place first.
2. **Index it.** Catalog every artifact: its type, its purpose, and what it requires to
   be done, verified, or published. Write the index to `docs/plans/index.md`. The index
   is the source of truth; the checklist is built from it, not from the artifacts
   directly.
3. **Fan out.** For each section of the index, spawn a subagent to build the checklist
   items for that section. Pass the subagent the index section and the relevant
   artifacts. The subagent returns checklist items — each with the action, the channel
   or location, and any dependencies. Parallelize the subagents; the index is what
   makes fan-out safe.
4. **Aggregate.** Collect the subagent outputs into a single checklist, ordered by the
   index. Deduplicate items that appear in more than one section.
5. **Review.** Check the checklist against the index: every indexed item must have a
   checklist entry. If an item is missing, spawn a subagent to close the gap.

A checklist is a record of what must be done, not a summary of what was made. If an
item is missing from the checklist, it will not be done.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
