---
name: "spell-builder"
description: "Create, edit, and validate spell definitions (YAML/JSON) that compose connectors and step commands into end-to-end spells. Use when building new spell definitions, modifying existing ones, or exploring available spell components."
---

# Spell Builder

Purpose: produce production-ready spell definitions (YAML/JSON) that compose step commands and connectors into end-to-end automated spells, with proper data flow, validation, and engine integration.

## Read First — Companion Files

| File | When to read |
|------|--------------|
| [architecture.md](architecture.md) | **Always** — three-layer model (spell → step → connector); putting logic in the wrong layer is the most common mistake |
| [permissions.md](permissions.md) | When defining or editing any step — required disclosure & dry-run report format |
| [preflight.md](preflight.md) | When the step depends on runtime state (clean git tree, logged-in CLI, reachable host) |

## Prerequisites

- MoFlo project with `cli/spells` package
- Familiarity with YAML syntax

## Quick Start

Ask the user:

> **What would you like to do?**
> 1. **Create** a new spell definition from scratch
> 2. **Edit** an existing spell definition
> 3. **Discover** available step commands and connectors
> 4. **Validate** an existing spell file

Then follow the appropriate section below.

---

## Section 1: Create a New Spell

### Step 1: Gather Spell Metadata

| Field | Required | Example |
|-------|----------|---------|
| **Name** | Yes (kebab-case) | `deploy-staging`, `security-audit` |
| **Description** | Recommended | `Deploy to staging with smoke tests` |
| **Version** | Optional (default `1.0`) | `1.0` |
| **Abbreviation** | Optional | `ds` (short lookup key for `/flo -wf ds`) |
| **MoFlo Level** | Optional (default `none`) | `none`, `memory`, `hooks`, `full`, `recursive` |

### Step 2: Define Arguments (Optional)

If the spell needs runtime parameters, define each argument:

| Field | Required | Description |
|-------|----------|-------------|
| **Name** | Yes | Argument identifier (e.g., `target`, `severity`) |
| **Type** | Yes | `string`, `number`, `boolean`, or `string[]` |
| **Required** | Optional (default `false`) | Whether the argument must be provided |
| **Default** | Optional | Default value if not provided |
| **Enum** | Optional | Allowed values (e.g., `[low, medium, high]`) |
| **Description** | Optional | Help text |

Arguments are referenced via `{args.argumentName}`.

### Step 3: Define Steps

Walk the user through adding steps one at a time. For each step:

| Field | Required | Description |
|-------|----------|-------------|
| **ID** | Yes (unique) | Step identifier (kebab-case, e.g., `run-tests`) |
| **Type** | Yes | One of the available step command types (see Discovery section) |
| **Config** | Yes | Type-specific configuration (see per-step README) |
| **Output** | Optional | Variable name to store step output (for downstream steps) |
| **Continue on Error** | Optional | `true` to proceed even if this step fails |
| **MoFlo Level** | Optional | Override spell-level mofloLevel (can only narrow, not escalate) |
| **Permission Level** | Optional | `readonly`, `standard`, `elevated`, `autonomous` — auto-derived from capabilities when omitted |

**Data flow between steps:** Use `{stepId.outputKey}` syntax to reference output from a previous step. For example, if step `fetch-data` outputs a `url` field, a later step can use `{fetch-data.url}`.

**Special variable references:**
- `{args.name}` — references a spell argument
- `{credentials.NAME}` — references a credential (resolved at runtime)
- `{stepId.outputKey}` — references output from a previous step

#### REQUIRED: Permission disclosure on step creation

After defining each step, display its permission profile. **See [permissions.md](permissions.md) for the required format and per-capability warnings.** Apply automatically — users must understand what each step can do before it becomes part of a spell.

#### REQUIRED: Preflight checks with human-readable hints

When a step depends on runtime state the user controls (clean git tree, logged-in CLI, reachable host, etc.), declare a `preflight:` block so the spell fails fast with a helpful message before any side effects. Every preflight MUST include a `hint:` field — the user-visible message on failure. **See [preflight.md](preflight.md) for the full guide (severity levels, resolutions, hint copywriting rules).**

