---
name: write-unit-tests
description: How to write Vitest specs for Brain Games. Use when writing or changing any file under test/nuxt/, when a source file under app/ needs its spec, when the Stop hook reports a missing spec, or when the test-writer agent runs. Covers the spec path rule, the patterns for games, composables, components, pages and game JSON, and the mutation check that proves each test can fail.
---

# Write unit tests

## Where specs live

Rule: `app/<path>/<Name>.<ext>` → `test/nuxt/<path>/<Name>.spec.ts`.

| Source                                 | Spec                                             |
| -------------------------------------- | ------------------------------------------------ |
| `app/components/games/MemoryPairs.vue` | `test/nuxt/components/games/MemoryPairs.spec.ts` |
| `app/components/home/GameTile.vue`     | `test/nuxt/components/home/GameTile.spec.ts`     |
| `app/pages/games/[id].vue`             | `test/nuxt/pages/games/[id].spec.ts`             |
| `app/composables/useProgress.ts`       | `test/nuxt/composables/useProgress.spec.ts`      |
| `app/error.vue`                        | `test/nuxt/error.spec.ts`                        |

No spec needed for: `app/app.vue`, `app/layouts/**`, `app/components/games/registry.ts`, `app/data/**` (covered by `test/nuxt/data/game-contract.spec.ts` and `copy.spec.ts`), `app/assets/**`, `shared/types/**`, `*.d.ts`.

The Stop hook enforces this. Check paths without running the suite:

```
.claude/hooks/require-tests.sh --dry-run app/path/To/File.vue
```

## Setup

- Vitest runs in the Nuxt environment with happy-dom (`vitest.config.ts`). Auto-imports work in specs.
- Imports: `~/` is `app/`, `~~/` is the repo root.
- Shared data lives in `test/nuxt/fixtures.ts`: `mathGame`, `reactionGame`, `breathGame`, and `makeGame(bandsAt, lowerIsBetter)`. Add new fixtures there, not inline copies of game JSON.
- `restoreMocks` is on. Reset `localStorage` and fake timers in `beforeEach`/`afterEach`.
- Run one file: `npx vitest run test/nuxt/components/games/X.spec.ts`. Run all: `npm test`.

## Patterns

### Games (`app/components/games/*.vue`)

Test only the contract: props in, `finish(score)` out. Model: `test/nuxt/components/games/MentalMath.spec.ts`.

```ts
beforeEach(() => vi.useFakeTimers())
afterEach(() => vi.useRealTimers())

it('finishes with the number solved when time runs out', async () => {
  const wrapper = await mountSuspended(MentalMath, { props: { game: mathGame } })
  // play through the DOM: setValue, trigger('click'), trigger('keydown', { key: 'Enter' })
  vi.advanceTimersByTime((mathGame.durationSec ?? 60) * 1000 + 200)
  expect(wrapper.emitted('finish')).toEqual([[3]])
})
```

- Drive the game through the DOM like a player. Do not call internal functions.
- Use the real game JSON from `~/data/games/<id>.json` via a fixture.
- Control randomness with `vi.spyOn(Math, 'random').mockReturnValue(...)` when the score depends on it.
- Check `finish` is emitted exactly once, with the exact score.
- Check that no timer is left after `wrapper.unmount()`: `expect(vi.getTimerCount()).toBe(0)`.
- Check keyboard play (Enter or Space) for the main action.

### Composables (`app/composables/*.ts`)

Call the composable inside a component setup with `withSetup`. Use it from `test/nuxt/fixtures.ts` if it is there; otherwise copy the helper at the top of `test/nuxt/composables/useCountdown.spec.ts`.

- State made with `useState` survives between tests. Call `clearNuxtState('<key>')` (from `#imports`) before each fresh instance. Model: `test/nuxt/composables/useProgress.spec.ts`.
- Pin the date with `vi.useFakeTimers({ toFake: ['Date'] })` and `vi.setSystemTime(...)` for streaks, days and daily picks.
- For progress, assert what is written to `localStorage` under the `bgarden` key.

### Components and pages

Mount with `mountSuspended(Component, { props })` or render a route with `mountSuspended(Page, { route: '/games/math' })`.

- Assert what the user sees: text, `aria-current`, `aria-label`, links (`href`), disabled state, the count of tiles.
- Assert behaviour from functional-requirements: band highlight, "not played yet", struck-through daily games, 404 for an unknown id.
- Seed progress through `localStorage.setItem('bgarden', JSON.stringify({...}))` plus `clearNuxtState('progress')`, not by mocking `useProgress`.
- Do not snapshot whole components. Do not assert CSS class names unless the class is the behaviour (for example `.you` on the current band).

### Utils (`app/utils/*.ts`)

Plain function tests. Cover the edges named in the requirements, for example `bandIndex` with `lowerIsBetter` and `at: null`.

### Game JSON

`test/nuxt/data/game-contract.spec.ts` checks every file against functional-requirements §4. If you add a field to the contract, add the check there.

## Write tests from the spec, not the code

- Every expected value comes from `docs/functional-requirements.md`, the game JSON, or `RUN.<id>` in `docs/design.html`. Never copy an output from the code under test.
- Name each test after the behaviour: `it('adds 5 XP when a previous best is beaten')`.
- One behaviour per test.

## Prove each test can fail

A test that never fails is worth nothing. For each new test:

1. Make one real mutation in the source that breaks the behaviour: flip a comparison, change a constant, drop a line, skip the `emit`.
2. Run the spec. It must fail, and the failure message must point at that behaviour.
3. Undo the mutation. Run again. It must pass.

When the code does not exist yet (red phase), the first failing run is the proof. Note in your report which mutation you used for each test, or "red before implementation".

## Pitfalls

- A component that uses `useTheme` or `useHead` must be unmounted (`afterEach(() => wrapper.unmount())`) before `clearNuxtState('progress')`, or the run reports unhandled rejections.
- To mock a game component loaded by `defineAsyncComponent` in the registry, the `vi.mock` factory must return `__esModule: true` along with `default`.

## Never

- Never weaken an assertion, add `.skip`, or delete a test to get green. Fix the code or ask.
- Never mock the unit under test.
- Never use real timers or real waits (`setTimeout` in a test). Use fake timers.
- No comments in spec files unless the user asks.
