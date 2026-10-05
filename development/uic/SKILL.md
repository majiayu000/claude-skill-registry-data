---
name: uic
description: Use when automating browser interactions with a web app that has a manifest.json or data-agent-id attributes. Use when the agent needs to find, target, or.
---

# UI Contracts for Agent Automation

UI Contracts makes web app UIs machine-readable with stable hierarchical IDs, so agents can find, target, and interact with any interactive element by name instead of fragile selectors.

## Quick Start

```bash
npx uicontract scan ./src -o manifest.json
npx uicontract name manifest.json -o manifest.json
npx uicontract find "login" --json
npx uicontract describe <agent-id> --json
npx uicontract list --type button --json
npx uicontract diff old.json new.json --json
```

## Core Workflow

### 1. Discover

Check for an existing `manifest.json` in the project root. If none exists, generate one:

```bash
npx uicontract scan ./src -o manifest.json
npx uicontract name manifest.json -o manifest.json
```

### 2. Find

Search for elements by description. Fuzzy matching is enabled by default:

```bash
npx uicontract find "pause subscription" --json
npx uicontract find "pase subscribtion" --json   # fuzzy match still finds it
npx uicontract find "billing" --type button --json
```

### 3. Target

Use the `agentId` from the find result to target the element in the browser.

**agent-browser:**

```bash
# Scoped snapshot to find the element ref:
agent-browser snapshot -s '[data-agent-id="settings.billing.pause-subscription.button"]'
# Returns: - button "Pause subscription" [ref=e1]

# Interact using the ref:
agent-browser click @e1
```

**CSS selector (any tool):**

```css
[data-agent-id="settings.billing.pause-subscription.button"]
```

**Playwright MCP:** Launch with `--test-id-attribute=data-agent-id`, then use `ref` values from the accessibility snapshot.

See [references/browser-tool-bridge.md](references/browser-tool-bridge.md) for all supported tools.

### 4. Verify

Compare the current manifest against a baseline to detect breaking changes:

```bash
npx uicontract diff baseline.json current.json --json
```

Exit code 1 means breaking changes were found.

## Commands

### Discovery

**scan** -- Discover interactive elements in source code.

```bash
npx uicontract scan <directory> -o manifest.json
```

| Flag | Description |
|------|-------------|
| `-o, --output <path>` | Output file path (default: `manifest.json`) |
| `--framework <name>` | Force a specific framework parser |
| `--json` | Write raw JSON to stdout |
| `--verbose` | Enable debug logging |

**name** -- Assign stable hierarchical IDs to discovered elements.

```bash
npx uicontract name manifest.json -o manifest.json
```

| Flag | Description |
|------|-------------|
| `-o, --output <path>` | Output file path |
| `--ai` | Use AI-assisted naming for ambiguous elements (experimental) |
| `--ai-provider <name>` | AI provider: `openai`, `anthropic`, or `google` (auto-detected from env) |
| `--ai-model <model>` | Override the default model for the AI provider |
| `--ai-timeout <ms>` | Timeout for AI naming requests (default: 10000) |

**annotate** -- Insert `data-agent-id` attributes into source files.

```bash
npx uicontract annotate manifest.json --dry-run
npx uicontract annotate manifest.json --write
```

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview patches without modifying files |
| `--write` | Apply patches to source files |
| `--backup-dir <path>` | Directory for pre-annotation backups (default: `.uic-backup/`) |

### Query

**find** -- Search for elements by description.

```bash
npx uicontract find <query> --json
```

| Flag | Description |
|------|-------------|
| `--manifest <path>` | Path to manifest file (default: `manifest.json`) |
| `--type <type>` | Filter by element type (`button`, `input`, `a`, etc.) |
| `--exact` | Disable fuzzy matching, require exact substring |
| `--json` | Output as JSON array |

**describe** -- Show detailed info for one element.

```bash
npx uicontract describe <agent-id> --json
```

| Flag | Description |
|------|-------------|
| `--manifest <path>` | Path to manifest file (default: `manifest.json`) |
| `--json` | Output as JSON object |

**list** -- List elements with optional filters.

```bash
npx uicontract list --json
```

| Flag | Description |
|------|-------------|
| `--manifest <path>` | Path to manifest file (default: `manifest.json`) |
| `--type <type>` | Filter by element type |
| `--route <route>` | Filter by route prefix |
| `--component <name>` | Filter by component name |
| `--routes` | List all unique routes |
| `--components` | List all unique component names |
| `--json` | Output as JSON array |

### Governance

**diff** -- Compare two manifests for breaking changes.

```bash
npx uicontract diff <old-manifest> <new-manifest> --json
```

| Flag | Description |
|------|-------------|
| `--allow-breaking` | Exit 0 even when breaking changes are found |
| `--json` | Output diff as JSON object |

Change categories:
- **Breaking**: removed elements, renamed agent IDs, changed element types.
- **Informational**: added elements, changed labels, moved source locations.

## Selector Patterns

Use these CSS attribute selectors to target `data-agent-id` values:

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Exact | `[data-agent-id="id"]` | Target one specific element |
| Prefix | `[data-agent-id^="settings.billing."]` | All elements in a section |
| Substring | `[data-agent-id*="billing"]` | Any element mentioning "billing" |
| Suffix | `[data-agent-id$=".button"]` | All buttons |
| Presence | `[data-agent-id]` | Any UI Contracts-annotated element |

## Integration Example

UI Contracts + agent-browser, three steps:

**Step 1 -- Find the element:**

```bash
npx uicontract find "pause subscription" --json
```

**Step 2 -- Navigate to the page:**

```bash
agent-browser open http://localhost:3000/settings/billing
```

**Step 3 -- Target and interact:**

```bash
agent-browser snapshot -s '[data-agent-id="settings.billing.pause-subscription.button"]'
# Returns: - button "Pause subscription" [ref=e1]
agent-browser click @e1
```

## Key Rules

- Always use `--json` for machine parsing. The JSON format is stable across versions.
- Never hardcode CSS selectors when an agent ID is available.
- Check `conditional: true` elements -- they may not be in the DOM without the right app state.
- Check `dynamic: true` elements -- their count depends on runtime data.
- Run `npx uicontract diff` before and after changes to catch regressions.
- Run `npx uicontract scan` after UI changes to keep the manifest current.
- Commit the baseline manifest to version control for CI diffing.

## References

| File | Contents |
|------|----------|
| [references/browser-tool-bridge.md](references/browser-tool-bridge.md) | Tool-specific targeting (agent-browser, Playwright MCP, Chrome MCP, Cypress) |
| [references/workflow-patterns.md](references/workflow-patterns.md) | Multi-step automation recipes (form fill, nav test, CI regression, annotation pipeline) |
| [references/manifest-schema.md](references/manifest-schema.md) | Full manifest.json structure, element fields, agent ID format |
