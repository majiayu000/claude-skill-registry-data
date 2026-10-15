---
name: handoff
description: End a current-events-dashboard session or hand off mid-task — PROGRESS entry, ROADMAP ticks, the ≤80-line HANDOFF.md (rotate if replaced), commit, gate, push, the cold-start validation round when the page was replaced, then the validated resume prompt and the wrap-up message. Use at any wind-down, usage-cap break, or before saying "session closed".
---

# handoff

The runbook is `docs/HANDOFF_PROCEDURE.md`. Short form, in order:

1. **Clean stop.** Finish the unit or commit a named WIP state with the exact commands to continue.
2. **PROGRESS.md entry** (prepend, newest first): what changed; how it was verified (commands + results); what failed;
   your own corrections. Check it against its sources for dropped caveats.
3. **docs/ROADMAP.md:** tick finished tasks; make the next task concrete enough to start cold.
4. **HANDOFF.md** (≤ 80 lines; `node scripts/handoff_lint.mjs` must PASS). If the state or NEXT ACTION changed
   materially, REPLACE the page: append the old page whole to `HANDOFF_ARCHIVE.md` under `## ARCHIVED #N (YYYY-MM-DD)`,
   then write `## ⚑ LATEST #N+1 (YYYY-MM-DD) — title`. Keep exactly one `### ` action under `## NEXT ACTION`. Name no
   sha; never restate a number that lives elsewhere, link to it instead.
5. **Commit** each carrier as you write it.
6. `node scripts/ship_state.mjs` → obey → `node scripts/gate.mjs` → `git push origin main` (Windows git; G-003; the
   pre-push hook refuses main without a gate stamp). Don't edit the tree while the gate or a round runs.
7. **If HANDOFF.md changed at all** (replaced or edited): `ship_state` prints `ROUND-DUE` with the exact Workflow call
   (`.claude/workflows/coldstart-validate.js`). Run it, read `docs/coldstart/r<R>/RESULT.json`, act on it
   (routing FAIL → one page fix + re-round; content finding → fix, set `CONTENT-FIXED` with `content_fixes` and
   `content_fix_blob` (`git hash-object HANDOFF.md`), or re-round; any other page edit needs a re-round;
   TREE blockers → fix before stopping), commit the round directory, gate, push, until `ship_state` says
   `SHIPPED-CLEAN`. **Never surface the resume prompt before the round passes.**
8. **Surface** the canonical resume prompt from `CLAUDE.md` in a fenced block with the verdict line, e.g.
   "READY and FULLY VALIDATED: routing PASS (3/3 resumers, same first action), content PASS".
9. **Wrap-up message** (last message of the session): what shipped (live URL if it changed) and the pushes made;
   what was verified and how; what is still open; the recommended next step with its justification. Send a
   PushNotification with the one-line headline.
