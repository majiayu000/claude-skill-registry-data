---
name: nextjs-turbopack
description: >
  Next.js 16+ with Turbopack — the default dev bundler, its filesystem cache, module-trace (NFT) failures, and when to fall back to webpack. Use when developing or debugging a Next.js 16+ app, diagnosing slow `next dev` startup or HMR, reading a `next build` route table, or resolving a Turbopack-specific build error such as "Encountered unexpected file in NFT list". Do NOT use for Next.js App Router semantics — RSC boundaries, `<Suspense>` under `cacheComponents`, data fetching (that is `interactive-web-development` and `devskyy-dashboard-patterns`) — and do NOT use for Vercel deploy mechanics.
origin: ECC
---

# Next.js and Turbopack

Next.js 16+ runs `next dev` on Turbopack by default: an incremental bundler written in Rust
with a filesystem cache, so restarts reuse prior work instead of rebuilding from zero.

This repo's dashboard is the concrete case: `frontend/` on **Next.js 16.2.9**, Turbopack,
`cacheComponents: true` (`frontend/next.config.ts:32`).

## When to use

Use when one of these is observably happening:

- `next dev` cold start or HMR is slow enough to interrupt work.
- A `next build` fails with a Turbopack-specific message — most often
  `Encountered unexpected file in NFT list`, or a module-resolution error webpack did not raise.
- You need to read the `next build` route table and know what `○`, `◐`, and `ƒ` mean before
  claiming a route is static.
- You are deciding whether to pass `--webpack` for a dev session.

**Do NOT use when:**

