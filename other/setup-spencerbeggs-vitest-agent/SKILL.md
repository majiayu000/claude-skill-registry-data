---
name: setup
description: Set up @vitest-agent/plugin in the current project
disable-model-invocation: true
---

# Setup @vitest-agent/plugin

Wire `@vitest-agent/plugin` into this project's Vitest configuration and
emit the canonical 2.0 config. Work through the seven steps below in
order. The flow is deterministic — verify each prerequisite, then make a
small number of edits to one config file.

## 1. Verify Vitest 5.0 or newer

Read the project's `package.json` and any workspace-root `package.json`.
Find the installed `vitest` version. If `vitest` is missing, or the
version is below 5.0, stop and tell the user to install it first, e.g.
`pnpm add -D vitest@latest`. Do not continue until Vitest 5.0+ is
present — the plugin requires it.

## 2. Verify `@vitest-agent/plugin`

Look for `@vitest-agent/plugin` in `dependencies` or `devDependencies` of
the project `package.json`. If it is missing, install it as a dev
dependency with the project's package manager (npm / pnpm / yarn / bun —
detect from the lockfile or the `packageManager` field). The plugin's
MCP loader (`bin/start-mcp.sh`) requires the package to be present in
the user's `node_modules`.

## 3. Verify a coverage provider

Check for `@vitest/coverage-v8` or `@vitest/coverage-istanbul`. If
neither is installed, install `@vitest/coverage-v8` as a dev dependency
by default. The canonical config below sets `coverage.provider: "v8"`;
if the user already has the istanbul provider, keep their choice and
adjust the emitted `provider` value to match.

## 4. Detect the existing config shape

Look for `vitest.config.ts`, `vitest.config.js`, or `vitest.config.mjs`
at the project root. If the file exists in plain
`defineConfig({ ... })` form, convert it to the async-arrow pattern
shown in step 5 — this preserves type inference for
`AgentPlugin.discover()`. Convert silently and note the conversion in
the final summary; the file is git-tracked and reversible.

## 5. Emit (or rewrite) the canonical 2.0 config

Write the project's Vitest config to this canonical shape:

```ts
import { AgentPlugin } from "@vitest-agent/plugin";
import { defineConfig } from "vitest/config";

export default async () => {
  const { projects, tags } = await AgentPlugin.discover();
  return defineConfig({
    plugins: [
      AgentPlugin({
        coverageTargets: AgentPlugin.COVERAGE_LEVELS.standard.coverageTargets,
      }),
    ],
    test: {
      projects,
      tags,
      coverage: {
        enabled: true,
        provider: "v8",
        thresholds: AgentPlugin.COVERAGE_LEVELS.standard.thresholds,
      },
    },
  });
};
```

The 2.0 options surface has five fields — `console`, `coverageTargets`,
`transport`, `reporter`, and `onRunEvent` — and `coverageTargets` is the
only one this skill ever emits. Leave `console`, `reporter`, `onRunEvent`,
and `transport` at their defaults; the plugin wires its built-in default
reporter and the Ink mount internally. The `coverageTargets` value comes
from the `standard` preset so the user gets a sensible tier without
picking one; they edit the file to switch presets
(`none` / `basic` / `standard` / `strict` / `full`).

Coverage is split: the `coverage.thresholds` block lives on Vitest's
native `test.coverage` config, while `coverageTargets` lives on the
`AgentPlugin()` call. Both are sourced from the same preset so they stay
consistent.

## 6. Migrate pre-2.0 patterns when upgrading

If the existing `AgentPlugin({ ... })` call carries any pre-2.0 option,
strip it and surface the change in the final summary. The rewrite is
one-way; the source file is git-tracked, so write directly rather than
prompting for a diff preview. Removed options and their migration
targets:

- `reporter: eventSourcedReporter` (and the import) — removed. The
  plugin owns the default reporter; drop it.
- `onRunEvent: live.event` — removed for the same reason.
- `coverageThresholds` at the `AgentPlugin` level — moves to Vitest's
  native `test.coverage.thresholds`.
- `autoUpdate` — replaced by Vitest's native
  `test.coverage.thresholds.autoUpdate`, or the
  `AgentPlugin.COVERAGE_AUTOUPDATE` preset helpers.
- `consoleMode`, `consoleOutput`, `detail` — superseded by the single
  `console` field.
- `format`, `mcp`, `coverageConsoleLimit`, `omitPassingTests`,
  `githubActions`, `githubSummary`, `githubSummaryFile`, `projectFilter`,
  the nested `reporterOptions` wrapper, `cacheDir`, `logLevel`, and
  `logFile` — all removed in 2.0. Drop them; none has a replacement on
  the `AgentPlugin` options surface.

## 7. Confirm to the user

Print a short summary of what changed (config written or rewritten,
dependencies installed, pre-2.0 options stripped). Suggest running an
initial test to populate the database — `run_tests({})` via the MCP
server, or the project's test script. Point the user at `/vitest-agent:configure`
for the read-only view of the resolved settings.
