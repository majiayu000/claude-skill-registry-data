---
name: spec-composition
description: When work would produce 2+ related specs, prefer initiative-first composition over `/design` × N siblings. Carries the canonical "multiple related specs" phrasing that both interactive triage (`/roadmap-review`) and design-time routing (`/design`) quote.
compatibility: opencode
metadata:
  audience: any-agent
  purpose: composition-discipline
---

## What I do

Hold the canonical doctrine — and one specific paste-ready sentence —
for the **"multiple related specs"** condition: when the body of work
in front of the user is two or more topically related specs with no
shared initiative parent.

Two surfaces consume me:

- **`/roadmap-review`** (interactive triage) — surfaces orphan
  clusters that already exist in the planning corpus and offers to
  `/compose` them into an initiative.
- **`/design`** (multi-spec routing, sibling spec
  `multi-spec-design-routing`) — catches the condition *at design
  time*, before the second or third related spec lands, and routes
  the user toward `/compose` first.

Both surfaces quote the same canonical sentence from me. I exist so
the wording stays consistent across the two moments and neither
surface re-invents it.

## Goal

When two or more related specs would be created (or already exist
unparented), prefer **initiative-first composition** — `/compose` into
a parent with phased children — over scaffolding N flat sibling
features. Flat orphans become discoverable only by accident; an
initiative parent makes the work legible as a unit.

This is composition discipline, not sizing. A `medium` cluster of
three orphans is a composition problem; the size ladder doesn't model
it. That's why this skill exists separately from `spec-sizing`.

## Canonical phrasing

The sentence both surfaces quote verbatim, substituting the slugs:

> `<slug-a>`, `<slug-b>`, and `<slug-c>` look topically related and
> none of them have an initiative parent. If they're one body of
> work, `/compose` lifts them into a shared initiative. If they're
> genuinely independent, no action needed. Want me to `/compose`
> them?

Do not paraphrase. Quoting keeps the user's mental model of the nudge
stable across the design-time and triage-time surfaces.

## Triggers

The nudge fires when **any** of the following is true during a
`/design` invocation. These are deliberately not AND-ed — each one
independently signals a composition moment, and a single trigger is
enough.

1. **Explicit multi-deliverable phrasing.** The `/design` request
   names ≥ 2 distinct deliverables. Pattern recognition the agent
   already does — no NLP, no learned model.
   - *"design X, Y, and Z"*
   - *"spec out these three things"*
   - *"I need specs for A and B"*
   - *"design these four features"*
   - *"and also"* / *"plus"* / *"along with"* when each side names a
     discrete deliverable

2. **Lead-identified sub-deliverables.** While clarifying the
   request, the lead recognizes ≥ 2 independent sub-deliverables that
   would each warrant their own spec — different surfaces, different
   acceptance criteria, could ship independently. This is design
   judgment, not a mechanical rule. Lean toward *not* firing if
   uncertain.

3. **Rolled-up size ≥ `large`.** If the lead can estimate the
   deliverables' sizes individually, and the midpoint-sum across them
   rolls up to `large` or higher on the shared ladder (per the
   midpoint-sum mechanic in `internal/snapshot/rollup.go`), the
   cluster wants an initiative parent regardless of how the request
   was phrased. Fall back to triggers #1 / #2 when there isn't enough
   information to estimate.

Any-of. One trigger is sufficient.

## Phrasing

Paste-ready text the lead quotes when a trigger fires. Direct,
non-hedging — name the alternative and ask. The canonical sentence
under `## Canonical phrasing` above is the orphan-cluster variant
used by `/roadmap-review`; the variants below are the design-time
variants, parameterized by which trigger fired.

### Trigger #1 — request names multiple deliverables

> You named N deliverables here (`<thing-a>`, `<thing-b>`,
> `<thing-c>`). I'd recommend running `/compose` instead — that
> creates an initiative with N child stubs, ready for individual
> `/design` passes when each is up. The alternative is N flat
> sibling specs with no parent, which usually gets reparented later
> anyway. Want me to `/compose` this, or proceed with the siblings
> here?

### Trigger #2 — lead spotted sub-deliverables during clarification

