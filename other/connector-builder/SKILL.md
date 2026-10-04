---
name: "connector-builder"
description: "Scaffold new spell step commands and connectors. Use when building new step commands for spells or extending the spell engine with new capabilities. Connectors are for new I/O transport types OR platforms requiring complex multi-step interaction (e.g., browser-based automation)."
---

# Connector Builder

Purpose: scaffold production-ready step commands (`StepCommand`) and, when truly needed, generalized I/O connectors (`SpellConnector`) with proper types, tests, and registration.

## Read First — Companion Files

| File | When to read |
|------|--------------|
| [templates/connector.md](templates/connector.md) | When generating a generalized connector — full source + test + registration scaffold |
| [templates/step-command.md](templates/step-command.md) | When generating a step command — full source + test + registration scaffold |
| [../spell-builder/architecture.md](../spell-builder/architecture.md) | **Always** — three-layer model and connector-vs-step decision tree |
| [../spell-builder/permissions.md](../spell-builder/permissions.md) | When defining capabilities — required disclosure format |
| [../spell-builder/preflight.md](../spell-builder/preflight.md) | When authoring preflight checks — copywriting rules for user-visible `reason` strings |

## Prerequisites

- MoFlo project with `cli/spells` package
- TypeScript 5+
- Vitest for testing

## What This Skill Does

1. Guides you through building a **step command** (spell step logic) or, rarely, a **generalized connector** (new I/O transport)
2. Generates type-safe TypeScript implementing the correct interface
3. Creates a test file with vitest mocks
4. Shows how to register the component and use it in spell YAML

---

## Quick Start

Ask the user:

> **What do you want to build?**
> 1. **Step command** — executes logic within a spell step (transform data, control flow, etc.)
> 2. **Generalized connector** — wraps a new I/O transport type (e.g., WebSocket, gRPC, MQTT)

**Important:** Simple service integrations (Slack webhook, S3 upload, Jira comment) should compose existing connectors (`http`, `github-cli`, `playwright`) in spell YAML — no dedicated connector needed. However, platforms requiring complex multi-step browser interaction (like Outlook.com web UI) DO warrant a dedicated connector. See [../spell-builder/architecture.md](../spell-builder/architecture.md) for the decision tree.

**Documentation requirement:** When creating any new step command or connector, you MUST also create a README.md following `.claude/guidance/moflo-guidance-rules.md`. Use existing READMEs in `.claude/skills/spell-builder/steps/` or `connectors/` as templates. Apply automatically — the user should never need to ask.

---

## Building a Generalized Connector (Rare — New I/O Transports Only)

**You almost certainly want a step command, not a connector.** The three built-in connectors (`http`, `github-cli`, `playwright`) cover web APIs, CLI tools, and browser automation. Only create a new connector for a fundamentally new I/O transport (WebSocket, gRPC, MQTT, etc.) that no existing connector supports.

### Step 1: Gather Requirements

| Field | Required | Example |
|-------|----------|---------|
| **Name** | Yes | `websocket`, `grpc`, `mqtt` |
| **Description** | Yes | `WebSocket bidirectional messaging` |
| **Version** | Yes (default `1.0.0`) | `1.0.0` |
| **Capabilities** | Yes — pick from `read`, `write`, `search`, `subscribe`, `authenticate` | `read`, `write` |
| **Actions** | Yes (at least 1) | `connect`, `send`, `receive`, `close` |

For each action, ask:
- Action name (kebab-case)
- Description
- Input parameters (name, type, required?)
- Output fields (name, type)

**Verify the connector is generalized:** the name should describe an I/O transport, not a service. `websocket` is correct; `slack` is not.

### Step 2: Disclose Permissions

Before generating any source, surface the connector's capability profile to the user. Capabilities like `shell`, `fs:write`, `credentials`, `agent`, `net`, and `browser` carry specific risk classifications and required warning text. **See [../spell-builder/permissions.md](../spell-builder/permissions.md)** for the levels (`readonly`/`standard`/`elevated`/`autonomous`), risk classes (`[SAFE]`/`[SENSITIVE]`/`[DESTRUCTIVE]`), and the warning text to display per capability.

### Step 3: Generate Connector Source + Test

Use the full scaffold in [templates/connector.md](templates/connector.md). It implements the `SpellConnector` interface with all required pieces:

- `name`, `description`, `version`, `capabilities`
- Lifecycle methods: `initialize` and `dispose`
- `execute(action, params)` dispatcher
- `listActions()` schema reporter
- Per-action validation function
- Vitest test file with mocks

The generated test file lives at `src/cli/__tests__/spells/<name>.test.ts`.

