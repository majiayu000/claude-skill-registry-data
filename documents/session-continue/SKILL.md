---
name: session-continue
description: "Use at session start to resume in-flight work — reads the root SESSION-STATE/ carry ledger and orients. Carries present → pick one (surface the list when several sessions are in flight), follow its Read first into the card it names and read the latest block of each type as the lead, reconstruct where work stopped + the next step, confirm before diving in. None, or the picked carry pointing at gone targets → report no in-flight carry and hand off to /super-bootstrap:needs-me. Claims the picked carry — renames it to this session's id so whoever resumes the work also owns closing it; unpicked carries and every carry body stay untouched. No argument; reads current session state. Mirror of /super-bootstrap:session-close."
tags: [session, resume, carry, ledger, session-opener]
---

# Session Continue — Cold-Open Orientation

Mirror of `/super-bootstrap:session-close`: it lands the carry, this picks it up. The read side of the cold-pickup test — "can a cold session orient from files alone?" — run as a procedure. **Consumer** of the `SESSION-STATE/` ledger — reads every carry in it, claims the one the user picks, leaves the rest as found. Naming, slots, and conflict handling follow session-close's § Ledger convention.

## Two entry states

| Detected state | Shape |
|---|---|
| Root `SESSION-STATE/` holds ≥1 carry, the picked one's pointers resolve | **resume** — reconstruct that carry, confirm the next step |
| Folder absent or empty, OR every carry names gone targets | **cold-orient** — no in-flight carry to take; hand off to `/super-bootstrap:needs-me` |

## Protocol

The gateway runs this inline — it reads the live session's root and docs in its own context, dispatches no subagent, pins no model.

### 1. Read the ledger

List root `SESSION-STATE/` with `ls` (or Read a concrete path) — an empty glob result is not evidence of absence, so gate on a listing that errors loudly. Any carry file → **resume**. Folder absent or empty → **cold-orient**.

Read every carry file. Each is one session's independent carry: an empty or conflict-marked file is dead on its own terms and leaves its siblings fully valid.

A root `SESSION-STATE.md` left by the single-file contract reads as one more carry — offer it alongside the rest.

### 2. Resume — pick a carry, then reconstruct

Exactly one live carry → take it. Several → surface the list (label, anchor, next step, last-modified) and let the user pick; the others stay as found. A carry whose owning session is long gone still reads as a normal carry — offer it with its age and let the user resume, leave, or clear it.

**Claim the taken carry** — rename it `<label>-<this-session-id>.md`: label kept, id replaced, content untouched. The pick is the gate: a carry nobody took keeps its author's id, and a live session's carry is only claimable when the user — who alone knows what else is running — hands it over.

The carry holds the volatile delta + pointers; the card holds the durable state. Reconstruct the picked carry:

- Parse the convention's slots.
- **Follow Read first** — open each card it names (`docs/work/{ID}.md`) and read the cold-reader read set `docs/work/README.md` § Thread contract names as the lead, the latest `## Progress` as the resume point (done step, next step, binding watch-outs). Then any other doc it names. The picture is the card's current truth, not the carry's echo.
- **Test each pointer** — a card ID or doc path that no longer resolves is a gone target (a deleted card = resolved). Any load-bearing pointer gone → that carry is stale; say why, then offer the remaining carries, or drop to **cold-orient** when none is left.

### 3. Cold-orient — no carry

No carries, or every one stale → report "no in-flight carry" and hand off to `/super-bootstrap:needs-me`. `docs/work/` absent → "No runway installed. Run `/super-bootstrap:setup`." instead.

### 4. Surface + confirm

Surface the reconstructed picture: where work stopped, the next step, the watch-outs — card first, carry delta beside it. Then **confirm the next step before executing** — this skill orients and hands back; it does not auto-dive. A confirmed card resumes as pickup — framing line + route per `CLAUDE.md`.

## Output

- The shape taken (resume / cold-orient), the reconstructed picture (anchor, card lead, next step, watch-outs), and any gone pointers that forced a fallback.
- Every carry found, when more than one — so the user sees what the other sessions are holding, not only the picked one.
- Resume: the claimed filename and the next step echoed for confirmation. Cold-orient: that no carry was in flight, and the needs-me handoff.

## Rules

- **Claim on pick, bodies read-only.** The rename that claims the taken carry is this skill's one write — bodies stay as authored (rewrite is session-close's park, delete its done-close), and untaken carries stay as found.
- **Orient, don't dive.** Reconstruct the picture and confirm the next step; the user launches the work.
- **Card leads, carry trails.** Read the card's per-type lead blocks before trusting the carry's State; where they disagree, the card wins.
- **Stale carry falls back.** A load-bearing pointer to a gone target invalidates **that** carry — offer the siblings, or cold-orient when none remain. Name the gone pointer; never resume onto a dangling reference.
- **One dead carry leaves the rest alive.** Staleness, emptiness, and conflict markers are per-carry verdicts, never grounds to discard the ledger.
- **Inline procedure.** No argument, no subagent, no model pin.
