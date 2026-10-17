---
name: configure
description: View the resolved @vitest-agent/plugin configuration
disable-model-invocation: true
---

# Configure @vitest-agent/plugin

Display the project's resolved `@vitest-agent/plugin` configuration. This
command is read-only — it parses the Vitest config and renders what is
set; it never mutates the file. To change a setting, edit
`vitest.config.ts` directly.

## 1. Locate the Vitest config

Look for `vitest.config.ts`, `vitest.config.js`, or `vitest.config.mjs`
at the project root. If none exists, stop and point the user at
`/vitest-agent:setup`.

## 2. Parse the `AgentPlugin({ ... })` call

Read the `AgentPlugin()` call from the `plugins` array. Extract the five
options fields: `console`, `coverageTargets`, `transport`, `reporter`,
and `onRunEvent`. Any field not present in the call is at its default.

## 3. Parse `test.coverage`

Read Vitest's native `test.coverage` block. Extract `enabled`,
`provider`, `thresholds`, and `watermarks`.

## 4. Render the two tables

Render the five-field options table and the Vitest coverage block, for
example:

```text
## vitest-agent options (AgentPlugin({ ... }))

| Field           | Value                                                |
| --------------- | ---------------------------------------------------- |
| console         | { human: "ink", agent: "agent", ci: "agent" }        |
| coverageTargets | AgentPlugin.COVERAGE_LEVELS.standard.coverageTargets |
| transport       | { kind: "local" } (default)                          |
| reporter        | (default — plugin built-in)                          |
| onRunEvent      | (default — no tee)                                   |

## Vitest coverage (test.coverage)

| Field      | Value                                           |
| ---------- | ----------------------------------------------- |
| enabled    | true                                            |
| provider   | "v8"                                            |
| thresholds | AgentPlugin.COVERAGE_LEVELS.standard.thresholds |
| watermarks | (default)                                       |
```

For any field left at its default, render `(default)` with a short note
of the default value rather than leaving the cell blank.

## 5. Detect the coverage preset

When `coverageTargets` and `thresholds` match one of the named presets
(`AgentPlugin.COVERAGE_LEVELS.{none|basic|standard|strict|full}`),
render the preset name. When they do not match a preset, render
`"custom"` and a per-metric breakdown of the actual values.

## 6. Point at the manual edit path

End by telling the user which file and line to edit for the
`AgentPlugin` options and for the Vitest coverage block, and point them
at the `configuration` skill for the field reference. Do not modify the
config.
