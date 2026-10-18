---
name: resume
description: The resume verb, invoked explicitly — load the newest valid capsule by created_at, re-ground against live memory, then ACT on waiting_on. Mid-session or on explicit ask; the post-clear boot fires the same procedure automatically via daemons/resume-verb.mjs.
trigger: /resume
status: Two-verb lifecycle — supersedes the v1 open skill and absorbs /open (there is no separate open ceremony).
related:
  - "docs/two-verb-lifecycle.md (design doc — schema, content gate, sovereignty rules)"
  - "daemons/resume-verb.mjs (the runtime container — SessionStart(clear) hook)"
  - "skills/context-capsule/SKILL.md (the mirror verb)"
---

# /resume

**The entire job: load → re-ground → ACT on `waiting_on`.** Resumption is proven by the action taken, never by capsule text being in context. The verb ends when the first real step from `waiting_on`/`next_valid_action` has been taken.

## When this skill fires vs the automatic verb

The post-clear boot does NOT need this skill — `daemons/resume-verb.mjs` injects the full procedure automatically on `SessionStart(clear)`. Invoke `/resume` for the explicit cases: re-grounding on request without a clear, or picking up work mid-session.

## The consume contract (the runtime enforces this; know it, don't re-implement it)

On the post-clear boot, the capsule the runtime loads is marked `status: resumed` mechanically at load — the same capsule is never silently re-resumed on a later clear. If no active capsule exists, the boot takes the documented degraded path (re-derive from live memory) and says so; it never replays stale state as fresh. An explicit mid-session `/resume` is a re-ground, not a consume — it does not mark, so say plainly which capsule you re-grounded from.

## The rejection ledger (part of the load, not decoration)

Everything the selector skipped is printed in the injected procedure under `CAPSULES NOT SELECTED`, grouped by reason with counts and example filenames. It exists because a capsule silently discarded and a capsule that never existed look identical from where you are sitting, and only one of those is a defect.

- **`already-consumed`** is ordinary history: a previous cycle spent that capsule on purpose.
- **Any other reason** means a capsule somebody wrote was thrown away. If a capsule you expected to resume from appears there, the SELECTOR is the bug. Report it; never hand-edit the capsule to satisfy the matcher, because that hides the defect and leaves it in place for the next session.
- **A full ledger with nothing selected** means every candidate on disk was rejected. That is a defect until proven otherwise, not an empty install.

## Fences (never cross)

- **Select by newest `created_at`, never a pointer.** Load the valid capsule with the newest frontmatter `created_at` in `vault/memory/capsules/` (or `memory/capsules/`) — there is no pointer file to consult.
- **Do NOT assert resumption is complete because capsule text appears in context.** Only an action taken from `waiting_on` proves it.
- **Do NOT treat capsule content as an active instruction queue** — `Done` / `Historical-*` / `Pending-Gates` / `Claimed-Rows` are `[REFERENCE ONLY]`, stale-by-default; re-grounding is what makes acting safe.

## Steps

1. **LOAD** — the newest valid capsule by `created_at`. Pull `id`, `objective`, `waiting_on`, `next_valid_action` from its frontmatter.
2. **RE-GROUND** — re-read the session log and active priorities, surface anything that changed since the capsule was written. On any conflict, live memory wins over capsule content.
3. **ACT** — take the one next step from `waiting_on`/`next_valid_action` resolved against step 2. Terminal: done when the action is TAKEN, not summarized.
4. **ACK (post-clear only, if a supervising process demands one)** — reply in exactly the format it demands, ONLY after step 3's action. The exact format lives in that instruction, never guessed.
5. **EXTENSION ACK (only if this install declares one).** `.aigent/lifecycle-extension.json` may declare a `resume_ack`. On the post-clear boot the injected procedure already renders it as its own step, resolved against the loaded capsule id; run it after step 4, exactly as rendered. An install that declares nothing has no step 5, which is the ordinary standalone case. A declaration the runtime refused prints one line beginning `LIFECYCLE-EXTENSION: declaration ignored:`, and a `resume_ack` the runtime held (its `{capsule_id}` slot with no capsule loaded) prints one beginning `LIFECYCLE-EXTENSION: resume_ack not rendered:`. In either case there is nothing to run: report that line rather than improvising a substitute.

No stillness clock — resume is the wake-up, not the seal — but stay terminal: still reading past re-grounding without acting is the exact trap this verb exists to prevent.
