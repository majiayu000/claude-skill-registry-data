---
name: umbrella-webpack-audit-bundles
description: "Measure Webpack production bundle composition, entry dependencies and font/icon costs; propose evidence-backed optimizations without pruning application imports."
---

# Audit Webpack Bundles

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. This skill supports **Analyze** and read-only **Verify** only; there is no Apply mode. Do not mutate application/config/lock files or invoke a repair skill from an audit request. Execution-based verification requires isolated build outputs as described below.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

This is read-only for application sources. Builds/stats write artifacts, so use an isolated output/checkout instead of cleaning the active app. Use installed tools; installing an analyzer is a separate change.

1. Capture production stats, chunks/modules and manifest. Record versions/mode/command and raw versus gzip/Brotli sizes. Development output is not a production baseline. Validate exit status and JSON; logs mixed into stats are not valid JSON.
2. Trace actual page requests. Separate initial/async/independent entries, including PDF/embeds. Files emitted to disk do not all download: font preferences and unicode ranges affect requests.
3. Investigate duplicate dependencies, broad vendor chunks, full framework imports, repeated CSS and fonts/icons. Establish usage from sources and representative runtime paths before recommending removal. Account for dynamic Razor/JS classes and icon pseudo-elements.
4. Measure cold builds/warm rebuilds only with comparable documented cache conditions. Distinguish Sass/checking/bundling costs where possible; do not infer migration benefits from unrelated benchmarks.

## Output and verification

Report bytes by entry/category, largest contributors, actual requests and prioritized tradeoffs. Give evidence and a validation recipe per recommendation. Preserve accessibility fonts, licensed icons and rarely used routes. Confirm sources/locks remain unchanged. This audit proposes changes; it does not implement pruning.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
