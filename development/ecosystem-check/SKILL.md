---
name: ecosystem-check
layer: method
description: Before building new infrastructure or a non-trivial capability, check whether the Nuxt ecosystem, UnJS, Vite, or other OSS already solves it — within our constraints (Nuxt, OSS, self-hostable, no mandatory SaaS). Use when weighing build-vs-adopt or starting new infra/tooling.
allowed-tools: Bash, Read, Grep, Glob, WebSearch, WebFetch
---

# Check the ecosystem before you build

Before writing new infrastructure or a non-trivial capability, **assume it may already be solved** and check — in order — before committing to a build.

> Real example (this repo): we nearly hand-rolled a "runtime ports" layer so crouton could run off Cloudflare. Turned out **db0 + NuxtHub multi-vendor already do it** — `NITRO_PRESET=node-server` emits libSQL + fs + fs-lite automatically. A feared 26-package core rewrite became a 2-line fix. Checking first saved it. (And we rejected **Turso Cloud** because it's SaaS — chose self-hosted libSQL to honour the OSS constraint.)

## Where to look (in order)
1. **Already installed** — check the dep tree *first*; it may already ship what you need. `node -e "require.resolve('<pkg>')"`, scan `package.json` / lockfile. (db0 was already there.)
2. **Nuxt ecosystem** — Nuxt modules, NuxtHub, Nuxt UI, VueUse. (CLAUDE.md already mandates VueUse / Nuxt UI first.)
3. **UnJS** — the layer under Nitro/Nuxt: `db0` (SQL), `unstorage` (KV/blob/cache), `nitro`, `ofetch`, `h3`, `consola`, `unctx`, `defu`… Most "platform" concerns live here and are usually already in the tree.
4. **Vite ecosystem** — Vite plugins for build/dev-time concerns.
5. **Wider OSS** — only then, a well-maintained OSS library.
6. **Build it ourselves** — last resort, when nothing fits or the fit is poor.

## Filter by our constraints (hard gates)
- **Nuxt-native / Nitro-compatible** — works with our stack and both runtime targets.
- **OSS & self-hostable** — prefer a library/repo over a service. **No mandatory SaaS** in the critical path (e.g. self-hosted libSQL/`sqld`, not Turso Cloud).
- **License** — permissive (MIT/Apache) preferred; check copyleft (AGPL) implications before adopting.
- **Maintained** — recent releases, real usage; not abandoned.
- **Config over code** — if an existing tool does the job by *configuration* (like db0 connectors selected by preset), that beats a custom abstraction.

## Verify, don't assume
- Ecosystem facts are **version-sensitive** — confirm the current state with `WebSearch` / `WebFetch` and the tool's own docs, **not memory**.
- **Prove it locally** before committing to the approach (we regenerated the NuxtHub config under the node preset to confirm it emits libSQL).

## Capture the decision
When the check changes the plan, record it on the relevant issue/doc: *what already solves it and why* — or *why nothing fit and we're building*. Keeps the build-vs-adopt reasoning visible for the next person.
