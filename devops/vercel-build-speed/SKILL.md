---
name: vercel-build-speed
description: Cut Vercel build times for Next.js App Router projects — measure per-phase from the build log, then attack page count, duplicated type checks, and dead Turbopack-era config. Use when deploys have crept past a few minutes, or before optimizing anything on a guess.
user-invocable: true
argument-hint: "[project path or Vercel deployment URL]"
metadata:
  version: "1.0.1"
---

# Vercel Build Speed (Next.js App Router)

Derived from taking a real production Next.js 16 / Turbopack app from **7m21s to
3m46s**, measured per-phase on Vercel at every step. The single most useful
lesson was epistemic: **the obvious lever was the wrong one.** Removing ~560MB
of assets bought about 5 seconds. Cutting prerendered page count bought ~50.

## Calibration — this is one case study, not a benchmark

Every number here comes from **one app, one Vercel plan, one 4-core / 8GB build
machine**, in mid-2026 on Next 16.2. The app was a localized content site:
four locales, ~2500 prerendered pages, a large `public/`, a 1.5GB git history.
Weight the findings accordingly:

**Likely to generalize** — the method (read the phase table, change one class of
thing per deploy, re-attribute after each), the `vercel.json` failure mode, the
Turbopack dead-config audit, and the *shape* of the ranking: compute and page
count beat bytes.

**Re-measure for your project** — every specific duration, and especially the
three "myths". "Clone time is not proportional to tree size" and "Deploying
outputs has a fixed floor" each rest on **two observations on one project**.
They may be artifacts of this repo's history size or this plan's build
infrastructure. If your `public/` dominates a small output, or your history is
shallow, you may see the opposite. Do not skip a change because this document
says the lever is weak — measure it.

**Has a shelf life** — Turbopack and the Next config surface move fast. The
`experimental.bundleAnalyzer` note in particular is a snapshot of 16.2 behavior
and will likely stop being true. Verify config keys against your own build
output, never against this file.

## Rule 0: Measure the phases before changing anything

Every Vercel build log is already an itemised profile. Pull it and build the
table before forming any theory.

```
Cloning completed: 21.6s
✓ Compiled successfully in 31.8s
  Finished TypeScript in 29.3s
✓ Generating static pages (2549/2549) in 84s
Build Completed in /vercel/output [4m]
Deploying outputs...          ← next timestamp minus this one
Created build cache: 20s
```

Via MCP: `get_deployment_build_logs` with `direction: "head"` then `"tail"`, and
`since` to window the middle. Total = first timestamp to last.

**Never extrapolate a rate from one measurement.** In the source engagement I
derived "0.42s per MB of `public/`" from a single 158s→61s drop and used it to
justify three follow-on projects. The drop was real; the attribution was wrong —
that same commit also cut static pages 2549→875, which did nearly all the work.
Two later predictions built on that rate delivered ~0 and ~5s.

Change one class of thing per deploy, and re-read the phase table.

## Levers, ranked by measured impact

| Lever | Measured | Risk |
|---|---:|---|
| Reduce prerendered page count | ~50s | SEO trade — decide deliberately |
| `typescript.ignoreBuildErrors` (when CI type-checks) | ~32s | ships before parallel CI reports |
| `experimental.cpus` 1 → 2 | ~8s | may OOM; test on a preview |
| Remove per-page `console.log` | ~5s + readable logs | none |
| Commit deterministic prebuild output | ~4s | none |
| `HUSKY=0` in `vercel.json` build env | ~1s | none |
| **Removing asset bytes** | **~5s for 560MB** | none, but near-worthless for build time |

### Page count is usually the biggest lever

`generateStaticParams` multiplies fast. A localized route is
`locales × items × sub-items`:

```
hexagram/[n]/line/[position]  → 4 × 64 × 6 = 1536 pages
```

Prerender the primary locale and let the rest fall through to ISR. Both stay
indexable; only the first crawler hit per URL is slower.

```ts
export const revalidate = 604800;

// Prerender English only. zh / th render on first request and cache via
// `revalidate` above. Do NOT set dynamicParams = false.
export async function generateStaticParams() {
  return Array.from({ length: 64 }, (_, i) =>
    Array.from({ length: 6 }, (_, p) => ({
      locale: "en", number: String(i + 1), position: String(p + 1),
    }))).flat();
}
```

Verify every non-prerendered locale still returns 200 **and** real localized
content — a 200 can hide an English fallback. Compare CJK character counts, not
status codes.

### Duplicated type checking

`next build` type-checks even when CI and a pre-push hook already do. Check
`.github/workflows/*` first; if `tsc --noEmit` runs there, the build-path copy is
the largest cuttable item once assets turn out not to matter.

```js
typescript: { ignoreBuildErrors: true },
```

The trade is real and worth writing into the config as a comment: CI runs *in
parallel* with the Vercel build, so a type error can ship before CI flags it. A
pre-push hook covers ordinary pushes; the exposure is `--no-verify`, web edits,
and agent pushes. Gating properly means serializing CI before the build, which
*increases* time-to-production — often not worth it.

### Per-page `console.log` is a real cost

