---
name: dream-cycle
description: Use for the nightly Dream Cycle.
---

# Dream Cycle

The agent "sleeps": each night cron job `dream-cycle` (03:30) runs `scripts/dream_cron.py` → `scripts/dream_cycle.py`:

1. **REM replay**: reads all user/assistant messages of the day from `state.db`
2. **Fragment extraction**: pulls error/exception fragments via regex
3. **Motif detection**: matches against lexicon in `MOTIFS` dict (timeout, permission, auth, build, api-rate, memory, path-bug)
4. **Nightmare detection**: motif seen on 3+ prior days → becomes an *intention* (fix at root)
5. **Output**: upsert into `dreams.json` + `reports/dream-YYYY-MM-DD.md`, report delivered by cron

## Extending
- Add motifs to the `MOTIFS` dict in `scripts/dream_cycle.py`
- Manual replay: `python scripts/dream_cycle.py 2026-08-31`
- Schema gotcha: `messages.timestamp` is REAL unix epoch — use `date(timestamp,'unixepoch')`.

## Morning routine
Read latest `reports/dream-*.md`; act on nightmare-intentions first (root fix, not symptom).