> Listening to this, it sounds like ≥ 2 independent pieces of work
> (`<piece-a>`, `<piece-b>`) — each could ship on its own and each
> wants its own acceptance criteria. I'd recommend `/compose`
> instead — scaffold an initiative parent now and `/design` each
> child when you're ready to flesh it out. Want to switch, or stay
> in `/design` and ship this as a single spec?

### Trigger #3 — rolled-up size ≥ `large`

> This is shaping up as ≥ `large` rolled up across multiple
> deliverables. That's initiative territory — I'd recommend
> `/compose` instead, which scaffolds the parent and lets you
> sequence the children. Want to switch, or stay in `/design` and
> ship this as a single spec?

Substitute the slugs / deliverable names inline; otherwise quote
verbatim. The wording is short and decision-oriented — a fired
nudge should be a 5-second yes/no, not a conversation.

## Stance

The recommendation is **advisory**, never a block. Same stance as
the sizing nudge in `spec-sizing` ("user always wins"), word-for-word
on the override behavior:

- The lead surfaces the recommendation **once per `/design`
  invocation**.
- The user can answer *"no, just do them as siblings"* / *"proceed"*
  / *"stay in design"* / *"ship it"* — any clear decline — and the
  lead resumes the design flow as if the nudge had not fired.
- The lead records the user's choice in the session so the rest of
  the session does not re-litigate it. **One decline covers the whole
  session** (see Suppression).
- On *"yes, compose,"* the lead hands off cleanly into the existing
  `/compose` flow with the user's original `/design` request as the
  initiative input — it does not simulate `/compose` or scaffold flat
  siblings.

The nudge is **friction with an off-ramp**, not a gate. A loud linter
warning, not a build failure.

## Precedence

When the **routing nudge** (this skill) and the **sizing nudge**
(`spec-sizing`) would both fire on the same `/design` request, the
routing nudge fires **first**, and the sizing nudge stands down for
that moment.

Concretely:

- Routing nudge: *"Your request describes ≥ 2 specs — consider
  `/compose` to scaffold the cluster as an initiative."*
- Sizing nudge: *"This individual spec is `large` / `x-large` /
  `giant` — consider `/split` or `/compose` for this spec
  specifically."*

They describe different moments — composition shape vs. individual
spec size — but the user shouldn't get both at once.

- **If the user accepts routing** and pivots to `/compose`, the
  sizing nudges resurface naturally inside the per-child `/design`
  passes as each child is fleshed out. Each child is sized on its
  own when it lands, so the sizing nudge fires per-child at the
  natural moment.
- **If the user declines routing** and proceeds with N siblings,
  the sizing nudge fires per-sibling as usual — each sibling is
  sized when written, and the sizing nudge fires per the schedule
  in `spec-sizing`.

Either way, the two stances stay consistent ("user always wins") and
exactly one nudge fires per moment. `spec-sizing` cross-references
this precedence rule so the two skills agree.

## Suppression

Three suppression rules keep the nudge from re-firing at the wrong
moments:

1. **Already in a `/compose` flow.** If the `/design` invocation was
   itself launched from `/compose` (e.g., the user is now fleshing
   out a freshly-scaffolded child stub of an initiative), the
   composition decision has already been made. Do not fire.

2. **User declined earlier in this session.** If the user has
   already declined the routing nudge in this session ("no, siblings
   is fine" / "ship as siblings" / similar) on a prior `/design`,
   the lead **suppresses re-firing for the rest of the session**.
   One decline covers the whole session — do not re-litigate on
   each sibling.

3. **The sizing nudge would also fire.** Per the Precedence rule
   above: when both would fire on the same `/design` request, the
   routing nudge claims the slot first. The sizing nudge stands
   down for that moment and fires per-child later (either inside
   the `/compose` child specs, or per-sibling if the user declined
   routing).

These three suppressions are inclusive — any one of them stops the
nudge. The lead does not need to walk all three before deciding to
stay quiet.

## Cross-skill references

- **`spec-sizing`** — the size ladder. This skill does not duplicate
  the per-type bands or the tier definitions; sizing remains the
  source of truth for "how big is this." Composition discipline is a
  separate axis.
- **`roadmap-review`** — interactive triage that fires the canonical
  phrasing above when priority-4 findings (orphan clusters) surface.
