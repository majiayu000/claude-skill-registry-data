---
name: run-batch
description: Run one planning batch - start an implementation agent per unit in its own worktree, log the times, merge, run the full checks once. Use when the user says "start batch N" or "run the next batch".
---

# Run a batch

Read `planning/batches/NN/README.md` and each unit file. Do not start a batch while the previous one has units that are not approved.

1. **Brief** each agent with: the unit file path; the code repo and how to make its own worktree and branch (named after the unit, from `main`; never work in `main/` or another unit's worktree); the project rules (code `AGENTS.md`); and these lines:
   - Run `date -u +%FT%TZ` when you start and when you finish; put both in your report.
   - Re-check the effort score of your unit; report any factor that is wrong and why.
   - Finish the whole unit. Do not build extra work. Write anything extra you find (bugs, missing pieces, better designs) as a new unit file in `planning/batches/proposed/` and name it in your report. If extra work blocks you, stop and report.
   - Follow the code repo rules: tests first (TDD), deep modules (interface and doc comment, then the test, then the code), product docs in ASD-STE100. Run the fast checks before you report. Take screenshots in a headless or agent mode if the unit changes what you see, and give their paths.
   - Report: what changed, how to test it, the screenshots, the timestamps, the effort re-check, the proposed units.
2. **Start** the 5 agents in parallel. Log each launch time in the time log (`planning/EFFORT.md`, Time log), with the effort before.
3. **When an agent reports**: log "agent done". Merge its branch into main (`--no-ff`); the unit with the protocol or format change merges last. Mark it merged in the batch README, and remove its worktree and branch.
4. **Breaking things** (build or CI fails, crash, format mismatch, data loss, core action broken): start a 6th agent on `fix-<name>` at once, merge it first, give it a unit file and a time-log row.
5. **Wave**: when all units are merged, run the full checks and the benchmarks once on main. Fix or report failures before the report.
6. **Next**: run `/batch-report`.
