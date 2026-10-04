---
name: performance-uefn-checklist
description: Short, actionable checklist of UEFN/Verse performance red flags (per-tick work, unbounded loops, uncached expensive calls, deprecated APIs). Read during project-bootstrap's A3 static review, or by coder/qa-regression when performance is specifically in question — not needed for routine feature work.
---

# UEFN performance checklist

Static red flags — this doesn't replace actually measuring FPS at playtest (`qa-regression`'s
job), it's what to look for when reading code before a playtest even happens.

- [ ] Work running every tick that could run less often, or only on a relevant event instead.
- [ ] Unbounded or growing loops/collections — spawning without a cap, arrays that only grow and
      are never trimmed.
- [ ] Expensive calls (actor spawn/destroy, MCP/device queries, distance or trace checks against
      many actors) inside a loop or a per-tick path instead of cached or throttled.
- [ ] Per-player work that scales badly with player count (an O(n²) pattern across players is
      the classic version of this).
- [ ] Heavy logic left running after it's no longer needed — not cleaned up on round end or
      device reset.
- [ ] Calls to a deprecated Verse/UEFN API or device feature (check `BUGS.md`'s "Deprecated
      functions" section and Epic's official docs if unsure — see `~/.claude/CLAUDE.md` rule 4).

Each hit goes in `Claude/docs/BUGS.md` as its own entry (title, where it is, likely impact,
suggested fix), noted as a static finding for `qa-regression` to confirm at actual playtest.
