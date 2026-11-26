---
name: runs
description: Keep the recorded runs from filling the disk (rule 66). `log runs` lists every run under ~/.logCli/runs with its size, whether rea settled it and whether the request docs hold it; `log runs prune --apply` deletes the analysed ones, keeping each one's findings, steps and requests by domain. Use when the storage hook speaks, AdsPower says it is running out of disk space, or the owner asks to clear the runs.
---

# runs

Every action records a raw HAR (rule 19): a warm-up run is about 1.5 GB,
an inspect run up to 1.4 GB. On 2026-10-22 they reached 12.5 GB, the disk had
2 GB left and AdsPower refused to start Bethlehem's browser.

## The loop

1. **Analyse** (rule 25): a run may go only when rea settled it
   (`settle.json`: every step read, findings.md written) and the request docs
   hold its requests (`log capture docs` ran after it, kept in log.db).
   - Not settled: `log capture settle <its capture folder>`.
   - Not in the docs: `log capture docs`, then write any request's
     reasoning it asks for.
2. **Look:** `log runs` lists each run with `may go` or why it is kept, and
   counts those not in the docs.
3. **Prune:** `log runs prune --apply` (`--before <YYYY-MM-DD>` keeps the
   runs from that day on). First it takes every step's internal API calls
   out of its HAR (`exchanges.json`: what was sent and what came back, rule
   73), the same as `log runs exchanges` does for every run on disk. A run
   with a step HAR it can't read is not pruned. Each pruned run leaves:
   - `~/.logCli/runs/kept/<action>/<run>/`: findings.md, steps.jsonl,
     settle.json, pruned.json, goalFindings.md and .jsonl, every inspect
     step's `steps/<step>/exchanges.json`, `reading.json` and
     `readingState.json`, and every settle cut's
     `<browser>/steps/<step>.exchanges.json` (2 MB for 11 steps, against
     1.2 GB of HAR);
   - one line in `~/.logCli/runs/pruned.jsonl`: size, settled, documented, and
     its requests counted by docs domain (`groups`, `reels`, `checkpoint`…).

   A request's doc keeps what its pruned runs showed. The docs build folds
   every request's fields and sightings into `~/.logCli/rea/clientFacts.json`
   (local: run ids carry account ids). Each run is counted once, a request
   seen again only adds its new rows, and a field a later build couldn't read
   (the bundle wasn't captured) keeps what was known. Without the store, a
   request starts from its committed doc (`factsFromDoc`). The store also
   keeps each request's newest 3 real exchanges (one per step: what it sent
   and what came back, secrets and signed link tokens out, each cut to 6,000
   characters by depth), and its doc shows them under "What it sent and what
   came back". First seen
   2026-10-22: a rebuild after the prune had cut FBYRPTimeLimitsEnforcementQuery
   from 17 runs to 1.

## The hook

`scripts/hooks/storage.ts` (SessionStart, UserPromptSubmit, `src/agentHooks/registry`)
says in the agent's context when `~/.logCli/runs` holds over 2 GB or the disk
has under 5 GB free (`storageVerdict`), measured at most every 15 minutes.
`log runs space` prints the same.

## Tests

`bun test` loads `scripts/tests/preload.ts` (bunfig.toml), which points
`LOG_RUNS_DIR` at a scratch folder: tests never write into the real runs
again (the profile tests had left about 76 `galwayOne` folders there).

Code: `src/browser/runStore`, `src/cli/runs`. The requirements: [docs/specs/runsAndRea.md](../../docs/specs/runsAndRea.md).
