---
name: "Track: Claude Code Pain Points"
description: "Silently log friction with Claude Code itself (bugs, missing features, annoying limitations) for hud-cc_releases to check against future fixes"
when_to_use: "The moment Claude Code (the CLI/harness, not any project it's working in) visibly blocks, crashes on or annoys Jason and his reaction shows it bothered him: a curse, a workaround, a retried command, 'this is annoying', an explicit 'log this'. Not for project bugs, only for the tool itself."
metadata:
  family: track
disable-model-invocation: false # its whole value is firing at the moment of friction, unprompted; the write is append-only, low-stakes, reversible, and needs no gate
allowed-tools: ["Read", "Edit", "Write"]
---

# Track: Claude Code Pain Points

Claude Code's changelog is thousands of lines the reader will never proactively read against their own experience. This skill is the other half of `hud-cc_releases`: it catches friction with the tool itself as it happens, so that skill can later recognise "oh, this actually got fixed" instead of surfacing every bugfix in the changelog and hoping one lands.

## When this fires

Not every hiccup. The bar: something about Claude Code's own behaviour (not the user's codebase, not a library, not the user's own mistake) visibly cost Jason time or got in his way, and his reaction shows it registered as friction, not a shrug. Signals: a curse or frustrated aside, an explicit workaround adopted mid-session, a retry of the same thing a different way, a flat "this is annoying" / "why does it do that". An explicit "log this as a pain point" always fires regardless of tone.

Does not fire for: bugs in the user's own project, a one-off fluke that isn't reproducible, something already covered by an existing open entry (check first: see below).

## What to log

Append one entry to `library/state/cc-pain-points.json` (create as `[]` if somehow missing; it shouldn't be, `hud-cc_releases` ships it):

```json
{
  "id": "kebab-case-slug",
  "description": "free-text account of the friction, in Jason's own words/framing where possible",
  "logged": "YYYY-MM-DD",
  "sourceSession": "short context: project or task at the time, optional",
  "resolvedIn": null,
  "resolvedNoted": null
}
```

Write the description as the actual problem experienced, not the changelog's eventual language for it: `hud-cc_releases` matches by meaning later, and a description in Jason's own framing is exactly what makes that match possible. Concrete over vague: "worktree isolation blocked a plain `git log` from a subagent, had to disable isolation to get unstuck" beats "worktree isolation is annoying".

**Before appending**, read the existing file and check no open entry (`resolvedIn: null`) already describes the same friction, same underlying cause, even if the trigger differed. If one exists, don't duplicate; this skill only adds genuinely new pain points.

## After logging

Do it silently. No confirmation message, no "I've logged this as a pain point": the point is zero friction added on top of the friction just experienced. Continue the conversation as normal; the log entry is infrastructure, not an output to announce.

## Second entry point: marking an entry resolved

`hud-cc_releases` calls this skill (never writes the JSON itself) once Jason has explicitly confirmed a changelog fix addresses a specific open entry. When invoked for this, the calling instruction names the entry's `id` and the version that fixed it: find that entry, set:

```json
"resolvedIn": "2.1.222",
"resolvedNoted": "YYYY-MM-DD"
```

and stop. This path only ever runs after confirmation has already happened upstream; don't re-ask here, don't second-guess the match. If the named `id` isn't found, say so plainly rather than silently no-op-ing.

## Red flags

**Never** log a pain point the user didn't actually seem bothered by, inferring frustration from ordinary conversation causes false positives that pollute the store. **Never** log project-level bugs here, this store is Claude-Code-the-tool only. **Never** mark an entry resolved except via the second entry point above, and never invoke that path without an upstream confirmation already having happened; this skill trusts the caller's confirmation, it doesn't generate its own.