### Step 4: Generate the Spell YAML

Assemble the definition into:

```yaml
name: <spell-name>
abbreviation: <optional-abbreviation>
description: <optional-description>
version: "<version>"
mofloLevel: <optional-level>

arguments:
  <arg-name>:
    type: <string|number|boolean|string[]>
    required: <true|false>
    default: <optional-default>
    enum: [<optional-values>]
    description: <optional-help-text>

steps:
  - id: <unique-step-id>
    type: <step-command-type>
    config:
      <type-specific-config-fields>
    output: <optional-variable-name>
    continueOnError: <optional-true>
    mofloLevel: <optional-level>
```

### Step 5: Validate the Spell

Validate against the engine schema. The following rules must pass:

1. **`name`** is required and must be a non-empty string
2. **`steps`** is required and must be a non-empty array
3. Each step must have a unique **`id`** (no duplicates)
4. Each step must have a valid **`type`** matching a known step command
5. **Variable references** (`{stepId.outputKey}`) must not be forward references
6. **Argument references** (`{args.name}`) must match declared arguments
7. **`mofloLevel`** must be one of: `none`, `memory`, `hooks`, `full`, `recursive`
8. Step-level `mofloLevel` cannot exceed the spell-level `mofloLevel`
9. No **circular** condition jumps (condition steps referencing each other in a loop)
10. **Argument definitions** must have valid types, and defaults must match their declared type
11. **`permissionLevel`** (if declared) must be one of: `readonly`, `standard`, `elevated`, `autonomous`

If validation fails, show the specific errors and guide the user to fix them.

### Step 5b: REQUIRED — Permission Dry-Run Report

After schema validation passes, display the full spell-wide permission report and require user acceptance before the spell can be cast. **See [permissions.md](permissions.md) for the exact format.** On acceptance the permission hash is stored — subsequent runs do not re-prompt unless the spell's permissions change.

### Step 6: Write the File

Ask the user where to save:

- **Project spells:** `spells/<name>.yaml` (user-level, project-specific)
- **Claude spells:** `.claude/spells/<name>.yaml` (Claude Code integration)

Prefer the MCP tool when available:

```
mcp__moflo__spell_create — name, definition (YAML string), description
```

Or write the file directly to the chosen directory.

---

## Section 2: Edit an Existing Spell

### Step 1: Load the Spell

Ask for the spell file path, or use `mcp__moflo__spell_list` to browse available spells. Read the YAML/JSON file and parse the current definition.

### Step 2: Present Current Structure

Show a summary: name, description, version, abbreviation, arguments (if any), steps list with id/type/output variable/continueOnError.

### Step 3: Apply Changes

| Operation | Description |
|-----------|-------------|
| **Add step** | Insert a new step at a given position |
| **Remove step** | Delete a step by id (warn about broken references) |
| **Reorder steps** | Move a step to a new position (warn about broken forward refs) |
| **Update step config** | Modify a step's configuration fields |
| **Update step type** | Change a step's command type (reset config to match) |
| **Add/remove arguments** | Modify spell argument definitions |
| **Update metadata** | Change name, description, version, abbreviation, mofloLevel |

After each change, re-validate and show any errors introduced. **When adding or modifying a step, display its permission report (see [permissions.md](permissions.md)).** If the change introduces new destructive capabilities or raises the permission level, call this out explicitly.

### Step 4: Save

Write the updated YAML back to the original file (or a new path if requested).

---

## Section 3: Discover Available Spell Components

### Step Commands

Each step type has its own self-contained README under `.claude/skills/spell-builder/steps/`:

```
.claude/skills/spell-builder/steps/
  <step-name>/README.md    — config, outputs, usage examples, source path
```

To find available steps, `Glob` `.claude/skills/spell-builder/steps/*/README.md` and read each H1.

**Runtime source:** `src/cli/spells/commands/` — each step is a TypeScript file registered in `index.ts`.

**Adding a new step:** create `steps/<name>/README.md` (use existing READMEs as templates and follow `.claude/guidance/moflo-guidance-rules.md`); the step source goes in `src/cli/spells/commands/` and is registered in `index.ts`. No changes to this SKILL.md needed.

