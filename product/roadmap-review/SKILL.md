---
name: roadmap-review
description: The doctrine for `/roadmap-review` — interactive triage of roadmap-shape drift, walked one item at a time, with paste-ready resolution phrasing for the active sizing lens.
compatibility: opencode
metadata:
  audience: roadmap-reviewer-agent
  purpose: shape-triage
---

## What I do

Define the doctrine the `roadmap-reviewer` agent quotes from when the
user runs `/roadmap-review`. I carry:

- the **Lenses** model (sizing is active in v1; horizons / releases /
  sprint-shape are named placeholders the agent **refuses** to act on),
- the **prioritization rules** for the active sizing lens,
- the **four canonical resolution options** with paste-ready phrasing,
- the **stop condition** for a session,
- the **session record** format and path.

I am the source of truth for the triage loop. The agent loads me on
invocation and quotes me directly — it does not improvise wording, and
it does not invent resolutions outside the four I name.

## `hero check` vs `/roadmap-review` (one sentence)

> `hero check` is **workspace hygiene** — a one-shot report of stale
> specs, missing fields, convention drift, and warning counts.
> `/roadmap-review` is **roadmap shape** — an interactive triage that
> walks each high-impact drift, proposes a resolution, and executes the
> resolution CLI on confirm. Both surface drift; only `/roadmap-review`
> resolves it.

The agent prompt quotes this verbatim. If a user asks "which do I run,"
both surface drift — only `/roadmap-review` resolves it.

## Walk one at a time

The defining behavior. The agent does not produce a wall of prose or
enumerate all drift at once. It surfaces one finding, proposes one
resolution, accepts the user's answer, executes on confirm, and
advances to the next. No bulk operations. The user can opt into more
explicitly, but the default rhythm is one item at a time.

