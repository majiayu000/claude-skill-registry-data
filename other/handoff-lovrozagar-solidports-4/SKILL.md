---
name: handoff
description: "Write a session handoff under .tmp/grunt/handoffs/. Continue with /pickup."
---
# handoff

One turn. Author from this session. Write once, report path, stop.

## Invocation

`/handoff [focus]`

Focus narrows what the handoff carries. Empty → whole session.

## When

Context large + work unfinished → write handoff, then advise a new session. Also on host/tool churn, or before a long unrelated detour.

Nothing done yet (no edits, no findings) → `nothing to hand off` and stop. Do not write an empty file.

## Path

`.tmp/grunt/handoffs/{serial}-{slug}-{YYYYMMDDTHHMMSSZ}.md`

- serial: unpadded int ≥ 1, next after existing handoffs (own counter; not plan serials)
- slug: lower, non `[a-z0-9]` → `-`, collapse, trim 50
- stamp: `created` with `-` and `:` dropped (`20260827T143000Z`)

## Format

```yaml
---
serial: 1
name: <slug>
status: open        # open | resumed | done
created: 2026-08-27T14:30:00Z   # UTC, seconds, no ms
source: "<≤120 chars of the session task>"
---
```

Headings, this order only: `# {slug}`, `## Goal`, `## State`, `## Context`, `## Next`, `## Watch-outs`.

| Section | Amount |
|---|---|
| Goal | 1–3 sentences. What the session is trying to land. |
| State | bullets. Past tense for landed work / changed / green-red, with absolute paths. |
| Context | bullets. Abs paths, decisions, verdict facts the next session needs. |
| Next | checkbox steps, `N [ ]` phase + `N.M [ ]` leaf, all `[ ]` fresh |
| Watch-outs | bullets. Footguns. `(none)` allowed. |

Boxes: `^{id} [ ] {text}$`, id `N` / `N.M` / `N.M.K`. Not `- [ ]`, not `1. [ ]`. Every phase has ≥1 leaf. Fresh handoff has zero `[x]`.

Facts only. Absolute paths. No transcript paste, no dump, no secrets/tokens.

## Write

Line 1 of the body: `HANDOFF_NAME: <3-6 word name>`, then the body only.

Write under `.tmp/grunt/handoffs/` (any filename in that dir). Grok `orchestrate-parent.js` runs `.rulesync/scripts/persist-handoff.mjs`: serial/slug from `HANDOFF_NAME:` / heading, injects frontmatter, rewrites path + content. Invalid handoff or a write outside that dir is denied — fix the body, do not retry elsewhere.

Host without that hook: name the file per **Path** yourself, or pipe the body to `node .rulesync/scripts/persist-handoff.mjs --workspace {repo}` and use its `path`.

## Report

```
[handoff]: serial={int} path=.tmp/grunt/handoffs/{serial}-{slug}-{stamp}.md
next: start a new session; `/pickup {serial}`
```

Do not dump the handoff body.

## Picking one up

`/pickup {serial}` owns pickup. Load the file, set `status: resumed`, work `Next` leaves in order, flip only the box. All `[x]` → `status: done`. Do not re-plan; a stale leaf → `/write-plan` a follow-up.

## Rules

- One write. `/handoff` is not a mode.
- Handoff ≠ plan: no Steps/Verify phases, no `.tmp/grunt/plans/` write. Handoff ≠ implementation journal.
- Never rewrite or renumber an existing handoff; new session = new serial.
- Protocol: `.rulesync/reference/cascade.md`. Do not paste it here.