### Connectors

Each connector has its own self-contained README under `.claude/skills/spell-builder/connectors/`:

```
.claude/skills/spell-builder/connectors/
  <connector-name>/README.md    — actions, capabilities, usage, source path
```

To find available connectors, `Glob` `.claude/skills/spell-builder/connectors/*/README.md`.

**Runtime source:** `src/cli/spells/connectors/` — each connector is a TypeScript file registered in `index.ts`.

**Adding a new connector:** create `connectors/<name>/README.md`; the connector source goes in `src/cli/spells/connectors/` and is registered in `index.ts`. **When to create a new connector vs composing existing ones:** see [architecture.md](architecture.md).

---

## Section 4: Validate an Existing Spell

### Step 1: Load and Parse

Read the spell file (YAML or JSON). The parser auto-detects format.

### Step 2: Run Validation

Check against all engine validation rules from Section 1, Step 5.

### Step 3: Report Results

- **Valid:** confirm the spell passes all checks.
- **Invalid:** list each error with its path and message, then offer to fix.

---

## Reference

### Type Definitions

- **Spell definition:** `src/cli/spells/types/spell-definition.types.ts` — `SpellDefinition`, `StepDefinition`, `ArgumentDefinition`, `ArgumentType`
- **Step command interface:** `src/cli/spells/types/step-command.types.ts` — `StepCommand`, `StepConfig`, `StepOutput`, `CastingContext`, `MofloLevel`, `CapabilityType`
- **Connector interface:** `src/cli/spells/types/spell-connector.types.ts` — `SpellConnector`, `ConnectorAction`, `ConnectorOutput`, `ConnectorAccessor`

### Engine Components

- **Schema validator:** `src/cli/spells/schema/validator.ts` — `validateSpellDefinition()`
- **YAML/JSON parser:** `src/cli/spells/schema/parser.ts` — `parseSpell()`
- **Grimoire (registry):** `src/cli/spells/registry/spell-registry.ts` — `Grimoire`
- **Definition loader:** `src/cli/spells/loaders/definition-loader.ts` — two-tier loading (shipped + user)

### MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__moflo__spell_create` | Create a new spell definition |
| `mcp__moflo__spell_list` | List available spells |
| `mcp__moflo__spell_cast` | Cast (execute) a spell |
| `mcp__moflo__spell_status` | Check spell execution status |

### MoFlo Integration Levels

| Level | Access |
|-------|--------|
| `none` | No MoFlo integration (default) |
| `memory` | Read/write MoFlo memory |
| `hooks` | Memory + hook triggers |
| `full` | Hooks + swarm/agent spawning |
| `recursive` | Full + nested spell invocation |

### Variable Reference Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `{args.name}` | Spell argument | `{args.target}` |
| `{credentials.NAME}` | Runtime credential | `{credentials.GITHUB_TOKEN}` |
| `{stepId.key}` | Previous step output | `{fetch-data.url}` |

### Example: Complete Spell

```yaml
name: security-audit
abbreviation: sa
description: Run security checks on a target directory
version: "1.0"
mofloLevel: memory

arguments:
  target:
    type: string
    required: true
    description: Directory to audit
  severity:
    type: string
    default: medium
    enum: [low, medium, high, critical]
    description: Minimum severity to report

steps:
  - id: scan-deps
    type: bash
    preflight:
      - name: "npm available"
        command: "npm --version"
        hint: "npm isn't installed or isn't on your PATH. Install Node.js from https://nodejs.org and try again."
    config:
      command: "npm audit --json"
      cwd: "{args.target}"
    output: audit-result

  - id: analyze-findings
    type: bash
    config:
      command: |
        claude -p "Analyze these npm audit results and filter for severity >= {args.severity}.
        Audit output: {scan-deps.stdout}"
      timeout: 300000
    output: analysis

  - id: save-report
    type: memory
    config:
      operation: write
      namespace: security
      key: "audit-{args.target}"
      value: "{analysis.summary}"
```

### Related Skills

- [/connector-builder](../connector-builder/) — scaffold new connectors and step commands when the spell needs a component that doesn't exist yet
