---
name: blender-mcp-phased-build
description: Use when supervising a multi-phase Blender build (a character, prop, or rig) that is actually executed by a separate Claude Code + blender-mcp terminal session, while this session only has file-level access to the project folder (e.g. via a device bridge). Enforces one-phase-per-message hand-offs, direct image verification of every render instead of trusting text self-reports, file-based delivery of fix instructions to avoid terminal paste corruption, and a time-boxing rule so cosmetic issues don't consume the whole build.
---

# Blender MCP Phased Build — Supervisor Skill

## When this applies

You (the supervising session) do NOT have a live Blender MCP tool. The actual
`execute_blender_code` calls happen in a separate Claude Code terminal session
the user runs themselves. You only have file-level access to the shared
project folder (list/read/stage/commit). Your job is to act as the build's
reviewer and project manager: hand out one phase at a time, independently
verify every claimed result by looking at the actual rendered image, catch
regressions the executor's own summary missed, and keep the build moving
under real time pressure without letting polish work stall structural work.

Do not attempt to run Blender code yourself. If no such tool is available in
this session, don't search for one — route all execution through the user's
terminal session.

## Setup checks (do once, cheap)

- Confirm the bridge is live with a plain directory listing on the project
  root or its output folder — this doubles as an "are we still connected"
  check without asking the user to test anything.
- Compare file mtimes against what you last saw. A newer `.blend` save or new
  `preview_*.png` files mean work already happened even if the user hasn't
  pasted anything yet — check before asking "did you run it?" or assuming the
  terminal is idle.
- Identify the pre-existing safe fallback deliverable (an already-working
  export, a prior good save) and treat it as untouchable for the rest of the
  build unless the user explicitly says otherwise.

## The core loop, one phase at a time

1. **Send exactly one phase's instructions per message.** Never bundle two
   build phases into one instruction, even if the user is in a hurry — a
   failed phase 2 in the middle of a phase 2+3 instruction is much harder to
   isolate and fix than a failed phase 2 alone.
2. **Tell the executor what to render and where to save it** (explicit file
   names like `preview_phaseN_front.png`, `preview_phaseN_side.png`, plus any
   close-up the phase specifically needs), and tell it to stop and wait after
   rendering rather than cascading into the next phase on its own.
3. **When the user reports back** (pasted terminal output, or just "done"),
   do not accept the text summary as ground truth. Stage every rendered image
   this phase produced and view each one directly before deciding pass/fail.
   A model's own "looks clean" or "follows the curvature" is not evidence —
   only the pixels are. This single habit is what catches regressions the
   executor didn't notice (an inverted silhouette, a missing signature
   element, a flat plate where curvature was claimed, geometry that's present
   in name only).
4. **Check multiple angles when a single angle can hide the defect.** A front
   view alone can make a flat plate look curved; a silhouette bug can be
   invisible from the "wrong" side. If the phase's spec calls out a specific
   view as the one that matters, treat that view as the actual test, not a
   nice-to-have.

## Fix-instruction delivery (avoid terminal paste corruption)

If a phase needs correction, do not paste a long fix instruction back through
the chat for the user to relay — long pasted text into a terminal session
reliably gets fragmented or interleaved. Instead:

1. Write the fix as its own short, self-contained `.md` file (root-caused
   problem, the specific fix, and what to verify afterward).
2. Deliver it with `SendUserFile`, then write it into the project folder so
   the executor session can read it directly.
3. Give the user a single short line to paste into their terminal, e.g.
   `Read phaseN_fix.md in the project root and follow it.` — never the fix
   content itself.

This keeps every instruction the executor receives byte-exact, and keeps a
durable paper trail of exactly what was asked for at each step.

## Time-boxing rule (critical under deadline pressure)

- **One corrective pass per issue, then move on regardless of outcome** for
  anything cosmetic or non-structural (surface polish, a decorative element,
  a boundary that's slightly rough). State plainly in the fix instruction that
  the executor should proceed to the next phase after this pass whether or
  not the result is perfect.
- **Escalate instead of iterating a third time.** If a *structural* problem
  (not cosmetic) has failed two different technical approaches, stop silently
  retrying and put the decision to the user explicitly (e.g. "keep pushing on
  approach X, or fall back to the simpler Y") rather than burning a third
  attempt on your own judgment.
- If an optional/decorative detail has produced multiple consecutive defects,
  drop it entirely rather than fixing it again — structure and silhouette
  matter more than an optional detail, and time spent polishing something
  that might get cut later is time the deadline can't afford.

## Sequencing multiple build/polish documents

If the work spans more than one prompt/spec (e.g. a full build prompt, then a
separate later-stage polish prompt), do not merge them into one document even
if they sound similar. Keep them sequential and independent:

- Add an explicit **interface contract** to the first document: exact output
  filenames, required object/bone/animation names, export settings, and any
  other detail the second stage depends on.
- Add an explicit **handoff condition**: the exact state that means "stage one
  is done, safe to start stage two."
- Only introduce the second document once the first's handoff condition is
  actually met and verified — the same image-verification discipline applies
  to confirming the handoff, not just individual phases.

## Version and file safety

- Respect explicit constraints the user states about file safety (e.g. "don't
  delete any Blender file") for the entire remainder of the engagement, not
  just the message where it was said.
- Prefer Save-As versioning per phase (`v01`, `v02`, ...) over overwriting a
  single working file in place, so a bad phase can be rolled back without
  losing prior good work.
- Never let a fix or export step touch the pre-identified fallback deliverable
  from the setup step.
