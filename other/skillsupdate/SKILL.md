---
name: skillsUpdate
description: >-
  Local-only maintenance of observable Store guidance across Svelte Readable,
  React ReadonlySignal, and Streaming/Kefir Observable families. Use for
  cross-family behavior, docs, install routing, or verification updates.
type: core
sources:
  - ../../skills/SKILL.md
  - ../../skills/svelte/SKILL.md
  - ../../skills/react/SKILL.md
  - ../../skills/streaming/SKILL.md
  - ../../docs/SELECTORS.md
  - ../../docs/INSTALLATION.md
  - ../../scripts/postinstall.mjs
  - ../../scripts/cli.mjs
  - ../../scripts/validate-release.mjs
triggers:
  - skillsUpdate
  - observable skill maintenance
  - selector output cache guidance
  - Svelte readable selector guidance
  - React ReadonlySignal selector guidance
  - Streaming Kefir Observable selector guidance
  - new observable family
---
# skillsUpdate — local observable skill maintenance

This is a repository-local maintenance skill. Keep it under `.agents/skillsUpdate/SKILL.md` only. Do not copy it into `skills/`, do not add `.agents/` to `package.json` `files`, and do not add `.agents/` or `skillsUpdate` to package `exports` or packaged skill install bundles.

Use this skill before changing observable Store guidance that affects direct selector outputs: Svelte `Readable`, React `ReadonlySignal`, or Streaming/Kefir `Observable`. The goal is to update every family consistently without mixing their runtime patterns.

## Observable family matrix

| Family | Root router | Selectors | Lifecycle / scheduling | Store / integration | Package install routing | Docs, tests, verification |
| --- | --- | --- | --- | --- | --- | --- |
| Svelte readable | skills/SKILL.md, skills/svelte/SKILL.md | skills/svelte/selectors/SKILL.md | skills/svelte/selector-lifecycle/SKILL.md, skills/svelte/selector-scheduling/SKILL.md | skills/svelte/store/SKILL.md, skills/svelte/component-integration/SKILL.md | scripts/postinstall.mjs svelte bundle and scripts/cli.mjs / docs/INSTALLATION.md install-skills:svelte help | docs/SELECTORS.md, docs/ARCHITECTURE.md, docs/TESTING.md, npm run validate:architecture, npm run validate:release when dependencies/build outputs are available |
| React ReadonlySignal | skills/SKILL.md, skills/react/SKILL.md | skills/react/selectors/SKILL.md, skills/react/signals/SKILL.md | skills/react/selector-lifecycle/SKILL.md, skills/react/selector-scheduling/SKILL.md | skills/react/store/SKILL.md, skills/react/component-integration/SKILL.md | scripts/postinstall.mjs react bundle and scripts/cli.mjs / docs/INSTALLATION.md install-skills:react help | docs/SELECTORS.md, docs/ARCHITECTURE.md, React ESLint guidance under eslint-plugins/react/, npm run validate:architecture, npm run validate:release when available |
| Streaming/Kefir Observable | skills/SKILL.md, skills/streaming/SKILL.md | skills/streaming/selectors/SKILL.md | skills/streaming/selector-lifecycle/SKILL.md; scheduling guidance lives in streaming selector/lifecycle docs and shared selector docs unless a streaming scheduling leaf is added | skills/streaming/store/SKILL.md; no component-integration leaf exists for this no-UI/default family | scripts/postinstall.mjs streaming bundle and scripts/cli.mjs / docs/INSTALLATION.md install-skills:streaming help | docs/SELECTORS.md, docs/ARCHITECTURE.md, docs/TESTING.md, Streaming/no-UI import guidance, npm run validate:architecture, npm run validate:release when available |

## Cross-family update rule

When one observable behavior changes, update the root router and every affected family leaf in the same review pass. Do not let one family describe behavior as unique when the implementation applies to all three families.

For selector-output caching, every observable family must say the direct output is reused for the same Store object, Store-created selector, and selector arguments while the cache entry is retained. Never-observed outputs are cached too; concurrent consumers share an output, removing only one retains it, and final-consumer cleanup evicts that output. A retained JavaScript reference does not prevent eviction. Whole-Store disposal evicts its entries; cache counts are not active-subscription counts.

