---
name: writing-tests
description: The spec conventions for this repo — globals are off, specs sit beside their subject, titles name the failure being pinned, specs assert observable behaviour rather than copy, call order or internals, and every boundary has one recipe. Use when adding or changing any *.spec.ts anywhere in the workspace.
---

# Writing specs here

One recipe. None of it is configured per project — every `vitest.config.ts` in the workspace builds
on [`@joinery/configs`](../../../packages/configs/src/vitest/node.ts), so the conventions below are
the whole of what makes a spec fit in. The test a spec has to pass: **a change to behaviour fails
it, and a change that alters no behaviour — rewording copy, moving a margin, reordering two
independent calls — leaves it green.**

## The three things that break first

- **`globals: false`.** Import `describe`, `it`, `expect` and `vi` from `vitest` in every file. A
  spec written against the ambient globals fails to typecheck, not to run, so the error arrives from
  somewhere unhelpful.
- **The spec sits beside its subject**, same basename: `translationsKey.ts` →
  `translationsKey.spec.ts`. There is no `__tests__` and no fixtures directory anywhere in the
  workspace; the `__mocks__` folders in huella-legal's layers feed Storybook and no spec reads them.
  Test data is a `const` at the top of the file it belongs to, and a content domain value (`Entry`,
  `Term`, `Author`, `Asset`) comes from the seeded `fake*` factories in `@joinery/content/testing`,
  overriding only the fields the test asserts on. Any other incidental value (a bio, a heading, a
  paragraph) comes from the same entry's seeded `faker`. The one exception is an app's `e2e/`:
  Playwright specs, the `server.ts` MSW preload, its `fakes.ts` data, `vendors.ts`, the shared
  steps in `forms.ts` and the copy lookup in `copy.ts` sit there, since they test the built app
  rather than a file.
- **Console output fails the spec.** The presets' setup file records every `console` call and throws
  after the test, so expected output is stubbed and asserted on:
  `vi.spyOn(console, "warn").mockImplementation(() => {})`. The guard restores every spy after each
  test. Playwright specs import `test` from `@joinery/configs/playwright/utils/test`, which fails on browser
  output. [`0032`](../../../docs/decisions/0032-console-output-policy.md) has the policy.

## Titles name the failure, not the function

A title says what would be true if the code were wrong. No "should", no restating the method name:

```ts
it("keys by vendor, project and locale so tenants never share a payload", () => {
it("hands the transport to the provider, so it can never be built unable to fetch", async () => {
it("rejects an unregistered vendor name instead of returning a broken provider", async () => {
```

A comment above a `describe` or a tricky `it` explains why the test exists — the same rule the root
[`CLAUDE.md`](../../../CLAUDE.md) applies to code comments. `it.each` covers validation matrices;
[`TolgeeProvider.spec.ts`](../../../packages/i18n/src/core/adapters/providers/TolgeeProvider.spec.ts)
is the example.

## What a spec asserts

| Assert | Not | Why |
| --- | --- | --- |
| Copy computed from data — a status mapped to its label, a count worded | Static copy — a heading, an intro, a button's wording | A reworded heading is not a regression. In an app with i18n the spec merges placeholder messages and asserts on those, so copy can't reach it at all |
| The outcome: the request sent, the file written, the state left behind | Which call came when (`toHaveBeenNthCalledWith`) | A reorder that changes nothing must not fail. Lint bans it |
| What renders: text, `aria-*`, a prop handed to a child | `wrapper.vm`; a class where an `aria-*` attribute or the text carries the same state | The instance changes without behaviour changing, and lint bans it. A class is fine when it is the only trace of the state |
| The values that matter | A snapshot | It passes whatever it was first given and fails on every unrelated change. Lint bans it |
| The real implementation, or a working fake | A copy of production logic written into the spec | A copy drifts from the original and keeps passing; the copied `assertForm` in four route specs had |

**Fakes before mocks.** A fake that behaves — a store that keeps what it was given, an endpoint that
answers — lets a spec assert state. [`operations.spec.ts`](../../../apps/wp-editor/server/services/operations.spec.ts)
runs the real store in a `mkdtemp` folder against a stateful fake WordPress, with no mocks at all.
A call assertion is fine when the call is the outcome — the mail sent, the branch created — and
never as a stand-in for the state it causes. Mocking a one-line adapter and asserting the argv it
was handed tests the mock; [the scripts `CLAUDE.md`](../../../infrastructure/scripts/CLAUDE.md) bans it.

**Type every fixture.** A fixture for a view model or an artifact is built by the real mapper
(`toArticleSummary(fakeEntry())`, `assembleWorkflows(…)`) or written with `satisfies` its type, so a
schema change fails the spec at typecheck instead of passing on a stale shape.

## The boundary recipes

A mock sits at the edge of what the code owns, never inside it.

