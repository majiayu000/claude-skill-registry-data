---
name: domain-tests
description: Use when adding or changing logic in kasane's `src/data/`, `src/state/`, or `src/api/` layers, or when asked to add test coverage, write unit tests, or verify pure functions in this repo.
---

# Domain Tests

kasane's whole product claim is that episode N maps to chapters X-Y. The functions that decide that live in `src/data/mapping.ts` (arc lookups), `src/data/arcLayout.ts` (where a position lands on the rail and pie) and `src/data/pairing.ts` (which anime goes with which manga). Everything else is presentation.

**REQUIRED BACKGROUND:** `superpowers:test-driven-development` for the RED-GREEN cycle. This skill covers the repo-specific conventions and what is worth testing here.

## The convention

`src/state/syncMerge.test.ts` is the reference. Match it:

- Colocate as `<module>.test.ts` next to the source. Tests run on `bun test` (`bun run test`); `@/` resolves to `src/`. Import `describe`/`it`/`expect` (and `mock`/`spyOn`) from `bun:test` in every test file.
- Native-only modules (`react-native`, AsyncStorage, `expo-linking`) and `@/api/supabase` are mocked in the preload `test/setup.ts` — bun has no `jest.mock` hoisting, so they must be mocked before any test file imports them. Drive the Supabase auth mocks via `@test/mocks/supabase`. Test-only modules live under `test/`, never in `src/`.
- `bun run test` passes `--parallel`: each test file runs in its own worker process with its own global (`--parallel` implies `--isolate`), and the preload runs once per file. Module state does **not** leak between files. Do not rely on it leaking, and do not assume a bare `bun test` — which is still single-process — will catch the same bugs.
- One `describe` per exported function, `it` names stating the behaviour, not the mechanism.
- Build inputs as typed literals with an explicit type annotation, never a cast.
- Assert whole objects with `toEqual`, not field-by-field. A regression that adds a stray key should fail.
- Small named helpers for repeated construction (`const iso = (ms: number): string => new Date(ms).toISOString()`).
- No network, no `@supabase/supabase-js`, no `react-native` imports in a pure-logic test. If a module needs mocking to test, the logic is in the wrong file: extract it, the way `syncMerge.ts` was extracted out of `sync.ts`.

Repo rules apply to test files too: no `interface`, no `any`, no casts, `const` over `let`, `Array.prototype` methods over loops.

## Coverage

`bun test` reports coverage on every run and enforces a floor from `bunfig.toml`. That floor is applied **per file, not across the run** — one module below the bar fails the suite even when the total is far higher. Only files a test actually imports are measured, so an entirely unimported module is invisible rather than failing. Because of that, the number is set by the weakest covered file, not the average; raising it means covering that file first.

Coverage is a floor, not the goal. A module at 100% whose assertions are `toBeTruthy()` catches nothing. Before claiming a test is worth having, mutate the source it covers — flip a `<=` to `<`, drop a `.sort`, widen a filter — and confirm the suite goes red.

## What is worth testing, in priority order

| Function                                                      | Cases that matter                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `episodeToChapters`                                           | Exact lower and upper boundary of an arc; an episode inside a gap between arcs; an episode past the last adapted arc; arcs with `episodes: undefined` (unadapted tail) never matching.                                                                                             |
| `chapterToEpisodes`                                           | Same boundaries; a chapter in an unadapted arc returns `null` rather than the arc's chapters; a chapter beyond the last arc.                                                                                                                                                       |
| `pairResults`                                                 | A manga absorbing its anime adaptation; an anime with no source manga staying `anime-only`; several anime sharing one source manga collapsing to one `routeId` and keeping the **first**; badge assignment for all three values.                                                   |
| `buildSyntheticMapping`                                       | Returns `null` with no relations, with no qualifying partner, and when either count is missing; picks the **earliest** partner by `startDate.year`; produces `[1, episodes]` to `[1, chapters]`.                                                                                   |
| `getAnimeFranchise`, `hasAnimeSequels` (`src/api/anilist.ts`) | Franchise-root detection and cumulative `totalTvEpisodes`. Feed fixture AniList payloads through `graphqlRequestMock`; do not hit the network. Type fixtures against the exported query types (`FranchiseRawNode`), never a hand-copied shape.                                     |
| `rowToMapping` (`src/data/catalog.ts`)                        | Supabase rows arriving out of `position` order must sort; null episode bounds must become `undefined`, not `[null, null]`. Pure: pass the fixtures in `@test/fixtures/catalog` straight in. `fetchCatalog` (`src/api/catalog.ts`) gets one end-to-end test through `serveCatalog`. |
| `fractionAt` (`src/data/arcLayout.ts`)                        | The end of each arc lands exactly on its bar's edge, including on mappings with gaps between arcs; positions in a gap park at the previous segment's end.                                                                                                                          |

