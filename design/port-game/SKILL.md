---
name: port-game
description: Port one game from the design file into Nuxt. Use when the user asks to port, build, or finish a game listed under "Porting status" in CLAUDE.md (pairs, odd, serial7, words, category, backward, digits, sequence, nback, stroop, schulte, hand), or mentions RUN.<id>. Copies RUN.<id> from docs/design.html into app/components/games/<Component>.vue with a spec and a registry line. Runs inside the /feature loop.
---

# Port a game

This skill fills in steps 1, 3 and 4 of the `feature` skill for a game port. Still run the full `feature` loop: plan, approval, red, green, check, UI check, review.

## Find the pieces

1. `<id>` is the game id, for example `pairs`.
2. Read `app/data/games/<id>.json`. Its `component` value is `<Component>`, for example `MemoryPairs`.
3. Read `RUN.<id>` in `docs/design.html` (`grep -n "RUN.<id>=" docs/design.html`). Also read every helper it calls (`h`, `pick`, `shuffle`, `listGame`, `stopAll`, timers) so you know what each one does.
4. Read the game's row in `docs/functional-requirements.md` §5. The spec tests that behaviour.
5. Read one finished game as a model: `app/components/games/MentalMath.vue` and `test/nuxt/components/games/MentalMath.spec.ts`.

## Rules for the port

- Copy the logic of `RUN.<id>`. Same rules, same numbers, same timings, same scoring. Do not redesign it.
- Contract: `defineProps<{ game: GameDef }>()` and `defineEmits<{ finish: [score: number] }>()`. Nothing else. No progress, no routing.
- Read copy from `props.game` (`durationSec`, `unit` and so on). Never hard-code game copy that lives in the JSON.
- Timers: `useCountdown` for the game clock, `useTimeouts().later` for sequencing. No raw `setInterval`/`setTimeout` unless cleared in `onBeforeUnmount`.
- Random: use `pick`, `ri` and the other helpers in `app/utils/random.ts`. Add a helper there (with a spec) if the design uses one that is missing.
- Encouragement: `useCheer().cheer()` on the same milestones as the design. Mistake copy stays kind: "It was X. Carry on from there."
- Markup: reuse the classes from `app/assets/css/components.css` that design.html uses (`.bar`, `.hud`, `.big`, `.field`, `.board`, `.cell`, `.react`, `.breath`, `.card`, `.go`, `.ghost`, `.row`, `.note`, and others). Every other style is Tailwind utilities that map to the tokens (CLAUDE.md rule 7). The design's `max-width` queries map to `max-xl` (1000px), `max-lg` (760px), `max-md` (640px), `max-sm` (560px) and `max-xs` (380px). No raw colours, no new rules in `components.css` unless the class is shared by two or more games. Prettier sorts the classes (`prettier-plugin-tailwindcss`).
- Tests find elements by `data-testid`, ARIA attributes (`aria-pressed`, `aria-current`) or `data-state`, never by a styling class.
- The design's game class `grid` is called `board` in components.css, because `grid` is a Tailwind utility. Write `class="board"` where `RUN.<id>` writes `grid`.
- Accessibility: real `<button>` elements, `aria-label` on icon-only buttons, Enter/Space works, inputs have `font-size` of 16px or more.
- WordSprint and CategoryChallenge share `listGame()`. Port it once as `app/composables/useListGame.ts` with its own spec `test/nuxt/composables/useListGame.spec.ts`.
- Stay under about 150 lines. Move logic into a composable if it grows.
- No code comments.

## Files

| File                                             | Action                                                                                |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| `app/components/games/<Component>.vue`           | New. The port.                                                                        |
| `test/nuxt/components/games/<Component>.spec.ts` | New. Written first by the `test-writer` agent. See the `write-unit-tests` skill.      |
| `app/components/games/registry.ts`               | Add one line: `<Component>: defineAsyncComponent(() => import('./<Component>.vue')),` |
| `app/composables/<useX>.ts` + spec               | Only if logic is split out.                                                           |
| `CLAUDE.md` "Porting status"                     | Move the game from "To port" to "Done". Ask the user before editing CLAUDE.md.        |

The registry key must equal `component` in the JSON. If it does not, the game falls back to `ComingSoon.vue`.

## What the spec must cover

- The score passed to `finish` for a known play, using fake timers and the real game JSON.
- Each rule in the §5 row: timing, level-ups, the end condition, and what a mistake does.
- Lower-is-better games (`pairs`, `schulte`, `reaction`): the score goes the right way.
- Keyboard play: Enter or Space triggers the main action.
- No timer still runs after unmount (`vi.getTimerCount()` is 0 after `wrapper.unmount()`).

## Done when

- The spec went red before the port and is green after it.
- `npm run lint`, `npm run typecheck` and `npm test` pass.
- `ui-verifier` compared `/games/<id>` with `docs/design.html#<id>` in the ready, playing and result states and found no high or medium issues.
- In the app, the tile, the ready demo, the result band and the sidebar highlight all work.