- The error is App Router semantics, not bundling: `Uncached data was accessed outside of
  <Suspense>`, a server/client boundary violation, a `'use client'` misplacement. Those are
  `interactive-web-development` (boundary patterns) and `devskyy-dashboard-patterns`
  (this project's rules). Turbopack is not the cause.
- The failure is at deploy time on Vercel, not at build time locally.
- The project is not Next.js 16+. Turbopack defaults and flags differ by major version — check
  the docs for that release rather than applying this skill.

## Inputs

| Required before starting | How to confirm | If absent |
|---|---|---|
| A Next.js 16+ project with deps installed | `node -p "require('next/package.json').version"` in the app dir | **STOP.** Never diagnose a bundler from `package.json`'s range (`^16`) — read the resolved version. Observed here: `16.2.9`. |
| `next.config.ts` / `.js` readable | `sed -n '1,40p' frontend/next.config.ts` | **STOP.** `turbopack.root`, `cacheComponents`, and experiments change what every symptom means. |
| A build log you produced this session | run the build yourself | **STOP.** Do not attribute behavior to Turbopack from a log someone else pasted or from config alone. Config is `[repo]`; bundler behavior needs `[repro]`. |
| For a "it got slower" claim: a baseline timing | previous run's `Compiled successfully in Xs` | **STOP** on the severity claim. Without a baseline you have an observation, not a regression. |

## Procedure

1. Resolve the real version: `cd frontend && node -p "require('next/package.json').version"`.
2. Read the config for `turbopack`, `cacheComponents`, and `experiments`.
3. Reproduce the symptom with a full build and keep the log:
   `npm run build > /tmp/build.log 2>&1; echo $?`.
4. Confirm which bundler ran — the banner line prints it explicitly. If it does not say
   `(Turbopack)`, everything downstream in this skill is about a different bundler.
5. Read the route table symbols before describing rendering behavior:
   `○` static prerender · `◐` Partial Prerender (static shell + server-streamed slice) ·
   `ƒ` dynamic, server-rendered per request.
6. For an NFT trace failure, follow the printed import trace to the module doing dynamic
   filesystem work and either scope the path (`path.join(process.cwd(), 'data', bar)`),
   restrict it to dev, or annotate `path.join(/*turbopackIgnore: true*/ …)`.
7. For a suspected cache problem, check `.next/cache` exists after a build, then re-run and
   compare compile times. Do not delete `.next` reflexively — that destroys the evidence and
   the cache in one move.
8. Only after 1–7 consider `--webpack` (or `--no-turbopack`, depending on release), and say in
   the report exactly which Turbopack behavior forced it.

## Verification

Two independent checks: one proves the build is green, one proves *which bundler* produced it.

1. Production build is green:

```bash
cd /Users/theceo/DevSkyy/frontend && npm run build > /tmp/next-build.log 2>&1; echo "exit=$?"
```

**PASS:** `exit=0` and the log contains `Compiled successfully`. Observed 2026-07-28 on this
tree: `exit=0`, `✓ Compiled successfully in 5.8s`, `Finished TypeScript in 6.6s`,
`✓ Generating static pages using 9 workers (77/77) in 763ms`. `[repro]`

2. Turbopack actually ran, and the cache exists — a green build under a silently different
   bundler proves nothing about Turbopack:

```bash
grep -m1 'Next.js' /tmp/next-build.log && ls -d /Users/theceo/DevSkyy/frontend/.next/cache
```

**PASS:** the banner reads `▲ Next.js <version> (Turbopack)` and `.next/cache` exists.
Observed: `▲ Next.js 16.2.9 (Turbopack)`, `- Cache Components enabled`, and
`frontend/.next/cache/` present. `[repro]`

3. Route-shape claims must come from the table, not from reading page source:

```bash
grep -cE '^\S*[[:space:]]*[├└]?[[:space:]]*◐' /tmp/next-build.log
```

**PASS:** the count matches the number of routes you claim are partially prerendered. Observed
on this tree: 3 routes marked `◐` (including `/collections/[slug]` and
`/admin/elite-studio/operations/[id]`) alongside 38 marked `○`. `[repro]`

**A gate that dies is not a gate that passed.** A build killed by a timeout leaves a truncated
log whose missing error lines look exactly like success — treat a non-terminating build as
UNKNOWN and re-run (bug-230). **Prove the check can fail:** check 1 is falsifiable by
construction — introduce a type error and `next build` goes red at the `Running TypeScript`
stage, since this project type-checks inside the build. **Attribute before blaming your change:**
extract the pristine tree with `git archive HEAD frontend | tar -x -C <scratch>`, symlink
`node_modules`, and build there. **Never `git stash`** — the stash stack is shared across
worktrees.

## Worked example

Diagnosing the real warning this repo's build emits, 2026-07-28:

```text
$ cd frontend && npm run build
▲ Next.js 16.2.9 (Turbopack)
- Cache Components enabled
- Experiments (use with caution):
  · serverActions
✓ Compiled successfully in 5.8s
…
Encountered unexpected file in NFT list
A file was traced that indicates that the whole project was traced unintentionally.
Import trace:
  App Route:
    ./frontend/next.config.ts
    ./frontend/lib/catalog.ts
    ./frontend/app/api/catalog/summary/route.ts
```

Read literally: `app/api/catalog/summary/route.ts` imports `lib/catalog.ts`, which performs
filesystem work dynamic enough that Turbopack's module tracer gave up and traced the whole
project. The consequence is a bloated serverless bundle for that route, not a broken page —
which is why the build still exits 0 and the warning is easy to ignore for months. The fix is
in `lib/catalog.ts`, not in the route and not in `next.config.ts`: statically scope the path
(`path.join(process.cwd(), 'data', …)`) or mark it `/*turbopackIgnore: true*/`. `[repro]`

Note what this example does **not** claim: it says nothing about production behavior on
Vercel. That would need its own probe. `[repro]` covers the local build only.

## How it works

- **Turbopack** — incremental bundler for `next dev` and, from Next.js 16, `next build` as
  shown by the banner above. Filesystem cache under `.next/cache`; restarts reuse prior work.
- **Default in dev** — from Next.js 16, `next dev` runs Turbopack unless disabled.
- **Webpack fallback** — only for a Turbopack bug or a webpack-only dev plugin. Disable with
  `--webpack` (or `--no-turbopack`, release-dependent — check the docs for your version).
- **Bundle Analyzer (16.1+)** — experimental; inspect output and find heavy dependencies.

```bash
next dev
next build
next start
```

## Failure modes

| Symptom | Root cause | Do this |
|---|---|---|
| `Encountered unexpected file in NFT list` | A traced module does dynamic `fs`/`path` work, so the tracer includes the whole project | Follow the printed import trace to the *leaf* module (here `frontend/lib/catalog.ts`); scope the path, dev-gate it, or add `/*turbopackIgnore: true*/` |
| "Turbopack is slow" reported after deleting `.next` | The FS cache was destroyed, so the run was a cold start by definition | Compare warm-to-warm. Never `rm -rf .next` as a first move |
| Claim that a route is static, contradicted in production | Read from page source instead of the build's route table | `○` vs `◐` vs `ƒ` come from the table only |
| Build green locally, `Uncached data was accessed outside of <Suspense>` elsewhere | `cacheComponents: true` — an App Router contract violation, not a bundler issue | Wrap the dynamic reader in `<Suspense>`; see `interactive-web-development`. Do not reach for `--webpack` |
| `--no-turbopack` not recognised | Flag name changed across 16.x | Check the docs for the resolved version; do not guess the flag |
| Bundler behavior asserted from `next.config.ts` alone | Config is `[repo]`, behavior is `[repro]` | Run the build and read its banner before asserting anything |
| `ERR_INVALID_THIS` during install/deploy | pnpm on Node 22+ | Use npm. Repo rule for every Vercel-deployed workspace |

## Best practices

- Stay on a recent 16.x for stable Turbopack and cache behavior.
- Keep dynamic filesystem access out of modules reachable from route files — it is the single
  biggest source of NFT trace blowups.
- Do not clear `.next` to "fix" a slow build; measure warm builds against each other.
- For production bundle size, use the version's official analyzer rather than eyeballing
  `.next` output.
