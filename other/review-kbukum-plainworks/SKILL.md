---
name: review
description: >-
    Run plainworks' standing engineering-baseline review over a change set (a branch, commit range,
    or HEAD~1) or over a whole package/tree. Sequences nine focused passes — structure & placement,
    canonical reuse, principles, security & privacy, quality, tests/TDD, docs & supply chain,
    comments & TSDoc, and (for UI) accessibility/responsive/performance. Use before merging a change,
    when auditing a package, or before a release. Always run it in a fresh, clean-context reviewer
    with a high-capability model.
---

# Reviewing plainworks against its engineering baseline

plainworks is foundation infrastructure that downstream consumers build on: a defect in `std` or a core seam propagates to every package that implements it and every app that consumes the kit. The standard is correspondingly high — security, async/concurrency, and composition each get their own pass. This skill encodes plainworks' permanent review baseline as **nine focused passes** (the ninth runs only when the change touches interactive UI) plus two orchestrators.

The authoritative baseline lives in [`../../copilot-instructions.md`](../../copilot-instructions.md) and [`../../../docs/architecture.md`](../../../docs/architecture.md). A plan, spec, or issue may be passed in **as a scope checklist only** — it defines intended scope, never excuses a baseline violation. If the code diverges from the plan, report the divergence; the baseline wins.

## Run in a separate, clean-context agent — with a high-capability model

**Always dispatch a review to a fresh reviewer with no shared session context**, and use a high-capability model (GPT Sol, `gpt-6-sol`) — never inline in the session that wrote the code. A reviewer that "remembers" writing the change rationalizes it; an independent agent re-derives every judgment from the code and the principles. Hand it only the scope (diff or package/tree) and this skill. Then re-evaluate its findings before changing code.

## Scope: the blast radius, not just the diff

A change is a probe into its neighborhood, not an island. Review the changed lines **and** their blast radius — the rest of each touched file, the code the change calls and is called by, and closely-related files in the same package. Pre-existing defects, dead code, duplicated concerns, and design smells in that blast radius are **in scope** and reported like any other finding. Because plainworks is pre-stable with **no backward compatibility owed**, prefer a root-cause redesign over patching the symptom — decide Redesign / Align / Enhance / Drop, never "leave it patched." Don't expand into unrelated code silently; when a fix reaches past the touched files, say so and keep it coherent.

## Pick a driver

- **Change set** → [`references/review-changes.md`](references/review-changes.md). A diff (branch, commit range, or `HEAD~1`). Use after every change set, especially fast AI-assisted work.
- **Whole tree / package** → [`references/review-project.md`](references/review-project.md). A standing audit independent of any diff. Use periodically, before a release, or when onboarding.
- **Review → fix in one pass** → [`references/review-details.md`](references/review-details.md). Splits the review into parallel subagent passes by TypeScript concern, then plans and applies the fixes. Use when one driver should take a change from review through to merged fixes.

## The focused passes (run in order)

Stop and reject as soon as a change fails pass `00` or `01` — misplaced or duplicated code makes every later pass unreliable. Passes `00`–`07` run on every change; pass `08` runs **only when the change touches interactive UI** (a `"use client"`/`./client` module, a `.tsx` component, or its styles/tests) — skip it with an explicit note otherwise. Each file also carries a "Project mode" note for tree-wide sweeps and can be run standalone.

1. [`references/00-structure-placement.md`](references/00-structure-placement.md) — package placement (`packages`/`apps`/`internal`), acyclic layering + the layer map, barrel discipline, the server/client import boundary, generator-born packages.
2. [`references/01-canonical-reuse.md`](references/01-canonical-reuse.md) — did the code reimplement a concern `@plainworks/std` (or the platform) already owns? *(blocker class)*
3. [`references/02-principles.md`](references/02-principles.md) — typed/minimal APIs, errors & resilience, async/concurrency, composition, current idioms, AI features.
4. [`references/03-security-privacy.md`](references/03-security-privacy.md) — trust-boundary validation, header-only auth, PKCE/cookie MUSTs, server/client custody, crypto, data minimization.
5. [`references/04-quality.md`](references/04-quality.md) — root-cause over patches, dead code, ESM/exports discipline, maintainability, Biome gates.
6. [`references/05-tests-tdd.md`](references/05-tests-tdd.md) — TDD, determinism (fake timers, seeded RNG, no real net/FS), coverage thresholds, `@plainworks/testkit` reuse.
7. [`references/06-docs-supply-chain.md`](references/06-docs-supply-chain.md) — TSDoc, Conventional Commits, the single catalog, a Changeset present, SHA-pinned actions, `bun.lock` committed.
8. [`references/07-comments-tsdoc.md`](references/07-comments-tsdoc.md) — comments and TSDoc describe the code as it is, not plans/history/process.
9. [`references/08-ui-accessibility.md`](references/08-ui-accessibility.md) — *(UI changes only)* WCAG 2.2 AA (roles/keyboard/focus/contrast/target size + axe), mobile-first fluid layout & container queries, `prefers-reduced-motion`/`-color-scheme`, code-split/memo discipline, and the server/client separation of a component's logic from its `"use client"` leaf.

## Severity and finding format

```
severity (blocker / should-fix / nit) — file:line — what's wrong — which principle — suggested fix
```

- **blocker** — hard-principle violation (upward/sideways/cyclic import, concern reimplemented instead of reusing `std`, `any` in a public surface, thrown string / swallowed error on a runtime path, unbounded stream/buffer or missing cancellation, module-level singleton / import-time side effect / global registry, server-only auth pulled into a `"use client"` graph, token in a URL, trust boundary not validated, behavioral change with no test, an interactive control that is keyboard-inoperable or has no accessible name/role, a hand edit under `packages/elements/src/shadcn/` or `shadcn.lock.json` that the registry pipeline didn't produce, a vendored atom given a variant upstream doesn't ship, **compatibility scaffolding in alpha** — a shim, alias, deprecated re-export, compat flag, a parallel old-and-new model for one concern, new code shaped around a superseded path, or a superseded path left with no named deletion). Fix before merge.
- **should-fix** — real defect or debt that isn't a baseline violation (a hand-rolled fake that belongs in `testkit`, an over-long concern-mixed file, an inline version that should be `catalog:`, a missing Changeset, a new/changed component with no axe assertion, a fixed-pixel layout trap or missing reduced-motion path, an outdated pattern where a current idiom exists).
- **nit** — minor/style, take-it-or-leave-it.

## Validation is via bun run / turbo (see the `validate` skill)

**Scope every command to the changed package(s)** — the unscoped gates are for a project audit or CI sign-off:

```bash
bun run lint
bun run check-shape                           # when manifests, build descriptions, or generators changed
turbo run typecheck build test --filter=@plainworks/<name>
turbo run test --filter='...[origin/main]'   # affected set
bun run check-boundaries                      # placement/acyclicity (fast, source-level)
bun run check-versions                        # catalog single-source
bun run --filter @plainworks/elements registry:validate   # vendored atoms match shadcn.lock.json
```

Treat a green run as **necessary but not sufficient**: it does not catch unbounded streams/buffers, missing timeouts/cancellation, module-level singletons, import-time side effects, or a token leaking into a URL. Those are on the reviewer.