### Step 4: Register the Connector

Add to `src/cli/spells/connectors/index.ts` so the engine discovers it:

```typescript
import { <name>Connector } from './<name>.js';
export { <name>Connector };

export const builtinConnectors: SpellConnector[] = [
  httpConnector,
  githubCliConnector,
  playwrightConnector,
  <name>Connector,  // <-- add here
];
```

### Step 5: Example Spell YAML

```yaml
name: example-with-<name>
version: "1.0"
description: Example spell using the <name> connector

connectors:
  - <name>

steps:
  - name: do-something
    type: bash
    config:
      command: "echo 'preparing...'"

  - name: use-<name>
    type: <name>          # the step command registered in Step 4
    config:
      action: <action-1>
      # ...action params
```

**Do not reach a connector from an `agent` step.** That step type has never been executable. A connector is reached from its own step command (Step 4 above), from a composite step's `tool` action, or from a custom step command.

---

## Building a Step Command

### Step 1: Gather Requirements

| Field | Required | Example |
|-------|----------|---------|
| **Type** | Yes (kebab-case) | `transform`, `notify`, `validate-schema` |
| **Description** | Yes | `Transform data using jq-like expressions` |
| **Config fields** | Yes (at least 1) | `expression: string`, `input: object` |
| **Capabilities** | No | `fs:read`, `fs:write`, `net`, `shell`, `memory`, `credentials`, `browser`, `agent` |
| **Permission Level** | No | `readonly`, `standard`, `elevated`, `autonomous` — auto-derived from capabilities when omitted |
| **MoFlo level** | No (default `none`) | `none`, `memory`, `hooks`, `full`, `recursive` |
| **Prerequisites** | No | External CLI tools needed |

### Step 2: Disclose Permissions

After gathering capabilities, you MUST display the permission implications to the user — same rules as the connector path. **See [../spell-builder/permissions.md](../spell-builder/permissions.md)** for the format and per-capability warnings. Steps using destructive capabilities will require user acceptance before first run via the spell-wide dry-run report.

### Step 3: Generate Step Command Source + Test

Use the full scaffold in [templates/step-command.md](templates/step-command.md). It implements the `StepCommand<TConfig>` interface with all required pieces:

- `type`, `description`, `capabilities`, `defaultMofloLevel`
- `configSchema` (JSONSchema for runtime validation)
- `validate(config, context)` and `execute(config, context)` methods
- `describeOutputs()` for downstream variable references
- Optional `preflight` block — see [../spell-builder/preflight.md](../spell-builder/preflight.md) for `reason` copywriting rules
- Optional `rollback(config, context)` for failure cleanup
- Vitest test file with `mockContext`

For compile-time type safety on the config, prefer the `createStepCommand()` factory from `src/cli/spells/commands/create-step-command.ts`.

### Step 4: Register the Step Command

Add to `src/cli/spells/commands/index.ts`:

```typescript
import { <type>Command } from './<type>-command.js';
export { <type>Command };
export type { <Type>StepConfig } from './<type>-command.js';

export const builtinCommands: readonly StepCommand[] = [
  agentCommand,
  bashCommand,
  // ... existing commands
  <type>Command,  // <-- add here
];
```

### Step 5: Example Spell YAML

```yaml
name: example-with-<type>
version: "1.0"
description: Example spell using the <type> step

steps:
  - name: my-step
    type: <type>
    config:
      <field1>: "value"
      <field2>: "optional-value"
```

---

## Reference

### Type Definitions

- **Connector interface:** `src/cli/spells/types/spell-connector.types.ts` — `SpellConnector`, `ConnectorAction`, `ConnectorOutput`, `ConnectorCapability`
- **Step command interface:** `src/cli/spells/types/step-command.types.ts` — `StepCommand`, `StepConfig`, `StepOutput`, `CastingContext`, `JSONSchema`
- **Step factory:** `src/cli/spells/commands/create-step-command.ts` — `createStepCommand()`

### Existing Components

**Shipped connectors** (`src/cli/spells/connectors/`): `http` (http-tool.ts), `github-cli` (github-cli.ts), `playwright` (playwright.ts)

**Built-in step commands** (`src/cli/spells/commands/`): `agent` (agent-command.ts), `bash` (bash-command.ts), `condition` (condition-command.ts), `prompt` (prompt-command.ts), `memory` (memory-command.ts), `wait` (wait-command.ts), `loop` (loop-command.ts), `browser` (browser-command.ts), `github` (github-command.ts)

### Related Skills

- [/spell-builder](../spell-builder/) — composes connectors and steps into spell definitions; references this skill when a needed connector doesn't exist
