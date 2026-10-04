---
name: test
description: Runs tests and helps write test cases for react-basics-ui. Use when user asks to run tests, write tests, check if tests pass, or mentions testing. Triggers on "test", "run tests", "write tests", "vitest", "coverage".
---

# Test

Run the Vitest suite. Report output as-is.

## Commands

```bash
# Everything — both projects (348 files, ~7.2k tests)
npx vitest run

# Just the unit suite in jsdom — fast, no browser (284 files)
npx vitest run --project unit        # or: npm run test:unit

# Just the story play() functions in headless Chromium (64 files)
npx vitest run --project storybook   # or: npm run test:stories

# Single file
npx vitest run <path-to-test-file>

# By name
npx vitest run -t '<test name substring>'

# Single directory
npx vitest run src/components/forms/inputs/Button

# With coverage
npx vitest run --coverage
```

`npm test` starts **watch** mode; `npm run test:run` is the single-run alias. Always use single-run mode when reporting results — never leave watch mode running.

## Two projects

`vitest.config.ts` declares `test.projects` (Vitest 4 — `defineWorkspace` is gone):

| Project | Environment | Runs |
|---|---|---|
| `unit` | jsdom | `src/**/*.test.{ts,tsx}` — 284 files |
| `storybook` | headless Chromium via Playwright | every story's `play()`, discovered from the `stories` globs in `.storybook/main.ts` — 64 files |

The browser is not incidental to the `storybook` project. Play functions drive real pointer and keyboard input and assert on focus and visibility, which jsdom does not model faithfully. Don't "simplify" it to jsdom.

It needs a browser binary: `npx playwright install chromium` on a fresh clone. If the storybook project fails to launch, that is the first thing to check.

Environment (`unit`): jsdom, globals on, `src/test/setup.ts` (jest-dom matchers, `cleanup()` after each test, a `scrollIntoView` stub since jsdom implements no layout). The `storybook` project uses `.storybook/vitest.setup.ts`, which applies `preview.ts` so stories under test load `global.css`. The `@` alias maps to `src/` in both.

## Test file conventions

Tests are co-located with the component they cover. The name before `.test` signals what kind of test it is:

| Pattern | Count | Covers |
|---|---|---|
| `<Name>.test.tsx` | 167 | Core behaviour — rendering, props, interaction |
| `<Name>.boundary.test.tsx` | 60 | Edge cases — empty, null, extreme, conflicting props |
| `<Name>.styles.test.ts` | 43 | Asserts the class strings in `<Name>.styles.ts` |
| `<Name>.contract.test.ts` | 11 | Prop-to-class mapping is exhaustive and stable |
| `<Name>.mutation.test.tsx` | 9 | Targets specific mutants — assertions that a subtle logic change would break |
| `<Name>.integration.test.tsx` | 3 | Several components composed together |

When adding a test, match the existing flavour for that component rather than inventing a new suffix.

## Test naming convention

Test descriptions use the **"should"** convention — describe what the unit **should do**, not what it does. This is near-universal in the suite (~4.2k of them), so match it.

```typescript
// Good
it('should render children inside the portal container')
it('should return null when items array is empty')
it('should focus the next item on ArrowDown')

// Bad
it('renders children inside the portal container')
it('returns null when items array is empty')
```

## Shared test infrastructure

Before writing inline mocks, **check what already exists** — don't duplicate helpers.

| Location | What's there |
|---|---|
| `src/test/setup.ts` | Global setup — matchers, cleanup, jsdom stubs |
| `src/test/mocks` | Shared mock implementations (e.g. `PORTAL_MOCK`) |

`vi.mock()` calls must stay in each test file (Vitest hoists them), but the mock *implementation* should come from the shared helper:

```typescript
vi.mock('@/components/utility/Portal', async () => {
  const { PORTAL_MOCK } = await import('@/test/mocks');
  return PORTAL_MOCK;
});
```

Mocking `Portal` is common: it renders into `document.body` by default, which puts the subject outside the container returned by `render()`.

## Testing this library specifically

- **Assert behaviour and accessible output**, not implementation. Query with `getByRole`/`getByLabelText` over test IDs — for a component library, the accessible tree *is* the public contract.
- **Style tests assert class strings**, not computed styles. jsdom applies no stylesheet, so `toHaveStyle` only sees inline styles; a component's Tailwind classes must be asserted as strings.
- **Tokens do not resolve in jsdom.** `var(--semantic-*)` stays literal. Assert the variable reference, not a colour.
- **Watch for timing.** Some components move focus inside `requestAnimationFrame`. If focus assertions fail, that is usually why — prefer `await waitFor(...)` over adding sleeps.

## If there are failures

Show the full output. If the user asks, help diagnose or fix. When a failure looks environmental (jsdom version behaviour, rAF timing) rather than a real defect, say so explicitly and show the evidence — don't quietly rewrite the assertion to pass.

---

## Boundary with Other Skills

| Skill | Relationship |
|-------|-------------|
| `/test-driven-development` | This skill is a **utility** — runs tests, writes individual test cases on demand. `/test-driven-development` is a **workflow** — Red→Green→Refactor with user validation. |
| `/lint` | Type errors often surface first as confusing test failures. Run `/lint` before deep-diving one. |
| `/storybook` | Stories are the visual counterpart to these tests; interaction stories with `play()` cover flows that unit tests can't show. |
