---
name: configuration
description: Guide @vitest-agent/plugin configuration including thresholds, targets, output format, and plugin options. Use when setting up or modifying the plugin configuration.
disable-model-invocation: true
---

# Vitest Agent Plugin Configuration

## Plugin Options (vitest.config.ts)

The plugin is configured via `AgentPlugin` in your Vitest config:

```typescript
import { AgentPlugin } from "@vitest-agent/plugin";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [
    AgentPlugin({
      // Output format: "markdown" | "json" | "vitest-bypass" | "silent"
      format: "markdown",

      // Per-executor console matrix. The plugin auto-detects the
      // executor (human, agent, ci) and picks the matching slot.
      console: {
        human: "passthrough",   // Vitest's reporters render
        agent: "agent",         // markdown final-frame string
        ci: "passthrough",      // Vitest's reporters render
      },

      reporterOptions: {
        // Coverage thresholds (Vitest-native format)
        coverageThresholds: {
          lines: 80,
          branches: 80,
          functions: 80,
          statements: 80,
        },

        // Aspirational goals (informational, not enforced)
        coverageTargets: {
          lines: 95,
          branches: 90,
        },

        // Auto-ratchet baselines toward targets
        autoUpdate: true,

        // Max low-coverage files shown in console
        coverageConsoleLimit: 10,
      },
    }),
  ],
});
```

## Key Options

| Option | Default | Description |
| ------ | ------- | ----------- |
| `format` | `"markdown"` | Output format for console |
| `console` | `{}` | Per-executor matrix (`human`/`agent`/`ci`) controlling visible output |
| `onRunEvent` | none | Live event tap; gated to `console.human: "ink"` mode |
| `coverageThresholds` | `{}` | Enforced minimums (fail build) |
| `coverageTargets` | none | Aspirational goals (informational) |
| `autoUpdate` | `true` | Auto-ratchet baselines |

## Checking Current Configuration

Use the `configure` MCP tool to view current settings from the
database. Settings are captured on each test run.

## Common Configurations

### Strict CI mode

```typescript
AgentPlugin({
  format: "markdown",
  console: { agent: "agent" },
  reporterOptions: {
    coverageThresholds: { lines: 90, branches: 85 },
  },
})
```

### Development mode (quiet)

```typescript
AgentPlugin({
  format: "vitest-bypass",
  console: { human: "passthrough" },
})
```

### Live Ink animation for humans

```typescript
import { AgentPlugin } from "@vitest-agent/plugin";
import { createLiveInk, eventSourcedReporter } from "@vitest-agent/ui";

const live = createLiveInk();

AgentPlugin({
  console: { human: "ink", agent: "agent" },
  reporter: eventSourcedReporter,
  onRunEvent: live.event,   // fires only when human resolves to ink
})
```

## Inline projects (monorepo configs)

Under Vitest 5, an inline project object in `test.projects` inherits the
root config — including its `plugins` array — by default. `AgentPlugin`
therefore reaches an inline project automatically; set `extends: false`
on a project to opt it out, which also drops `AgentPlugin` from that
project since inheritance is how the plugin gets there.
