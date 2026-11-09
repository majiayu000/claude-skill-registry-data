---
name: build-game-ui
description: Design and implement game HUDs, menus, screen flows, input focus, and state synchronization across engines. Use for playable interfaces requiring controller, keyboard, pointer, touch, safe-area, or lifecycle verification.
engines: [AGNOSTIC]
---

# Build Game UI

## When to use

- Building a HUD, inventory, pause screen, settings flow, or other game interface.
- Fixing lost focus, competing screens, stale HUD state, or binding prompts.
- Preparing engine-specific UI implementation and representative device verification.

## Workflow

1. Read `ENGINE.md`, resolve the effective engine, and select its UI feature skill through `resolve-skill.sh`. Keep hierarchy and interaction rules here; the compatible engine skill owns UI APIs. Browser tooling requires an actual browser surface, including a selected engine's web build.
2. Define the player's information needs before, during, and after decisions. Assign persistent, contextual, and on-demand information, reading order, semantic states, and non-color cues. Prefer measured legibility in play over static mockup density.
3. Specify layout constraints for supported aspect ratios, pixel densities, safe areas, localization expansion, text scaling, split-screen viewports, and touch targets. Test small and large content rather than scaling one reference image uniformly.
4. Give each screen explicit lifecycle and input ownership: enter, suspend, resume, exit, modal stack, allowed actions, pause policy, and initial/return focus. Route an action to one owner; a modal must prevent hidden gameplay or lower screens from consuming the same input. Closing an outer screen dismisses or reparents owned children deliberately.
5. Map navigation through semantic destinations, including disabled, hidden, removed, or virtualized controls. Restore focus to the invoking control when valid, otherwise a defined fallback. Support device changes and binding-aware prompts without stealing active text entry or pointer intent.
6. Initialize HUDs from an authoritative snapshot and subscribe to subsequent changes without a snapshot/event race, using a revision or equivalent ordering contract. Render state without becoming its owner. Unsubscribe on teardown, avoid duplicate listeners on reopen, clear stale asynchronous responses, and reconcile scene, player, save, or network changes.
7. Define loading, empty, disconnected, error, and confirmation states. Keep essential information available when animation, audio, or haptics are reduced or unavailable. Coordinate presentation with `build-gameplay-runtime`; screen transitions do not decide gameplay outcomes.
8. Verify actual input and runtime behavior using the scenarios below. Record environment, scope, expected/observed results, evidence, and blocked or not-run cases with the gameplay review's `ui` profile.

## Verification scenarios

- Open a nested modal with a held gameplay action; confirm exclusive ownership, release handling, return focus, and pause policy after close.
- Remove the focused inventory item, disable a neighboring control, switch device, and change a binding; confirm a reachable fallback and accurate prompt.
- Resize, apply the largest supported text scale, use long localized strings, and test each local player's safe area without covering critical information.
- Apply a state change during HUD creation, hide/reopen it repeatedly, then switch scenes or player; confirm no lost update, duplicate notification, stale data, or surviving listener.
- Test reduced motion, low contrast situations, muted audio, and missing tactile devices; essential states and actions remain understandable.

## Output

- An information hierarchy, screen-state/input-ownership contract, navigation map, and responsive layout rules.
- Engine-compatible UI implementation with explicit state bindings, lifecycle disposal, accessibility, and error behavior.
- Scenario evidence and residual risks for the tested build, device, input method, and layout range.

## Guardrails

- Do not certify native UI using browser screenshots, or treat DOM focus as evidence of engine-native focus.
- Do not duplicate authoritative gameplay state inside a widget or depend on animation completion to unlock essential actions.
- Do not imply physical haptic output from an API mock or a visual effect.
