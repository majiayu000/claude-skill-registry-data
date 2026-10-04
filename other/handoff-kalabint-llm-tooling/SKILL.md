---
name: handoff
description: Read OR write the project's session-handoff doc. WRITE mode updates it so a fresh agent can pick up the work (what was built, in-flight files, open questions). LOAD mode reads the doc AND the files it references so YOU get up to speed at the start of a session. Use when the user says "update handoff", "write a handoff", "hand off", or signals a session is wrapping up (→ write); or "read the handoff", "load the handoff", "get up to speed", "catch me up", or pastes the doc path at the start of a session (→ load).
argument-hint: "[what the next session should focus on]"
---

"Handoff" has two modes. Pick one before doing anything:

- **LOAD (onboard)** - the user is *starting/resuming* a session and wants YOU current.
  Triggers: "read the handoff", "load the handoff", "get up to speed", "catch me up",
  pasting the doc's path, or invoking `/handoff` in a fresh session with no work to record yet.
  Action: read the doc top to bottom, then read the load-bearing files it points to (its
  "Files to read to proceed" / open-items / in-flight sections), then STATE the ranked next
  possible steps (name the file/function/check each involves) and WAIT for the user to pick.
  Do NOT edit the handoff, change code, or run builds.
- **WRITE (update)** - the user is *wrapping up* and wants the doc to capture this session.
  Triggers: "update handoff", "write a handoff", "hand off", end-of-session signals.
  Action: follow "## What to write" below.

If genuinely ambiguous, infer from session state: a fresh session with nothing new to
record → LOAD; a session with substantive uncommitted/just-built work → WRITE. When still
unclear, ask which.

## LOAD mode
1. Locate the handoff (see "## Where it lives") and read it fully.
2. Read the files it names - the "Files to read to proceed" section, plus any file/function
   cited in the open items or in-flight threads. The point is to hold the same context the
   previous agent had, so you can act, not just summarise.
3. Reply with the ranked next possible steps (file/function/check per step) and wait. Do not
   touch code or the doc.

## WRITE mode
Update the project's session-handoff document so a fresh agent can continue. Bias hard
toward what the next agent must **read** and **do**, not a changelog of everything done.

## Where it lives
- Find the existing handoff first: a `*_session_handoff.md` / `HANDOFF.md` / `docs/handoff*.md`
  at the repo root or one directory ABOVE it (handoffs are often kept as a sibling of the repo,
  untracked). Update that file in place - do not start a fresh one.
- If none exists, create `<repo-parent>/<project>_session_handoff.md`.

## What to write
0. **Start-here preamble** (top of the doc, a blockquote) - the user pastes this doc's path
   to begin a session, so the doc must instruct its own reader: read top to bottom, then
   STATE the ranked next possible steps (naming the file/function/check each involves) and
   WAIT for the user to pick - do not change code or run builds first.
1. **Header** - date, repo path, branch, where to edit/build/commit.
2. **State of the work** - what was built this session, grouped by component, one line each.
   Reference commits by short hash. Mark every item explicitly: COMMITTED / DEPLOYED /
   UNCOMMITTED / NOT-DEPLOYED (these diverge - be precise).
3. **Files to read to proceed** (the load-bearing section) - ONLY the in-flight, uncommitted,
   and not-started files; the ones the next agent opens to continue. Full paths, one line on
   what's there + status. Skip done/committed files - the agent doesn't need them.
4. **Open / NOT done** - concrete, actionable next steps and unresolved questions. Name the
   file/function/check for each. Include any mid-diagnosis thread with the exact thing to re-check.
5. **Current live state** - what's running/deployed vs not; any manual DB/state changes made.

## Style
- No "better safe than sorry" / cautionary framing unless a real risk is at hand.
- No emojis, no time estimates.
- Terse and factual: what changed + why, commit hashes, file paths.
- Don't duplicate what's already in commits / PRs / design docs - reference them by hash/path.
- Redact secrets, tokens, PII.

If the user passed an argument, treat it as the next session's focus and bias the doc toward it.
After updating, reply with the handoff path and a one-line summary of the open items.