A `console.log` in a layout, context provider, or data loader fires once per
prerendered page. At 2500 pages that is thousands of lines streamed to log
ingest, and it makes the build log useless for diagnosing anything else. Hunt
them in render paths and module scope, not just obvious debug code.

### Deterministic prebuild work belongs in git

If `prebuild` regenerates identical output every deploy (image derivatives,
manifests), commit the output and run the generator on demand instead. This also
breaks the "sources must be on disk at build time" coupling that keeps large
inputs in the repo.

## Myths — things that look like levers and are not

**Clone time is not proportional to tree size.** 596MB → 194MB moved it 21.6s →
21.8s. Vercel appears to reuse a warm repo (fetch + checkout), so the tip size
barely matters.

**"Deploying outputs" has a fixed floor.** It stayed at ~61s while `public/`
went 222MB → 61MB. It is dominated by function bundles and orchestration, not
static bytes.

**Therefore: moving assets to a CDN is not a build-time optimization.** Do it
for edge delivery and repo hygiene — both good reasons — but do not promise
build seconds for it.

**Compile time may be hardware-bound.** Compare a *cold* local build against
Vercel:

```bash
rm -rf .next && npm run build   # compare "Compiled successfully in Xs"
```

A 4x gap (8.7s local arm64 vs 34.5s on a 4-core Vercel machine) means the module
graph is fine and the machine is the constraint. The lever is a larger build
machine, not refactoring. Turbopack's filesystem caching currently covers dev
only, so Vercel builds compile cold by design.

## Turbopack-era dead config

Next 16 defaults to Turbopack, which **silently ignores** things webpack honored.
Audit for:

- **A `webpack()` function in `next.config.js`** — ignored entirely. Often it
  also shims packages that were removed years ago. Verify with
  `ls node_modules/<pkg>` before deleting, then delete it.
- **`@next/bundle-analyzer`** — a webpack plugin, so `ANALYZE=true next build`
  has been a no-op since the Turbopack switch. It looks like working tooling.
- **Unrecognized config keys** — Next warns but keeps building:
  ```
  ⚠ Unrecognized key(s) in object: 'optimizeFonts'
  ```
  Grep your build logs for `Invalid next.config.js options detected`. Do not add
  new ones: `experimental.bundleAnalyzer` is documented for 16.1+ but is
  **rejected on 16.2** — verify any config key against your exact version by
  reading the build output, not the docs.

Re-test webpack-era workarounds. `experimental.cpus: 1` is a common one, added to
stop webpack OOMing; under Turbopack with a smaller page count it may lift
cleanly. Check whether an ADR or comment explains it, then test on a preview and
update that record if the constraint is gone.

## `vercel.json` traps

**It has no comments, and an invalid key kills deployments silently.** Adding a
`"//"` pseudo-comment inside `build.env` made the file fail schema validation.
Vercel then created **no deployment at all** for three consecutive pushes — no
error, no failed build, nothing in the dashboard. Pushes succeeded, CI passed,
and the only symptom was a deploy that never appeared.

```jsonc
// WRONG — "//" is not a valid env var name; kills all deploys
"build": { "env": { "//": "why", "HUSKY": "0" } }

// RIGHT — rationale goes in the commit message
"build": { "env": { "HUSKY": "0" } }
```

**If pushes stop producing deployments, suspect `vercel.json` before suspecting
project settings.** Diagnosing this as "preview deployments are disabled" is
tempting and wrong. Confirm with `git log -S'<the key>' -- vercel.json` to check
whether the suspect change was already present in the commit you think proves
the setting is off.

## Verify like Vercel, not like localhost

Files you `git rm --cached` still sit on disk, so a local build finds them and
passes while Vercel fails. Before trusting a local verification, move them aside:

```bash
mkdir -p .local-artwork
mv public/<removed-dir> .local-artwork/
rm -rf .next && npm run build
```

Then check the rendered output, not just the exit code: image `src` values,
`og:image` URLs, retired paths returning 404.

Beware line-based greps on rendered HTML — a meta description containing a
newline spans lines and a `grep` will report it missing. Use a multiline-aware
parser before concluding something is broken.

## Tracing — local only

```bash
NEXT_TURBOPACK_TRACING=1 npm run build
npx next internal trace .next/trace-turbopack   # serves a viewer
```

**Never enable this on Vercel.** It produced a **499MB** `.next/trace-turbopack`,
which would land in the build output and inflate the phase you are trying to
shrink.

`.next/trace` (small, JSONL) is often enough — aggregate spans by duration.
Treat per-route spans like `check-page` as a parallelism signal rather than a
hotspot: their aggregate can exceed wall-clock many times over.

## Checklist

1. Pull the build log; build the phase table
2. Count prerendered pages; scope `generateStaticParams` to one locale where ISR suffices
3. Check whether CI already type-checks; if so, cut the build-path copy
4. Grep the build log for config warnings and dead `webpack()` config
5. Remove per-page `console.log`
6. Test `experimental.cpus` on a preview deployment
7. Re-measure per-phase — attribute to the phase that actually moved
8. Only then consider assets, and justify them on delivery, not build time
