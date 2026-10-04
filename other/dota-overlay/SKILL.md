---
name: dota-overlay
description: >
  Governs the Windows live overlay window in Dota AI Coach — window
  behavior (transparent, always-on-top, click-through, non-focus-stealing,
  DPI-aware, multi-monitor), layout constraints (never covering essential
  Dota HUD areas, draggable configuration, compact/expanded modes),
  performance (low CPU/GPU usage), and the five primary live components
  (NextItemCard, PowerSpikeCard, BuybackAlert, PlanCard, ThreatIndicator).
  Use whenever building, modifying, or reviewing the overlay window,
  positioning/layout logic, or any of the five live UI components. A
  visually polished overlay that steals focus, covers the HUD, or drains
  GPU is a shipped defect, not a minor issue — this is a gaming-overlay
  constraints gate as much as a UI guide.
---

# Dota Overlay

## Why gaming overlays are a distinct discipline

A normal desktop application window can assume it has focus when
visible, can occupy screen space freely, and can spend a reasonable CPU/
GPU budget on rendering. None of that is true for a gaming overlay
rendered on top of Dota 2 during active play: the game must keep focus
and keyboard/mouse input at all times, the overlay must not obstruct the
information the player needs to actually play, and it's competing for
CPU/GPU headroom with the game itself, where even small overhead can cost
frame rate the player will immediately notice and resent. Every
requirement in this skill exists because violating it makes the overlay
actively worse than having no overlay at all.

## Window behavior requirements

Full implementation guidance in `references/window-behavior.md`; summary
of what each requirement means and why it's non-negotiable:

- **Transparent** — the overlay window's background must be transparent
  except where a component is actually rendering content, so it never
  visually obscures the game behind empty overlay space.
- **Always-on-top** — the overlay must stay above the game window
  without the player needing to manage window order themselves.
- **Click-through** — mouse clicks must pass through to the game
  everywhere the overlay isn't showing an interactive element; the
  overlay must never accidentally intercept a click meant for the game.
- **Does not steal focus** — the overlay must never take keyboard focus
  or activate itself in a way that pulls input away from the game, even
  when it updates its content or a new alert appears.
- **DPI aware** — the overlay must render correctly and stay correctly
  positioned across different Windows DPI scaling settings, coordinating
  with the same resolution/scaling concerns `dota-cv` handles for capture.
- **Multi-monitor** — the overlay must track and render correctly
  relative to whichever monitor the game window is actually on, including
  setups where monitors have different DPI/resolution from each other.

## Layout constraints

**Never cover essential Dota HUD areas.** This is the overlay's most
important layout rule and the one most likely to be silently violated by
well-intentioned but careless positioning. See
`references/hud-safe-zones.md` for what counts as essential (minimap,
inventory, ability bar, health/mana, top hero bar, etc.) and how to keep
overlay components positioned in genuinely safe zones across the
resolution/aspect-ratio/scaling variance `dota-cv`'s
`resolution-and-scaling.md` already documents for this same underlying
problem.

**Draggable configuration.** The player must be able to reposition
overlay components (or component groups) to fit their own HUD layout/
preferences, since "essential HUD area" varies somewhat by player setup
(custom HUD skins, personal preference for where they keep their eyes).
See `references/hud-safe-zones.md` for how draggable positioning and
safe-zone constraints interact — the player's freedom to reposition
should be bounded by, not exempt from, the "never cover essential HUD"
rule.

## Performance

**Low CPU/GPU usage** is a hard requirement, not an optimization target
to defer. The overlay renders continuously alongside the game; any
meaningful overhead directly costs the player frame rate during the exact
moments (fights, high-pressure decisions) where frame rate matters most.
See `references/performance.md` for concrete guidance (render only on
actual content change, avoid unnecessary continuous animation, minimize
overdraw) and how this ties into `dota-testing`'s performance-benchmark
requirements.

## Prefer minimal UI, with compact and expanded modes

