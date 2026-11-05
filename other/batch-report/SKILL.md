---
name: batch-report
description: Write the REPORT.md of a merged planning batch - per unit what changed, times, effort estimated vs actual, stats, screenshots, how to test, proposed units. Use after a batch has merged and passed its checks, and after each change round.
---

# Batch report

Write `planning/batches/NN/REPORT.md`. One section per unit:

```markdown
## `unit`

- **Merged:** <sha>
- **What changed:** what a user, an admin or a developer now sees or can do, in plain words; then the main files.
- **Time:** launched <time>, agent done <time>, merged <time>; agent time <h:mm> (pauses named and taken out).
- **Effort:** estimated <level> (U1 M1 ...), actual <level> (U2 M1 ...). The factor that was wrong and why.
- **Stats:** files, lines added and removed, areas, commits (`python3 tools/unit-stats.py <sha> <code repo>`).
- **Screenshots:** `shots/<unit>-*.png` (copied from the agent's paths), or "none: no visible change".
- **How to test:** the commands and the steps to check it yourself.
- **Proposed:** the new units in `proposed/` from this work.
```

At the end: the wave results (checks, benchmark numbers next to the last wave) and anything open.

Then fill the time log rows (agent time, effort after, the wrong factor, stats). For a change round, update the unit's section: add a `Round N` line with what changed, the time, and how to test the changes.

Tell the user: the batch is ready to test, one line per unit with its "how to test", and where to write the review (the `## Review` section at the end of each unit file).
