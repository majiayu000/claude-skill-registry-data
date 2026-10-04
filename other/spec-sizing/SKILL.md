---
name: spec-sizing
description: The shared 6-tier size ladder, per-type bands, and the nudge protocol delivery leads use to surface promotion recommendations on oversized specs.
compatibility: opencode
metadata:
  audience: delivery-leads
  purpose: sizing-nudge
---

## What I do

Define the **shared 6-tier size ladder** that lives in `size:` frontmatter
on every sized spec, and the **nudge protocol** delivery leads follow
when they encounter an oversized one.

Two jobs:
1. Tell a lead what a `size:` value means (and what the spec writer
   probably meant by choosing it).
2. Tell a lead exactly what to say, when, and how loud — so the same
   nudge fires consistently across sessions, agents, and trackers.

This skill is **the source of truth**. The delivery leads reference it;
the CLI (`hero size`, `hero sprint estimate`, `hero check`, `hero_warnings`)
implements the mechanics. The nudge text below is paste-ready — leads
quote it directly so wording stays consistent.

## When to use me

- **Design time** — when authoring a new spec via `/design`, stamp
  `size:` based on the design conversation. Default to `medium` only
  when truly undetermined.
- **Delivery pickup** — when starting `/deliver` on a spec, read its
  `size:` and `size_ack:`, run `hero size --check`, and fire the
  appropriate nudge.
- **Mid-delivery** — if scope grows or drift surfaces, bump declared
  `size:` via `hero size <slug> <tier>` instead of ignoring.

## The ladder

One vocabulary across all sized spec types. Each tier represents
roughly the same **absolute magnitude of effort**, regardless of
which type carries it. What's "normal" for an initiative is alarming
for a feature — that's what the per-type bands below capture.

| Tier | Magnitude | Rough shape |
|---|---|---|
| `trivial` | hours | A single change. Reads in one sitting. |
| `small` | ~1 day | One file or one tight cluster. One PR. |
| `medium` | a few days | A small handful of files; one delivery loop. |
| `large` | week+ | Multi-day work; spans several files or one subsystem. |
| `x-large` | weeks | Real multi-week effort; likely wants phasing. |
| `giant` | month+ | Enormous; almost certainly an initiative in disguise. |

### Per-type bands

| Tier | Feature / Bug / Enhancement | Epic | Initiative |
|---|---|---|---|
| `trivial` | normal | rare | — |
| `small` | normal | normal | small |
| `medium` | normal | normal | normal |
| `large` | **soft nudge** | normal | normal |
| `x-large` | **strong nudge** | nudge | normal |
| `giant` | **promote → initiative** | **promote / `/compose`** | **`/compose` into phases** |

### Why this shape (Option C)

Shared vocabulary, absolute magnitude, per-type bands layered on top.
A `giant feature` ≈ a `small initiative` in absolute effort — so
promotion is literally "move one step up the type ladder." One
mental model, one promotion rule. Don't re-litigate this choice;
the spec rejected the alternatives explicitly.

## Nudge intensity by tier and moment

Even `giant` is **advisory**. Friction climbs but the user always
wins. Never block delivery; record the user's choice and proceed.

| Tier | Design-time | On scope-up edit | Mid-delivery |
|---|---|---|---|
| `large` | soft ask once | quiet | mention in handoff |
| `x-large` | strong ask; recommend `/compose` or `/split` | re-ask if scope grew | flag each delivery session |
| `giant` | super-strong; require `size_ack: giant` | re-recommend each time | strong rec every session until ack, split, or scope shrinks |

## Tracker-aware tuning

The threshold at which the nudge fires shifts based on what the
tracker can do for hierarchy. Read `hero.json: tracker.type` and the
adapter's `supports_hierarchy` flag (slice 5 wires the adapter side;
until then default to "no tracker" behavior).

| Regime | Nudge schedule | Promotion offered |
|---|---|---|
| **No tracker** (`type: "none"`) | Most aggressive: `large` → soft, `x-large` → strong, `giant` → super-strong | Local promotion only — turn this spec into an initiative with children in `.hero/`. |
| **Tracker without hierarchy** (basic GitHub issues, flat Linear, etc.) | Same as no-tracker | Local promotion only — Hero handles parent/child locally; the tracker just sees the child issues. |
| **Tracker with strong hierarchy** (Jira epics, Linear projects, GitHub sub-issues) | Less aggressive: soft starts at `x-large`, strong at `giant` | Promotion offers to **create the parent in the tracker too**, so the human team's view stays coherent. |

