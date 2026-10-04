---
name: integration-singleton-isolation
description: >-
  Use when an integration or unit test mutates module-level state that outlives it, such as `await
  import('@/…')` for a side effect, a `bind*` or `set` call on an `export default new …` singleton,
  or an assignment to `process.env`, and the file has an ordering dependency — adding a case breaks
  a previously green sibling, an assertion passes only in one run order, or a test comment claims a
  precedence that nothing in the file pins.
---

# Integration test isolation for module singletons

## Profile keys consumed

- `make.test_integration`
- `make.test_unit_client`
- `framework.di`
- `framework.state`
- `framework.i18n`
- `architecture.source_root`
- `architecture.path_aliases`

Run the affected suite through the target mapped by `make.test_integration` (or
`make.test_unit_client` for a unit file); skip with a recorded note when the key maps to `null`.

## Overview

A module-level singleton keeps its state for the whole test file. A test that binds a source,
imports a module with side effects, or sets partial state leaks that mutation into every later test
in the file, producing assertions that only pass in one execution order. Reset in `afterEach` and
keep one behaviour per `it`.

## When to use

- A test calls `await import('@/…')` for the side effect, or a `bind*` / `set` method on a
  singleton.
- Adding a test to a `describe` block breaks an unrelated, previously green test.
- An assertion passes only because a later mutation has not happened yet.
- A comment says "before X initializes" but nothing in the file pins that precedence.
- Not for: state already scoped per test by the runner (React Testing Library cleanup, a fresh
  store created inside the test by `framework.state`).

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — sixteen `export default new …` singletons under `architecture.source_root`,
  exercised from `tests/integration/**`; the locale-formatter core's `bindLanguageSource` is the
  canonical case.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — no `framework.di`
  singleton layer, but the GraphQL client is a module-level `export default client` that reads
  `i18n.language` at module evaluation; integration tests live in `tests/integration/{api,flows}`.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  `tests/integration/components` holds composition tests only, so module-level mutable state is
  rare; the reset rule still applies where it exists.

## Core pattern

Restore every process-level and singleton-level mutation after each test, and give each behaviour
its own case:

```ts
import i18n from '@/i18n';

describe('locale formatter service (integration)', () => {
  const ORIGINAL_ENV = { ...process.env };
  const ORIGINAL_LANGUAGE = i18n.language;
  const service = container.resolve<LocaleFormatter>(
    LOCALE_FORMATTER_TOKENS.LocaleFormatterService
  );

  afterEach(async () => {
    process.env = { ...ORIGINAL_ENV };
    localeFormatterCore.bindLanguageSource(null);
    await i18n.changeLanguage(ORIGINAL_LANGUAGE);
  });

  it('falls back to the environment main language while no source is bound', () => {
    delete process.env.REACT_APP_MAIN_LANGUAGE;
    expect(service.currency(1234.5)).toBe('1\u00A0234,50\u00A0₴');
  });

  it('prefers the bound language over the environment main language', async () => {
    await i18n.changeLanguage('en');
    localeFormatterCore.bindLanguageSource(i18n);
    process.env.REACT_APP_MAIN_LANGUAGE = 'uk';
    expect(service.currency(1234.5)).toBe('₴1,234.50');
  });
});
```

The second test mutates three things: it binds the source, changes the shared i18n language, and
sets the environment variable the fallback reads. One `afterEach` reverses all three — unbind,
restore `process.env`, put the language back — so the first test passes whatever the order. Leaving
the language changed would be the same leak in a slower form: every later test in the run would
format against `en`. The `@/…` specifier is whichever alias `architecture.path_aliases` maps to the
source root.

## Splitting and pinning

- **Split a merged test.** One `it` that asserts, mutates the singleton, then asserts again encodes
  its own ordering dependency. Two `it` blocks with a shared `afterEach` assert the same two
  behaviours and stay order-free.
- **Pin the precedence.** When the resolver is a fallback chain (`explicit ?? bound ?? env`), write
  one test that sets all three and asserts the winner. Reordering the chain then fails a test
  instead of silently changing behaviour.
- **Reset through the public API.** Use the method the singleton exposes
  (`bindLanguageSource(null)`, `set(initialState)`); do not reach into private fields, and do not
  clear the whole `framework.di` container — that invalidates spies captured at module load.

## Common mistakes

- Resetting in `beforeEach` only — the last test in the file still leaves state behind for the next
  file when the runner shares a module registry.
- Restoring `process.env` but not the singleton, the bound source, or a shared library's own state
  such as the active i18n language — reverse every mutation the test made, in one `afterEach`.
- Using `jest.resetModules()` as the reset — it gives later tests a _different_ singleton instance
  than the one the outer `describe` resolved.
- Ordering tests so the file passes, instead of removing the dependency.