Both lookup helpers return the **first** matching arc. Overlapping arcs therefore make a lookup silently order-dependent, which is why `mapping-audit` treats overlap as an error. The tests pin that behaviour so a future refactor to `filter` does not change answers.

## Testing a hook

Every `useQuery` lives in `src/queries/`, and `src/queries/catalog.test.ts` is the reference. Use `renderHook` and `settle` from `@test/renderHook`: the hook renders inside a `QueryClientProvider` with `retry: false`, and settles by awaiting a **macrotask** (`setTimeout`) inside `act()` — a microtask flush alone resolves the first query in a file but not later ones.

A settle helper must **throw** when it runs out of ticks. Returning quietly turns "the query never resolved" into a confusing assertion diff further down the test.

## One good example

```ts
import { describe, expect, it } from "bun:test";
import { episodeToChapters } from "./index";
import type { SeriesMapping } from "@/types";

const mapping: SeriesMapping = {
  anilistAnimeId: 1,
  anilistMangaId: 2,
  title: "Test",
  mappings: [
    { episodes: [1, 12], chapters: [1, 40], arc: "First" },
    { episodes: [13, 24], chapters: [41, 80], arc: "Second" },
    { chapters: [81, 120], arc: "Unadapted tail" },
  ],
};

describe("episodeToChapters", () => {
  it("resolves the last episode of an arc to that arc's chapters", () => {
    expect(episodeToChapters(mapping, 12)).toEqual([1, 40]);
  });

  it("resolves the first episode of the next arc", () => {
    expect(episodeToChapters(mapping, 13)).toEqual([41, 80]);
  });

  it("returns null past the adapted range", () => {
    expect(episodeToChapters(mapping, 25)).toBeNull();
  });
});
```

## Common mistakes

| Mistake                                   | Fix                                                                                                                                                                                                                       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Testing only the middle of a range        | Off-by-one lives at the boundary. Assert both ends of every arc.                                                                                                                                                          |
| Using a real catalog entry as the fixture | Catalog data changes in Supabase and would silently break the test. Build minimal literals.                                                                                                                               |
| Mocking `supabase` to test merge logic    | The pure part already lives in `syncMerge.ts`; test it there. `sync.test.ts` covers only orchestration — what gets pushed, retried or skipped — against a fake of the two user tables, with fake timers for the debounce. |
| `as SeriesMapping` on a partial literal   | Banned by CLAUDE.md and hides the missing fields the function reads. Build the whole object.                                                                                                                              |
| Asserting `toBeTruthy()` on a tuple       | `toEqual([41, 80])` catches a swapped pair; `toBeTruthy` does not.                                                                                                                                                        |
| Leaving a module singleton set            | The zustand stores outlive the test. Reset them in `beforeEach`, so the file's own first test is protected too — `afterEach` only tidies up for whoever runs next.                                                        |
| Calling `mockClear` in a test file        | The preload already clears call history after every test. A local reset is redundant, and clearing shared history breaks anything asserting on an import-time call.                                                       |
| Asserting on an import-time `mock.calls`  | Module-scope side effects fire once per process, so the history may be cleared before your test runs. Record what you need as state on the mock — see `authSubscribers`.                                                  |
| Chasing the coverage number               | Mutate the source and watch it go red. Percentage is a floor, not evidence.                                                                                                                                               |