## The acknowledgement protocol

`size_ack:` has two jobs. Both come down to the same principle: when
someone inspected the actual work and concluded the declared tier is
right, the system should stop arguing.

### Job 1 — suppress the `giant` design-time nudge

```yaml
---
title: ...
type: feature
size: giant
size_ack: giant
---
```

`size_ack: giant` says "yes, I know it's giant, I'm shipping it as
one spec anyway." Suppresses the super-strong design-time
recommendation to `/compose`. **Does not** suppress mid-delivery
surfacing — every delivery session on a `giant` spec still gets the
strong rec, because that's where the size is being felt.

### Job 2 — inspector wins over the computed heuristic

```yaml
---
title: ...
type: feature
size: medium
size_ack: medium
---
```

When `size_ack:` matches the declared `size:`, the drift detector
treats it as "the work was inspected; declared stands." Suppresses
the drift warning even when `hero sprint estimate`'s computed bucket
disagrees. This is the **inspector-wins rule**: the person who
looked at the actual implementation outranks a word-count heuristic
that only inspected the spec body.

When to use it:
- A `/roadmap-review` session walked the drift and the user/agent
  confirmed declared is right (prose-dense specs that compute high,
  structured-data-dense specs that compute low)
- A delivery-lead audit confirmed the spec scope matches declared
  after delivery — agent acks before flipping `status: completed`

When NOT to use it:
- Just to silence drift you haven't actually inspected. Acking
  without thinking is the same anti-pattern as marking a ticket
  `won't-fix` to clear a queue.

### Rules

- The user, or an agent that just inspected the work, decides to
  set `size_ack`. The lead asks; the lead does not auto-stamp
  on a spec it hasn't read.
- **Stale acks are ignored.** If you bump declared (`size: medium →
  large`) but the ack stays at the old value (`size_ack: medium`),
  the drift detector treats the ack as stale and re-fires. Update
  the ack or drop it.
- If the spec is split or scope shrinks, drop the `size_ack` field.
- The `roadmap-reviewer` agent should ack every "keep declared as-is"
  decision in its session — that's the durable record of inspection.

## Drift handling

When `hero size --check`, `hero check`, or `hero_warnings` surfaces
drift between declared and computed size, the lead does **not**
ignore it. Two flavors:

- **Leaf drift** (feature/bug/enhancement): declared `size:` differs
  from `hero sprint estimate` bucket. Bump declared via
  `hero size <slug> <tier>` to reflect what the spec actually is, then
  re-fire the nudge for the new tier.
- **Container drift** (epic/initiative): declared `size:` is smaller
  than the aggregated child rollup. Bump declared to at least the
  rollup tier.

Bumping the declared field is **the lead's job**, not the engineer's.
Don't write code to auto-bump — surface the recommendation and let
the user or the lead update it via the CLI.

## Phrasing — paste-ready

These are the lines the lead should quote. Tune by tier and (where
noted) tracker regime. Keep them short and concrete. Don't add
hedging like "you might possibly want to consider"; say the thing.

### `large` on feature/bug/enhancement — soft, design-time only

> This is `large` (week+ of work). Doable as one spec, but if it
> spans more than one subsystem consider `/split` into two specs.
> No action needed if you're comfortable with the scope.

Mid-delivery for `large` is quiet — mention in handoff only if
useful, otherwise stay out of the way.

### `x-large` on feature/bug/enhancement — strong, every session

> This is `x-large` (multi-week). Strongly recommend `/split` to
> break it into 2–3 child specs, or `/compose` if it deserves an
> initiative parent. Promotion creates a new initiative spec and
> converts this one into N child specs — real overhead, but cheaper
> than delivering a runaway spec. Want me to `/split` now?

Re-fire on every `/deliver` pickup. If the user says "ship it as-is,"
proceed — no `size_ack` needed for `x-large`.

### `giant` on feature/bug/enhancement — super-strong, requires ack

