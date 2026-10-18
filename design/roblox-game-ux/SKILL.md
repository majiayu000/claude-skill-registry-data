---
name: roblox-game-ux
description: Design and critique Roblox game UX, HUDs, menus, onboarding, mobile controls, and progression surfaces. Use when making a Roblox experience feel clear, fast, touch-friendly, and retention-aware.
---

# Roblox Game UX

## UX Principles

- Put the player into the core action within 10-30 seconds.
- Teach by doing, with objective markers and contextual prompts instead of instruction walls.
- Keep the first screen focused on play, not menus or exposition.
- Make rewards loud enough to understand but short enough to keep momentum.
- Design for phone screens first, then expand to desktop and tablet.

## Mobile-First Controls

- Use large touch targets and generous spacing.
- Avoid controls that require precision dragging unless the whole game is built around it.
- Add auto-targeting, aim assist, snapping, or simplified actions where useful.
- Keep critical buttons away from screen edges and system gesture zones.
- Make HUD text readable on small screens and keep important information out of thumb-heavy areas.

## HUD And Menus

- Surface current objective, currency, progress, health/energy, and next reward.
- Keep deep menus optional during the first session.
- Use clear iconography and consistent button placement.
- Make progress bars and collection meters visible during the loop.
- Avoid popups that interrupt core action, especially in the first five minutes.

## Onboarding Flow

Recommended first-session order:

1. Spawn facing the first interactable or objective.
2. Prompt one action.
3. Give immediate feedback and reward.
4. Show the next short goal.
5. Reveal social or progression context after the player has already acted.

## UX Review Output

When reviewing a Roblox UX, report:

- First-action time.
- Friction points before gameplay.
- Mobile-control risks.
- Missing progression signals.
- Social visibility gaps.
- Monetization interruptions.
- Priority fixes ranked by retention impact.

## Design The UI Before It Is Built

For any non-trivial UI surface, produce and get approval on a **UI design artifact** before `roblox-ui-implementation` builds it. This is the visual contract; it prevents Claude from improvising layout, states, and mobile behavior mid-build. Roblox UI is built in Studio, so the artifact is a markdown design brief (optionally with reference images/screenshots), not an HTML mockup.

Create it under `design/features/<feature-slug>/design.md` (global patterns live in `design/DESIGN.md`; see `docs/agents/design.md`). The brief must cover:

- User goal and which surface/flow this is (HUD, shop, reward, menu…).
- Layout and responsive behavior across **mobile, tablet, and desktop**, including safe areas and thumb zones.
- Every relevant state: **default, empty, loading, error, and permission/locked**.
- Interactions and copy rules.
- A `Status:` line — `draft` until the user approves, then `approved`.

Iterate with the user until they approve, then set `Status: approved`. A UI slice cannot become `ready-to-build` (in `roblox-to-issues` / `roblox-triage`) until this artifact is approved.

## Next

Once the design brief is approved, hand it to `roblox-ui-implementation` to build. If the UI is part of a larger feature, slice it with `roblox-to-issues`. Verify the built result with `roblox-mobile-playtest` and `roblox-playtest-qa`.