Punting the keystrokes back to the user ("now run `hero size foo
large`") defeats the loop. On confirm the agent **runs the CLI
itself** and surfaces the output before advancing.

## Lenses

The extensibility seam. A lens is an analytical perspective the
reviewer applies — sizing today, others tomorrow. Adding a new lens
later means moving its section from Scaffolding to Active and filling
in the four sub-sections (prioritization, resolution options, phrasing,
stop condition). The agent prompt does not change.

### Active

#### Sizing

The only lens implemented in v1. Surfaces drift between declared
`size:` and computed effort, oversized leaves that should `/split`,
container drift, and topical clusters that lack an initiative parent.

##### Prioritization rules

The agent walks findings in this order. It does not re-sort.

1. **`giant` without `size_ack`** — highest. Month+ specs that haven't
   been consciously acknowledged are the loudest shape failure.
2. **`x-large` features / bugs / enhancements** — multi-week leaf
   work. Almost always wants a `/split`.
3. **Container drift** (epic/initiative declared smaller than the
   rolled-up children) — the parent is lying about its scope.
4. **Multi-spec topical clusters** without an initiative parent — the
   "2+ related orphans" case. See `spec-composition` for the detection
   heuristic and canonical phrasing.
5. **`large` features / bugs / enhancements** — soft. Surface only if
   nothing higher remains.

`giant` initiatives are normal — they belong in the loop only when
they have no children yet (signal that `/compose` hasn't been run).

##### Resolution options + paste-ready phrasing

Exactly four. Any other resolution is out of spec.

| Resolution | When the agent offers it | On confirm |
|---|---|---|
| **Acknowledge** | `giant` leaf where the user explicitly wants single-pass delivery | `hero size --ack giant <slug>` (or write `size_ack: giant` to frontmatter if the CLI flag doesn't exist yet) |
| **`/compose`** | `x-large` / `giant` that should become an initiative with phased children | Invoke the `/compose` flow against the slug — agent hands off, doesn't simulate |
| **`/split`** | `large` / `x-large` leaf that belongs as 2–3 sibling specs | Invoke the `/split` flow against the slug — agent hands off |
| **Re-horizon** *(sizing-lens version: bump declared tier)* | Drift where declared < computed; user agrees the spec really is the bigger tier | `hero size <slug> <new-tier>` |

Quote these scripts verbatim:

**Acknowledge** (for unacknowledged `giant` leaves):
> This `giant` spec is intentional? I can stamp `size_ack: giant` so
> it stops asking at design time — mid-delivery checks continue.
> Confirm?

**`/compose`** (for `x-large` / `giant` that should be an initiative):
> This is `x-large` — recommended path is `/compose` into 3–5 phased
> children. Want me to kick that off now?

**`/split`** (for `large` / `x-large` leaves across subsystems):
> This is `large` across two subsystems — `/split` into a pair of
> sibling specs. Run it?

**Re-horizon** (for declared < computed drift):
> Declared `medium`, computed `large`. Bump to `large`? (Y/n)

##### Stop condition

A session ends on the first of:

1. **No high-impact drift remains** — priorities 1–4 are exhausted.
   The agent reports the clean state and exits.
2. **User halts** — any of "stop," "enough," "done," "later," or
   declining a resolution without picking another. The agent does not
   ask "are you sure"; it accepts and exits.
3. **Five items resolved in this session** — soft cap to keep
   momentum. The agent reports the cap, summarizes what was resolved,
   and suggests re-running tomorrow.

The cap lives here, in the skill — tunable without touching the agent
prompt.

### Scaffolding (not implemented — future work)

The agent **refuses** to act on these. It does not improvise a triage.
Canonical refusal phrase, substituting the lens name:

> "<lens>-lens triage isn't implemented yet — that's deferred to
> future lens work. I can only act on sizing drift in this version."

#### Horizons

Placeholder. v1 does not act on horizon drift.

#### Releases

Placeholder. Same refusal pattern.

#### Sprint-shape

Placeholder. Same refusal pattern.

## Session record (knowledge capture)

On exit — any reason — the agent writes a short note to
`.hero/knowledge/roadmap-review-sessions/{YYYY-MM-DD}-{HHMM}.md`.
This is the dogfood signal: cadence over time, items resolved per
session, what gets deferred. Sibling spec
`roadmap-review-ambient-surfacing` reads these records to power the
"stop nagging if nothing's changed since the last triage" rule, so the
`drift_count_at_exit:` frontmatter field is **load-bearing**, not
optional.

Format:

```markdown
---
type: note
created: <ISO-8601 timestamp>
tags: [roadmap-review, sizing]
drift_count_at_exit: <int>
---

# Roadmap review — <YYYY-MM-DD HH:MM>

**Findings surveyed:** N (M sizing-drift, K missing-parent clusters)
**Walked:** N
**Resolved:** N (X `/split`, Y ack, Z size bump)
**Deferred:** N (user said "later")
**Exit reason:** <user halt | cap reached | exhausted | empty>

## Items
- `<slug>` (<tier>, <ack-state>) → <what happened>
- `<slug>` (declared <tier>, computed <tier>) → <what happened>
- `<slug-a>` + `<slug-b>` cluster → <what happened>
```

`drift_count_at_exit` is the count of remaining sizing-drift findings
at the moment the agent exited (after resolutions applied). Sibling
ambient-surfacing reads it to decide whether to suppress the next 24h
nudge. If the field is missing, the ambient reader treats it as "count
unchanged" — forward-compatible, but write the field every time.

## Ambient surfaces

When this skill's interactive triage isn't actively running, three
ambient surfaces carry the same paste-ready hint pointing here:

- **NEXT.md projection** — a `## Roadmap shape` section appears
  between `## Next` and `## Blocked on` when drift surfaces.
- **`hero_pulse` / `hero_kickoff` MCP tools** — both responses
  populate a `size_drift` field (count + hint) when drift surfaces.
- **Delivery-lead pre-flight** — `feature-delivery-lead` and
  `platform-delivery-lead` quote the hint verbatim in their handoff
  output when the workspace-wide count is non-empty.

All three quote the canonical hint from `internal/sizing/ambient.go` —
they do not compose the string themselves. The noise threshold (active
spec union 7d recency union horizon:now unsized initiatives) and the
24h stop-nagging rule (suppress while a recent
`.hero/knowledge/roadmap-review-sessions/` record's
`drift_count_at_exit:` is still ahead of the current filtered count)
keep the channel from going noisy. Tune via
`hero.json: roadmap.ambient_recency_days` and
`roadmap.stop_nagging_hours`.

## Cross-skill references

- **`spec-sizing`** — the size ladder, per-type bands, design-time
  nudges, and drift-handling rules live there. This skill is the
  *triage loop* over that ladder; the ladder itself is not re-litigated
  here.
- **`spec-composition`** — the canonical "multiple related specs"
  detection heuristic and phrasing. Priority-4 findings (orphan
  clusters) quote `spec-composition` for the recommendation script.
- **`note-capture`** — session record writes follow the note format
  defined there.

## What the agent must not do

- Improvise a resolution outside the four named above.
- Bulk-operate. No "acknowledge all `giant`," no "bump all drift."
- Punt CLI keystrokes back to the user. On confirm, the agent runs the
  CLI itself.
- Act on a non-sizing lens. Refuse with the scaffolded phrase above.
- Write to the tracker. Read-local-only is a hard boundary.
- Re-ask after a halt word. "stop," "enough," "done," "later" exit
  immediately.
