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

**A bare `/handoff` with an active doc that is already current means LOAD, not WRITE.** If the
doc for this session exists and nothing substantive has happened since it was written, do not
rewrite it to record trivia - do the LOAD action: state the ranked next possible steps from
its open-items section and wait. Rewriting a doc you just wrote is churn, and it buries the
open items under a changelog.

## LOAD mode
1. Locate the handoff (see "## Where it lives") and read it fully.
2. Read the files it names - the "Files to read to proceed" section, plus any file/function
   cited in the open items or in-flight threads. The point is to hold the same context the
   previous agent had, so you can act, not just summarise.
3. Reply with the ranked next possible steps (file/function/check per step) and wait. Do not
   touch code or the doc.
   If the doc has a "Suggested skills" section, invoke those skills first - they are
   part of getting current, not a later step.

## WRITE mode
Update the project's session-handoff document so a fresh agent can continue. Bias hard
toward what the next agent must **read** and **do**, not a changelog of everything done.

**Never overwrite a handoff.** Before rewriting an existing one, run:

```bash
python3 ~/.claude/skills/handoff/archive_handoff.py <path-to-handoff.md>
```

It copies the doc to `.handoff-history/<doc-name>/vNN_<UTC>.md` beside it and leaves the live
doc alone; edit the live doc normally afterwards. History is separate files, so the live doc
stays small and nothing pays for versions it did not ask for. `vNN` naming keeps snapshots
out of the resolver's `*handoff*<sid>*.md` glob, so a snapshot is never mistaken for the doc.

Never write a handoff with `cat > file` / `Write` / `>` without archiving first. Five full
overwrites of one doc were recoverable only by scraping the session transcript; the sixth
would not have been.

## Where it lives

**This project keeps ONE DOC PER SESSION**, as siblings of the repo, untracked:
`<repo-parent>/<project>_session_handoff_<session-id-prefix>.md`
(e.g. `<repo-parent>/myproject_session_handoff_a1b2c3d4.md`). A new session
normally gets a NEW doc. Do not assume the newest existing file is the one to overwrite.

Decide new-vs-merge like this, in order:

0. **Is a handoff already ACTIVE for this session?** Check this FIRST, every time - it
   overrides every rule below, so repeated `/handoff` calls converge on one file instead of
   spawning a doc per invocation. A handoff is active if either:
   - a doc for the current session already exists. Derive the session id from the scratchpad
     path (`/tmp/claude-*/<mangled-repo>/<session-id>/scratchpad`), take its first segment,
     and glob `<repo-parent>/*_session_handoff*<prefix>*.md`; or
   - this session was onboarded in LOAD mode from a specific doc, or the user pasted a doc
     path earlier in the conversation.

   If one is active: **update that file in place, archive first** (helper above). If
   the user names a topic that the active doc does not cover, widen or retitle the active
   doc rather than creating a second one. Only
   split off a new doc when the work has genuinely moved to an unrelated thread, and then
   cross-reference both ways.

1. **The user named a topic or scope in the argument** ("handoff privacy pii session",
   "handoff the tile work") -> that IS the instruction to create a NEW doc scoped to that
   topic. Write it, name it after the session, and cross-reference the sibling docs. Do not
   fold this session's work into an unrelated existing handoff, and do not ask.
   (Only reachable when step 0 found no active doc - otherwise the active doc wins.)
2. **The session clearly continues the thread of an existing handoff** (same branch, same
   feature, that doc's open items are what got worked on) -> update THAT file in place.
3. **Otherwise ambiguous** (an existing doc might or might not be the right home) -> ASK, via
   AskUserQuestion: list the candidate doc paths with their dates and one-line topics, and
   offer "new doc" as the first option. Do not silently pick.

Look for candidates with `*_session_handoff*.md` / `HANDOFF.md` / `docs/handoff*.md` at the
repo root or one directory ABOVE it. When writing a new doc, add a one-line "Sibling docs:"
reference to the adjacent handoffs so the set stays navigable.

**Point the doc at durable paths.** If the session's artefacts live in a session scratchpad
under `/tmp`, copy what the next agent needs somewhere permanent first and reference that;
a handoff pointing into a scratchpad is dead on arrival.

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

6. **Suggested skills** - name the skills the next agent should invoke with the
   Skill tool, and one line each on why THIS work calls for them. The next agent sees
   only a one-line description in a skill listing, never the reason this session
   reached for one, so an unnamed skill is one that will not be found. Name the
   trigger too where it matters ("run the build skill first, it encodes the
   signing-key split").

## Style
- No "better safe than sorry" / cautionary framing unless a real risk is at hand.
- No emojis, no time estimates.
- Terse and factual: what changed + why, commit hashes, file paths.
- Don't duplicate what's already in commits / PRs / design docs - reference them by hash/path.
- Redact secrets, tokens, PII.

If the user passed an argument, treat it as the next session's focus and bias the doc toward it.
After updating, reply with the handoff path and a one-line summary of the open items.
