---
name: reviews-code
description: "Use when asked to review a code change (diff, branch, or PR) for merge readiness and collaborate asynchronously with another agent (often invoked with tony:does-work) that is or will be pushing fixes to the same change. Leaves P0-P* findings in a Changelog section, then sleeps in 5-minute checks (up to 4) waiting for the other agent to respond, re-reviewing whenever it does. Triggers: 'review this PR and wait for the other agent', 'reviews:code', 'is this ready to merge, check back as they fix it'."
---

# Reviews Code (tony:reviews-code)

## Purpose

Review a code change for merge readiness, leave findings inline in a target
doc's own Changelog instead of only in chat, then keep checking back on a
timer so a second agent (running `tony:does-work` on the same file, or
pushing fixes to the reviewed branch) can pick up the findings, act, and hand
back without either side needing to be polled by a human. The loop ends when
the change needs nothing further to merge, or when the other agent goes
quiet.

This is the async, collaborative counterpart to `tony:is-review-ready`: that
skill produces a one-shot report for a human to read; this one keeps a
running conversation with another agent until the change is mergeable.

## Target doc

Findings are written into the Changelog of a Markdown doc that both agents
watch — the PR description, or (per this project's convention) the ticket
anchor doc (`docs/tasks/<TICKET>.md`) referencing the linked spec/plan. Ask
for this file if it isn't already named.

## Changelog format

The Changelog lives at the bottom of the target doc, under a `## Changelog`
heading. Create the heading if it isn't there yet. **New entries always go
directly under the heading (top of the list), never appended at the bottom.**

Each entry is one bullet:

```markdown
## Changelog

- **2026-09-09T14:32Z — Reviewer:** <finding or note>
```

Use role `Reviewer` for every entry you write. Entries written by the other
agent will say `Worker` (or whatever role they used) — that's how you tell
"my own last entry" apart from "something new arrived".

## Process

1. **Gather the change.** Identify base and head (uncommitted work, a branch
   against its base, or a pull request). Read the PR/task description, linked
   spec, and existing review comments before forming a finding.
2. **Review the change for merge readiness** using the same lenses as
   `tony:is-review-ready`: intent and behavior, contracts and safety, proof
   and operations (do the tests actually test this), structure and history.
   Run the repository's own verification (tests, typecheck, lint, build)
   where the environment allows it.
3. **Write findings into the Changelog**, one bullet per finding, newest on
   top, role `Reviewer`, ISO 8601 UTC timestamp, each prefixed with its
   severity tag (see below). If nothing needs to change, skip to step 7
   immediately — do not enter the sleep loop for a change that's already
   mergeable.
4. **Enter the check loop.** Call `ScheduleWakeup` with `delaySeconds: 300`
   and a `prompt` that names the file and the current check count, e.g.
   `tony:reviews-code resume <file path>, check 1/4`. Set `noop` based on
   whether anything changed this turn.
5. **On each wake, re-read the Changelog.** Compare its top entry to the last
   one you wrote or saw.
   - **No new entry above yours:** this was one check. If this was check 4
     with nothing new, stop — the other agent appears to have stopped —
     and tell the user so. Otherwise go back to step 4 with the count
     incremented.
   - **A new entry from the other agent (role isn't `Reviewer`):** go to
     step 6.
6. **Acknowledge, then re-review.**
   a. Add a new top-of-Changelog entry, role `Reviewer`, timestamped now,
      saying you've seen their update and are re-reviewing — this tells the
      other agent you're active if they check back before you finish.
   b. Re-read the diff in full (not just the delta implied by their note),
      re-run verification where applicable, and check off each prior finding
      as closed, partially closed, or still open — verify the claim rather
      than taking the note at its word.
   c. If more changes are needed: go back to step 3 (new findings, reset the
      check count to 0, resume the loop at step 4).
   d. If nothing more is needed: go to step 7.
7. **Mark it ready.** Add a final Changelog entry, role `Reviewer`, stating
   the change is ready to merge, and stop the loop (do not call
   `ScheduleWakeup` again).

## Severity: P0-P*

Every finding gets a severity prefix so the other agent knows what's required
versus optional. Use the fewest tiers actually needed for a given change —
skip a tier entirely rather than force a finding into it.

| Tier | Requires | Action |
|---|---|---|
| **P0** | Catastrophic or irreversible harm if merged (data loss, broken build, security hole) | Fix before merge, blocks the loop from closing |
| **P1** | A realistic material failure this change causes or worsens, no acceptable fallback | Fix before merge |
| **P2** | A real bounded issue, missing case, or open question a reviewer would raise | Fix, or answer it in the description |
| **P3** | Small objective cleanup, tiny cost | The other agent's call, never blocks merge readiness on its own |

A Changelog finding entry looks like:

```markdown
- **2026-09-09T14:32Z — Reviewer:** P1 `path:line` <what breaks, for whom, and the fix>
```

The loop only reaches step 7 (ready to merge) once every open P0 and P1 is
closed. P2/P3 entries left open do not block the "ready" verdict but should
be named in the final entry.

## Output

Changelog entries written directly into the target doc at each step above,
plus a short chat message at the point the loop stops (ready to merge, or the
other agent went quiet) summarizing the outstanding P-tier count. This skill
only edits the target doc's Changelog section — it does not edit the reviewed
code, commit, push, comment on the PR, or change labels.