Per `dota-live-coach`'s core rule (the engine may know hundreds of
variables; the player should see 1-3 actions), the overlay's default
visual footprint should be minimal — small, glanceable components, not a
dashboard. Support two modes:

- **Compact** — the default, minimal-footprint presentation, showing only
  what `dota-live-coach`'s priority/budget rules currently call for.
- **Expanded** — a player-initiated, larger view (e.g. for reviewing
  more detail between fights, matching `dota-live-coach`'s guidance that
  richer explanation belongs in a pulled-up detail view, not the live
  stream). Expanded mode is opt-in per session/component, never the
  overlay's default resting state during active play.

See `references/components.md` for how each of the five primary
components maps to compact vs. expanded presentation.

## The five primary live components

Full detail per component in `references/components.md`; summary:

- **NextItemCard** — the current top item recommendation (per
  `dota-item-recommender`), compressed to `dota-live-coach`'s message
  style.
- **PowerSpikeCard** — upcoming/active power-spike window information
  (per `dota-domain`'s power-spike concept).
- **BuybackAlert** — buyback availability/status, typically P0-tier (per
  `dota-live-coach`'s priority tiers) given how costly a missed buyback
  read can be.
- **PlanCard** — the current short-term plan (e.g. `dota-live-coach`'s
  `Farm → BKB → fight.` pattern), representing a sequence rather than a
  single fact.
- **ThreatIndicator** — currently relevant enemy threat information (tied
  to `dota-item-recommender`'s enemy-hero/visible-enemy-item context
  inputs), surfaced compactly.

Every component's content is produced upstream (by
`dota-item-recommender`, `dota-draft`, `dota-domain` reasoning, filtered
through `dota-live-coach`'s presentation rules) — this skill governs how
that already-decided, already-compressed content is *rendered and
positioned*, not what it says. A component showing too much text or
updating too often is a `dota-overlay`/`dota-live-coach` coordination bug
to fix at the presentation layer, not a reason to change the underlying
recommendation.

## Coordinate with frontend-design, preserve gaming-overlay constraints

Visual polish (typography, color, spacing, motion) should draw on the
project's `frontend-design` skill/guidance for a distinctive, well-
designed look — but every design choice must be checked against this
skill's constraints before being applied here specifically:

- Motion/animation must respect the performance budget
  (`references/performance.md`) — a beautiful but continuously-animating
  component is a regression here even if it would be fine in a normal
  desktop app.
- Color/contrast choices must preserve click-through correctness and
  avoid visually implying interactivity where none exists (a
  click-through region that *looks* clickable misleads the player).
  Overlay components rendered on top of gameplay are Overlay/Voice-layer
  UI per `dota-architecture`, subject to this skill's constraints first;
  general `frontend-design` guidance applies within those bounds, not
  instead of them.
- Layout choices must respect HUD safe zones
  (`references/hud-safe-zones.md`) — a visually elegant layout that
  happens to cover the minimap is not an acceptable tradeoff.

When `frontend-design` guidance and this skill's constraints seem to be
in tension, this skill's constraints win — the overlay's job is to be
useful and unobtrusive during live competitive play first, visually
polished second.

## Relationship to other skills

- `dota-live-coach` — governs message content, priority, and brevity;
  this skill governs how that content is rendered/positioned on screen.
- `dota-item-recommender` / `dota-draft` / `dota-domain` — the upstream
  sources of what each component displays.
- `dota-cv` — shares the same resolution/DPI/multi-monitor correctness
  problem (from the opposite direction: reading the screen vs. drawing on
  it); reuse the same geometry-handling discipline rather than
  reinventing it.
- `dota-architecture` — the overlay is the Overlay/Voice layer; it must
  not call external APIs directly and must not contain recommendation
  logic, per that skill's dependency rules.
- `dota-testing` — performance benchmarks for the overlay are part of the
  project's standard performance-benchmark test category.
