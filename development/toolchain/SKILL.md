---
name: toolchain
description: Dorkroom's lint/format/typecheck/dependency toolchain — oxlint, Biome, the side-by-side TypeScript 7 (compiler) / TypeScript 6 (API) split, and the two-tier dependency pinning policy. Use when changing lint or format config, upgrading TypeScript or build tooling, adding or pinning dependencies, or debugging why a lint rule is not running.
---

# Dorkroom toolchain

## Lint and format

- **Lint with `oxlint`, format with Biome.** Each package's `lint` runs `oxlint` (lint, config in
  `.oxlintrc.json`) then `biome check --linter-enabled=false .` (formatting + import sorting only —
  Biome is no longer the linter). `bun run format` writes Biome formatting.
- Several jsx-a11y rules are set to `warn` (consumer-labelled input primitives, intentional modal
  backdrops) rather than `error`; fix genuine findings and tighten to `error` over time.

## Type-aware lint

- Type-aware rules (`no-floating-promises`, `no-misused-promises`, etc.) run via `bun run lint:types`
  (`oxlint --type-aware`, powered by `oxlint-tsgolint`).
- **Not in the CI gate yet:** tsgolint can't parse a couple of the project tsconfigs (`tsconfig-error`)
  and it surfaces ~200 findings to triage. Run it locally to catch real async bugs; wire it into the
  gate once those are resolved.

## Typecheck and build

**Two TypeScripts are installed on purpose. 7 compiles; 6 provides the API. Do not collapse them.**

- Typecheck/build run on **stable TypeScript 7**, installed as `typescript-7` (an npm alias for
  `typescript@^7.0.2` — the Go compiler). Every package's `build`/`typecheck` script invokes it by
  explicit path: `node ../../node_modules/typescript-7/bin/tsc`.
- **`typescript` is deliberately held on 6.x — it is the compiler _API_, not the compiler.**
  TypeScript 7.0 ships no programmatic API (it returns in 7.1), and `@vercel/node` does
  `require.resolve('typescript')` against the project to compile `api/**/*.ts` at deploy time, so a
  7.x `typescript` silently breaks the serverless build (`ts.sys`/`ts.readConfigFile` are
  `undefined`). Vite, Vitest, and the editor language service resolve the same package. This is the
  side-by-side layout from
  [Announcing TypeScript 7.0](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/#running-side-by-side-with-typescript-6.0).
  `renovate.json` disables `typescript` majors so the 6→7 bump stops being re-proposed;
  lift the hold and collapse the two packages once 7.1 restores the API (Microsoft's stated window
  is 3–4 months from the 7.0 RC, so roughly Q4 2026).
- **Renovate owns every dependency in this repo** (`renovate.json`). It replaced Dependabot, whose
  bun-ecosystem support had three disqualifying failure modes: it silently skips aliased packages
  ([dependabot-core#15847](https://github.com/dependabot/dependabot-core/issues/15847) — how the
  `typescript-7` pin sat on the moving `rc` dist-tag from #133 until caught manually), it unifies a
  version across every workspace manifest (how PR #187 rewrote apps/mobile's tailwindcss from v3 to
  v4 while calling itself a patch bump), and it bumps react-dom without react (issue #208 — always
  fails CI). Things about the config that are load-bearing:
  - The typescript-7 rule matches on **`matchDepNames: ["typescript-7"]`, not `matchPackageNames`.**
    The alias resolves to `packageName: "typescript"`, so a `matchPackageNames` rule would also
    match the 6.x compiler-API pin and propose exactly the 6→7 bump that breaks the Vercel build.
  - Global **`rangeStrategy: "bump"`**: under the default `replace` strategy an in-range release
    like typescript 7.1.0 would satisfy `^7.0.2` and produce **no PR** — and 7.1 is precisely the
    release we are waiting for. `bump` moves the floor, so releases arrive as visible PRs.
  - Global `minimumReleaseAge: "7 days"` mirrors the `bunfig.toml` soak gate, so Renovate never
    proposes a version `bun install` would refuse.
  - react/react-dom (+ their @types) are grouped into one PR (`groupName: "react"`) — they must be
    the exact same version or react-dom refuses to boot.
  - Expo SDK-managed native modules are disabled entirely: `expo install --fix` owns those
    versions, and nothing in CI builds the native app to catch a bad bump.
  - GitHub's "automated security fixes" (Dependabot security PRs) are disabled at the repo level;
    Renovate's `vulnerabilityAlerts`/`osvVulnerabilityAlerts` cover security updates instead.
  - Renovate requires the GitHub App to be installed on the repo; the config file alone does
    nothing. If updates ever go quiet for a long stretch, check that first.
- **Don't reach for the `@typescript/typescript6` compat wrapper** that the announcement recommends
  (`typescript@npm:@typescript/typescript6`). Under bun 1.3.11 it self-destructs: the wrapper's
  `@typescript/old` → `npm:typescript@^6` dependency dedupes against the `typescript` alias key and
  resolves to the wrapper itself, so `require('typescript')` returns an empty module. Plain
  `typescript@^6.0.3` gives the same API plus the lib files and `tsserver` the wrapper only proxies.
- **`bunx tsc` is TypeScript 6.** Both packages ship a `tsc` bin and bun links `typescript`'s. Use
  the explicit `node node_modules/typescript-7/bin/tsc` path (as the package scripts do) whenever
  you mean the 7.x compiler.

## Dependency pinning

Pinning is **two-tier**:

- Toolchain that shapes the production bundle (vite, vitest, tailwindcss, jsdom, etc.) is pinned exact.
- Everything else uses `^` ranges.
- Babel (`@babel/*`) stays on ranges — Vite 8/Oxc does the actual transforms, so Babel is dev-only
  tooling here.
- The `bunfig.toml` `minimumReleaseAge` gate (7 days) backstops the ranges. To install something
  published in the last week (e.g. an urgent CVE patch), run `bun install --minimum-release-age 0`.
- **The gate currently has no exemptions, and it is worth keeping it that way.**
  `minimumReleaseAgeExcludes` existed only while `typescript-7` tracked the moving `rc` dist-tag,
  which could resolve to a same-day pre-release; it was dropped once that pin went stable. Adding a
  package back to that list punches a permanent hole in the supply-chain soak gate — prefer the
  one-off `--minimum-release-age 0` flag.
