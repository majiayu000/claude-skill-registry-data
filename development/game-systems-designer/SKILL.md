---
name: game-systems-designer
description: Use when designing the systems of a game from a locked concept — core loops, meta loops, player verbs, progression, content systems, level structure, and narrative integration. Triggers on "game design doc", "GDD", "system spec", "core loop design", "progression design", "level design", "MDA", or "design the systems". Produces a design doc plus per-system specs that game-balancer numbers, iap-manager stocks, and godot-engineer builds. Stops at design — no number tuning, pricing, or engine code. For balance numbers see game-balancer; for the engine implementation see godot-engineer.
when_to_use: |
  Use when a locked game concept is ready to be turned into a definition of what the game is
  (core loop, meta loops, player verbs, progression, content systems,
  level structure, narrative integration); when an existing design doc needs a new system added
  or an existing one reworked; when a live game update requires a system change; or when a
  prototype has validated a core loop and needs meta and content layers designed around it.
  Triggers on "game design doc", "GDD", "system spec", "core loop design", "progression
  design", "level design", "MDA", or "design the systems".

  Not when: the request is still SHAPING the game concept/brief — load-bearing items (target
  player, core fantasy, platform, success bar) are not yet locked and you have a "game design
  plan" or "game design doc" ask without a locked concept to design from — use
  `game-design-shaper` first. Not
  when the systems are locked and the team wants numbers tuned — use `game-balancer`. Not when
  the task is writing the engine implementation — use `godot-engineer`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Game Systems Designer

Your job is to turn a locked concept one-pager into a **design** that downstream skills can build, balance, monetize, and ship. You produce: the design doc, per-system specs, loop diagrams, progression structure, and level/content framework. You do not pick numbers (`game-balancer`) or write engine code (`godot-engineer`).

If systems are locked and the team wants numbers tuned, **stop** and route to [game-balancer](../game-balancer/SKILL.md).

## Procedure

1. Read the locked concept one-pager end-to-end (fantasy, aesthetics, player verbs, payment rails, comp titles).
2. Apply MDA backwards — start from *aesthetics* → *dynamics* → *mechanics*. See [references/mda-framework.md](references/mda-framework.md).
3. Specify the core loop — see [references/core-loops-and-progression.md](references/core-loops-and-progression.md). One core loop only.
4. Specify meta loops — what carries between sessions; each must connect back to the core loop.
5. Specify player verbs — for each verb (max 3): input, representation, feedback, failure mode, depth axis. See [references/player-verbs.md](references/player-verbs.md).
6. Specify content systems — type, volume per arc, variety source. See [references/content-and-levels.md](references/content-and-levels.md).
7. Specify narrative integration — delivery method, minimum narrative needed. See [references/narrative-and-pacing.md](references/narrative-and-pacing.md).
8. Specify failure and onboarding — see [references/onboarding-and-failure.md](references/onboarding-and-failure.md).
9. Fill `assets/design-doc-template.md` — canonical design output.
10. Fill `assets/system-spec-template.md` once per major system.
11. Validate cohesion — see [references/cohesion-checklist.md](references/cohesion-checklist.md). Every system must answer "what does this make better in the rest of the game?"
12. Hand off to [game-balancer](../game-balancer/SKILL.md), [iap-manager](../iap-manager/SKILL.md), [godot-engineer](../godot-engineer/SKILL.md).

## Universal Rules

- Aesthetics first, mechanics last
- One core loop; two means one is meta
- Three player verbs maximum
- Every system must compound — a system that doesn't make another better should be cut
- Failure is a system — design how it feels fair and what players take from it
- Numbers are placeholders — use `<TBD by game-balancer>` for damage values, XP curves, drop rates
- Pricing is not a system — no dollar values or store SKUs in the design doc
- Stop at the spec — no engine code, shaders, or networking

## Related Skills

- [game-balancer](../game-balancer/SKILL.md) — tunes the numbers in the system specs
- [iap-manager](../iap-manager/SKILL.md) — catalogs the SKUs the design implies
- [godot-engineer](../godot-engineer/SKILL.md) — builds the design in Godot 4 + C#
- [content-ops](../content-ops/SKILL.md) — expert-panel scoring of the design doc before committing to build
