---
name: extract-tool-graph
description: Use when investigating conditional tool availability, finding tools that exist but are hidden behind gates, or mapping the full capability surface of a system
---

## Announce at start: "Using codebase-analyzer to extract the tool graph."

## Overview

Map ALL tools/capabilities that exist in the codebase, including those conditionally excluded. The tool graph reveals what the system CAN do, even if it doesn't currently expose it.

**Prerequisite:** Reads `docs/analysis/agent-loop.md` and `docs/analysis/build-pipeline.md`.

## Process

### Step 1: Find Tool Definitions

Search for every tool definition across the codebase:

- **Function handlers** — request/response handlers, middleware chains
- **API endpoints** — route registrations, controller methods
- **CLI commands** — argument parsers, subcommand definitions
- **Plugin hooks** — lifecycle callbacks, event subscribers, extension points

Use broad search patterns: route registrations, decorator annotations, command maps, handler dictionaries, and interface implementations.

### Step 2: Map Tool Registry

Trace how tools are registered and discovered:

- Static registries (maps, arrays, enums defined at module load)
- Dynamic registries (tools added at runtime via registration calls)
- Convention-based discovery (auto-loading from directories, reflection)
- Dependency injection containers (services registered by name or interface)

### Step 3: Identify Conditional Registration

Find tools defined but only registered under certain conditions:

- Feature-flag-guarded registrations (`if config.featureEnabled('x')`)
- Environment-dependent registrations (`if process.env.NODE_ENV === 'production'`)
- Role-dependent registrations (`if user.role === 'admin'`)
- Provider-specific registrations (`if provider === 'openai'`)

These tools EXIST in the code but are invisible at runtime. They are the hidden capability surface.

### Step 4: Find Dynamic Tool Registration

Trace tools loaded from external sources:

- Database-driven tool menus or permission sets
- Config-file-driven feature lists
- Plugin system tool discovery (scanning directories, loading modules)
- Remote API-driven capability negotiation

Dynamic registration is the hardest to trace statically. Look for factory patterns, loader functions, and service locators.

### Step 5: Map Parameters, Constraints, and Side Effects

For each tool in the graph:

- **Parameters**: What inputs does it accept? Required vs optional.
- **Constraints**: Validation rules, type restrictions, value bounds.
- **Side effects**: What does it modify? Files, database, network, state.
- **Dependencies**: What other tools or services does it require?

## Dispatch Rule

If the tool graph spans 5+ files, dispatch `code-explorer` agent to trace registration chains. Manual tracing of complex registration flows is error-prone and time-consuming.

## Cross-Gate-Tool Matrix

Present findings as a structured matrix:

```
| Tool            | Build Gate | Runtime Gate | Permission Gate | Provider Gate | Config Gate |
|-----------------|------------|--------------|-----------------|---------------|-------------|
| tool.search     | Y          | Y            | Y               | Y             | Y           |
| tool.admin      | N          | Y            | conditional     | Y             | N           |
| tool.debug      | conditional| Y            | N               | N             | conditional |
```

Rows = tools, columns = gate types, cells = available (Y/N/conditional with condition noted).

## Adversarial Lens

If a tool was designed to be hidden, how would it avoid detection? Check: tools registered dynamically at runtime (not in static analysis), tools loaded from external config, tools that are "disabled" but still have their registration code. The most dangerous tools are the ones that exist but aren't supposed to.

## Red Flags

- **Only finding registered tools** — you are missing defined-but-excluded tools, which is the entire point of this analysis
- **Not cross-referencing build pipeline** — build-time gates remove tools before they even reach the registry; check `docs/analysis/build-pipeline.md`
- **Ignoring dynamic registration** — factory patterns and plugin loaders create tools you won't find by grepping for definitions
- **Missing side effects** — a tool that writes to disk or makes network calls is architecturally different from a read-only query tool

## SECURITY_SIGNAL

Escalate if you find:
- Tools with admin-level capabilities not gated by authentication
- Tools that access sensitive data (PII, secrets, credentials) without audit logging
- Dynamic tool loading from untrusted sources (user uploads, external APIs)
- Tools that bypass authorization checks via indirect code paths

## Output Contract

Write `docs/analysis/tool-graph.md` using the standard contract.

Include:
1. Complete tool inventory (name, type, location, registration mechanism)
2. Registration chain map (how each tool gets registered)
3. Conditional registration summary (tools hidden behind gates)
4. Cross-gate-tool matrix
5. Dynamic registration patterns found
6. Security signals (if any)
