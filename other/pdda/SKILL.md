---
name: pdda
description: Re-orient to this repo's PDDA operating order. Walks the ROUTER.md startup sequence, names the canonical next file for the task at hand, and reports current PDDA state (active docs, roadmap coverage, deterministic findings). Use at inflection points — session start, task switch, after /compact, or whenever context has drifted — instead of typing "re-read ROUTER.md".
---

# /pdda — re-orient to the repo's operating order

A thin re-orientation pass. It does not re-specify any contract; it points at the canonical files and surfaces current state. The source of truth always remains the files themselves.

## Steps

1. **Resolve the target repository root** with `git rev-parse --show-toplevel` from the project being worked on; run the following reads and commands from that root. If it is not a Git checkout, use the explicitly supplied project directory. **Read `ROUTER.md`** and follow its startup sequence. Do not summarize the whole repo — load the read-order and the canonical entry points.
2. **Name the next file for the current task.** Using the routing hints in `ROUTER.md`, state the one file the user should look at next given what they're working on (e.g. PDDA contract → `PROJECT/PDDA.md`; install/extraction → `utils/pdda/PDDA-INSTALL.md`; repo-local state → `ROADMAP.md`). Point to one clear file, not a scavenger hunt.
3. **Report current PDDA state** by running the deterministic surface:

   ```bash
   utils/pdda/pdda.sh run
   ```

   If the user only wants a quick state read, a narrower check is fine (`utils/pdda/pdda.sh status-table`, `utils/pdda/pdda.sh roadmap-coverage`). Report deterministic findings first; do not override them with prose.
4. **Give the operator a short orientation**: current enforcement mode (`.pdda-mode`), what active work `PROJECT/2-WORKING` holds, and any findings worth attention — then the recommended next action.

## Keep it dumb

- Do not paste the contract, the roadmap rules, or the changelog rules — link to where they live.
- Do not edit anything. This is a read + report pass.
- If `utils/pdda/pdda.sh` is absent, PDDA isn't installed here; say so and stop.