| Subject | The boundary | Example |
| --- | --- | --- |
| A Nuxt module | `vi.mock("@nuxt/kit")` | [`module.spec.ts`](../../../packages/content/src/nuxt/module.spec.ts) |
| A cached server route in a package | `nitropack/runtime` + `ofetch` | [`translations.get.spec.ts`](../../../packages/i18n/src/nuxt/runtime/server/translations.get.spec.ts) |
| A route, middleware or plugin in an app's `server/` | `stubNitro()` from `@joinery/configs/vitest/utils/nitro`, before the dynamic `import()` | [`contact.post.spec.ts`](../../../apps/huella-legal/layers/contact/server/api/contact.post.spec.ts) |
| A page or composable reading the app's own API | `serveEndpoint` from `@joinery/configs/vitest/utils/nuxt` answers the route until the test ends; the real `useFetch` runs | [`WorkflowHomePanel.spec.ts`](../../../apps/developer-portal/layers/workflows/app/components/WorkflowHomePanel.spec.ts) |
| A developer-portal page reading a snapshot artifact | `mockNuxtImport("<name>Artifact")` over a `vi.hoisted` state, reset in a `beforeEach` | [`coverage.spec.ts`](../../../apps/developer-portal/layers/health/app/pages/coverage.spec.ts) |
| A composable reading a third-party API | `serveEndpoint` on the absolute URL | [`useIssues.spec.ts`](../../../apps/developer-portal/layers/github/app/composables/useIssues.spec.ts) |
| Nuxt Content | `mockNuxtImport("queryCollection")` returning an in-memory collection | [`changelog.spec.ts`](../../../apps/developer-portal/layers/projects/app/pages/changelog.spec.ts) |
| A provider | nothing — inject a fake `HttpClient` through the port | [`TolgeeProvider.spec.ts`](../../../packages/i18n/src/core/adapters/providers/TolgeeProvider.spec.ts) |
| A filesystem | a real `mkdtemp` folder | [`operations.spec.ts`](../../../apps/wp-editor/server/services/operations.spec.ts) |
| A vendor, from an app's e2e | nothing — preload MSW with the package's `testing` handlers | [`server.ts`](../../../apps/huella-legal/e2e/server.ts) |

Nitro auto-imports `defineEventHandler`, `useRuntimeConfig`, `getRequestHeaders` and the rest at
build time, so a server file imports none of them and they do not exist under vitest. `stubNitro`
stubs `defineEventHandler` and h3's own `createError`; anything else the file reads is a
`vi.stubGlobal` beside it. Another layer's server util (`assertForm`) is stubbed with the real
export, imported by relative path — `#layers/…` resolves for types only in the node project.

A provider never needs `vi.mock`. The `HttpClient` port exists so the transport can be passed in;
reaching for a module mock there means the injection was skipped.

## Mounting

- **Mount real components.** Nuxt UI renders in happy-dom; a hand-written stub of `UCard` or
  `UButton` re-implements it and hides what the real one does — the developer-portal stubs hid a
  `<button>` the specs then clicked by mistake. Stub only a child that has its own spec, and give
  the stub a `const` so `findComponent(Stub)` finds it; a child that only hands its slot props on
  is `slotStub({ … })`, as `FormChallenge` is in every form spec.
- **One mount per test.** Two mounts of a page in one test share its `useFetch` key while the first
  is alive, so the second sees the first's data. Between tests Nuxt purges it on unmount, except
  for a read with its own `getCachedData`, such as huella-legal's `useCachedFetch`, whose spec
  calls `clearNuxtData()` in a `beforeEach`.
- **A composable runs in `withSetup(() => useX(), { route })`**, which mounts it, awaits what it
  returns and resolves to `{ value, wrapper }`, or rejects with what it threw. A `useAsyncData`
  state awaits to Nuxt's bare state, dropping what the composable added to it, so wrap it:
  `async () => { const issues = useIssues(); await issues; return { issues }; }`.
- **Overlays render in a portal.** `UModal`, `USlideover` and `UPopover` content is in
  `document.body`, not the wrapper. Open a popover through its model (`setValue(true, "open")`);
  opening on click is the library's job.
- **A page with a route-leave guard mounts through `<NuxtPage>`** at its `route`, since
  `onBeforeRouteLeave` only registers inside the router view. Assert where navigation lands with
  `vi.waitFor`, since the destination page loads lazily.
  [`settings.spec.ts`](../../../apps/developer-portal/layers/workflows/app/pages/workflows/%5Bid%5D/settings.spec.ts)
  is the example.

## E2E

| Need | Use |
| --- | --- |
| Name a control | `getByRole("button", { name: t("newsletterForm.submit") })`, with `t` from the app's `e2e/copy.ts` — it throws on a missing key, so the spec survives a reword but not a lost key |
| WCAG 2.1 AA | `expect(await axeViolations(page)).toEqual([])` from `@joinery/configs/playwright/utils/a11y` |
| No bare message keys | `rawKeysIn(text, MESSAGES)` from `@joinery/configs/playwright/utils/i18n`; huella-legal's `smoke.spec.ts` walks the main routes with it |

## The two specs that pin invariants rather than behaviour

Both are easy to break by accident and neither is optional:

- **`src/index.spec.ts`** asserts `Object.keys(api).sort()` against a literal list, so widening the
  public API is a decision rather than a side effect of adding a file. Add an export, add the line.
- **`core/ports/*Provider.spec.ts`** pins that `configProblems()` / `optionProblems()` runs from the
  base constructor, before a subclass's field initialisers. Both `*:new-vendor` skills lean on it.

## Verify

```sh
pnpm check                                 # affected lint, typecheck and test, failures inline
pnpm exec nx test @joinery/<name>         # the test target alone, full output
pnpm exec nx run-many -t test              # the whole workspace
```

To check a spec earns its place, break the line it guards — flip a comparison, drop a branch — and
watch it fail, then revert. A spec that stays green has pinned nothing.

Every project has a `test` target, and every `vitest.config.ts` is a short wrapper. The Nuxt apps
use `vitest.createNuxtConfig`, which adds a `nuxt` project through `@nuxt/test-utils`, so a spec
under their `app/` can `mount` a component and `mockNuxtImport` a composable.