Design-time and first delivery pickup:

> This is `giant` (month+). I strongly recommend promoting to an
> initiative with phased child specs — `/compose` will scaffold the
> parent and let you slot child specs under it. Promotion isn't free
> (new parent spec, re-parenting this one, writing N child specs),
> but a month-long single spec almost always runs aground. If you
> want to proceed without splitting, I'll stamp `size_ack: giant` in
> the frontmatter so I stop asking at design time. Mid-delivery I'll
> still surface the size each session. Split or ack?

Mid-delivery with `size_ack: giant` set:

> Reminder: this spec is `giant` and acknowledged. I'll proceed, but
> if the next phase feels rough, that's the signal to `/split`.

Mid-delivery **without** `size_ack`:

> Still `giant` and unacknowledged. Quick decision: `/split` now,
> or stamp `size_ack: giant` and I'll stop asking at design time
> (mid-delivery checks continue).

### `large`/`x-large` on epic — light touch

Epics expect to be large. Only nudge at `giant`:

> Epic is `giant` — that's bigger than an epic should carry. Recommend
> promoting to an initiative (the next type up) and `/compose`-ing
> phases. Want me to scaffold the initiative parent?

### `giant` on initiative — `/compose` recommendation

> Initiative is `giant`. Single-pass delivery isn't realistic at
> this scope. Strongly recommend `/compose` to break it into 3–5
> sequential phases, each its own deliverable child. Want me to
> sketch the phase boundaries?

### Tracker-aware variants

When `tracker.type != "none"` AND `supports_hierarchy: true`:

- Raise the trigger floor: skip the `large` soft nudge, start at
  `x-large`.
- Append to the promotion ask:

> When you split, I can also create the parent issue in <tracker> so
> your team's tracker view matches the spec hierarchy. Want both?

When the tracker has no hierarchy support, fire the local-only
phrasing above and do not offer tracker-side parent creation.

## What to do on drift

`hero size --check` flags declared-vs-computed mismatch. The lead's
move:

1. Read the drift line. Two columns: declared tier and computed tier.
2. **If declared is too small** (most common): bump it.
   ```
   hero size <slug> <new-tier>
   ```
   Then re-evaluate: the new tier may itself trigger a nudge (e.g.
   bumping `medium` → `x-large` lands you in strong-nudge territory).
3. **If declared is too large** (rare; usually after scope shrinks):
   bump it down. No nudge fires; the spec just looks less alarming.
4. **Container drift**: same — bump the container's declared `size:`
   to at least match the child rollup, then check whether the new
   container tier itself triggers a nudge.

Don't ignore drift. The whole point of the field is to make scope
changes visible — ignoring drift makes `size:` lie, and a lying
field is worse than no field.

## Don't block

The user can override every nudge. The system records the choice
(via `size_ack:` for `giant`, or just by the user saying "ship it"
for `large`/`x-large`) and proceeds. Document the choice in the
delivery handoff so the next session sees it.

The nudge is a loud linter warning, not a gate. Treat it that way.

## Composing with related skills

- **`spec-format`** — defines `size:` as a living frontmatter field
  alongside `status:`. Cross-references this skill for the ladder.
- **`agent-reliability`** — the Persistence rule applies: don't yield
  mid-delivery just because a nudge fired. Surface the nudge, get the
  user's call, proceed.
- **`kickoff-prompt`** — when rewriting a spec's `## Kickoff` after a
  size change, reflect the new tier (and the ack state if `giant`).
- **`roadmap-review`** — the interactive triage surface for the drift
  this skill detects. `hero size --check` reports drift; `/roadmap-review`
  walks it one item at a time and executes the resolution CLI on confirm.
- **`spec-composition`** — owns the canonical "multiple related specs"
  phrasing and the multi-spec routing nudge. When a `/design` request
  would produce N related specs (user names multiple deliverables, or
  the rolled-up scope reaches `large`), the routing nudge from
  `spec-composition` fires **first** — the sizing nudge stands down
  for that moment per the precedence rule documented in that skill.
  Sizing nudges resurface per-child after the user either pivots to
  `/compose` (each child gets sized when its `/design` runs) or
  declines and proceeds with siblings (each sibling gets sized when
  written). One nudge per moment; never both at once.
