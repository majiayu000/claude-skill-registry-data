---
name: svelte-game-writer
description: End-to-end planning, building, and testing of small-scale browser games in SvelteKit + TypeScript running in Docker, including scaffolding, game loop, input, UI, tests, and Docker dev/release setups. Use when a user asks to create or modify a SvelteKit game project, prototype a simple single-player game, or add tests. When requirements are unclear, ask clarifying questions and offer to choose defaults automatically if the user prefers. This skill uses SvelteKit+TS in Docker only (debug hot-reload + nginx release); do not switch stacks unless the user explicitly asks to change scope. Not for multiplayer, servers, or backend services.
---

# Svelte Game Writer

Build small, single-player browser games end-to-end in SvelteKit + TypeScript running in Docker. Focus on local gameplay only (no multiplayer, no backend services).

## Quick intake

Ask only what is needed to proceed:
- Game type and core loop (e.g., runner, puzzle, shooter)
- Rendering mode (DOM/SVG vs Canvas)
- Input targets (keyboard, mouse, touch)
- Target device (desktop, mobile, both)
- Art/audio constraints (placeholders OK?)
- Testing scope (unit only vs unit + e2e)

If any answer is unclear, ask a brief clarification and offer to proceed with automatic defaults if the user prefers.

## Workflow

1) **Plan**
   - Summarize the core mechanics in 1–2 sentences.
   - Define win/lose conditions and progression.
   - List game states/scenes (e.g., menu, play, pause, game-over).
   - Identify data structures and update frequency (fixed timestep vs variable delta).

2) **Scaffold**
   - Use the SvelteKit + TypeScript Docker scaffold in `assets/bare-docker-app/` and copy it into the project root.
   - Keep dependencies minimal and local-only.
   - Provide both Docker dev (hot-reload) and release (nginx) flows.
   - Add test tooling: Vitest + @testing-library/svelte; Playwright for smoke tests.

3) **Implement core loop**
   - Use `requestAnimationFrame` with a fixed timestep accumulator for deterministic logic.
   - Separate `update(dt)` from `render()`; avoid heavy work in Svelte reactive statements.
   - Keep game state in a plain object/store; expose read-only to UI.

4) **Input + UI**
   - Centralize input handling (keyboard/pointer) and normalize to actions.
   - Keep UI (score, lives, menus) in Svelte components; keep simulation logic framework-agnostic.

5) **Assets**
   - Use placeholders by default; allow easy swap via a simple `assets.ts` map.
   - If audio is required, gate playback on first user interaction.
   - Docker bare scaffold lives in `assets/bare-docker-app/` (SvelteKit + TypeScript, dev+prod Docker, nginx release).

6) **Testing**
   - Unit test pure logic: collisions, scoring, state transitions.
   - Component test HUD/menus with Testing Library.
   - Optional Playwright smoke test: load page, start game, verify canvas/UI renders.
   - If MCP is available, prefer Playwright MCP and use `browser_take_screenshot` for visual confirmation.

7) **Deliver**
   - Provide run/test commands and a brief README-style usage note.
   - Call out constraints (no multiplayer/server) and suggested extensions if requested.

## Project structure (default)

- `src/lib/game/` core logic (state, systems, input)
- `src/lib/game/render/` rendering helpers (canvas, sprites)
- `src/lib/ui/` Svelte components (HUD, menus)
- `src/routes/` entry
- `src/app.d.ts` SvelteKit types
- `tsconfig.json` TypeScript config
- `tests/` unit + component tests
- `e2e/` Playwright smoke tests (optional)

## Implementation patterns

### Game loop (fixed timestep)

- Keep a `state` object with positions/velocities/flags.
- In `tick(now)` accumulate `delta` and call `update(fixedDt)` in a loop.
- Render with interpolation factor `alpha` if needed.

### Input mapping

- Map raw events to actions (`left`, `right`, `jump`, `fire`).
- Store current and edge states (pressed, justPressed).

### Scene/state machine

- Use a simple enum + switch to drive scene transitions.
- Keep transition logic in `update()`; UI observes current scene.

## Testing guidance

- Use deterministic seeds for random elements in tests.
- Mock `performance.now` and `requestAnimationFrame` for unit tests.
- Prefer small pure functions for collision, spawning, and scoring.

## TypeScript reliability guidelines

- Type all public module boundaries (inputs/outputs) and shared state objects; avoid `any`.
- Use `readonly` for immutable state snapshots and `as const` for action enums.
- Prefer discriminated unions for game states/scenes and exhaustive `switch` with `never`.
- Use `satisfies` to validate configuration objects without widening types.
- Keep math/physics in pure, typed functions; make side effects explicit.

## Constraints

- Do not design or implement multiplayer, servers, or backend APIs.
- Do not switch away from SvelteKit + TypeScript + Docker unless the user explicitly changes scope.
- If the user requests those, explain the constraint and offer a single-player alternative or ask to switch scope.

## Output quality checklist

- Game starts, runs, and ends deterministically.
- Controls feel responsive and are documented.
- No console errors at idle or during play.
- Tests pass locally with provided commands.