- Svelte: direct calls return cached Store-bound readables, not context-helper reads; keep component-init placement policy, subscription ownership, and `.select()` / `.effect()` escape hatches. Fresh Svelte `init()` requires component initialization; it does not provide the context needed by `useRunSaga`. Teach explicit owner `init`/`onMount`/`runSaga` startup, not an invented provider.
- React: direct calls return cached `ReadonlySignal` values; direct signal consumption stays preferred, with `.useValue(...args)` only for necessary hook/plain-value fallbacks.
- Streaming: direct calls return cached Kefir Observables; `.withStore(streamStore)` accepts an initialized StreamingStore. The Store object is the source/cache key and supplies the internal Kefir state stream for computation; the raw observable is not the public binding argument. Distinct Store objects remain distinct cache sources even if they expose the same stream.

Keep scheduling qualifications consistent: initial snapshots are prompt when all
inputs are available; Store-state writes coalesce on the Store cadence, while
reactive-argument changes may emit immediately downstream. A cold Streaming
argument with no value delays initial output. No public fast-selector API exists;
one-shot `.select`/`.effect` and Redux selector-channel reads are distinct paths.

Also update any anti-pattern language so agents do not add manual memoization, debounce/throttle wrappers, extra cache maps, props drilling, signal proxies, or stream passing solely to avoid valid repeated selector calls.

## Consistency checklist for behavior changes

1. Read `skills/SKILL.md` first and verify routing does not imply the behavior is Svelte-only, React-only, or Streaming-only unless the code truly is family-specific.
2. For each affected family, update its root `SKILL.md` routing table and the exact selector/lifecycle/scheduling/store leaves from the matrix.
3. Update `docs/SELECTORS.md` when conceptual API behavior, lifecycle tables, proxy memoization, output caching, or anti-pattern guidance changes.
4. Update `docs/ARCHITECTURE.md`, `docs/TESTING.md`, or `docs/INSTALLATION.md` only when the behavior changes architecture policy, verification expectations, or install routing.
5. Check package install routing in `scripts/postinstall.mjs` and CLI/help text in `scripts/cli.mjs` when a skill directory, bundle, or install target changes.
6. Check ESLint/architecture guidance if the change affects selector call modes, direct selector preference, component lifecycle boundaries, import boundaries, or no-extra-selector-caching rules.
7. Run or document the smallest valid checks: path inspection, `npm run validate:architecture` for skills/docs that govern Redux/selector policy, and `npm run validate:release` when dependencies and build prerequisites are available.

## New observable family checklist

Use this checklist before adding a fourth observable-style Store output family.

1. Define the public package entrypoint, Store class, direct selector output type, state source identity, lifecycle model, and scheduling/caching behavior.
2. Add package exports and release-validation import/type checks for the new public entrypoint only if the runtime API is approved.
3. Add a new packaged family router under `skills/<family>/SKILL.md` plus leaves for selectors, lifecycle/scheduling, store/integration, migration/setup if needed, and family-specific pitfalls.
4. Update `skills/SKILL.md` routing decision order, route matrix, selector-output cache routing, and consumer install routing without weakening the exclusive-one-family-per-app rule.
5. Update `skills/setup/SKILL.md` and relevant `skills/core/**` references when setup, import boundaries, testing, selector channels, or verifier guidance must mention the new family.
6. Add a package install target and bundle in `scripts/postinstall.mjs`, CLI command/help in `scripts/cli.mjs`, and docs table entries in `docs/INSTALLATION.md`.
7. Update `docs/SELECTORS.md`, `docs/ARCHITECTURE.md`, README examples, and tests/verification docs for the new output type and call modes.
8. Add or update ESLint architecture guidance/rules if the family introduces component lifecycle, import boundary, direct selector preference, or no-extra-caching concerns.
9. Update `scripts/validate-release.mjs` so package contents, exports, imports, blocked paths, and type declarations match the new approved API.
10. Verify with static path review, focused tests for the new family, `npm run validate:architecture`, and `npm run validate:release` when prerequisites are available.

## Local packaging guardrail

This local skill is intentionally excluded from npm packaging. Current package validation allows `package.json`, repo metadata, configured runtime files, `dist/`, `docs/`, and packaged `skills/`; `.agents/` is not allowed. If `.agents/skillsUpdate/SKILL.md` appears in an npm pack dry run, treat it as a release-blocking packaging regression.