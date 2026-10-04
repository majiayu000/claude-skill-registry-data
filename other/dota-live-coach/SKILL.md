---
name: dota-live-coach
description: >
  Governs live coaching UX and recommendation presentation in Dota AI
  Coach — how much the engine's analysis actually reaches the player
  during active gameplay, message priority (P0/P1/P2), message brevity
  and phrasing, and anti-spam mechanisms (hysteresis, cooldowns, change
  thresholds). Use whenever building or reviewing overlay/voice message
  logic, deciding what to surface from a recommendation engine's output,
  writing live-facing copy, or debugging players feeling spammed/
  overwhelmed by the coach. This is a presentation and attention-budget
  gate — a technically correct recommendation that reaches the player as
  a wall of text, or too often, is a shipped defect, not a minor UX
  polish item.
---

# Dota Live Coach: Presentation and Attention Budget

## Core rule

> The engine may analyze hundreds of variables.
> The player should normally see only 1-3 actions.

`dota-domain`, `dota-item-recommender`, and `dota-draft` all produce
richly reasoned, multi-factor analysis — that's correct and necessary
upstream. This skill governs the very different problem of what actually
reaches the player *during a live match*, when their attention is almost
entirely consumed by playing the game. A player who's shown everything
the engine knows learns to ignore all of it; a player shown 1-3 clear
actions at the right moment actually uses them. Rich analysis and
minimal live presentation are not in tension — they're sequential stages
(see "Where this fits" below).

This is a distinct concern from `dota-item-recommender`'s `alternatives`
field or `dota-draft`'s six-factor score — those are for auditability,
review, and (per those skills' explanation-stage guidance) a
richer post-hoc or on-demand view. Live presentation is a hard filter on
top of that full output, not a rendering of it.

## Priority tiers: P0 / P1 / P2

Every live message has exactly one priority. Full detail and examples in
`references/priority-tiers.md`; summary:

- **P0 (critical)** — time-sensitive, high-stakes, act-now information.
  Interrupts or takes visual/audio precedence. Reserve for things where
  missing the window has an immediate, significant cost (e.g. `No
  buyback.` before a risky fight, `Three dead → objective.`).
- **P1 (actionable)** — a concrete recommended action, not urgent enough
  to interrupt but worth surfacing promptly (e.g. `BKB in 400g.`, `Farm →
  BKB → fight.`).
- **P2 (informational)** — useful context that doesn't call for
  immediate action (e.g. `Power spike ready.`). Lowest visual priority;
  the first thing suppressed under attention-budget pressure (see below).

The 1-3-message budget applies **across all tiers combined** — P0 doesn't
get its own separate budget on top of P1/P2; a P0 firing should generally
displace, not add to, whatever P1/P2 messages are currently shown. See
`references/priority-tiers.md` for the suppression/displacement rules.

## Message style

Live messages are extremely concise — short imperative fragments, not
sentences, and never an explanation during active gameplay. Full style
guidance and more examples in `references/message-style.md`; the
reference examples:

```
BKB in 400g.
Farm → BKB → fight.
No buyback.
Power spike ready.
Three dead → objective.
```

Notice the pattern: no subject pronoun, no justification clause, no
hedging — just the fact or the action. **Do not give lengthy explanations
during active gameplay.** The *why* behind a message (the `reasonCodes`,
the six-factor breakdown, the full analysis) belongs in a different
surface — a post-game review, a details panel the player can pull up
between fights on their own initiative, never pushed into the live
message stream. See `references/message-style.md` for how to compress a
rich recommendation into one of these fragments without losing the part
that actually matters for the next 10 seconds of play.

## Preventing recommendation spam

A live coach that fires a new message every time an underlying value
changes is unusable — GSI/CV data updates frequently (per `dota-gsi`),
and most updates don't represent a meaningfully new situation. Three
mechanisms, used together, keep messages meaningful rather than noisy —
full detail in `references/anti-spam-mechanisms.md`:

- **Hysteresis** — a condition must clear a meaningfully different
  threshold to *stop* triggering than the one that made it *start*
  triggering, so the message state doesn't flicker on/off around a single
  boundary value.
- **Cooldowns** — a minimum time between messages (per priority tier,
  and often per message *type*), so even a genuinely fluctuating
  situation doesn't produce a rapid-fire sequence of restatements.
  P0 has the shortest allowed cooldown (it needs to be able to fire when
  it matters), P2 the longest.
- **Change thresholds** — a new message only fires if the underlying
  value changed by enough to matter for the player's next decision (e.g.
  "BKB in 400g" shouldn't re-fire for every 10 gold of farm — only when
  the number crosses a threshold worth re-announcing, or the recommended
  action itself changes).

None of these alone is sufficient — see `references/anti-spam-mechanisms.md`
for how they compose and for concrete parameter guidance (starting points
for cooldown durations per tier, how to pick change thresholds per
message type).

## Where this fits in the pipeline

Per `dota-architecture`, this skill governs the **Overlay/Voice** layer's
consumption of the **Recommendation Orchestrator**'s output — it does not
change what Recommendation Engines compute or how the Orchestrator
prioritizes between them; it governs the final filter/compression step
between "what the system knows" and "what the player sees right now."
Concretely:

```
Recommendation Orchestrator output (rich, multi-factor, per
  dota-item-recommender / dota-draft)
        ↓
Live presentation filter (THIS SKILL: priority assignment,
  hysteresis/cooldown/threshold gating, message compression to
  1-3 concise fragments)
        ↓
Overlay / Voice (rendering)
```

A recommendation engine bug (wrong item, wrong pick) is a
`dota-item-recommender`/`dota-draft` problem. A player feeling spammed,
overwhelmed, or confused by *how* a correct recommendation was presented
is a bug in this layer, and should be fixed here — don't fix presentation
problems by dumbing down the upstream analysis, and don't fix analysis
problems by adding more live message volume.

## Relationship to other skills

- `dota-item-recommender` / `dota-draft` — produce the rich,
  multi-factor recommendations this skill compresses for live display;
  their `reasonCodes`/explanation output is the raw material for P1/P2
  message content, and their full detail belongs in a non-live surface.
- `dota-architecture` — this skill governs the Overlay/Voice layer
  specifically; it doesn't change the Recommendation Orchestrator's own
  responsibilities.
- `dota-gsi` — the update frequency and partial-payload nature of live
  state (per `dota-gsi`'s state-diffing guidance) is exactly why
  anti-spam mechanisms are necessary here, not optional polish.
