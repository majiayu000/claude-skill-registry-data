---
name: game-feel-and-juice
description: Use when designing, tuning, or reviewing the moment-to-moment feel of ANY action in ANY genre — responsiveness, input latency, forgiveness windows (coyote time, input buffering), the juice toolkit (hit-stop, screen shake, squash/stretch, particles, easing, sound layering), the 12 animation principles, camera feel, and UI/menu feel. Also use to diagnose controls that feel floaty, laggy, mushy, weightless, or a screen so noisy you can't read game state. Triggers on "game feel", "juice", "juicy", "feels floaty", "feels unresponsive", "input lag", "coyote time", "input buffering", "hit-stop", "screen shake", "squash and stretch", "easing", "tweening", "feedback", "make it feel good", "game feels mushy".
---

# Game Feel & Juice

How to make *any* action — a jump, a gunshot, a match-3 pop, a card play, a button press — feel responsive, weighty, and readable. Feel is engineerable: tight control + a consistent simulation + a tuned layer of feedback, with feedback held to a measured ceiling so it communicates instead of overwhelming.

> **Tier:** universal craft (→ `gamestack-core`). Applies to every genre and every game. The combat-specific application of these tools lives in `combat-design`, which cites *up* to this skill.

## When to use this

- Tuning how a verb feels: input response, forgiveness windows, the juice bundle on an action
- Authoring a per-action **feedback budget** a generator can apply consistently
- Auditing why controls feel floaty/laggy or why the screen is unreadable noise
- Specifying camera feel, UI/menu feel, and animation timing at the design level

## Scope

This skill owns **the feel of an action in isolation** — control, simulation fidelity, and the feedback layered on top. Adjacent concerns live in sibling skills:
- Combat-specific feel: hit-stop per damage tier, telegraphing as fairness, enemy/encounter feel → `combat-design` (applies this skill to hits)
- Where feedback fits the HUD and information hierarchy → `ui-ux-and-feedback`
- Visual readability, silhouette, signal color → `art-direction-and-readability`
- Macro rhythm across a session (this skill is the second-to-second layer) → `pacing-and-the-player-journey`
- Reward/flow/motivation theory underneath → `game-design-fundamentals`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in six sub-domains: Swink's three building blocks (control · simulated space · polish), input & response (latency, buffering, coyote time, forgiveness), the juice toolkit (squash/stretch, anticipation, follow-through, hit-stop, shake, particles, easing, sound), the 12 animation principles applied to games, camera feel, and UI/menu feel. Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The two ideas to anchor on

> **1. Fix feel before you juice it.** Game feel (Swink) is real-time *control* of an avatar in a consistent *simulated space*; juice is the audiovisual *polish* on top. Polish layered over laggy controls or inconsistent physics is lipstick — strip every effect and the core must still feel right. Order: latency → forgiveness → simulation → *then* juice.

> **2. Juice has a ceiling — it's an inverted U.** The largest study on the subject (Kao 2020, N=3,018) found *Extreme* juice hurts experience, motivation, *and* raw performance as much as *None*. Tune to the **Medium–High band**; reserve the biggest effects for the rarest moments. More feedback that obscures game state makes the player feel *controlled by* the game, not in control of it.

> **Why this matters doubly for a generator:** a human team feels laggy controls or a juice-overloaded screen as "off." An autonomous generator does not. Hand-author the physics constants, the forgiveness windows, and a **per-action feedback budget table** (event × magnitude → bounded bundle) as inviolable contracts; let generation compose vetted parts inside them; run a feedback-budget linter and a physics-contract validator before any content is committed.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
