---
name: architectural-reconciliation
description: >-
  Use when merging a long-lived feature branch whose conflicts are architectural rather than textual
  — the branch built a route manifest while the base adopted a route registry, reads `process.env`
  directly while the base adopted a typed env layer, or news up a service while the base moved to a
  DI composition root. Applies when two competing patterns both compile and a reviewer has to decide
  which layer owns the concern.
---

# Architectural Reconciliation

## Profile keys consumed

- `make.lint_tsc`
- `make.lint`
- `make.lint_deps`
- `make.lint_metrics`
- `make.test_unit_client`
- `make.test_integration`
- `framework.di`

Every verification command goes through the profile's `make` target map. A `null` value for one of
these keys means the capability is absent in this repository: skip that check with a recorded note
rather than improvising a raw host command.

## Overview

When a branch predates a refactor on the base branch, the merge conflict is semantic: both patterns
compile, both pass their own tests, and a naive merge ships two answers to one question. Reconcile
by naming the canonical layer, porting the feature's intent into it, and deleting the orphan.

## When to use

- A merge shows conflicts that are competing patterns, not different line positions.
- The branch predates an architectural refactor on the base branch.
- Two files claim the same responsibility (a manifest and a registry, a config reader and a typed
  env accessor) and it is unclear which one the shell actually loads.
- A boundary gate (dependency-cruiser, a scoped `no-restricted-imports`) fires only after the merge.
- Not for: ordinary textual conflicts where both sides mean the same thing, and not for deciding
  which architecture _should_ win — the base branch already decided that.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the canonical layers to reconcile against are the route registry
  (`src/routes/registry.ts`, `src/routes/route-composer.tsx`, module-owned
  `features/<f>/routes/index.ts` contracts), the typed env layer (`src/config/env/raw-env.ts`,
  `env.ts`, `env-schema.ts`, `.env.example`, checked by the repository's env-example sync target),
  and the DI composition roots (`src/config/dependency-injection-config.ts` plus per-area `di.ts` /
  `tokens.ts`).
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the technique
  transfers, but there is no DI container (`framework.di` is absent) and `src/routes/` is empty; the
  canonical surfaces are `next.config.js`, the `pages/` tree and `src/config/env.ts`.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — the
  technique transfers; the canonical surfaces are the `src/index.ts` public barrel and the
  `api-extractor.json` API report, with no DI container or route registry.

## Procedure

1. **Name the canonical layer.** Read the base branch, not the branch under merge, and write down
   which layer owns the concern, what the authoritative contract is, and what file shape it demands.
   Routing, env access, DI wiring and state are the four that most often diverge; for state, check
   whether the base expects instance methods on a registered class rather than static or free ones.
2. **Audit the branch for competing patterns.** List every file that uses the superseded pattern,
   reaches for an internal API the base branch has since made private, or declares a type in a
   location the base branch moved. For each, record what it is trying to do and where the canonical
   layer already does it.
3. **Port the intent, delete the orphan.** Move the feature's behaviour into the canonical layer — a
   new route becomes an entry in the module's route contract, a new setting becomes a field on the
   raw-env snapshot plus the schema plus `.env.example`, a new collaborator becomes a token plus a
   registration. Then delete the branch's parallel implementation outright. Keeping both is the one
   outcome guaranteed to be wrong.
4. **Move the types with the code.** Type declarations belong in the canonical layer's own type
   location, not wherever the branch left them, or the boundary gates fire on the merged tree.
5. **Sync the documentation, after the port.** Update the repository's architecture guidance,
   `agents.md`, and the module `README.md` so they describe what the code now does, and state in the
   change description which pattern was superseded and why. Documentation updated before the port
   describes an intention, not a system.
6. **Verify end to end** — the type check mapped by `make.lint_tsc`, the lint aggregate mapped by
   `make.lint`, the boundary gate mapped by `make.lint_deps`, the unit and integration suites mapped
   by `make.test_unit_client` / `make.test_integration`, and the complexity metrics gate mapped by
   `make.lint_metrics`, since porting often moves several concerns into one file.

```bash # profile-example
# With a profile whose keys map to these targets, step 6 is:
make lint-tsc && make lint-deps && make lint-metrics
make test-unit-all && make test-integration
# and the SPA shape's env layer additionally has:
make check-env-sync
```

## Worked example

A branch declares its pages in a parallel manifest while the base branch has adopted module-owned
route contracts collected by a registry and assembled by a composer. The reconciliation keeps the
registry: the branch's real deliverables were a deferred route fallback and named chunks, so the
fallback moves into the single `Suspense` boundary in the root layout, the chunk names move onto the
contract loaders, the manifest file is deleted, and the golden tests that pinned the old shell are
rewritten against the contract. The same shape applies to a config reconciliation: settings the
branch read from the process environment become fields on the typed env layer, the accessor stays
free of the container so it can run before dependency injection is initialised, and the direct reads
disappear.

## Common mistakes

- Merging both patterns "for now" — pick the canonical one and port; two owners is a latent bug.
- Papering over the divergence with a suppression directive or a hand-edited conflict marker —
  neither removes the second implementation.
- Updating the architecture docs before porting the code — the docs then describe an intention.
- Copying the branch file into the new folder without adapting it — audit its dependencies and its
  container-freedom constraints first.
- Skipping the metrics and boundary gates after the port — a ported file often crosses a complexity
  or layering threshold that neither branch crossed alone.
