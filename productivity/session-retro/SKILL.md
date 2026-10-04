---
name: session-retro
description: Synthesizes evidence-grounded lessons from the current session and routes them through a log→promote→retire lifecycle so they change future behavior. Use when the user says "retro", "reflect on this session", "lessons learned", "takeaways", or at a session boundary / after a milestone or postmortem-worthy failure.
---

# Session Retro

Extract lessons from THIS session, grounded in quoted evidence, and disposition each one through a lifecycle. Never freeform-reflect: self-generated narrative lessons measure at +0.0pp downstream benefit (curated: +16.2pp) and confabulate under sparse feedback. The template and the lifecycle are the mechanism, not the prose. Evidence basis: [REFERENCE.md](REFERENCE.md).

## Hard rules

1. **Evidence or it didn't happen.** Every lesson quotes a verbatim signal from this session's transcript: a command's output line, an error, a user correction, a diff. A lesson you cannot anchor to a quote is discarded, not softened.
2. **Blameless framing.** Describe the condition that allowed the outcome ("probe measured from origin because the GO name mismatched"), never fault ("I carelessly…"). Blame framing degrades the honesty of the raw input.
3. **No promotion from a single episode.** First occurrence → dated log entry only. Promote at 2 occurrences for user corrections, 3 for self-observed patterns.
4. **Session boundaries only.** Run after work concludes, never mid-task — mid-task reflection compounds in-progress misdiagnosis.
5. **Self-assessment is not a signal.** "The fix worked" counts only if a tool result in the transcript shows it. Otherwise the lesson's outcome field is UNVERIFIED.

## Workflow

### 1. Gather (before writing anything)
Sweep the session for these signal classes; collect verbatim quotes:
- User corrections and constraints ("don't / only / stop / actually…", rephrased requests)
- Failures: non-zero exits, tracebacks, failed edits, denied permissions, reverted work
- Repeats: the same fix attempted 2+ times, the same file re-read, the same question re-asked
- Surprises: output contradicting a stated prediction; `ATTEMPT:` entries in docs/STATE.md
- Wins worth keeping: an approach that verifiably worked where a prior one failed

### 2. Draft candidates (forced template — all five fields or discard)
```
LESSON: <one-line behavior change, imperative>
EVIDENCE: <verbatim quote + where it occurred>
CONDITION: <what allowed it — system/process, not blame>
APPLIES-WHEN: <trigger context for the lesson>
STOPS-APPLYING: <what would make it obsolete>
STATUS: candidate | OUTCOME: <verified signal, or UNVERIFIED>
```

### 3. Disposition each candidate
Read `lessons-log.md` in the memory directory (system prompt lists the path; create the file with a `# Lessons log` header and a MEMORY.md pointer line if absent).
- **New** → append dated entry to `lessons-log.md`. Nothing else.
- **Recurrence hit** (grep log + MEMORY.md for the same failure shape; threshold per Hard rule 3) → promote: write a `feedback`/`project` memory file per the memory-system format, link `[[lessons-log]]`, add its MEMORY.md index line, and mark the log entries `PROMOTED → <file>`.
- **Contradicts an existing memory** → flag both to the user; never silently overwrite.

### 4. Retire (the pass that keeps the system alive)
Scan `lessons-log.md` and promoted memories for: entries `STOPS-APPLYING` now true, entries 10+ sessions old never recurring and never promoted, promoted lessons whose behavior change demonstrably never fires. Propose each for deletion (list them; user approves — deletion is a hard stop). Cap check: MEMORY.md index growing past ~30 lines or the log past ~100 entries means retirement is overdue — say so. Do not build separate dedup machinery; retirement subsumes it.

### 5. Close the loop
A promoted lesson is **applied**, not done. Its memory file keeps `STATUS: applied` until a later session's retro finds evidence it actually fired (behavior changed, mistake not repeated) → `STATUS: verified`, or fired wrong → retire it. When checking recurrence in step 3, also check open `applied` lessons for firing evidence.

### 6. Report
Terse table to the user: lesson | disposition (logged / promoted / retirement-proposed / contradiction-flagged) | evidence quote. No narrative recap of the session. Lessons the user pushes back on are deleted, not argued.

## What this skill is not
Not a session summary (that's docs/STATE.md), not auto-memory's per-fact capture, not a place for facts the repo already records. One writer: only this skill appends to `lessons-log.md`.
