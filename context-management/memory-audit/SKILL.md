---
name: memory-audit
description: Audit the project's persistent agent memories for backfire-risk, stale/superseded state, contradictions, redundancy, and bloat. Lists problems for the user to disposition - does NOT auto-correct. Surfaced on a 14-day cadence by a SessionStart hook. Use when the user asks to audit/review/clean up memories, or when the overdue reminder fires.
---

# Memory audit

Keep the memory store **true and non-backfiring**. Memories are loaded into every session, so a wrong, stale, or over-prescriptive entry silently steers behaviour. This skill runs a periodic review.

Surfaced every 14 days by `~/.claude/hooks/memory-audit-due.sh` (SessionStart), gated on `~/.claude/skills/memory-audit/.last_audit`.

## Run order

1. **Pre-pass (cheap, mechanical).** This also resets the 14-day timer:
   ```bash
   python3 ~/.claude/skills/memory-audit/scan.py
   ```
   It lists the project's memory files with age/size and shortlists stale-marker / bloat / oldest candidates, and prints the MEMORY.md index size vs budget. Derives the memory dir from cwd; pass `--dir <path>` to override.

2. **Dispatch read-only auditors in parallel** (one message, multiple Agent calls, for context hygiene). Batch the files by type (user-profiles + profiling-feedback / feedback-rules / project / reference) so each worker applies a consistent lens. Every worker prompt MUST say: READ-ONLY, do not modify; read full content (not skim); flag only problems; return `FILENAME - [CATEGORY, severity] one-line issue ("quote")`; end with a CLEAN list.

3. **Synthesise one LIST, grouped by category. Do NOT auto-correct.** The user dispositions; you correct only what they approve (then re-run scan.py / re-stamp).

## The rubric (weight BACKFIRE highest - it is the category to act on)

- **BACKFIRE** - a rule or profiling claim that, applied literally, degrades behaviour: over-prescriptive behavioural rule that makes the agent formulaic/lazy/over-cautious/rigid; over-confident profiling stated as fact (especially psychological); a rule that **inverts into harm** (e.g. "user fabricates framing" → distrust sincere statements; "user is blind to X" → condescend); pathologizing; self-fulfilling labels. Memories get deleted purely for this. When unsure, flag it.
- **STALE / SUPERSEDED** - describes work as planned/uncommitted/not-done/in-progress that has likely shipped; a "current state" snapshot that aged; or a claim contradicted by a newer memory. Flag as RISK (you usually can't verify against the live repo) with reasoning; cheap checks (`git log`, file existence) are worth doing.
- **CONTRADICTION** - two memories give conflicting instructions (name both). Cross-file; catch in synthesis.
- **WRONG** - an internal technical/factual claim that's dubious or overstated.
- **REDUNDANT** - substantially overlaps another memory.
- **BLOATED** - crams many distinct facts / too long to act on (one memory = one fact).
- **SENSITIVE** - records PII / secrets / home location / live credentials; flag for awareness.

## Notes

- Cross-check siblings before repeating a flag - if one worker calls a file clean and another flags it, reconcile.
- "List, don't correct" is the default end state. Corrections are a separate, user-approved step -  correct on falsification, don't churn for refinement.
- After applying approved corrections, re-run `scan.py` (resets `.last_audit`) so the next surfacing is 14 days out.
