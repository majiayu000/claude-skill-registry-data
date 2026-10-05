---
name: umbrella-gulp-configure-build-tasks
description: "Create or repair Gulp orchestration for Webpack and Sass, including cross-platform sequencing, completion, failure propagation and reliable watch/clean commands."
---

# Configure Gulp Build Tasks

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Map package scripts, Gulp tasks, editor bindings and CI. Use gulp.series for dependent work and gulp.parallel only for independent work. Replace shell ampersand chaining where ordering or success is shell-dependent; preserve caller aliases.
2. Return streams/promises or completion callbacks consistently. An async function returning a stream does not await stream completion: wrap completion in a promise or return a stream from a non-async task. Propagate failures across the complete copy/Sass/PostCSS pipeline.
3. Spawn the local Webpack CLI with process.execPath and an argument array, not shell-built text. Reject spawn errors, nonzero exits and signals. Stopping orchestration must close its watchers and long-lived child processes.
4. One-off/release Sass errors must fail the task. Log-and-continue belongs only in watcher cycles. Separate watch behaviour from minification settings.
5. Watch imported helpers as well as entries; recopy before compiling where copies remain. Handle add/change/rename/unlink, removing only proven generated counterparts. Exclude dependency/output roots and avoid output-triggered loops.
6. Start each watcher once. If watch includes watch-scoped, do not launch both via project-open bindings. Sequence cleanup before initial builds. Resolve/verify cleanup roots and never delete hand-authored isolated CSS through blanket globs.

## Verify

In isolated fixtures exercise first build, invalid Sass release failure, repair/rebuild, helper edits, entry addition/removal and process shutdown. Test Windows/POSIX where available; report untested platforms. One helper edit must update all affected outputs without restarting or duplicating watchers.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
