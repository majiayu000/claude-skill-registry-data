---
name: plan-batches
description: Split enormous units, then order all planning units into batches of 5 that agents run in parallel, by priority, with dependencies always in an earlier batch. Use after new units are added, after scoring, or when the user asks to re-order or clean up the batches.
---

# Plan batches

Rules: `planning/batches/README.md`. No time estimates.

1. **Split enormous units.** For each unit scored 12 or more, split it into 2 or 3 units that each score 11 or less: by item group, by module, the protocol or format change on its own, or a spike or decision part first. Move the plan text verbatim (shared context goes to every part). Write new unit files, delete the old one, fix links and the `Depends on` lines of units that depended on it. Use one subagent per 2-3 units when there are many.
2. **Collect** for each unit: priority tier (breaking, user feel, user feature, developer tool, platform), effort level, protocol or format change (y/n), main files, dependencies. A unit that another unit needs inherits that unit's priority.
3. **Order**, batch by batch, from the units whose dependencies are all in earlier batches:
   - 2 low or med units by priority;
   - 1 high unit by priority;
   - 1 unit with the longest chain of work after it (sum of effort totals of its dependents);
   - fill to 5 by priority.
   - At most one protocol or format change per batch; avoid two units with the same main files.
4. **Write**: move the unit files into `batches/NN/`, update each `# unit (Batch N)` title, regenerate each `batches/NN/README.md` (levels, protocol change, the table), regenerate the batch list in `BATCHES.md` (each unit with its level and a one or two sentence description), and fix every link.
5. **Check**: no dependency in the same or a later batch; `python3 tools/check-links.py` gives 0 broken. Commit.
6. **Report**: the first 3 batches in a table, what moved and why, and anything that broke a rule.
